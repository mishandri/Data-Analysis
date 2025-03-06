# Динамика уникальных пользователей
WITH all_users_act AS (
    SELECT created_at::date as ymd, user_id
    FROM coderun cr
    WHERE created_at::date >= '2022-01-01'
    UNION ALL
    SELECT created_at::date as ymd, user_id
    FROM codesubmit cs
    WHERE created_at::date >= '2022-01-01'
), 
activity AS (
    SELECT DISTINCT user_id, ymd
    FROM all_users_act
),
unique_users AS (
    SELECT ymd, user_id,
           ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY ymd) AS user_row_num
    FROM activity
)
SELECT DISTINCT ymd, 
       COUNT(user_id) FILTER (WHERE user_row_num = 1) OVER(ORDER BY ymd) AS unique_cnt
FROM unique_users
ORDER BY ymd;