select * from crypto_simulation_bollinger

-- 2024
select * from crypto_simulation_bollinger
where TestPeriod = '2024-01-01 - 2025-01-01'
and TradeType = 'Long' 
and Band = 'Lower'
and BollingerTimeframe = '15m'
and Threshold = 0.015
and Leverage = 20
order by TotalReturn DESC

-- leverage 10; slightly less unprofitable
select * from crypto_simulation_bollinger
where TestPeriod = '2024-01-01 - 2025-01-01'
and TradeType = 'Long' 
and Band = 'Lower'
and BollingerTimeframe = '15m'
and Threshold = 0.015
and Leverage = 10
order by TotalReturn DESC

-- Short on upper band, also unprofitable
select * from crypto_simulation_bollinger
where TestPeriod = '2024-01-01 - 2025-01-01'
and TradeType = 'Short' 
and Band = 'Upper'
and BollingerTimeframe = '15m'
and Threshold = 0.015
--and Leverage = 20
order by TotalReturn DESC


-- 2025 half year testing, similar to 2024
select * from crypto_simulation_bollinger
where TestPeriod = '2025-01-01 - 2025-07-01'
and TradeType = 'Long' 
and Band = 'Lower'
and BollingerTimeframe = '15m'
and Threshold = 0.015
order by TotalReturn DESC

-- Threshold: 0.01
-- lowering Threshold, will it allow more mean reversal trades? guess not.
select * from crypto_simulation_bollinger
where TestPeriod = '2025-01-01 - 2025-07-01'
and TradeType = 'Long' 
and Band = 'Lower'
and BollingerTimeframe = '15m'
and Threshold = 0.01
order by TotalReturn DESC

-- Lets try to short; not great as well, but couple of profitable strats, mainly leverage 10
select * from crypto_simulation_bollinger
where TestPeriod = '2025-01-01 - 2025-07-01'
and TradeType = 'Short' 
and Band = 'Lower'
and BollingerTimeframe = '15m'
and Threshold = 0.01
order by TotalReturn DESC

-- lets try this setup on 2024; starting to see some decent profitable setups. Mainly leverage 10-15. <50% win rates but overall profit, Not great win rates for scalping.
select * from crypto_simulation_bollinger
where TestPeriod = '2024-01-01 - 2025-01-01'
and TradeType = 'Short' 
and Band = 'Lower'
and BollingerTimeframe = '15m'
and Threshold = 0.01
order by TotalReturn DESC

-- Threshold: 0.005
-- Lower threshold: 0.5% below Band; Pretty decent results
select * from crypto_simulation_bollinger
where TestPeriod = '2024-01-01 - 2025-01-01'
and TradeType = 'Short' 
and Band = 'Lower'
and BollingerTimeframe = '15m'
and Threshold = 0.005
order by TotalReturn DESC

-- Same setup but 2025 half; completely unprofitable
select * from crypto_simulation_bollinger
where TestPeriod = '2025-01-01 - 2025-07-01'
and TradeType = 'Short' 
and Band = 'Lower'
and BollingerTimeframe = '15m'
and Threshold = 0.005
order by TotalReturn DESC

-- Lets try it Long; Also not great and mainly unprofitable
select * from crypto_simulation_bollinger
where TestPeriod = '2025-01-01 - 2025-07-01'
and TradeType = 'Long' 
and Band = 'Lower'
and BollingerTimeframe = '15m'
and Threshold = 0.005
order by TotalReturn DESC

'''
Most profitable strat for 2024: Short when 0.5% under the lower band netting in the best case $8197
However the same set up for 2025 is completely unprofitable with the best case being -$2200
Reversing this setup for 2025 (doing long instead) also does not help with most scenarios being unprofitable.

Next step: incorporate other indicators (RSI, ATR, SD)
'''
-- lets try to 'save' it by testing 0.2-0.3 SL; basically did not help
select * from crypto_simulation_bollinger
where TestPeriod = '2025-01-01 - 2025-07-01'
and TradeType = 'Short' 
and Band = 'Lower'
and BollingerTimeframe = '15m'
and Threshold = 0.005
order by TotalReturn DESC

