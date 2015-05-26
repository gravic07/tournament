-- Table definitions for the tournament project.

DROP DATABASE tournament;
CREATE DATABASE tournament;
-- Connect to the newly created DB
\c tournament;


CREATE TABLE players (
	tournament   varchar(3),
		  name   text,
	  		id   serial PRIMARY KEY,
	  	UNIQUE   (id)
);

-- Inserting a "BYE" player to support handling bye rounds
INSERT INTO players (name, id) VALUES  ('BYE', 0);


CREATE TABLE matches (
	 tournament   varchar(3),
	  player_id   integer REFERENCES players (id) ON DELETE CASCADE,
	opponent_id   integer REFERENCES players (id) ON DELETE CASCADE,
		 result   text CHECK (result IN ('win', 'lose', 'tie')),
		  entry   serial PRIMARY KEY,
		 UNIQUE   (player_id, opponent_id)
);


/*
Create table listing entry #, tournament, player id, player name,
opponent id, opponent name and match result.
*/
CREATE VIEW v_results AS (
	SELECT
		namingPlayers.entry AS entry,
		namingPlayers.tournament AS tournament,
		namingPlayers.player_id AS player_id,
		namingPlayers.player_name AS player_name,
		namingPlayers.opponent_id AS opponent_id,
		players.name AS opponent_name,
		namingPlayers.result AS result
	FROM (
		SELECT
			matches.entry AS entry,
			matches.tournament AS tournament,
			matches.player_id AS player_id,
			players.name AS player_name,
			matches.opponent_id AS opponent_id,
			matches.result AS result
		FROM matches LEFT OUTER JOIN players ON matches.player_id = players.id
		WHERE matches.player_id <> 0
		GROUP BY
			matches.entry,
			players.name
		ORDER BY matches.entry
	) AS namingPlayers LEFT OUTER JOIN players
	ON namingPlayers.opponent_id = players.id
	GROUP BY
		namingPlayers.entry,
		namingPlayers.tournament,
		namingPlayers.player_id,
		namingPlayers.player_name,
		namingPlayers.opponent_id,
		players.name,
		namingPlayers.result
	ORDER BY entry
);


-- Create a table listing player id, name, and # of wins
CREATE VIEW v_wins AS (
	SELECT
		players.id AS id,
		players.name AS name,
		COALESCE(missing_zeros.wins, 0) AS wins
	FROM players LEFT OUTER JOIN (
		SELECT
			players.id AS player_id,
			players.name AS player_name,
			count(v_results.result) AS wins
		FROM players LEFT OUTER JOIN v_results ON players.id = v_results.player_id
		WHERE v_results.result = 'win'
		GROUP BY players.id, players.name
		ORDER BY wins DESC
		) AS missing_zeros ON players.id = missing_zeros.player_id
	WHERE players.id <> 0
	GROUP BY
		players.id,
		players.name,
		missing_zeros.wins
	ORDER BY wins DESC
);


-- Create a table listing player id, name, # of wins, and # of matches
CREATE VIEW playerStandings AS (
	SELECT
		v_wins.*,
		count(matches.player_id) AS matches
	FROM v_wins LEFT OUTER JOIN matches
	ON v_wins.id = matches.player_id
	WHERE v_wins.id <> 0
	GROUP BY v_wins.id, v_wins.name, v_wins.wins
	ORDER BY v_wins.wins DESC
);


-- Create a table listing player id, name, tournament, # of OMWs
CREATE VIEW v_omw AS (
	SELECT
	 	v_results.player_id AS id,
		v_results.player_name AS name,
		v_results.tournament AS tournament,
		sum(v_wins.wins) as omw
	FROM v_results LEFT OUTER JOIN v_wins
	ON v_results.opponent_id = v_wins.id
	WHERE v_results.player_id <> 0
	GROUP BY v_results.player_id, v_results.player_name, v_results.tournament
);


-- Create a table listing player id, name, tournament, wins, and OMWs
CREATE VIEW v_standings AS (
	SELECT
		players.id AS id,
		players.name AS name,
		players.tournament AS tournament,
		wins_omw.wins AS wins,
		wins_omw.omw AS omw
	FROM players LEFT OUTER JOIN (
		SELECT
			v_wins.*,
			v_omw.omw AS omw
			FROM v_wins LEFT OUTER JOIN v_omw
			ON v_wins.id = v_omw.id
		) AS wins_omw ON players.id = wins_omw.id
	WHERE players.id <> 0
	GROUP BY players.id, players.name, players.tournament, wins_omw.wins, wins_omw.omw
	ORDER BY wins_omw.wins DESC, wins_omw.omw DESC
);
