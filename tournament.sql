-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- Create tournament DB and connect to it
DROP DATABASE tournament;
CREATE DATABASE tournament;
\c tournament;

/* Evaluating use without this check in place
-- Create tournament 
CREATE TABLE tournament_log (
	  tournament_id   serial PRIMARY KEY,
	tournament_code   varchar(3),
			 UNIQUE   (tournament_code)
);

INSERT INTO tournament_log (tournament_code) VALUES ('ABC');
INSERT INTO tournament_log (tournament_code) VALUES ('XYZ');
*/


-- Create some tables.
CREATE TABLE players (
	tournament_code   varchar(3),
			   name   text,
	  		     id   serial PRIMARY KEY,
	  		 UNIQUE   (id)
);


-- Inserting 4 players into the ABC tournament
INSERT INTO players VALUES ('ABC', 'John Doe', 1);
INSERT INTO players VALUES ('ABC', 'Jim Doe', 2);
INSERT INTO players VALUES ('ABC', 'Joe Doe', 3);
INSERT INTO players VALUES ('ABC', 'Juan Doe', 4);

-- Inserting 4 players into the XYZ tournament
INSERT INTO players VALUES ('XYZ', 'Mike Smith', 11);
INSERT INTO players VALUES ('XYZ', 'Mark Smith', 12);
INSERT INTO players VALUES ('XYZ', 'Mitch Smith', 13);
INSERT INTO players VALUES ('XYZ', 'Matt Smith', 14);





-- Creating matches table consisting of tournament code, player's ID, opponent's ID, match result, and entry number
CREATE TABLE matches (
	tournament_code   varchar(3),
	      player_id   integer REFERENCES players (id) ON DELETE RESTRICT,
	    opponent_id   integer REFERENCES players (id) ON DELETE RESTRICT,
		     result   text CHECK (result IN ('win', 'lose', 'tie')),
		      entry   serial PRIMARY KEY,
		     UNIQUE   (player_id, opponent_id)
);


-- Insert two matches in tournament ABC
INSERT INTO matches VALUES ('ABC', 1, 2, 'win');
INSERT INTO matches VALUES ('ABC', 2, 1, 'lose');
INSERT INTO matches VALUES ('ABC', 3, 4, 'lose');
INSERT INTO matches VALUES ('ABC', 4, 3, 'win');

INSERT INTO matches VALUES ('ABC', 1, 4, 'win');
INSERT INTO matches VALUES ('ABC', 4, 1, 'lose');
INSERT INTO matches VALUES ('ABC', 2, 3, 'lose');
INSERT INTO matches VALUES ('ABC', 3, 2, 'win');

-- Insert two matches in tournament XYZ
INSERT INTO matches VALUES ('XYZ', 11, 12, 'tie');
INSERT INTO matches VALUES ('XYZ', 12, 11, 'tie');
INSERT INTO matches VALUES ('XYZ', 13, 14, 'win');
INSERT INTO matches VALUES ('XYZ', 14, 13, 'lose');




-- CUSTOM VIEWS
/*	v_namingPlayers functions as the foundation for v_results
	The players table  is used to fill in the players.name that is associated with matches.player_id
	NOTES:
		I'm currently unable to use the players table to add both the player_name and opponent_name (that is added in v_results)
		v_namingPlayers is used to attach the name to player_name and v_results attaches opponent.name
*/
CREATE VIEW v_namingPlayers AS (
	SELECT
		matches.entry AS entry,
		matches.tournament_code AS tournament,
		matches.player_id AS player_id,
		players.name AS player_name,
		matches.opponent_id AS opponent_id,
		matches.result AS result
	FROM matches LEFT OUTER JOIN players ON matches.player_id = players.id
	GROUP BY 
		matches.entry,
		players.name
	ORDER BY matches.entry
);


/*	v_results adds the opponents name to the v_namingPlayers view
	The players table  is used to fill in the players.name that is associated with v_namingPlayers.opponent_id
	NOTES:
		Maybe use a sub query?
*/
CREATE VIEW v_results AS (
	SELECT
		v_namingPlayers.entry AS entry,
		v_namingPlayers.tournament AS tournament,
		v_namingPlayers.player_id AS player_id,
		v_namingPlayers.player_name AS player_name,
		v_namingPlayers.opponent_id AS opponent_id,
		players.name AS opponent_name,
		v_namingPlayers.result AS result
	FROM v_namingPlayers LEFT OUTER JOIN players ON v_namingPlayers.opponent_id = players.id
	GROUP BY
		v_namingPlayers.entry,
		v_namingPlayers.tournament,
		v_namingPlayers.player_id,
		v_namingPlayers.player_name,
		v_namingPlayers.opponent_id,
		players.name,
		v_namingPlayers.result
	ORDER BY v_namingPlayers.entry
);


/*
	Creates a table showing player's ID, player's name, and the number of wins.
	Shows all registered players including those with 0 wins.
*/
CREATE VIEW v_wins AS (
	SELECT
		players.id AS player_id,
		players.name AS player_name,
		COALESCE(missing_zeros.wins, 0) AS wins
	FROM players LEFT OUTER JOIN (
	-- Using sub query to join the player list with a win count
		SELECT
			players.id AS player_id,
			players.name AS player_name,
			count(v_results.result) AS wins
		FROM players LEFT OUTER JOIN v_results ON players.id = v_results.player_id
		WHERE v_results.result = 'win'
		GROUP BY players.id, players.name
		ORDER BY wins DESC
		) AS missing_zeros ON players.id = missing_zeros.player_id
	GROUP BY
		players.id,
		players.name,
		missing_zeros.wins
	ORDER BY wins DESC
);

/*	v_OMW needs to display a table with player's ID, player's name, number of wins, and Opponent Match Wins
	NOTES:
		Gotta love Google:
				CREATE VIEW cumPoints AS
    				SELECT
    				    player AS id,
    				    COALESCE(SUM(points), 0) as points,
    				    COALESCE(sum(opp_points), 0) as OMP
    				FROM matches_by_player as MBP1
    				LEFT JOIN
    				   (SELECT
    				        MBP2.player as opponent,
    				        COALESCE(SUM(points), 0) as opp_points
    				    FROM matches_by_player as MBP2
    				    WHERE player IN
    				            (SELECT opponent
    				            FROM matches_by_player as MBP3)
    				    GROUP BY MBP2.player) as opp_list
    				    ON MBP1.opponent = opp_list.opponent
    				GROUP BY player
    				ORDER BY player;
		The following psql command returns a list of opponent IDs and names:
			SELECT opponent_id, opponent_name FROM v_results WHERE player_id = 1;
		It now needs to be combined with v_wins to get the opponents OMW?

		I am not sure how to populate for every player.
		The above psql statement seems like it will only work for one player at a time.
		
CREATE VIEW v_OMW AS (
	SELECT

);

*/


