#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
# This file defines multiple Python functions to be used in facilitating
# a Swiss-system tournament

import psycopg2


def connect():
    """Connect to the PostgreSQL database.

    Returns: a database connection.
    """
    return psycopg2.connect("dbname=tournament")


def deleteMatches(tournament='blnk'):
    """Remove all the match records from an individual or all tournaments

    When a tournament code is passed as the argument, only the players
    registered to that tournament will be deleted.  If no argument is passed,
    all players in all tournaments will be deleted.

    When a tournament code is passed as the argument, only the players
    registered to that tournament will be deleted.  If no argument is passed,
    all players in all tournaments will be deleted.

    Args:   tournament:  Optional argument that takes a three character code
                assigned to each tournament.
            blnk:  If there is no argument passed, all matches in all
                tournaments will be deleted.
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
    """Removes player(s) from the database.

    When a player's ID is passed as the argument, that player is deleted from
    the database.  If no player ID is specified, all players will be deleted.

    In both cases, when a player is deleted from the database all of the match
    records in which the player(s) were either the player or opponent will be
    deleted as well.  This is due to a constraint on the database requiring
    that a player be currently registered to have match records.

    Args:   player:  Optional argument that accepts the ID of a registered
                player.
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
    """Returns the number of players registered.

    When a tournament code is passed as the argument, the count returned will
    be limited to the players in that tournament.  If no argument is passed,
    the count of all registered players will be returned.

    Args:   tournament:  Optional argument that takes a three character code
                assigned to each tournament.
            blnk:  If there is no argument passed, all players in all
                tournaments will be counted.
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

    The database will automatically assign a unique serial id number for the
    player.

    Args:   tournament:  Optional argument that takes a three character code
                assigned to each tournament.  Player will be registered to
                compete in the tournament passed.
            name:  The player's full name.  This does not need to be a uniue
                value
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
    """Returns a list of all players and their win records, sorted by wins.

    The first entry will be the player in first place, or a player tied for
    first place.

    Returns:  A list of tuples, each of which contains:
                id:  The player's unique id (assigned by the database).
                name:  The player's full name (as registered).
                wins:  The number of matches the player has won.
                matches:  The number of matches the player has played.
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

    reportMatch() will also report the results for the opponent into the
    matches table.

    Args:   tournament:  A three character code assigned to each tournament.
                This would be the tournament that the players are enrolled in.
            player:  The id number of the first player.
            opponent:  The id number of the player's opponent.
            result:  The result of the match. Must be 'win', 'lose', or 'tie'.
                This is reported from the perspective of the 'player'.
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


# Make the tournament argument optional to that all players will be included
# if it is left blank.
def swissPairings(tournament='blnk'):
    """Returns a list of pairs of players for the next round of a match.

    This sorts the current players by wins and then by opponent match wins.
    If there is an odd number of players, a bye week is assigned to the
    player closest to last place that has not had a bye round already.  (Each
    player can only have one bye round.)  The first place player is then paired
    with the highest ranked player that he has not already playerd. (Each
    player can only play another player one time.)  If the pairings can not be
    completed due to a player having played all other players, the pairing will
    be aborted.

    Args:     tournament:  A three character code assigned to each tournament.
                  Only the players that are registered for the tournament code
                  passed in will be included in the pairings.

    Returns:  A list of tuples, each of which contains (id1, name1, id2, name2)
                  id1: the first player's unique id
                  name1: the first player's name
                  id2: the second player's unique id
                  name2: the second player's name
    """
    db = connect()
    db_cursor = db.cursor()
    getPlayers = "SELECT id, name FROM v_standings"
    fromTournament = " WHERE tournament = %s"
    if tournament == 'blnk':
        db_cursor.execute(getPlayers)
    else:
        db_cursor.execute(getPlayers + fromTournament, (tournament,))
    players = db_cursor.fetchall()
    swissPairs = []
    alreadyPlayed = []
    recordBye = []
    countOfPlayers = len(players)
    # Assign a bye week if there is an odd number of players in the round
    if countOfPlayers % 2:
        playersByLeastWins = """
        SELECT v_standings.id AS id, v_standings.name AS name
        FROM v_standings
        ORDER BY v_standings.wins, v_standings.omw
        """
        db_cursor.execute(playersByLeastWins)
        playersByLeastWins = db_cursor.fetchall()
        playersAlreadyBye = """
        SELECT player_id AS id, player_name AS name
        FROM v_results
        WHERE opponent_id=0
        GROUP BY player_id, player_name
        """
        db_cursor.execute(playersAlreadyBye)
        playersAlreadyBye = db_cursor.fetchall()
        byeCandidates = [player for player in playersByLeastWins
                          if player not in playersAlreadyBye]
        playerWithBye = [byeCandidates[0],]
        players = [player for player in players if player not in playerWithBye]
        recordBye = (byeCandidates[0][0], byeCandidates[0][1], 0, 'BYE')
        # print '==> Bye week for ' + str(playerWithBye)
    # Pair players based on the stipulations in the doc string
    while countOfPlayers > 1:
        player = players[0]
        findOpponents = """
            SELECT waldo.id, waldo.name
            FROM (
                SELECT v_standings.*, oppid.played
                FROM v_standings LEFT OUTER JOIN (
                    SELECT v_results.opponent_id AS played
                    FROM v_results
                    WHERE v_results.player_id = %s
                    GROUP BY v_results.opponent_id) AS oppid
                ON v_standings.id = oppid.played) AS waldo
            WHERE waldo.played IS NULL AND waldo.id <> %s
            """
        withTournament = " AND waldo.tournament =%s"
        byeInEffect = " AND waldo.id <> %s"
        if tournament == 'blnk':
            if recordBye == []:
                db_cursor.execute(findOpponents,
                (str(player[0]), str(player[0])))
            else:
                db_cursor.execute(findOpponents + byeInEffect,
                (str(player[0]), str(player[0]), str(playerWithBye[0][0])))
        else:
            if recordBye == []:
                db_cursor.execute(findOpponents + withTournament,
                (str(player[0]), tournament, str(player[0])))
            else:
                db_cursor.execute(findOpponents + withTournament + byeInEffect, (str(player[0]), str(player[0]), tournament,
                str(playerWithBye[0][0])))

        opponentList = db_cursor.fetchall()
        opponentList = [opponent for opponent in opponentList
                         if opponent not in alreadyPlayed]
        try:
            opponent = opponentList[0]
            # print '==> ' + str(player) + ' ... vs ... ' + str(opponent)
            match = player + opponent
            swissPairs += (match,)
            alreadyPlayed += (player, opponent)
            players = [x for x in players if x not in (player, opponent)]
            countOfPlayers = len(players)
        except:
            print str(player) + ' has played all opponents in Tournament: ' + tournament
            print 'Aborting swissPairings().'
            break
    print '==> ' + str(recordBye)
    for pair in swissPairs:
        print '==> ' + str(pair)
    db.rollback()
    db.close()
    recordBye = [recordBye,]
    return recordBye + swissPairs
