select * from crypto_simulation_b_3
where TradeType = 'Long' and Band = 'Lower'
order by TotalReturn DESC


select * from crypto_simulation_b_3
where TradeType = 'Long' and Band = 'Lower'
and RSILowerThreshold = 35
order by TotalReturn DESC

-- Lowering rsi band to 40-60 produces some positive results
select * from crypto_simulation_b_3
where TradeType = 'Long' and Band = 'Lower'
and RSILowerThreshold = 40
and TestPeriod = '2024-06-01 - 2024-07-01'
order by TotalReturn DESC

-- expand the testing to first half of 2024
select * from crypto_simulation_b_3
where TradeType = 'Long' and Band = 'Lower'
and RSILowerThreshold = 40
and TestPeriod = '2024-01-01 - 2024-06-01'
order by TotalReturn DESC

-- expand the testing to second half of 2024
select * from crypto_simulation_b_3
where TradeType = 'Long' and Band = 'Lower'
and RSILowerThreshold = 40
and TestPeriod = '2024-07-01 - 2025-01-01'
order by TotalReturn DESC


-- Test short when touching upper band, decent profits
select * from crypto_simulation_b_3
where TradeType = 'Short' and Band = 'Upper'
and RSILowerThreshold = 35
and TestPeriod = '2024-06-01 - 2024-07-01'
order by TotalReturn DESC

-- expand short testing to first second of 2024
select * from crypto_simulation_b_3
where TradeType = 'Short' and Band = 'Upper'
and RSILowerThreshold = 35
and TestPeriod = '2024-07-01 - 2025-01-01'
and Strategy = 'b_3'
order by TotalReturn DESC

-- testing without true entry logic, trades are entered at the initial candlestick
select * from crypto_simulation_b_3
where TradeType = 'Long' and Band = 'Lower'
and RSILowerThreshold = 35
and TestPeriod = '2024-07-01 - 2025-01-01'
and Strategy = 'b_3.1'
order by TotalReturn DESC


-- b_3.2 forcing one trade per day. To compare with the initial test 
select * from crypto_simulation_b_3
where TradeType = 'Long' and Band = 'Lower'
and RSILowerThreshold = 30
and TestPeriod = '2024-06-01 - 2024-07-01'
and Strategy = 'b_3'
order by TotalReturn DESC

select * from crypto_simulation_b_3
where TradeType = 'Long' and Band = 'Lower'
and RSILowerThreshold = 30
and TestPeriod = '2024-06-01 - 2024-07-01'
and Strategy = 'b_3.2'
order by TotalReturn DESC


-- try another longer test period
select * from crypto_simulation_b_3
where TradeType = 'Long' and Band = 'Lower'
and RSILowerThreshold = 30
and TestPeriod = '2025-01-01 - 2025-06-30'
and Strategy = 'b_3'
order by TotalReturn DESC

select * from crypto_simulation_b_3
where TradeType = 'Long' and Band = 'Lower'
and RSILowerThreshold = 30
and TestPeriod = '2025-01-01 - 2025-06-30'
and Strategy = 'b_3.2'
order by Leverage,StopLoss,TakeProfit DESC

