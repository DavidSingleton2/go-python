import random as r
import math as m
class goAI():
  def __init__(self, difficulty=0, size=19):
    self.__difficulty = difficulty
  
  def play(self, board):
    if self.__difficulty == 0:
      x = r.randint(0, len(board)-1)
      y = r.randint(0, len(board)-1)
    else:
      x, y = self.pursue(board)
    return (x,y)
  
  def pursue(self, board):
    targets = self.forestFire(1, board)
    x = r.randint(0,len(board)-1)
    y = r.randint(0,len(board)-1)
    candidates = None
    potential = 0
    for target in targets:
      targetBounds = []
      for coords in target[1]:
        if board[coords[0]][coords[1]] == 0:
          targetBounds.append(coords)
      if potential < self.invSigmoid(len(targetBounds)):
        candidates = targetBounds
    
    print(candidates, self.invSigmoid(len(candidates)))
    if candidates and (r.randint(0,10)) > 1:
      x = candidates[0][0]
      y = candidates[0][1]
    return (x,y)


      
  @staticmethod
  def invSigmoid(x):
    return (1/m.exp(x))


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
    nodesChecked = [[0 for col in range(len(board))] for 
      row in range(len(board))]
    # The next two lines traverse the 2D array.
    for row in range(len(board)):
      for col in range(len(board[row])):
        # Determines whether a node has already been traversed by the queue.
        if nodesChecked[row][col] == 0:
          # Creates an empty array for bound (perimeters of node-groups)
          boundsChecked = [[0 for col in range(len(board))] for 
            row in range(len(board))]
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
                  (i[0]+n[0] < len(board) and i[1]+n[1] < len(board))):
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