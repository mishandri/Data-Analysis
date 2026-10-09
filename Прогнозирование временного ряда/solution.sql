-- Прогноз ежедневной суммы успешных платежей.
-- Всё считается внутри ClickHouse, данные наружу не выгружаются.
--
-- Схема работы: агрегация платежей по дням, признаки, обучение на январе-июне,
-- прогноз на июль и сравнение с двумя baseline: "вчерашнее значение" и
-- "среднее за последние 7 дней".

-- 1. Дневные суммы успешных платежей за весь доступный период.
--    Здесь же сразу считаются признаки для будущего обучения.
CREATE OR REPLACE VIEW payment_agg AS
WITH payment_agg AS (
    SELECT
        toDate(operation_datetime) AS date_id,
        toUInt64(sum(amount))       AS amount
    FROM payment
    WHERE status = 'completed'
      AND operation_datetime >= '2024-01-01'
      AND operation_datetime <  '2024-08-01'
    GROUP BY date_id
),
bounds AS (
    SELECT
        (SELECT min(date_id) FROM payment_agg) AS start_date,
        (SELECT max(date_id) FROM payment_agg) AS end_date
)
SELECT
    a.date_id,
    a.amount,
    -- линейный тренд, приведённый к [0, 1]: SGD требует входы одного масштаба
    dateDiff('day', b.start_date, a.date_id)
        / dateDiff('day', b.start_date, b.end_date) AS trend,
    -- целевая переменная в логарифмах: суммы платежей мультипликативны
    -- и имеют тяжёлый хвост, после логарифма дисперсия выравнивается
    log(a.amount) AS target,
    -- недельная сезонность, one-hot по дням недели
    if(toDayOfWeek(a.date_id) = 1, 1, 0) AS DoW1,
    if(toDayOfWeek(a.date_id) = 2, 1, 0) AS DoW2,
    if(toDayOfWeek(a.date_id) = 3, 1, 0) AS DoW3,
    if(toDayOfWeek(a.date_id) = 4, 1, 0) AS DoW4,
    if(toDayOfWeek(a.date_id) = 5, 1, 0) AS DoW5,
    if(toDayOfWeek(a.date_id) = 6, 1, 0) AS DoW6,
    if(toDayOfWeek(a.date_id) = 7, 1, 0) AS DoW7
FROM payment_agg a
CROSS JOIN bounds b
ORDER BY a.date_id;

-- 2. Разделение строго по времени, не случайное перемешивание.
--    При случайном разделении будущее утекает в обучение и качество
--    выходит завышенным.
CREATE OR REPLACE VIEW payment_train AS
SELECT * FROM payment_agg
WHERE date_id >= '2024-01-01' AND date_id < '2024-07-01';

CREATE OR REPLACE VIEW payment_test AS
SELECT * FROM payment_agg
WHERE date_id >= '2024-07-01' AND date_id < '2024-08-01';

-- 3. Обучение. SGD, скорость обучения 0.1, размер батча 5.
--    Состояние модели сохраняется, поэтому обучение можно продолжить
--    на новых данных, не начиная с нуля.
CREATE OR REPLACE TABLE payment_model ENGINE = Memory AS
SELECT stochasticLinearRegressionState(0.1, 0.0, 5, 'SGD')(
    target, trend, DoW1, DoW2, DoW3, DoW4, DoW5, DoW6, DoW7
) AS state
FROM payment_train;

-- 4. Прогноз на июль.
CREATE OR REPLACE VIEW payment_forecast AS
WITH (SELECT state FROM payment_model) AS model
SELECT
    t.date_id,
    t.amount,
    exp(t.target)                                  AS fact,
    exp(evalMLMethod(model, t.trend,
                     t.DoW1, t.DoW2, t.DoW3,
                     t.DoW4, t.DoW5, t.DoW6, t.DoW7)) AS forecast
FROM payment_test AS t;

-- 5. Baseline. Без сравнения с ними качество модели не оценить:
--    любая кривая, повторяющая среднее, даст на «вчерашнем значении»
--    почти нулевую ошибку, и непонятно, добавила ли модель что-то сверх
--    простой экстраполяции.
--
--    baseline_1 «вчерашнее значение»: lag на 1 день из train,
--    для первого дня июля берётся последний день июня.
--    baseline_2 «среднее за неделю»: среднее по последним 7 дням train.
--    Оба считаются только на обучающей части, факт теста не подглядывается.
CREATE OR REPLACE VIEW payment_baseline AS
WITH lag_in_train AS (
    SELECT
        date_id,
        amount,
        -- в train каждая строка это предыдущий день, так что lag на 1
        -- восстанавливает наблюдение, не существовавшее в обучении
        lagInFrame(amount) OVER (ORDER BY date_id ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING) AS prev_day
    FROM payment_train
),
with_week AS (
    SELECT
        date_id,
        amount,
        avg(amount) OVER (ORDER BY date_id ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS week_mean
    FROM payment_train
)
SELECT
    f.date_id,
    f.amount                                            AS fact,
    exp(f.log_forecast)                                  AS forecast,
    w.prev_day                                           AS baseline_prev_day,
    t.week_mean                                          AS baseline_week_mean,
    -- приведение всего в одну шкалу для сравнения ошибок
    abs(f.amount - exp(f.log_forecast))                  AS err_forecast,
    abs(f.amount - w.prev_day)                           AS err_prev_day,
    abs(f.amount - t.week_mean)                          AS err_week_mean,
    abs(f.amount - exp(f.log_forecast)) / f.amount       AS wape_forecast,
    abs(f.amount - w.prev_day) / f.amount                AS wape_prev_day,
    abs(f.amount - t.week_mean) / f.amount               AS wape_week_mean
FROM (
    SELECT
        date_id,
        amount,
        evalMLMethod((SELECT state FROM payment_model), trend,
                     DoW1, DoW2, DoW3, DoW4, DoW5, DoW6, DoW7) AS log_forecast
    FROM payment_test
) AS f
LEFT JOIN lag_in_train AS w
       ON f.date_id = w.date_id + 1
LEFT JOIN (
    SELECT date_id + 6 AS date_id, week_mean
    FROM with_week
) AS t
       ON f.date_id = t.date_id;

-- 6. Итог по июлю: WAPE и MAE для модели и обоих baseline.
--    Сравнивать надо именно так: наивное «ошибка в процентах от факта»
--    по каждому дню отдельно завышает оценку в дни с большим отклонением.
SELECT
    'модель'            AS approach,
    round(sum(err_forecast) / sum(fact), 4)  AS wape,
    round(avg(err_forecast), 0)               AS mae
FROM payment_baseline
UNION ALL
SELECT 'baseline: вчера'  , round(sum(err_prev_day) / sum(fact), 4), round(avg(err_prev_day), 0) FROM payment_baseline
UNION ALL
SELECT 'baseline: неделя' , round(sum(err_week_mean) / sum(fact), 4), round(avg(err_week_mean), 0) FROM payment_baseline;

-- 7. Ошибка по дням июля, чтобы видеть не только итог.
SELECT
    date_id,
    fact,
    forecast,
    baseline_prev_day,
    baseline_week_mean,
    wape_forecast,
    wape_prev_day,
    wape_week_mean
FROM payment_baseline
ORDER BY date_id;
