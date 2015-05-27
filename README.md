#Swiss Tournament Generator

This application was created as my submission for Project 2 of Udacity's Full Stack NanoDegree program.  The objective was to create an application using Python and PSQL that could effectively conduct a Swiss Style Tournament and that would pass all of the checks within the *tournament_test.py* file.


##Files
| File | Description |
|------|-------------|
| **tournament.py** | This is the main Python file used to conduct the Swiss Style Tournament. |
| **tournament.sql** | This is the database used to store tournament records. |
| **tournament_test.py** | This is a python file created by Udacity and modified to perform essential tests on the tournament application. |
| **populate_data.py** | A Python file that will populate the tournament application with data.  Once you have logged into Vagrant with `vagrant ssh`, populate the data by entering: `python populate_data.py` |


## Installation
####Prerequisites:
| Prerequisite | Documentation | Download |
|---------------|---------------|----------|
| **Git** | [docs](https://git-scm.com/doc) | [download](http://git-scm.com/downloads) |
| **Virtual Box** | [docs](https://www.virtualbox.org/wiki/Documentation) | [download](https://www.virtualbox.org/wiki/Downloads)|
| **Vagrant** | [docs](https://docs.vagrantup.com/v2/) | [download](https://www.vagrantup.com/downloads)       |

####Installation Steps:
1. Open terminal:
  - Windows: Use the Git Bash program (installed with Git) to get a Unix-style terminal.
  - Other systems: Use your favorite terminal program.
2. Change to the desired parent directory
  - Example: `cd Desktop/`
3. Using Git, clone the VM configuration:
  - Run: `git clone http://github.com/udacity/fullstack-nanodegree-vm fullstack`
  - This will create a new directory titled *fullstack* that contains all of the necessary configurations to run this application.
4. Move to the *vagrant* folder by entering: `cd fullstack/vagrant/`
5. Using Git, clone this project:
  - Run: `git clone https://github.com/gravic07/tournament.git tournament`
  - This will create a directory inside the *vagrant* directory titled *tournament*.
6. Run Vagrant by entering: `vagrant up`


## Usage
Once the installation steps are complete, you are ready to connect to the
Vagrant box.  To connect:

1. Log into Vagrant VM by entering: `vagrant ssh`
2. Move to *tournament* directory by entering: `cd /vagrant/tournament/`
3. Create the *tournament* database by entering: `psql -f tournament.sql`
>**Note:** You can run `psql -f tournament.sql` at anytime to completely delete the database and start over.

4. If you would like to test the database against Udacity's criteria, enter: `python tournament_test.py`
>**Note:** To clear the database after running tournament_test.py, you can either call the deletePlayers() and deleteMatches() functions or refer to step 3.

5. Launch Python command line by entering `python`
6. Import tournament by entering: `import tournament`
7. Execute a desired function. (see below)

###Code Example  
An example of code from the Python shell inside the vagrant vm.

```
>>> import tournament

>>> tournament.registerPlayer('ABC', 'Player One')
    ==>  Player One has been registered for tournament: ABC

>>> tournament.registerPlayer('ABC', 'Player Two')
    ==>  Player Two has been registered for tournament: ABC

>>> tournament.swissPairings('ABC')
    ==> (1, 'Player One', 2, 'Player Two')
    [(1, 'Player One', 2, 'Player Two')]

>>> tournament.reportMatch('ABC', 1, 2, 'win')
    ==>  Match recorded successfully.
     ====>  Player ID: 1
     ====>  Opponent ID: 2
     ====>  Tournament: ABC
     ====>  Result: win
    ==>  Match recorded successfully.
     ====>  Player ID: 2
     ====>  Opponent ID: 1
     ====>  Tournament: ABC
     ====>  Result: lose
```



###Functions
>**Note:** Make sure you import tournament.py before attempting to call any of these functions by entering `import tournament` and pressing *enter*.

>**Note:** All functions need to be proceeded by `tournament.` e.g. `tournament.playerStandings()`

>**Note:** The *tournament* argument is a three character code that is assigned to players in the same tournament.

**registerPlayer(tournament, name)**  
Registers a player by the *name* provided.  The *tournament* argument is optional and if a tournament is passed, the player will be registered to that tournament.  A *player ID* will be automatically generated.

**countPlayers(tournament)**  
Counts the number of players in the registry.  The *tournament* argument is optional and if a tournament is passed, only the players registered for that tournament will be counted.

**deletePlayers(playerID)**
Deletes players from the registry.  The *playerID* argument is optional and if a player ID if passed, only that player will be deleted.

**reportMatch(tournament, player, opponent, result)**  
Reports a match between two players.  
  *tournament*:  tournament code  
      *player*:  id number of the player  
    *opponent*:  id number of the opponent
      *result*:  result of match (must be '*win*', '*lose*', '*tie*')
>**Note:** reportMatch() also reports a second match with the opponent as the player and the player as the opponent.

**deleteMatches(tournament)**  
Deletes all match record.  If a three character tournament code is passed, only the matches for the tournament will be deleted.

**playerStandings()**  
Returns the win record of all registered players.  
More specifically, returns a list of tuples each consisting of a player's id, name, # of wins, and # of matches.  The players are returned in Ascending order based on # of wins.  
Example:  
```
[ (103, 'Rich Guy', 3L, 3L),
  (111, 'Cool Guy', 2L, 3L),
  (104, 'Poor Guy', 2L, 3L),
  (108, 'Big Guy', 2L, 3L),
  (101, 'New Guy', 1L, 3L),
  (110, 'Bad Guy', 1L, 3L),
  (105, 'Tall Guy', 1L, 3L),
  (107, 'Small Guy', 1L, 3L),
  (109, 'Good Guy', 1L, 3L),
  (106, 'Short Guy', 0L, 3L),
  (102, 'Old Guy', 0L, 3L) ]
```

**swissPairings(tournament)**  
Returns a new round of matches based on the Swiss Tournament pairing guidelines.  
More specifically, returns a list of tuples each consisting of player id, player name, opponent id, and opponent name.  The *tournament* argument is optional and if a tournament is passed, only the players registered for that tournament will be considered in the pairing.  
Example:  
```
[ (106, 'Short Guy', 0, 'BYE'),
  (103, 'Rich Guy', 108, 'Big Guy'),
  (104, 'Poor Guy', 111, 'Cool Guy'),
  (109, 'Good Guy', 105, 'Tall Guy'),
  (101, 'New Guy', 110, 'Bad Guy'),
  (107, 'Small Guy', 102, 'Old Guy') ]
```
>**Note:** The above example returned a *BYE* round since an odd number of players where registered for the tournament.  

>**Note:** If swissPairings() can not be completed due to tournament guideline constraints, the pairing will be aborted.


## Contributing
In the off chance someone would like to contribute to this project, follow the usual steps:

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D


## Credits
Created by gravic07


## License
Licensed under the MIT License (MIT)
```
Copyright (c) [2015] [gravic07]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
