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

INSERT INTO tournament_log (tournament_code) VALUES ('XYZ');

-- Create some tables.
CREATE TABLE players (
	tournament_code   varchar(3) REFERENCES tournament_log (tournament_code) ON DELETE RESTRICT,
			   name   text,
	  		     id   serial PRIMARY KEY,
	  		 UNIQUE   (id)
);

INSERT INTO players VALUES ('XYZ', 'John Doe');




-- Not creating with ERROR 43: ERROR:  there is no unique constraint matching given keys for referenced table "players"

CREATE TABLE matches (
		   match_id   serial PRIMARY KEY,
	tournament_code   varchar(3) REFERENCES tournament_log (tournament_code) ON DELETE RESTRICT,
	      player_id   integer REFERENCES players (id) ON DELETE RESTRICT,
	    player_name   text REFERENCES players (name) ON DELETE RESTRICT,
	    opponent_id   integer REFERENCES players (id) ON DELETE RESTRICT,
	  opponent_name   text REFERENCES players (name) ON DELETE RESTRICT,
		     result   text CHECK (result IN ('win', 'lose', 'tie')),
		     UNIQUE   (player_id, opponent_id)
);



-- Create some views.




-- Let's fill in some data...











