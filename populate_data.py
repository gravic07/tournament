#!/usr/bin/python

import random

from tournament import connect
from tournament import reportMatch
from tournament import swissPairings

from tournament_test import testDelete

# You can add players to the list below in the form of:
# (tournament, player id, player name)
thePlayers = [
	('WOW', 101, 'New Guy'),
	('WOW', 102, 'Old Guy'),
	('WOW', 103, 'Rich Guy'),
	('WOW', 104, 'Poor Guy'),
	('WOW', 105, 'Tall Guy'),
	('WOW', 106, 'Short Guy'),
	('WOW', 107, 'Small Guy'),
	('WOW', 108, 'Big Guy'),
	('WOW', 109, 'Good Guy'),
	('WOW', 110, 'Bad Guy'),
	('WOW', 111, 'Cool Guy')
]

theResults = [
	'win',
	'lose',
	'tie'
]


def registerPlayerUpdated(tournament, id, name):
    """Add a player to the tournament database.

	This calls registerPlayer and adds the ability to set the players ID.

    Args:
      tournament:  A three character code assigned to each tournament.
			  id:  Establish the ID for player.  This NEEDS to be a unique value.
            name:  The player's full name.  This does not need to be a uniue value.
    """
    db = connect()
    db_cursor = db.cursor()
    query = "INSERT INTO players (tournament, id, name) VALUES (%s, %s, %s)"
    db_cursor.execute(query, (tournament, id, name,))
    print '==>  ' + name + ' has been registered for tournament: ' + tournament
    db.commit()
    db.close()


def signUps(listOfPlayers):
    """Register a list of players to their individually assigned tournament.

    """
    for player in listOfPlayers:
        registerPlayerUpdated(player[0], player[1], player[2],)
        print '==>  ' + player[2] + ' registered to tournament ' + player[0] + '.'


def roundOfSwiss(tournament):
    """Execute a round of the Swiss Tournament

	Args:	tournament:

    """
    matches = swissPairings(tournament)
    if matches[0][2] == 0:
        byeRound = matches[0]
        reportMatch(tournament, byeRound[0], 0, 'win')
        del matches[0]
    for match in matches:
        result = random.choice(theResults)
        reportMatch(tournament, match[0], match[2], result)
    print '==>  Round of Swiss complete!'

# Delete Players and matches
testDelete()

# Register a list of players.
signUps(thePlayers)

# Player some rounds using the Swiss Tournament system
roundOfSwiss('WOW')
roundOfSwiss('WOW')
roundOfSwiss('WOW')




'''
if __name__ == '__main__':
	#final function to run
'''
