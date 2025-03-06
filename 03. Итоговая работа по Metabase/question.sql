# Максимальное количество задач для компании
SELECT COUNT(DISTINCT codesubmit.problem_id) AS count FROM codesubmit
JOIN users ON users.id = codesubmit.user_id
JOIN company ON company.id = users.company_id
WHERE {{company_name}}

# Среднее количество задач для компании
WITH cnt_ex AS (
    SELECT COUNT(DISTINCT codesubmit.problem_id) AS cnt FROM codesubmit
    JOIN users ON users.id = codesubmit.user_id
    JOIN company ON company.id = users.company_id
    WHERE {{company_name}}
    GROUP BY codesubmit.user_id
)
SELECT AVG(cnt) AS "Среднее количество задач" FROM cnt_ex

# Как пользователи решают задачи
SELECT COUNT(DISTINCT codesubmit.problem_id) AS "Количество решенных задач", codesubmit.user_id AS "ID пользователя", max(users.email) AS "E-mail пользователя"  FROM codesubmit
JOIN users ON users.id = codesubmit.user_id
JOIN company ON company.id = users.company_id
WHERE {{company_name}}
GROUP BY codesubmit.user_id
ORDER BY 1 DESC

# 10 задач, у которых много попыток
WITH codes AS (
   SELECT c.created_at, c.problem_id, c.user_id, 'cr' AS TYPE
   FROM coderun c
   UNION ALL
   SELECT cs.created_at, cs.problem_id, cs.user_id, 'cs' AS TYPE
   FROM codesubmit cs
), total_table AS (
   SELECT created_at, problem_id, user_id, type, company_id
   FROM codes
   RIGHT JOIN users ON users.id = codes.user_id
   WHERE created_at IS NOT NULL
   ORDER BY user_id, problem_id, created_at
), solutions AS (
   SELECT COUNT(created_at) AS count, problem_id, user_id, company_id
   FROM total_table
   GROUP BY user_id, problem_id, company_id
)
SELECT SUM(count) AS sum, problem_id
FROM solutions
JOIN company ON company.id = solutions.company_id
WHERE {{company_name}}
GROUP BY problem_id
ORDER BY SUM(count) DESC
LIMIT 10

# Среднее количество попыток и сабмитов на решение задач
WITH codes AS (
   SELECT c.created_at, c.problem_id , c.user_id,  'cr' AS type
   FROM coderun c
   UNION ALL
   SELECT cs.created_at, cs.problem_id, cs.user_id,  'cs' AS type
   FROM codesubmit cs
),
total_table AS (
   SELECT created_at, problem_id, user_id, type, company_id
   FROM codes c
   RIGHT JOIN users u ON u.id = c.user_id
   WHERE created_at IS NOT NULL
   ORDER BY user_id, problem_id, created_at
),
solutions AS (
   SELECT COUNT(created_at) AS count, problem_id, user_id, company_id
   --, type
   FROM total_table
   GROUP BY user_id, problem_id, company_id
   --, type
)
SELECT AVG(count)::NUMERIC AS avg, problem_id
FROM solutions
JOIN company ON company.id = solutions.company_id
WHERE {{company_name}}
-- WHERE "type" = 'cr'
GROUP BY problem_id
ORDER BY AVG(count)::NUMERIC DESC
LIMIT 5

# Среднее количество попыток на решение задач
WITH codes AS (
   SELECT c.created_at, c.problem_id , c.user_id,  'cr' AS type
   FROM coderun c
   UNION ALL
   SELECT cs.created_at, cs.problem_id, cs.user_id,  'cs' AS type
   FROM codesubmit cs
),
total_table AS (
   SELECT created_at, problem_id, user_id, type, company_id
   FROM codes c
   RIGHT JOIN users u ON u.id = c.user_id
   WHERE created_at IS NOT NULL
   ORDER BY user_id, problem_id, created_at
),
solutions AS (
   SELECT COUNT(created_at) AS count, problem_id, user_id, company_id, type
   FROM total_table
   GROUP BY user_id, problem_id, company_id, type
)
SELECT AVG(count)::NUMERIC AS avg, problem_id
FROM solutions
JOIN company ON company.id = solutions.company_id
WHERE {{company_name}} AND "type" = 'cr'
GROUP BY problem_id
ORDER BY AVG(count)::NUMERIC DESC
LIMIT 5