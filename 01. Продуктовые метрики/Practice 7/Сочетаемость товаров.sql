/*
Необходимо изучить сочетаемость товаров. Фактически, вам нужно посмотреть,
какой товар и как часто встречается одновременно с другими товарами в чеке - и так по всем товарам.
*/

WITH soch AS (
    SELECT 
        dr_apt, 
        dr_nchk, 
        dr_dat,
        dr_ndrugs
    FROM sales
    GROUP BY dr_apt, dr_nchk, dr_dat, dr_ndrugs
    )
SELECT s1.dr_ndrugs AS product1,
    s2.dr_ndrugs AS product2, 
    COUNT(s1.dr_ndrugs) AS cnt
FROM soch AS s1
JOIN soch AS s2 
    ON s1.dr_ndrugs < s2.dr_ndrugs
    AND s1.dr_apt = s2.dr_apt
    AND s1.dr_nchk = s2.dr_nchk
    AND s1.dr_dat = s2.dr_dat
GROUP BY s1.dr_ndrugs, s2.dr_ndrugs
ORDER BY cnt DESC