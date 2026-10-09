/*
Необходимо провести XYZ анализ ассортимента. 
Обычно XYZ анализ всегда проводится вместе с ABC анализом, 
поэтому нужно «дописать» этот запрос в запрос для проведения ABC.
*/

WITH preparing_xyz AS (
    SELECT 
        dr_ndrugs AS product, 
        TO_CHAR(dr_dat, 'YYYY-WW') AS ym, 
        SUM(dr_kol) AS kol
    FROM sales
    GROUP BY product, ym
    ), 
    xyz AS (
    SELECT
        product,
        CASE
            WHEN STDDEV(kol)/AVG(kol) > 0.25 THEN 'Z'
            WHEN STDDEV(kol)/AVG(kol) > 0.1 THEN 'Y'
        ELSE 'X'        
        END AS xyz_sales
    FROM preparing_xyz
    GROUP BY product
    HAVING COUNT(DISTINCT ym) >= 4
    ),
    preparing_abc AS (
    SELECT
        dr_ndrugs AS product,
        SUM(dr_kol) AS amount,
        SUM(dr_kol * (dr_croz - dr_czak) - dr_sdisc) AS profit,
        SUM(dr_kol * dr_croz - dr_sdisc) AS revenue
    FROM sales s
    GROUP BY dr_ndrugs
    ),
    abc AS (
    SELECT product,
        CASE
            WHEN SUM(amount) OVER (ORDER BY amount DESC)/ SUM(amount) OVER() <=0.8 THEN 'A'
            WHEN SUM(amount) OVER (ORDER BY amount DESC)/ SUM(amount) OVER() <=0.95 THEN 'B'
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
    FROM preparing_abc
    )
SELECT
    abc.product,
    abc.amount_abc,
    abc.profit_abc,
    abc.revenue_abc,
    xyz.xyz_sales
FROM abc
LEFT JOIN xyz ON abc.product = xyz.product
ORDER BY product