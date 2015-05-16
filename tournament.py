#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.

    Returns a database connection.
    """
    return psycopg2.connect("dbname=tournament")


def deleteMatches(tournament='blank'):
    """Remove all the match records from the database.

    Args:
      tournament: All the matches in the entered tournament will be deleted.
      blank: If there is no argument passed, all matches in all tournaments will be deleted.
    """
    db = connect()
    db_cursor = db.cursor()
    if tournament == 'blank':
        query = "DELETE FROM matches"
        db_cursor.execute(query)
        print '==>  All matches were deleted successfully.'
    else:
        query = "DELETE FROM matches WHERE tournament_code = %s"
        db_cursor.execute(query, (tournament,))
        print '==>  All matches were deleted from ' + tournament + ' successfully.'
    db.commit()
    db.close()


def deletePlayers(player='blank'):
    """Remove all the player records from the database.

    When player ID is deleted, all match records for that ID are also deleted.

    Args:
      player: This is the ID of the player to be deleted.
      blank: If there is no argument passed, all players will be deleted.
    """
    db = connect()
    db_cursor = db.cursor()
    if player == 'blank':
        query = "DELETE FROM players"
        db_cursor.execute(query)
        print '==>  All players were deleted successfully.'
    else:
        query = "DELETE FROM players WHERE id = %s"
        db_cursor.execute(query, (player))
        print '==>  Player ID: ' + player + ' deleted.'
    db.commit()
    db.close()


def countPlayers(tournament='blank'):
    """Returns the number of players currently registered.

    Args:
      tournament: The number of players in the passed tournament code will be counted.
      blank: If there is no argument passed, all players in all tournaments will be counted.
    """
    db = connect()
    db_cursor = db.cursor()
    if tournament == 'blank':
        query = "SELECT count(*) FROM players"
        db_cursor.execute(query)
        rows = db_cursor.fetchone()
        print '==>  ' + str(rows[0]) + ' players are registered for all tournaments.'
    else:
        query = "SELECT count(*) FROM players WHERE tournament_code = %s"
        db_cursor.execute(query, (tournament,))
        rows = db_cursor.fetchone()
        print '==>  ' + str(rows[0]) + ' players are registered for tournament ' + tournament + '.'
    db.commit()
    db.close()
    return rows[0]


# DONE
def registerPlayer(tournament, name):
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
    # Try to register player 100 times. Incase serial generated id == previously entered user id
    for i in range(1, 100):
        try:
            db_cursor.execute(query, (tournament, name,))
            break
        except psycopg2.IntegrityError:
            # If error from duplicate id is thrown, roll back changes.
            db_cursor.rollback()
    else:
        print 'We tried 100 times to enter register the player and a unique id could not be assigned.  Run registerPlayer(tournament) again to try 100 more times.'
    db.commit()
    db.close()
    print '==>  ' + name + ' has been registered for tournament: ' + tournament


# DONE
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
    query = "SELECT * FROM playerStandings"
    db_cursor.execute(query)
    standings = db_cursor.fetchall()
    db.close()
    return standings
    print '==>  Player standings compiled successfully.'



# DONE
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
    print '==>  Match recorded successfully. \n ====>  Player ID: %s \n ====>  Opponent ID: %s \n ====>  Tournament: %s \n ====>  Result: %s' % (str(player), str(opponent), tournament_code, result)
    if result == 'win':
        db_cursor.execute(query, (tournament_code, opponent, player, 'lose'))
        print '==>  Match recorded successfully. \n ====>  Player ID: %s \n ====>  Opponent ID: %s \n ====>  Tournament: %s \n ====>  Result: lose' % (str(opponent), str(player), tournament_code)
    elif result == 'lose':
        print '==>  Match recorded successfully. \n ====>  Player ID: %s \n ====>  Opponent ID: %s \n ====>  Tournament: %s \n ====>  Result: win' % (str(opponent), str(player), tournament_code)
        db_cursor.execute(query, (tournament_code, opponent, player, 'win'))
    else:
        db_cursor.execute(query, (tournament_code, opponent, player, 'tie'))
        print '==>  Match recorded successfully. \n ====>  Player ID: %s \n ====>  Opponent ID: %s \n ====>  Tournament: %s \n ====>  Result: tie' % (str(opponent), str(player), tournament_code)
    db.commit()
    db.close()


def swissPairings(tournament):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    NEED TO:
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
    query = "SELECT id, name FROM v_standings WHERE tournament = %s"
    db_cursor.execute(query, (tournament,))
    players = db_cursor.fetchall()
    db.close()
    z_pairings = []
    opponent = []
    played = []
    num = len(players)
    while num > 1:
        player = players[0]
        db = connect()
        db_cursor = db.cursor()
        query = "SELECT waldo.id, waldo.name FROM (SELECT v_standings.*, oppid.played FROM v_standings LEFT OUTER JOIN (SELECT v_results.opponent_id AS played FROM v_results WHERE v_results.player_id = %s GROUP BY v_results.opponent_id) AS oppid ON v_standings.id = oppid.played) AS waldo WHERE waldo.tournament = %s AND waldo.played IS NULL AND waldo.id <> %s"
        db_cursor.execute(query, (str(player[0]), tournament, str(player[0])))
        opponent_list = db_cursor.fetchall()
        opponent_list = [x for x in opponent_list if x not in played]
        try:
            opponent = opponent_list[0]
            print 'Player ID: ' + str(player) + ' ... vs ... Player ID: ' + str(opponent)
            match = player + opponent
            z_pairings += (match,)
            played += (player, opponent)
            players = [x for x in players if x not in (player, opponent)]
            num = len(players)
        except:
            print 'Player ID: ' + str(player) + ' has played all opponents in Tournament: ' + tournament
            print 'Aborting roundOfSwiss().'
            print 'All matches to this point have been committed to the database.'
            break
    db.rollback()
    db.close()
    print '<::: Swiss Pairs :::>'
    return z_pairings

countPlayers()



'''







    db = connect()
    db_cursor = db.cursor()
    query = "SELECT id FROM v_standings WHERE tournament = %s"
    db_cursor.execute(query, (tournament,))
    players = db_cursor.fetchall()
    db.close()
    z_pairing = []
    WHILE len(players) > 1:
        player = players[0]

        db = connect()
        db_cursor = db.cursor()
        query = "SELECT v_results.tournament AS tournament, v_results.player_id AS player_id, v_results.opponent_id AS opponent_id, v_standings.wins AS opp_wins, v_standings.omw AS opp_omw FROM v_results LEFT OUTER JOIN v_standings ON v_results.opponent_id = v_standings.id WHERE v_results.tournament = %s AND v_results.player_id <> %d AND v_results.opponent_id <> %d"
        db_cursor.execute(query, (tournament, player, player))
        opponent_list = db_cursor.fetchall()
        db.close()

        opponent = opponent_list[0]
        match = player + opponent
        z_pairing += (match,)
        players.remove(player)
        players.remove(opponent)




    num_players = len(players)
    i = 0
    pairings = []
    while i < num_players:
    		match = players[i] + players[i+1]
    		pairings += (match,)
    		i = i + 2
    return pairings
    print '==>  Swiss pairings compiled successfully.'









registerPlayer('WOW', 'New Guy', )
registerPlayer('WOW', 'Old Guy')
reportMatch('WOW', 5, 6, 'win')
print swissPairings('ABC')
'''
