import re
import copy
import goAI
class Board:
  def __init__(self, size, opponent=False, board=None):
      self.__finish = False
      self.__size = size
      if size < 10:
        self.__acceptableInput = re.compile(r'^([A-Z][0-9])$')
      else:
        self.__acceptableInput = re.compile(r'^([A-Z][0-9]{1,2})$')
      name = ''
      self.__opponentIsComputer = opponent
      while name == '':
        name = input("Please enter your name: ")
      self.__playerName = name
      name = ''
      if opponent == True:
        while name == '':
          name = input("Please enter your opponent's name: ")
        self.__opponentName = name
      else:
        self.__opponentName = "Computer"

      if board:
        self.__grid = board
      else:
        self.__grid = [[0 for x in range(self.__size)] 
                        for col in range(self.__size)]
      self.__history = []
      self.__taken = [[] for x in range(3)]
      self.__score = 0

  def player(self):
    self.printGrid()
    print('It is '+self.__playerName + '\'s turn')
    self.printScore()
    print('Place a stone in the format [letter][number]')
    print('For Example: E3 or A11')
    valid = False
    while valid != True:
      pos = input('Stone Position: ')
      if self.__acceptableInput.match(pos):
        if (self.charToInteger(pos[0]) < self.__size and 
            int(pos[1:])-1 < self.__size):
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
  
  def opponent(self, goAI=None):
    if goAI == None:
      self.printGrid()
      print('It is '+self.__opponentName + '\'s turn')
      self.printScore()
      print('Place a stone in the format [letter][number]')
      print('For Example: E3 or A11')
      valid = False
      while valid != True:
        pos = input('Stone Position: ')
        if self.__acceptableInput.match(pos):
          if (self.charToInteger(pos[0]) < self.__size and 
              int(pos[1:])-1 < self.__size):
            if self.validate((int(pos[1:])-1,
                self.charToInteger(pos[0])),2):
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
    else:
      turn = goAI.play(self.__grid)
      while self.validate(turn, 2) != True:
        turn = goAI.play(self.__grid)
  def printGrid(self):
    print(('   '+('%s ')*(self.__size))%
      tuple(map((
        lambda x : chr(65+x)), 
      range(self.__size))))
    for col in range(len(self.__grid)):
      print(('%2d '%(col+1) + ('%s '*self.__size))%tuple(
        map(
          lambda x : self.printEntity(x),
        self.__grid[col])))
      
  def validate(self, pos, target):
    if target == 1:
      opponent = 2
    else:
      opponent = 1

    if self.__grid[pos[0]][pos[1]] == 0:
      valid = True
      replacement = copy.deepcopy(self.__grid)
      replacement[pos[0]][pos[1]] = target
      
      for group in self.forestFire(opponent, replacement):
        
        if (0 not in self.getVals(group[1], replacement)):
          for node in group[0]:
            replacement[node[0]][node[1]] = 0
            self.__taken[target].append(node)
      
      
      for group in self.forestFire(target, replacement):
        if 0 not in self.getVals(group[1], replacement):
          valid = False
      
      for state in self.__history:
        if replacement == state:
          valid = False
      
      if valid == True:
        self.__history.append(self.__grid)
        self.__grid = replacement
        self.updateScore()
    else:
      valid = False
    return valid
    
  def printEntity(self, ent):
    formatted = ''
    if ent == 0:
      formatted = '✛'
    elif ent == 1:
      formatted = '⚪'
    else:
      formatted = '⚫'
    return formatted
      
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
  
  def getVals(self, nodes, grid):
    vals = []
    for node in nodes:
      vals.append(grid[node[0]][node[1]])
    return vals

  def updateScore(self):
    self.__score = 0
    for row in range(len(self.__grid)):
      for col in self.__grid[row]:
        if col == 1:
          self.__score = self.__score + .25
        if col == 2:
          self.__score = self.__score - .25
    for taken in self.__taken[1]:
      self.__score += .25
    for taken in self.__taken[2]:
      self.__score -= .25

  def printScore(self):
    if self.__score > 0:
      print(self.__playerName+" has the advantage by "+
        str(self.__score)+" points.")
    elif self.__score < 0:
      print(self.__opponentName+" has the advantage by "+
        str(self.__score*-1)+" points.")
    else:
      print("Neither player has the advantage.")
  
  def win(self):
    return self.__finish