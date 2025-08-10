select distinct SimulationRunDate from casino_baccarat_simulation
order by SimulationRunDate

select * from casino_baccarat_simulation WHERE SimulationRunDate = '2025-08-10 23:32:31'
order by [GameNo], [Round]

-- Summary of simulations
select 
	GameNo,
	SUM(CASE WHEN Winner = 'Banker' THEN 1 ELSE 0 END) AS BankerWins,
	ROUND(1.0 * SUM(CASE WHEN Winner = 'Banker' THEN 1 ELSE 0 END) / COUNT(*), 2) AS BankerRatio,
	SUM(CASE WHEN Winner = 'Player' THEN 1 ELSE 0 END) AS PlayerWins,
	ROUND(1.0 * SUM(CASE WHEN Winner = 'Player' THEN 1 ELSE 0 END) / COUNT(*), 2) AS PlayerRatio,
	SUM(CASE WHEN Winner = 'Tie' THEN 1 ELSE 0 END) AS Ties,
	ROUND(1.0 * SUM(CASE WHEN Winner = 'Tie' THEN 1 ELSE 0 END) / COUNT(*), 2) AS TieRatio,
	COUNT(*) AS TotalGames
FROM casino_baccarat_simulation
WHERE SimulationRunDate = '2025-08-10 23:32:31'
GROUP BY GameNo

