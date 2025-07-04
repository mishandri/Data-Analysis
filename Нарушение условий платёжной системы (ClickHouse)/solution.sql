WITH 
24 AS hours, --Так можно задать переменные
20_000_000 AS threshhold, -- Можно указать явно тип данных toUInt64(20_000_000)
prepare AS (
    SELECT
        account_id,
        amount,
        operation_datetime - INTERVAL hours HOUR AS interval_start,
        operation_datetime AS interval_end,
        sum(amount) OVER(
            PARTITION BY account_id
            ORDER BY operation_datetime
            RANGE BETWEEN hours*60*60 PRECEDING AND CURRENT ROW 
            -- нужно указывать в таком же формате в каком и столбец
        ) AS interval_amount,
        count(operation_id) OVER(
            PARTITION BY account_id
            ORDER BY operation_datetime
            RANGE BETWEEN hours*60*60 PRECEDING AND CURRENT ROW 
        ) AS interval_count
    FROM
        payment
    WHERE
        status = 'completed'

)
SELECT
    *
FROM
    prepare
WHERE
    interval_amount >= threshhold;