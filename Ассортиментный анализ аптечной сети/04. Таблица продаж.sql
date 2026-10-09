/*
Необходимо построить полную таблицу продаж товаров во всех аптеках в формате 
«товар - аптека - продано штук». Если вдруг в какой-то аптеке конкретный товар 
не продавался, то просто выводим null.
*/

WITH products AS (
    SELECT DISTINCT dr_ndrugs FROM sales
    ),
    pharmas AS(
    SELECT DISTINCT dr_apt FROM sales
    )
SELECT ph.dr_apt AS id, p.dr_ndrugs AS product, ROUND(SUM(dr_kol)::numeric,2) AS cnt
FROM products p
CROSS JOIN pharmas ph
LEFT JOIN sales s ON p.dr_ndrugs = s.dr_ndrugs AND ph.dr_apt = s.dr_apt
GROUP BY  id, product