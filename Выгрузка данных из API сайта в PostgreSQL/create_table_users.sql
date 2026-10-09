-- Схема таблицы попыток решения.
--
-- Ключ по трём колонкам: user_id, created_at, attempt_type.
-- Одна и та же попытка может прийти из API повторно при перезапуске
-- скрипта, и без ключа она бы записалась второй раз.

CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR NOT NULL,
    oauth_consumer_key VARCHAR NOT NULL,
    lis_result_sourcedid VARCHAR,
    lis_outcome_service_url VARCHAR,
    is_correct VARCHAR(1),  -- "1" / "0" или NULL для запусков
    attempt_type VARCHAR(6), -- "run" / "submit"
    created_at TIMESTAMP,
    CONSTRAINT users_attempt_unique UNIQUE (user_id, created_at, attempt_type)
);

-- Индекс для выборок по дате. Без него ежедневный отчёт по вчера
-- будет делать последовательное сканирование всей таблицы.
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users (created_at);

-- Права на апсерт. Перезапуск скрипта в тот же день не должен падать
-- с нарушением уникальности: вместо INSERT используется upsert.
INSERT INTO users (
    user_id,
    oauth_consumer_key,
    lis_result_sourcedid,
    lis_outcome_service_url,
    is_correct,
    attempt_type,
    created_at
)
VALUES (
    %(user_id)s,
    %(oauth_consumer_key)s,
    %(lis_result_sourcedid)s,
    %(lis_outcome_service_url)s,
    %(is_correct)s,
    %(attempt_type)s,
    %(created_at)s
)
ON CONFLICT (user_id, created_at, attempt_type)
DO UPDATE SET
    oauth_consumer_key    = EXCLUDED.oauth_consumer_key,
    lis_result_sourcedid = EXCLUDED.lis_result_sourcedid,
    lis_outcome_service_url = EXCLUDED.lis_outcome_service_url,
    is_correct            = EXCLUDED.is_correct;

-- Первая загрузка периода нужна только для проверки, что данные пришли.
-- Не вставляем, а показываем масштаб: сколько строк уже есть и до какой даты.
SELECT
    COUNT(*)                AS total_rows,
    MIN(created_at)         AS first_attempt,
    MAX(created_at)         AS last_attempt,
    COUNT(DISTINCT user_id) AS unique_users
FROM users;

-- Уже загруженные попытки за период, чтобы понять, с чего продолжать.
SELECT
    DATE(created_at) AS day,
    COUNT(*)         AS attempts,
    COUNT(*) FILTER (WHERE attempt_type = 'submit')        AS submits,
    COUNT(*) FILTER (WHERE attempt_type = 'run')           AS runs,
    COUNT(*) FILTER (WHERE is_correct = '1')               AS correct,
    COUNT(DISTINCT user_id)                               AS users
FROM users
WHERE created_at >= %(start)s AND created_at < %(end)s
GROUP BY DATE(created_at)
ORDER BY day;
