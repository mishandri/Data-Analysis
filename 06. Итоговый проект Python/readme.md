# Итоговый проект Python

Само задание можно псотмреть в фале "[ТЗ проекта.md](ТЗ_проекта.md)"

1. Так как таблица в БД создаётся один раз, а данные потом просто заносятся в неё, то было решено создать её через DBeaver:

   ```pgsql
   CREATE TABLE IF NOT EXISTS users (
       user_id VARCHAR NOT NULL,
       oauth_consumer_key VARCHAR NOT NULL,
       lis_result_sourcedid VARCHAR,
       lis_outcome_service_url VARCHAR,
       is_correct VARCHAR(1),  -- Например, "1"/"0" или Null
       attempt_type VARCHAR(6), -- Например, "run"/"submit"
       created_at TIMESTAMP
   );
   ```
2.
