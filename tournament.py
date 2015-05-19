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


def deleteMatches(tournament='blnk'):
    """Remove all the match records from the database.

    Args:
      tournament:  A three character code assigned to each tournament.
            blnk:  If there is no argument passed, all matches in all tournaments will be deleted.
    """
    db = connect()
    db_cursor = db.cursor()
    if tournament == 'blnk':
        query = "DELETE FROM matches"
        db_cursor.execute(query)
        print '==>  All matches were deleted successfully.'
    else:
        query = "DELETE FROM matches WHERE tournament = %s"
        db_cursor.execute(query, (tournament,))
        print '==>  All matches were deleted from ' + tournament + ' successfully.'
    db.commit()
    db.close()


def deletePlayers(player='blnk'):
    """Remove all the player records from the database.

    When player ID is deleted, all match records for that ID are also deleted.

    Args:
      player:  This is the ID of the player to be deleted.
        blnk:  If there is no argument passed, all players will be deleted.
    """
    db = connect()
    db_cursor = db.cursor()
    if player == 'blnk':
        query = "DELETE FROM players where id <> 0"
        db_cursor.execute(query)
        print '==>  All players were deleted successfully.'
    else:
        query = "DELETE FROM players WHERE id = %s"
        db_cursor.execute(query, (player))
        print '==>  Player ID: ' + player + ' deleted.'
    db.commit()
    db.close()


def countPlayers(tournament='blnk'):
    """Returns the number of players currently registered.

    Args:
      tournament:  A three character code assigned to each tournament.
            blnk:  If there is no argument passed, all players in all tournaments will be counted.
    """
    db = connect()
    db_cursor = db.cursor()
    if tournament == 'blnk':
        query = "SELECT count(*) FROM players WHERE id <> 0"
        db_cursor.execute(query)
        rows = db_cursor.fetchone()
        print '==>  ' + str(rows[0]) + ' players are registered for all tournaments.'
    else:
        query = "SELECT count(*) FROM players WHERE tournament = %s, id <> 0"
        db_cursor.execute(query, (tournament,))
        rows = db_cursor.fetchone()
        print '==>  ' + str(rows[0]) + ' players are registered for tournament ' + tournament + '.'
    db.commit()
    db.close()
    return rows[0]


def registerPlayer(tournament, name):
    """Adds a player to the tournament database.

    Args:
      tournament:  A three character code assigned to each tournament.
            name:  The player's full name.  This does not need to be a uniue value

    Notes:
      The database will automatically assign a unique serial id number for the player.
    """
    db = connect()
    db_cursor = db.cursor()
    query = "INSERT INTO players (tournament, name) VALUES (%s, %s)"
    # Try to register player 100 times. Incase serial generated id == previously entered user id
    for i in range(1, 100):
        try:
            db_cursor.execute(query, (tournament, name,))
            break
        except psycopg2.IntegrityError:
            # If error from duplicate id is thrown, roll back changes.
            db.rollback()
    else:
        print 'We tried 100 times to enter register the player and a unique id could not be assigned.  Run registerPlayer(tournament) again to try 100 more times.'
    print '==>  ' + name + ' has been registered for tournament: ' + tournament
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
             id:  the player's unique id (assigned by the database)
           name:  the player's full name (as registered)
           wins:  the number of matches the player has won
        matches:  the number of matches the player has played

    Notes:
      The first entry will be the player in first place, or a player tied for first place.
    """
    db = connect()
    db_cursor = db.cursor()
    query = "SELECT * FROM playerStandings"
    db_cursor.execute(query)
    standings = db_cursor.fetchall()
    db.close()
    print '==>  Player standings compiled successfully.'
    return standings


def reportMatch(tournament, player, opponent, result):
    """Records the outcome of a single match between two players.

    Args:
      tournament:  A three character code assigned to each tournament.
          player:  The id number of the first playerselfself.
        opponent:  The id number of the player's opponent.
          result:  The result of the match. Must be 'win', 'lose', or 'tie'.

    Notes:
      reportMatch() will also report the results for the opponent into the matches table.
    """
    db = connect()
    db_cursor = db.cursor()
    query = "INSERT INTO matches (tournament, player_id, opponent_id, result) VALUES (%s, %s, %s, %s)"
    db_cursor.execute(query, (tournament, player, opponent, result))
    print '==>  Match recorded successfully. \n ====>  Player ID: %s \n ====>  Opponent ID: %s \n ====>  Tournament: %s \n ====>  Result: %s' % (str(player), str(opponent), tournament, result)
    if opponent <> 0:
        if result == 'win':
            db_cursor.execute(query, (tournament, opponent, player, 'lose'))
            print '==>  Match recorded successfully. \n ====>  Player ID: %s \n ====>  Opponent ID: %s \n ====>  Tournament: %s \n ====>  Result: lose' % (str(opponent), str(player), tournament)
        elif result == 'lose':
            print '==>  Match recorded successfully. \n ====>  Player ID: %s \n ====>  Opponent ID: %s \n ====>  Tournament: %s \n ====>  Result: win' % (str(opponent), str(player), tournament)
            db_cursor.execute(query, (tournament, opponent, player, 'win'))
        else:
            db_cursor.execute(query, (tournament, opponent, player, 'tie'))
            print '==>  Match recorded successfully. \n ====>  Player ID: %s \n ====>  Opponent ID: %s \n ====>  Tournament: %s \n ====>  Result: tie' % (str(opponent), str(player), tournament)
    db.commit()
    db.close()


def swissPairings(tournament):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    NEED TO:
        incorporate bye week if odd number of players

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
    z_pairings = []
    opponent = []
    played = []
    byeRound = []
    num = len(players)
    if num % 2:
        # Create a list of player IDs sorted by least wins and then least OMWs
    	query = "SELECT v_standings.id AS id, v_standings.name AS name FROM v_standings ORDER BY v_standings.wins, v_standings.omw"
    	db_cursor.execute(query)
    	losers = db_cursor.fetchall()
        # Create list of player IDs that have had a bye round already
    	query = "SELECT player_id AS id, player_name AS name FROM v_results WHERE opponent_id=0 GROUP BY player_id, player_name"
    	db_cursor.execute(query)
    	byeAlready = db_cursor.fetchall()
        # Remove player IDs that have had a bye round from the players
        # sorted by loses
    	byeCandidates = [x for x in losers if x not in byeAlready]
        # Report the bye match as a win for the player
        print byeCandidates
        print '^-- byeCandidates'
        # Shouldn't report match since is only reporting
        # reportMatch(tournament, byeCandidates[0][0], 0, 'win')
        # Remove the player select for bye from the list of players for the
        # Swiss pairings
        byeRound = [byeCandidates[0], ]
        print byeRound
        print '^-- Remove bye'
        players = [x for x in players if x not in byeRound]
        print players
        print '^-- players after removing bye'
    while num > 1:
        print players
        print '^-- After eiting the if statement'
        player = players[0]
        query = "SELECT waldo.id, waldo.name FROM (SELECT v_standings.*, oppid.played FROM v_standings LEFT OUTER JOIN (SELECT v_results.opponent_id AS played FROM v_results WHERE v_results.player_id = %s GROUP BY v_results.opponent_id) AS oppid ON v_standings.id = oppid.played) AS waldo WHERE waldo.tournament =%s AND waldo.played IS NULL AND waldo.id <> %s AND waldo.id <> %s"
        db_cursor.execute(query, (str(player[0]), tournament, str(player[0]), str(byeRound[0][0])))
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
    # print '==> Bye week for ' + byeCandidates[0][1] + ' (ID: ' + byeCandidates[0][1] + ').'
    for pair in z_pairings:
        print '==> ' + str(pair) + '/n'
    db.rollback()
    db.close()
    return byeRound + z_pairings

swissPairings('WOW')
