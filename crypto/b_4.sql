select * from crypto_simulation_b_4
where Strategy = 'b_4.2' and StandardDeviationThreshold = 0.007 and TradeType = 'Short'
order by TotalReturn DESC

-- Sum of long and short trades
select Leverage, StopLoss, TakeProfit, sum(TakeProfitCount) as TotalTP, sum(StopLossCount) as TotalSL, 
sum(NoExitCount) as TotalNoExit, sum(TotalTrades) as TotalTotalTrades, sum(TotalReturn) as TotalTotalReturn
from crypto_simulation_b_4
where Strategy = 'b_4.2' and StandardDeviationThreshold = 0.007 and TestPeriod = '2024-07-01 - 2025-07-01'
group by Leverage, StopLoss,TakeProfit
order by TotalTotalReturn DESC


-- 2024 testing, std threshold = 0.005
select * from crypto_simulation_b_4
where Strategy = 'b_4.2' and StandardDeviationThreshold = 0.005 and TestPeriod = '2024-01-01 - 2025-01-01'
order by TotalReturn DESC

select StandardDeviationThreshold,Leverage, StopLoss, TakeProfit, sum(TakeProfitCount) as TotalTP, sum(StopLossCount) as TotalSL, 
sum(NoExitCount) as TotalNoExit, sum(TotalTrades) as TotalTotalTrades, sum(TotalReturn) as TotalTotalReturn
from crypto_simulation_b_4
where Strategy = 'b_4.2' and StandardDeviationThreshold = 0.005 and TestPeriod = '2024-01-01 - 2025-01-01'
group by Leverage, StopLoss,TakeProfit
order by TotalTotalReturn DESC

-- 2024 testing, std threshold = 0.007
select * from crypto_simulation_b_4
where Strategy = 'b_4.2' and StandardDeviationThreshold = 0.007 and TestPeriod = '2024-01-01 - 2025-01-01'
order by TotalReturn DESC

select StandardDeviationThreshold,Leverage, StopLoss, TakeProfit, sum(TakeProfitCount) as TotalTP, sum(StopLossCount) as TotalSL, 
sum(NoExitCount) as TotalNoExit, sum(TotalTrades) as TotalTotalTrades, sum(TotalReturn) as TotalTotalReturn
from crypto_simulation_b_4
where Strategy = 'b_4.2' and StandardDeviationThreshold = 0.007 and TestPeriod = '2024-01-01 - 2025-01-01'
group by Leverage, StopLoss,TakeProfit
order by TotalTotalReturn DESC
