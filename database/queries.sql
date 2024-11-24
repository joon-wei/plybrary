-- Interval 1H (offset by 30 minutes)
WITH ranked_open AS (
    SELECT
        Ticker, 
        strftime('%Y-%m-%d %H:', Timestamp, '-30 minutes') || '30:00' AS interval_start,
        Open,
        ROW_NUMBER() OVER (
            PARTITION BY strftime('%Y-%m-%d %H:', Timestamp, '-30 minutes') || '30:00'
            ORDER BY Timestamp ASC
        ) AS row_num
    FROM stonk
    WHERE Ticker = 'AAPL'
),
ranked_close AS (
    SELECT
        Ticker, 
        strftime('%Y-%m-%d %H:', Timestamp, '-30 minutes') || '30:00' AS interval_start,
        Close,
        ROW_NUMBER() OVER (
            PARTITION BY strftime('%Y-%m-%d %H:', Timestamp, '-30 minutes') || '30:00'
            ORDER BY Timestamp DESC
        ) AS row_num
    FROM stonk
    WHERE Ticker = 'AAPL'
),
aggregates AS (
    SELECT 
        Ticker,
        strftime('%Y-%m-%d %H:', Timestamp, '-30 minutes') || '30:00' AS interval_start,
        MAX(high) AS High,
        MIN(low) AS Low,
        SUM(volume) AS Volume
    FROM stonk
    WHERE Ticker = 'AAPL'
    GROUP BY interval_start
)
SELECT
    o.interval_start as Time,
    o.Ticker,
    o.Open,
    c.Close,
    a.High,
    a.Low,
    a.Volume
FROM ranked_open o
JOIN ranked_close c ON o.interval_start = c.interval_start AND o.Ticker = c.Ticker
JOIN aggregates a ON o.interval_start = a.interval_start AND o.Ticker = a.Ticker
WHERE o.row_num = 1 AND c.row_num = 1
ORDER BY o.interval_start;


select * from pragma_table_info('stonk');


-- Interval 1D
SELECT 
    DATE(timestamp) AS date,
    AVG(open) AS avg_open,
    MAX(high) AS max_high,
    MIN(low) AS min_low,
    AVG(close) AS avg_close,
    SUM(volume) AS total_volume
FROM stonk
where ticker = 'AAPL'
GROUP BY date
ORDER BY date;