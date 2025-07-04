-- Создадим вьюшку для удобства
CREATE OR REPLACE VIEW payment_agg AS
WITH payment_agg AS (
    SELECT
        toDate(operation_datetime)  AS date_id,
        toUInt64(sum(amount))        AS amount 
    FROM 
        payment 
    WHERE
        status = 'completed'
        AND operation_datetime >= '2024-01-01'
        AND operation_datetime < '2024-08-01'
    GROUP BY
        date_id
),
(SELECT min(date_id) FROM payment_agg) AS start_date,
(SELECT max(date_id) FROM payment_agg) AS end_date
SELECT
    date_id,
    dateDiff('day', start_date, date_id) / dateDiff('day', start_date, end_date) AS trend, 
    amount,
    log(amount) AS target,
    -- Так как в данных есть сезонность, то добавим параметры для будущей модели
    if(toDayOfWeek(date_id)=1, 1, 0) AS DoW1,
    if(toDayOfWeek(date_id)=2, 1, 0) AS DoW2,
    if(toDayOfWeek(date_id)=3, 1, 0) AS DoW3,
    if(toDayOfWeek(date_id)=4, 1, 0) AS DoW4,
    if(toDayOfWeek(date_id)=5, 1, 0) AS DoW5,
    if(toDayOfWeek(date_id)=6, 1, 0) AS DoW6,
    if(toDayOfWeek(date_id)=7, 1, 0) AS DoW7
FROM
    payment_agg
ORDER BY
    date_id;

-- Разобъём наш датасет на трейн и тест, используя ещё две вьюшки
-- Train data
CREATE OR REPLACE VIEW payment_agg_train AS
SELECT * FROM payment_agg
WHERE date_id >= '2024-01-01' AND date_id < '2024-07-01';
-- Test data
CREATE OR REPLACE VIEW payment_agg_train AS
SELECT * FROM payment_agg
WHERE date_id >= '2024-07-01' AND date_id < '2024-08-01';

-- Для предсказания используем встроенную функцию стахастической линейной регрессии
-- Модификатор State сохранит состояние
CREATE OR REPLACE VIEW payment_agg_model AS
SELECT
    stachasticLinearRegressionState(0.1, 0.0, 5, 'SGD'),
    (
        target,
        trend,
        DoW1,
        DoW2,
        DoW3,
        DoW4,
        DoW5,
        DoW6,
        DoW7
    )
FROM
    payment_agg_train;

-- Сделаем прогноз
SELECT
    pat.date_id,
    pat.amount,
    toUInt256(exp(pat.target)) AS fact, -- для проверки
    toUInt256(exp(evalMLMethod(
        pam.state,
        pam.trend,
        pat.DoW1,
        pat.DoW2,
        pat.DoW3,
        pat.DoW4,
        pat.DoW5,
        pat.DoW6,
        pat.DoW7
    ))) AS forecast
FROM
    payment_agg_test AS pat
    CROSS JOIN payment_agg_model AS pam;
