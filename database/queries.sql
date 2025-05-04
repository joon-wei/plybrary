select * from crypto_1h 
where Symbol like 'TRUMP%'
and timestamp >= '2025-01-29' and timestamp <= '2025-01-30'
order by Timestamp
limit 1000;



select * from crypto_5m
where Symbol like 'SOL%'
and Timestamp >= '2024-12-30 23:50:00' and Timestamp <= '2024-12-31 00:10:00'
order by Timestamp asc;


-- Table sizes
select name, sum(pgsize) * 0.000001 as size from dbstat group by name;

-- Unique dates
select distinct substr(Timestamp,1,10) as Date from crypto_5m 
where Symbol like 'BTC%'
and Timestamp > '2024-12-30';
