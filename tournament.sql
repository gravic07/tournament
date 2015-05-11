-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP DATABASE tournament;
CREATE DATABASE tournament;
\c tournament;



CREATE TABLE tournament_log (
	  tournament_id   serial PRIMARY KEY,
	tournament_code   varchar(3),
			 UNIQUE   (tournament_code)
);

INSERT INTO tournament_log (tournament_code) VALUES ('ABC');
INSERT INTO tournament_log (tournament_code) VALUES ('XYZ');

-- Create some tables.
CREATE TABLE players (
	tournament_code   varchar(3) REFERENCES tournament_log (tournament_code) ON DELETE RESTRICT,
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
	tournament_code   varchar(3) REFERENCES tournament_log (tournament_code) ON DELETE RESTRICT,
	      player_id   integer REFERENCES players (id) ON DELETE RESTRICT,
	    --player_name   text,
	    opponent_id   integer REFERENCES players (id) ON DELETE RESTRICT,
	  --opponent_name   text,
		     result   text CHECK (result IN ('win', 'lose', 'tie')),
		      entry   serial PRIMARY KEY,
		     UNIQUE   (player_id, opponent_id)
);


-- Insert two matches in tournament ABC
INSERT INTO matches VALUES ('ABC', 1, 2, 'win');
INSERT INTO matches VALUES ('ABC', 2, 1, 'lose');
INSERT INTO matches VALUES ('ABC', 3, 4, 'lose');
INSERT INTO matches VALUES ('ABC', 4, 3, 'win');

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
	SELECT matches.entry AS entry, matches.tournament_code AS tournament, matches.player_id AS player_id,  players.name AS player_name, matches.opponent_id AS opponent_id, matches.result AS result
	FROM matches LEFT OUTER JOIN players ON matches.player_id = players.id
	GROUP BY matches.entry, players.name
	ORDER BY matches.entry
);


/*	v_results adds the opponents name to the v_namingPlayers view
	The players table  is used to fill in the players.name that is associated with v_namingPlayers.opponent_id
*/
CREATE VIEW v_results AS (
	SELECT v_namingPlayers.entry AS entry, v_namingPlayers.tournament AS tournament, v_namingPlayers.player_id AS player_id,  v_namingPlayers.player_name AS player_name, v_namingPlayers.opponent_id AS opponent_id, players.name AS opponent_name, v_namingPlayers.result AS result
	FROM v_namingPlayers LEFT OUTER JOIN players ON v_namingPlayers.opponent_id = players.id
	GROUP BY v_namingPlayers.entry, v_namingPlayers.tournament, v_namingPlayers.player_id, v_namingPlayers.player_name, v_namingPlayers.opponent_id, players.name, v_namingPlayers.result
	ORDER BY v_namingPlayers.entry
);


/*	v_wins needs to display a table with player's ID, player's name, and number of wins
	NOTES:
		This view has not been updated to use v_results
		This version also did not show 0s in the win column
		I thought I had the 0s working previously using COALESCE(count( *column* ), 0)
*/
CREATE VIEW v_wins AS (
	SELECT players.id AS player, players.name AS name, count(matches.result) AS wins
	FROM players LEFT OUTER JOIN matches ON players.id = matches.player_id
	WHERE matches.result = 'win'
	GROUP BY players.id
	ORDER BY wins DESC
);






