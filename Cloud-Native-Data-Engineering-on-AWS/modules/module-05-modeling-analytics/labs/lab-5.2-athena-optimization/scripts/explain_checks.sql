-- Lab 5.2: Use EXPLAIN to compare plans (Athena engine v3)

EXPLAIN
SELECT SUM(order_amount_usd)
FROM cnde_dev_datalake.fact_orders
WHERE year = '2024' AND month = '01' AND day = '15';

EXPLAIN
SELECT SUM(order_amount_usd)
FROM cnde_dev_datalake.fact_orders
WHERE CAST(concat(year, '-', month, '-', day) AS DATE) = DATE '2024-01-15';

-- Partition metadata check
SELECT * FROM "cnde_dev_datalake\$partitions"
WHERE tablename = 'fact_orders'
ORDER BY year, month, day
LIMIT 20;
