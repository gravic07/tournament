#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    db_cursor = db.cursor()
    query = "DELETE FROM matches"
    db_cursor.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database.
    
    Issues:
      Currently deletes matches as well do to coloumn constraint 'ON DELETE CASCADE'
    """
    db = connect()
    db_cursor = db.cursor()
    query = "DELETE FROM players"
    db_cursor.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    db_cursor = db.cursor()
    query = "SELECT count(*) FROM players"
    db_cursor.execute(query)
    rows = db_cursor.fetchone()
    db.commit()
    db.close()
    return rows[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    db_cursor = db.cursor()
    query = "INSERT INTO players (name) VALUES (%s)"
    db_cursor.execute(query, (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    db_cursor = db.cursor()
    query = "SELECT * FROM v_standings"
    db_cursor.execute(query)
    standings = db_cursor.fetchall()
    db.close()
    return standings
    print '!!-- playerStandings ran --!!'
    


def reportMatch(player, opponent, result):
    """Records the outcome of a single match between two players.

    Args:
      player:  the id number of the first player
      opponent:  the id number of the player's opponent
      result: the result of the match. Must be 'win', 'lose', or 'tie'
    """
    db = connect()
    db_cursor = db.cursor()
    query = "INSERT INTO matches (playerID, opponentID, result) VALUES (%s, %s, %s)"
    db_cursor.execute(query, (player, opponent, result))
    
    if result == 'win':
        db_cursor.execute(query, (opponent, player, 'lose'))
    elif result == 'lose':
        db_cursor.execute(query, (opponent, player, 'win'))
    else:
        db_cursor.execute(query, (opponent, player, 'tie'))

    db.commit()
    db.close()
    print '!!-- reportMatch ran --!!'

 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    prevent rematches between players
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    db_cursor = db.cursor()
    query = "SELECT id, name FROM v_standings"
    db_cursor.execute(query)
    players = db_cursor.fetchall()

    num_players = len(players)
    i = 0
    pairings = []
    while i < num_players:
        match = players[i] + players[i+1]
        pairings += (match,)
        i = i + 2
    db.close()
    return pairings
    print '!!-- swissPairings ran --!!'


    




