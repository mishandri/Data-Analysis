WITH tr AS (
SELECT 
    mg.group_name, 
    EXTRACT(month FROM p.transaction_date) AS month, 
    SUM(p.transaction_value) AS tr_sum,
    ROW_NUMBER() OVER(PARTITION BY EXTRACT(month FROM p.transaction_date) ORDER BY sum(p.transaction_value) DESC, mg.group_name) AS rn
FROM mcc_groups mg 
JOIN mcc_codes mc ON mc.group_id = mg.group_id 
JOIN purchases p ON p.mcc_code_id = mc.mcc_code_id
    AND p.transaction_date BETWEEN mc.valid_from AND mc.valid_to
WHERE p.transaction_date >= to_date('2019.01.01', 'yyyy.mm.dd')
    AND p.transaction_date < to_date('2020.01.01', 'yyyy.mm.dd')
GROUP BY EXTRACT(month from p.transaction_date), mg.group_id, mg.group_name
), dt AS (    
    SELECT gs AS month
    FROM generate_series(1,12) gs
), tr_lead AS (
SELECT *,
    LEAD(tr_sum) OVER (PARTITION BY month ORDER BY rn) as ld
FROM tr
)
SELECT tl.group_name,
    dt.month AS month,
    tl.tr_sum,
    tl.tr_sum - tl.ld AS abs_diff,
    1.0 * (tl.tr_sum - tl.ld) / tl.tr_sum AS rel_diff
FROM tr_lead tl
RIGHT JOIN dt ON tl.month = dt.month
WHERE rn = 1 OR rn IS NULL