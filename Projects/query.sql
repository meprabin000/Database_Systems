/* 3. Enter a team name andretrieve all the names and salaries of all team members who play on that team.*/
SELECT PLAYER.Name, PLAYER.Salary
FROM PLAYER, TEAM
WHERE PLAYER.Team_id = TEAM.Id AND TEAM.Name = '''Chicago Blackhawks''';

/* 4.Enter a player’s last name and first name and retrieve a list of their injuries. */
SELECT INJURY_RECORDS.Id, INJURY_RECORDS.Inci_desc, INJURY_RECORDS.Inj_desc
FROM INJURY_RECORDS, PLAYER
WHERE PLAYER.Name = '''Dylan Coghlan''' AND PLAYER.Id = INJURY_RECORDS.Player_id;

/* 5.List all captains and the team they play for.  */
SELECT TEAM.Captain, TEAM.Name as 'Team Name' FROM TEAM;

/* 6.For each team, retrieve the name and the number (count) of players on that team. Order the result by number of players in descending order. */
SELECT Team.Name, COUNT(PLAYER.Name) AS 'Number_of_players'
FROM PLAYER, TEAM
WHERE TEAM.Id = PLAYER.Team_id
GROUP BY TEAM.Name
ORDER BY COUNT(PLAYER.Name) DESC;

/* 7.For each host_team list the team’s name and the number of wins and losses of that team */
SELECT TEAM.Name,
  COUNT(
    CASE
      WHEN GAME.H_T_Score > GAME.G_T_Score THEN 1 END
      ) AS 'Number of wins',
  COUNT(
    CASE
    WHEN GAME.H_T_Score < GAME.G_T_Score THEN 1 END
      ) AS 'Number of losses'
FROM TEAM, GAME
WHERE TEAM.Id = GAME.Host_team
GROUP BY TEAM.Name;
