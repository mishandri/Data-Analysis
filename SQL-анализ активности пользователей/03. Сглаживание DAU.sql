WITH dau AS(
    SELECT entry_at::date AS ymd,
        COUNT(user_id) AS cnt
    FROM userentry
    WHERE date_part('year', entry_at) = '2022'
    GROUP BY entry_at::date
)
SELECT ymd,
    cnt,
    AVG(cnt) OVER(ORDER BY ymd) AS sliding_average,
    (
        SELECT percentile_cont(0.5) within group(ORDER BY b.cnt)
        FROM dau as b
        WHERE b.ymd <= dau.ymd
    ) AS sliding_median
FROM dau