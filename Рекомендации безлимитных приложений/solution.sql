WITH
toDate('2024-09-01') AS packet_start_date,
10 AS passed_days,
traffic_by_option AS (
    SELECT
        dt.account_id                               AS account_id,
        ifNull(dt.option_name, 'Unknown')           AS option_name,
        p.data_limit                                AS mb_limit,
        sum(dt.bytes_in + dt.bytes_out)/1_000_000   AS mb_total
    FROM
        data_traffic AS dt
        INNER JOIN packet AS p ON (
            p.account_id = dt.account_id
            AND toDate(p.packet_start) = packet_start_date
            AND p.data_limit != 0
        )
    WHERE
        dt.date_id >= packet_start_date
        AND dt.date_id < packet_start_date + INTERVAL passed_days DAY
    GROUP BY
        dt.account_id,
        option_name,
        mb_limit
),
top_option AS (
    SELECT
        account_id,
        argMax(option_name, mb_total) AS top_option_by_spend_mb
    FROM
        traffic_by_option
    WHERE
        option_name != 'Unknown'
    GROUP BY
        account_id
),
traffic_total_by_account AS (
    SELECT
        account_id,
        sum(mb_total)               AS mb_total,
        mb_total / passed_days * 30 AS mb_forecast,
        mb_forecast / min(mb_limit) AS ratio
    FROM
        traffic_by_option
    GROUP BY
        account_id
)
SELECT
    ttba.account_id,
    to.top_option_by_spend_mb
FROM
    traffic_total_by_account ttba
    LEFT JOIN top_option to USING account_id
    WHERE 
        ratio > 1
    ;