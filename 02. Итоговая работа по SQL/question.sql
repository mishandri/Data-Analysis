# Часть 1. Анализ прогресса студентов
#Из таблицы codesubmit определим сколько задач решил каждый студент, а из таблиц coderun+codesubmit
#выясним суммарное количество попыток на выполнение задач.
# Определим максимальное количество задач, решённое пользователями компании 1.
SELECT COUNT(DISTINCT c.problem_id) AS count FROM codesubmit c
JOIN users u ON u.id = c.user_id
WHERE u.company_id = 1

# Посмотрим, сколько задач решил каждый пользователь. Отсортируем по убыванию количества задач, чтобы было понятно сколько максимально решили задачи данные пользователи.
SELECT COUNT(DISTINCT c.problem_id) AS count, c.user_id FROM codesubmit c
JOIN users u ON u.id = c.user_id
WHERE u.company_id = 1
GROUP BY c.user_id
ORDER BY count DESC

# Изменим запрос так, чтобы посчитать среднее количество задач на пользователя:
WITH cnt AS (
   SELECT COUNT(DISTINCT c.problem_id) AS count, c.user_id  FROM codesubmit c
   JOIN users u ON u.id = c.user_id
   WHERE u.company_id = 1
   GROUP BY c.user_id
   ORDER BY count DESC
)
SELECT AVG(count) FROM cnt

# Получается, что в среднем пользователь компании 2 решает 31 задачу из всех 205 (то есть примерно 15%) 
# и 31 задачу из 139 максимальных (то есть примерно 22%).

# Часть 2. Анализ сложности решения задач у студентов
# Определим суммарное количество попыток на решение задач у данных пользователей:
WITH codes AS (
   SELECT c.created_at, c.problem_id, c.user_id, 'cr' AS TYPE
   FROM coderun c
   UNION ALL
   SELECT cs.created_at, cs.problem_id, cs.user_id, 'cs' AS TYPE
   FROM codesubmit cs
), total_table AS (
   SELECT created_at, problem_id, user_id, type
   FROM codes c
   RIGHT JOIN users u ON u.id = c.user_id
   WHERE u.company_id = 1 AND created_at IS NOT NULL
   ORDER BY user_id, problem_id, created_at
), solutions AS (
   SELECT COUNT(created_at) AS count, problem_id, user_id
   FROM total_table
   GROUP BY user_id, problem_id
)
SELECT SUM(count) AS sum, problem_id
FROM solutions
GROUP BY problem_id
ORDER BY SUM(count) DESC

# Вывод: Задачи 135, 140, 151, 134, 123, 122, 139, 119, 146, 137 решали большее количество раз. Можно сделать вывод, что данные задачи сложные.

# Найдём среднее количество попыток на решение задач (включая обе таблицы coderun и codesubmit):
WITH codes AS (
   SELECT c.created_at, c.problem_id , c.user_id,  'cr' AS type
   FROM coderun c
   UNION ALL
   SELECT cs.created_at, cs.problem_id, cs.user_id,  'cs' AS type
   FROM codesubmit cs
),
total_table AS (
   SELECT created_at, problem_id, user_id, type
   FROM codes c
   RIGHT JOIN users u ON u.id = c.user_id
   WHERE u.company_id = 1 AND created_at IS NOT NULL
   ORDER BY user_id, problem_id, created_at
),
solutions AS (
   SELECT COUNT(created_at) AS count, problem_id, user_id
   FROM total_table
   GROUP BY user_id, problem_id
)
SELECT AVG(count)::NUMERIC AS avg, problem_id
FROM solutions
GROUP BY problem_id
ORDER BY AVG(count)::NUMERIC DESC
LIMIT 5

# Если добавить условие type = ‘cr’, то получим среднее количество попыток:
WITH codes AS (
   SELECT c.created_at, c.problem_id , c.user_id,  'cr' AS type
   FROM coderun c
   UNION ALL
   SELECT cs.created_at, cs.problem_id, cs.user_id,  'cs' AS type
   FROM codesubmit cs
),
total_table AS (
   SELECT created_at, problem_id, user_id, type
   FROM codes c
   RIGHT JOIN users u ON u.id = c.user_id
   WHERE u.company_id = 1 AND created_at IS NOT NULL
   ORDER BY user_id, problem_id, created_at
),
solutions AS (
   SELECT COUNT(created_at) AS count, problem_id, user_id, type
   FROM total_table
   GROUP BY user_id, problem_id, type
)
SELECT AVG(count)::NUMERIC AS avg, problem_id
FROM solutions
WHERE "type" = 'cr'
GROUP BY problem_id
ORDER BY AVG(count)::NUMERIC DESC
LIMIT 5