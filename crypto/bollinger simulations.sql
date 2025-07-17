select * from crypto_simulation_bollinger
where Threshold = 0.985
and TestPeriod = '2025-01-01 - 2025-07-01'
order by TotalReturn DESC

-- Profitable strat 1: Short when reachest lower band
select * from crypto_simulation_bollinger
where Threshold = 0.985
and TestPeriod = '2024-01-01 - 2025-01-01'
and TradeType = 'Short' and Band = 'Lower'
order by TotalReturn DESC

-- Profitable Strat 2: Long when reaches upper band
select * from crypto_simulation_bollinger
where TestPeriod = '2024-01-01 - 2025-01-01'
and TradeType = 'Long' and Band = 'Upper'
order by TotalReturn DESC