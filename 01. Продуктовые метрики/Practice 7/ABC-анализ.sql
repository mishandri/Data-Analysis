/*
Необходимо провести многомерный ABC анализ:
- по количеству проданных позиций
- - по прибыли с позиции
по выручке
*/

WITH preparing AS (
SELECT
        dr_ndrugs AS product,
        SUM(dr_kol) AS amount,
        SUM(dr_kol * (dr_croz - dr_czak) - dr_sdisc) AS profit,
        SUM(dr_kol * dr_croz - dr_sdisc) AS revenue
    FROM sales s
    GROUP BY dr_ndrugs
)
SELECT product,
    CASE
        WHEN SUM(amount) OVER (ORDER BY amount DESC)/
            SUM(amount) OVER() <=0.8 THEN 'A'
        WHEN SUM(amount) OVER (ORDER BY amount DESC)/
            SUM(amount) OVER() <=0.95 THEN 'B'
        ELSE 'C'
    END AS amount_abc,
        CASE
        WHEN SUM(profit) OVER (ORDER BY profit DESC)/ SUM(profit) OVER() <=0.8 THEN 'A'
        WHEN SUM(profit) OVER (ORDER BY profit DESC)/ SUM(profit) OVER() <=0.95 THEN 'B'
        ELSE 'C'
    END AS profit_abc,
        CASE
        WHEN SUM(revenue) OVER (ORDER BY revenue DESC)/ SUM(revenue) OVER() <=0.8 THEN 'A'
        WHEN SUM(revenue) OVER (ORDER BY revenue DESC)/ SUM(revenue) OVER() <=0.95 THEN 'B'
        ELSE 'C'
    END AS revenue_abc
FROM preparing
ORDER BY product