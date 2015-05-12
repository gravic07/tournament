#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteTournaments():
    """Removes all tournaments."""
    db = connect()
    db_cursor = db.cursor()
    query = "DELETE FROM matches"
    db_cursor.execute(query)
    db.commit()
    db.close()


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
    print '!!-- There are ' + str(rows[0]) + ' players registered --!!'


def registerPlayer(tournament_code, name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      tournament_code: A three character code assigned to each tournament.
      name: the player's full name (need not be unique).
    """
    db = connect()
    db_cursor = db.cursor()
    query = "INSERT INTO players (tournament_code, name) VALUES (%s, %s)"
    db_cursor.execute(query, (tournament_code, name,))
    db.commit()
    db.close()
    print '!!-- ' + name + ' registered to tournament: ' + tournament_code + ' --!!'


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
    query = "SELECT * FROM v_wins"
    db_cursor.execute(query)
    standings = db_cursor.fetchall()
    db.close()
    return standings
    print '!!-- playerStandings ran --!!'
    


def reportMatch(tournament_code, player, opponent, result):
    """Records the outcome of a single match between two players.

    reportMatch() will also report the results for the opponent into the matches table.

    Args:
      tournament_code:  A three character code assigned to each tournament.
               player:  The id number of the first playerselfself.
             opponent:  The id number of the player's opponent.
               result:  The result of the match. Must be 'win', 'lose', or 'tie'.
    """
    db = connect()
    db_cursor = db.cursor()
    query = "INSERT INTO matches (tournament_code, player_id, opponent_id, result) VALUES (%s, %s, %s, %s)"
    db_cursor.execute(query, (tournament_code, player, opponent, result))
    print '!!-- Player ID: ' + str(player) + ' played ' + str(opponent) + ' in Tournament: ' + tournament_code + ' | Result: ' + result + ' --!!'
    if result == 'win':
        db_cursor.execute(query, (tournament_code, opponent, player, 'lose'))
        print '!!-- Player ID: ' + str(opponent) + ' played ' + str(player)  + ' in Tournament: ' + tournament_code + ' | Result: Lose --!!'
    elif result == 'lose':
        db_cursor.execute(query, (tournament_code, opponent, player, 'win'))
        print '!!-- Player ID: ' + str(opponent) + ' played ' + str(player)  + ' in Tournament: ' + tournament_code + ' | Result: Win --!!'
    else:
        db_cursor.execute(query, (tournament_code, opponent, player, 'tie'))
        print '!!-- Player ID: ' + str(opponent) + ' played ' + str(player)  + ' in Tournament: ' + tournament_code + ' | Result: Tie --!!'
    db.commit()
    db.close()

 
 
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


    



registerPlayer('WOW', 'New Guy', )
registerPlayer('WOW', 'Old Guy')
reportMatch('WOW', 5, 6, 'win')

