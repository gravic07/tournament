#!/usr/bin/python

import random
import itertools

from tournament import connect
from tournament import reportMatch

from tournament_test import testDelete


the_players = [
	(1, 'Jeff'),
	(2, 'Adarsh'),
	(3, 'Amanda'),
	(4, 'Eduardo'),
	(5, 'Philip'),
	(6, 'Jee')
]

the_results = [
	'win',
	'lose',
	'tie'
]


def registerPlayerUpdated(player_id, name):
	"""Add a player to the tournament database.

	The database assigns a unique serial id number for the player.  (This
	should be handled by your SQL database schema, not in your Python code.)

	Args:
	  name: the player's full name (need not be unique).
	"""
	db = connect()
	db_cursor = db.cursor()
	query = "INSERT INTO players (id, name) VALUES (%s, %s)"
	db_cursor.execute(query, (player_id, name))
	db.commit()
	db.close()


def createRandomMatches(player_list, rounds):
	num_players = len(player_list)
	for i in xrange(rounds):
		print 'round %d' % (i+1)

		i = 0;
		while i < num_players:
			result = random.choice(the_results)
			player_id = player_list[i][0]
			player_name = player_list[i][1]
			opponent_id = player_list[i+1][0]
			opponent_name = player_list[i+1][1]
			reportMatch(player_id, opponent_id, result)
			print "%s (id=%s) vs. %s (id=%s) ... %s %ss." % (
				player_name,
				player_id,
				opponent_name,
				opponent_id,
				player_name,
				result)
			i = i + 2




def setup_players_and_matches():
	'''
	'''
	testDelete()
	for player in the_players:
		registerPlayerUpdated(player[0], player[1])

	createRandomMatches(the_players, 1)






def reorderPlayers(swissPairing):
    '''
    db = connect()
    db_cursor = db.cursor()
    query = "SELECT id, name FROM v_standings"
    db_cursor.execute(query)
    players = db_cursor.fetchall()
    print players
    '''
    num_pairings = len(swissPairing)
    newPlayers = []
    i = 0
    while i < num_pairings:
        player1_id = swissPairing[i][0]
        player1_name = swissPairing[i][1]
        player2_id = swissPairing[i][2]
        player2_name = swissPairing[i][3]
        newPlayers += [(player1_id, player1_name)]
        newPlayers += [(player2_id, player2_name)]
        i += 1
    newPlayers.insert(0, newPlayers.pop())

    num_players = len(newPlayers)
    newPairings = []
    i = 0
    while i < num_players:
        match = newPlayers[i] + newPlayers[i+1]
        newPairings += (match,)
        i += 2
    return newPairings
    print '!!-- reorderPlayers ran --!!'



def runTheSwiss(pair_results):
    '''Plays the matches recomended by swissPairings()

    Runs reportMatch() on the pairs that are suggested from swissPairings()
    The result of the match is determined by using random(choice) on a list of the potential outcomes.
    '''
    the_results = [
        'win',
        'lose',
        'tie'
    ]

    pairings = len(pair_results)
    x = 0
    while x < (pairings * 2):
        try:
            for i in range(pairings):
                playerID = pair_results[i][0]
                opponentID = pair_results[i][2]
                result = random.choice(the_results)
                '''
                BUG: Right now this is reporting match individually.
                     I would like for all 3 of the reportMatch()s to be tried before commiting it to the DB.
                '''
                reportMatch(playerID, opponentID, result)
                x = (pairings * 2) + 1
        except psycopg2.IntegrityError:
            print 'RE-RUN # %d!!!' % (x+1)
            pair_results = reorderPlayers(pair_results)
            x += 1
    if x == (pairings * 2):
        print 'Everyone has played everyone...'
    else:
        print '!!-- Round Complete --!!'






runTheSwiss(swissPairings())







if __name__ == '__main__':
	setup_players_and_matches()
