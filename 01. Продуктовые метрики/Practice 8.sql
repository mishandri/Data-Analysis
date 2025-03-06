# Изменение пикового значения
WITH dates AS (
    SELECT ('01.01.2022'::date+ gs)::timestamp AS dt
    FROM generate_series(0,110) gs
), reg AS(
    SELECT 
        DATE_TRUNC('day',date_joined) as dj,
        COUNT(*) AS cnt
    FROM users u
    GROUP BY dj
    ORDER BY dj
)
SELECT 
    d.dt,
    COALESCE(r.cnt, 0) as cnt,
    MAX(cnt) OVER(ORDER BY dt) AS max_cnt,
    COALESCE(r.cnt, 0) - MAX(cnt) OVER(ORDER BY dt) AS diff
FROM dates d 
LEFT JOIN reg r ON d.dt = r.dj