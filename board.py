# Imports Regex Library
import re
# Imports copy library
import copy
# Imports goAI class 
import goAI
import hashlib
from collections import namedtuple
import os

leaderboardRecord = namedtuple('leaderboardRecord',
  ['name','opponent','score','hash'])

# Purpose: To store game logic and variables in single object
class Board:
  # Purpose: Constructor, initialises object
  def __init__(self, size, opponent=False, board=None):
      # Sets winner attribute to none
      self.__winner = 0
      # Sets consecutive passes attribute to 0
      self.__consecutivePasses = 0
      # Sets finish attribute to False
      self.__finish = False
      # Sets size attribute to the value of the size parameter
      self.__size = size
      # If/Else statement which defines the acceptable input format
      if size < 10:
        # If size is less than 10 then only 1 number is required for stone
        # input
        self.__acceptableInput = re.compile(r'^([A-Z][0-9])$')
      else:
        # If size is greater than 10 then 2 numbers may be required for 
        # stone input
        self.__acceptableInput = re.compile(r'^([A-Z][0-9]{1,2})$')
      # Initialises name value
      name = ''
      # Prompts the user for a name
      while name == '':
        name = input("Please enter your name: ")
      # Sets the attribute playerName to name
      self.__playerName = name
      # Resets name variable
      name = ''
      # If/Else statement executes depending on whether opponent is a computer
      if opponent == True:
        # Prompts opponent for a name
        while name == '':
          name = input("Please enter your opponent's name: ")
        self.__opponentName = name
      else:
        self.__opponentName = "Computer"
      # If a board is passed in the constructor, use board, otherwise create
      # an empty 2D array of size in attribute size
      if board:
        self.__grid = board
      else:
        self.__grid = [[0 for x in range(self.__size)] 
                        for col in range(self.__size)]
      # History is an empty 3D array containing previously plated board states
      self.__history = []
      # Taken is a record of all groups which have been captured by either 
      # player
      self.__taken = [[] for x in range(3)]
      # Score is the current score of the game
      self.__score = 0

  # Purpose: Allows the user to enter a stone
  def player(self):
    # Prints the current state of the grid
    self.printGrid()
    # Prints the name of the player
    print('It is '+self.__playerName + '\'s turn')
    # Prints the current score
    self.printScore()
    # Instructs the user how to place a stone
    print('Place a stone in the format [letter][number]')
    # Provides two examples
    print('For Example: E3 or A11')
    # Sets valid input flag to false
    valid = False
    # Continues to execute until the users input is valid
    while valid != True:
      # Prompts the user to enter a stone position
      pos = input('Stone Position (or resign or pass): ')
      # If/Else executes depending on whether the user chooses to pass, 
      # resign or attempt to play a valid move
      if pos == 'pass' or pos == 'resign':
        # Sets valid flag to True
        valid = True
        # Executes if the player wishes to resign
        if pos == 'resign':
          # Set finish to true and winner to the opponent
          self.__finish = True
          self.__winner = 2
        else:
          # Counts consecutive passes, will end game after 3 consecutive 
          # passes
          self.__consecutivePasses = 0
      # Checks the input matches the regex pattern in the acceptableInput 
      # attribute
      elif self.__acceptableInput.match(pos):
        # Checks the input correctly references in the grid
        if (self.charToInteger(pos[0]) < self.__size and 
            int(pos[1:])-1 < self.__size):
          # Checks that the position is valid and if so, changes the grid
          # position to the stone of that colour.
          if self.validate((int(pos[1:])-1,
              self.charToInteger(pos[0])),1):
            valid = True
          else:
            print('Move is invalid. Make sure the space is not occupied, the'+
              ' move does not consitute suicide and does not return the game'+
              ' to a previous state')
        else:
          print('Invalid Input. The Grid Position exceeds boundaries of grid')
      else:
        print('Invalid Input, grid position is not formatted correctly. '+
        ' Please attempt correct formatting [letter][number]')
  
  # Purpose: Allows the opponent to enter a stone
  def opponent(self, goAI=None):
    # If there is no goAI passed into the method
    if goAI == None:
      # Prints the current state of the grid
      self.printGrid()
      # Prints the name of the opponent
      print('It is '+self.__opponentName + '\'s turn')
      # Prints the current score
      self.printScore()
      # Instructs the user how to place a stone
      print('Place a stone in the format [letter][number]')
      # Provides two examples
      print('For Example: E3 or A11')
      # Sets valid flag to false
      valid = False
      # Continues to execute until users input is valid
      while valid != True:
        # Prompts the user to enter a stone position
        pos = input('Stone Position (or resign or pass): ')
        # If/Else executes depending on whether opponent chooses to pass, 
        # resign or attempt to play a valid move
        if pos == 'pass' or pos == 'resign':
          # Sets valid flag to True
          valid = True
          # Executes if the opponent wises to resign
          if pos == 'resign':
            # Sets finish to true and winner to the player
            self.__finish = True
            self.__winner = 1
          else:
            # Counts consecutive passes, will end game after 3 consecutive 
            # passes.
            self.__consecutivePasses += 1
        # Checks the input matches the regex pattern in the acceptableInput 
        # attribute
        elif self.__acceptableInput.match(pos):
          # Checks that the input correctly references the grid.
          if (self.charToInteger(pos[0]) < self.__size and 
              int(pos[1:])-1 < self.__size):
            # Checks that the position is valid and if so, changes the grid 
            # position to the stone of that colour
            if self.validate((int(pos[1:])-1,
                self.charToInteger(pos[0])),2):
              valid = True
            else:
              print('Move is invalid. Make sure the space is not occupied,'+
                ' the move does not consitute suicide and does not '
                +'return the game to a previous state')
          else:
            print('Invalid Input. The Grid Position exceeds boundaries' +
            ' of grid')
        else:
          print('Invalid Input, grid position is not formatted correctly. '+
          ' Please attempt correct formatting [letter][number]')
    # Executes if the goAI has been passed as a parameter
    else:
      # Allows the goAI to generate a position
      turn = goAI.play(self.__grid)
      # Continues to generate positions if they are invalid
      while self.validate(turn, 2) != True:
        turn = goAI.play(self.__grid)
  
  # Purpose: To print the current state of the board
  def printGrid(self):
    # Very complex print statement
    # All it does is print the letters A to whatever the board size is 
    # equivalent letter.
    # I can't entirely remember why I made it like this
    # Creates 'size' amount of formatted string elements
    # Then it formats them using a tuple.
    print(('   '+('%s ')*(self.__size))%
      tuple(
        # This tuple operation is performed on the result of a map function.
        # The map function takes a function as its 1st parameter and an array
        # as its second. It then applies the function passed in the 1st 
        # parameter to every element of the array in the 2nd parameter,
        # and returns a new array of these new elements.
        map(
          # This lambda statement defines a function which will take a number
          # and return a character using the ASCII value from the number plus 
          # 65
          (lambda x : chr(65+x)), 
          # This range statement returns an array of every number from 0 to 
          # self.__size - 1
          range(self.__size)
          )
        )
      )
    # Another overly complex print statement
    # Iterates through each row in the 2D array
    for row in range(len(self.__grid)):
      # Uses two format strings
      # The first is an integer which is populated by the current index of the
      # row plus 1.
      # The second is a series of format strings of length self.__size,
      # populated by a tuple
      print(('%2d '%(row+1) + ('%s '*self.__size))%
        tuple(
          # The map accepts a function and array, and returns a new array with
          # the result of each element of the previous array parsed into the
          # function.
          map(
            # Lambda function accepts a string and returns self.__print(entity)
            lambda x : self.printEntity(x),
            # The current row of the grid
            self.__grid[row])
          )
        )
      # It works okay
      
  # Purpose: To validate the player's/opponent's next move. Parameter pos
  # stores the users next stone position, and parameter target defines
  # the identity of the user.
  def validate(self, pos, target):

    # Sets the identity of the opponent
    if target == 1:
      opponent = 2
    else:
      opponent = 1
    
    # Sets GameEnd to False
    gameEnd = False

    # The following code blocks allow goAI to pass and retire
    # Executes if goAI retires
    if pos == (-1,-1):
      gameEnd = True
      self.__winner = 1
    # Executes if goAI passes
    elif pos == (-1,0):
      valid = True
    # Executes if either goAI or the player/opponent places a stone
    elif self.__grid[pos[0]][pos[1]] == 0:
      # Sets valid flag to True
      valid = True
      # Copies the current board to replacement
      replacement = copy.deepcopy(self.__grid)
      # Changes the stone position of replacement to that which the user 
      # entered
      replacement[pos[0]][pos[1]] = target
      
      # Iterates through opponents stone groups
      for group in self.forestFire(opponent, replacement):
        # If a group has no liberties
        if (0 not in self.getVals(group[1], replacement)):
          # Iterates through each stone in group
          for node in group[0]:
            # Removes stone from board
            replacement[node[0]][node[1]] = 0
            # Adds stone to taken list
            self.__taken[target].append(node)
      
      # Iterates through players stone groups
      for group in self.forestFire(target, replacement):
        # If, as a result of the players moves, one of their groups has no
        # more liberties, the move is marked invalid as it is suicide
        if 0 not in self.getVals(group[1], replacement):
          valid = False
      
      # If the move returns the board to a state that it has been in before, 
      # the move is invalid.
      for state in self.__history:
        if replacement == state:
          valid = False
      
      # Finds groups of empty intersections
      frees = self.forestFire(0, replacement)
      # Sets gameEnd flag to True
      gameEnd = True
      # For every group of blanks 
      for group in frees:
        # If the group is not larger than one stone
        if len(group[0]) > 1:
          # The game is not over
          gameEnd = False
      
      # If the move is valid
      if valid == True:
        # Append the current board state to history
        self.__history.append(self.__grid)
        # Set the current board state to the replacement state
        self.__grid = replacement
        # Count and update score
        self.updateScore()

    else:
      valid = False
    
    # If the game has ended and the move that ended it is valid
    if gameEnd == True and valid == True: 
      # set finish to true
      self.__finish = True
      # Set the winner to the current winner
      if self.__score > 0 and self.__winner != 2:
        self.__winner = 1
      elif self.__score < 0 and self.__winner != 1:
        self.__winner = 2
      else:
        self.__score = 0

    return valid
  
  # Purpose: Given a board entity (a number either 0, 1 or 2), return
  # the correct string representation
  def printEntity(self, ent):
    formatted = ''
    # Casewhere statement setting the formatted string to the correct
    # representation
    if ent == 0:
      formatted = '✛'
    elif ent == 1:
      formatted = '⚪'
    else:
      formatted = '⚫'
    return formatted
  
  # Purpose: Given a character or sequence of characters symbolic of an
  # integer expressed in base 26, return an equivalent base 10 integer
  def charToInteger(self, char):
    total = 0
    power = 0
    for i in range(len(char)-1, -1, -1):
      total += (ord(char[i])-65)*(10**power)
      power +=1
    return total

  # Purpose: Using the target stone colour, create a 2D array of groups and 
  # their perimeters.
  def forestFire(self, target, board):
    # nodes are evaluated positions on boards, actual stones or missing spots
    # bounds are the perimeters of nodes or groups of nodes
    # The queue algorithm should check nodes, before marking them as checked.
    
    # Creates a list of orthoganal neighbours
    neighbours = [(-1,0),
              (0,-1), (0,1),
                  (1,0)]

    # Creates an array to store orthogonic groups of target.
    groups = []
    # debugging flag used for performance, tracks how many times the "fire" 
    # propogates
    comparisons = 0
    # Creates an empty 2D array of nodes which have been previously traversed
    # by the queue.
    nodesChecked = [[0 for col in range(self.__size)] for 
      row in range(self.__size)]
    # The next two lines traverse the 2D array.
    for row in range(self.__size):
      for col in range(len(board[row])):
        # Determines whether a node has already been traversed by the queue.
        if nodesChecked[row][col] == 0:
          # Creates an empty array for bound (perimeters of node-groups)
          boundsChecked = [[0 for col in range(self.__size)] for 
            row in range(self.__size)]
          # Checks whether the node is of target value
          if board[row][col] == target:
            # Adds the first node to the queue
            queue = [(row,col)]
            # Appends a new group to the group array
            groups.append([[(row,col)],[]])
            # Consumption Queue for Nodes
            for i in queue:
              # Marks the node as checked by the queue
              nodesChecked[i[0]][i[1]] = 1

              # Checks Orthognoic Neighbours for Target Nodes
              for n in neighbours:
                # Checks whether neighbour nodes are in bounds of board
                if ((i[0]+n[0] > -1 and i[1]+n[1] > -1) and
                  (i[0]+n[0] < self.__size and i[1]+n[1] < self.__size)):
                  # Determines whether it has previously been checked by the 
                  # queue as it could be the neighbour of another node.
                  if boundsChecked[i[0]+n[0]][i[1]+n[1]] == 0:
                    # Determines whether neighbour is of target type.
                    if board[i[0]+n[0]][i[1]+n[1]] == target:
                      # Marks non-bound as Checked.
                      boundsChecked[i[0]+n[0]][i[1]+n[1]] = 1
                      # Adds neighbour to queue
                      queue.append((i[0]+n[0],i[1]+n[1]))
                      # Appends neighbour coordinates to group's nodes
                      groups[-1][0].append((i[0]+n[0],i[1]+n[1]))
                    else:
                      # Marks bound as Checked
                      boundsChecked[i[0]+n[0]][i[1]+n[1]] = 1
                      # Appends neighbour coordinates to group's perimeter.
                      groups[-1][1].append((i[0]+n[0],i[1]+n[1]))

              comparisons += 4
          else:
            nodesChecked[row][col] = 1
    return groups
  
  # Purpose: Given an array of tuples with two integers, return elements
  # from a 2D array indexed by the two integers
  def getVals(self, nodes, grid):
    vals = []
    for node in nodes:
      vals.append(grid[node[0]][node[1]])
    return vals

  # Purpose: By counting the stones of either player in self.__grid, update
  # self.__score to indicate who has more stones and hence a higher score on
  # the board.
  def updateScore(self):
    self.__score = 0
    for row in range(len(self.__grid)):
      for col in self.__grid[row]:
        if col == 1:
          self.__score = self.__score + .25
        if col == 2:
          self.__score = self.__score - .25

  # Purpose: Prints whoever has the advantage   
  def printScore(self):
    if self.__score > 0:
      print(self.__playerName+" has the advantage by "+
        str(self.__score)+" points.")
    elif self.__score < 0:
      print(self.__opponentName+" has the advantage by "+
        str(self.__score*-1)+" points.")
    else:
      print("Neither player has the advantage.")
  
  # Purpose: Determines whether game has finished, and prints winner
  def win(self):
    if self.__finish:
      print('The game has ended!')
      if self.__winner == 1:
        print("Congratulations to "+self.__playerName)
        print('They have won by a margin of '+str(self.__score)+' points.')
        self.saveToLeaderboard(1)
      elif self.__winner == 2:
        print("Congratulations to "+self.__opponentName)
        print('They have won by a margin of '+str(self.__score*-1)+' points.')
        self.saveToLeaderboard(2)
      else:
        print("Both players have played well, and a draw has occurred.")
      print('-'*80)
    return self.__finish

  def saveToLeaderboard(self, player):
    # Defines the salt for the hash
    # A salt is a small secret code which is appended to an item which is to 
    # be hashed. This makes the hash harder to reproduce.
    salt = 'the quick brown fox jumps over the cool dog, bro'
    # If/Else statement executes depending on whether a leaderboards.txt file
    # exists.
    if os.path.isfile('leaderboards.txt'):
      # Opens the leaderboard file in read mode
      leaderboardFile = open('leaderboards.txt', 'r')
      # Creates an empty leaders array
      leaders = []
      # Reads the first line in a priming read
      current = leaderboardFile.readline().strip()
      # Continues to read the file while the current line is not the sentinel
      # value.
      while current != 'ZZZ' and current != '':
        # Splits the record into four components
        name, opponent, score, hash = current.split(',')
        # Creates a new leader record using the name, opponent, score and hash
        # defined on the previous line
        leader = leaderboardRecord(name, opponent, score, hash)
        # Creates the verification token by concatenating the username and
        # the salt, before encoding it into a utf-8 byte array
        verificationToken = (leader.name+salt).encode('utf-8')
        # Hashes the verification token
        correctHash = str(hashlib.sha256(verificationToken).hexdigest())
        # Only if the hash stored in the file matches the hash generated in
        # python will the leader be added to the leaderboard
        if leader.hash == correctHash:
          leaders.append(leader)
        # Reads the next line of the leaderboard file
        current = leaderboardFile.readline().strip()
      leaderboardFile.close()
    else:
      leaders = []
    if player == 1:
      name = self.__playerName
      opponent = self.__opponentName
      score = self.__score
    else:
      name = self.__opponentName
      opponent = self.__playerName
      score = self.__score * -1
    verificationToken = (name+salt).encode('utf-8')
    hash = str(hashlib.sha256(verificationToken).hexdigest())
    leader = leaderboardRecord(name,opponent,score,hash)
    leaders.append(leader)
    leaderboardFile = open('leaderboards.txt','w')
    for i in range(len(leaders)):
      leaderboardFile.write(
        (leaders[i].name)+','+(leaders[i].opponent)+','+
        (str(leaders[i].score))+','+(leaders[i].hash)+"\n"
      )
    leaderboardFile.write('ZZZ')
    leaderboardFile.close()