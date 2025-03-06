ITH tmp AS (
    SELECT
        mg.group_name AS group_name,
        TO_CHAR(p.transaction_date, 'YYYY') AS year,
        ROW_NUMBER() OVER(PARTITION BY TO_CHAR(p.transaction_date, 'YYYY'), mg.group_name ORDER BY transaction_value DESC) AS rn,
        p.transaction_value
    FROM mcc_groups mg
    JOIN mcc_codes mc ON mg.group_id = mc.group_id 
    JOIN purchases p ON mc.mcc_code_id = p.mcc_code_id AND p.transaction_date BETWEEN valid_from AND valid_to
    WHERE p.transaction_date >= to_date('2019.01.01', 'yyyy.mm.dd') AND p.transaction_date < to_date('2021.01.01', 'yyyy.mm.dd')
    ORDER BY group_name, transaction_value DESC, rn, year
), yr AS (
    SELECT year, rn, group_name
    FROM (SELECT generate_series(2019, 2020) AS year) y
    CROSS JOIN (SELECT generate_series(1, 3) AS rn) r
    CROSS JOIN (SELECT DISTINCT group_name FROM mcc_groups) g
)
SELECT 
    yr.group_name, 
    yr.year, 
    yr.rn, 
    tmp.transaction_value
FROM yr
LEFT JOIN tmp 
    ON yr.year = tmp.year::INTEGER 
    AND yr.rn = tmp.rn 
    AND yr.group_name = tmp.group_name
ORDER BY yr.group_name, yr.rn, yr.year