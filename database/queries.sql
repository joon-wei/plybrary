-- Table sizes
select name, sum(pgsize) * 0.000001 as size from dbstat group by name;

-- Unique dates
select distinct substr(Timestamp,1,10) as Date from crypto_5m 
where Symbol like 'BTC%'
and Timestamp > '2024-12-30';
