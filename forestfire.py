example1 = [[0,0,0],[0,1,0],[0,0,0]]
solved1 = [[0,1,0],[1,0,1],[0,1,0]]
dimensions = 3

# Purpose: Using the target stone colour, create a 2D array of groups and 
# their perimeters.
def forestFire(target, board):
  # nodes are evaluated positions on boards, actual stones or missing spots
  # bounds are the perimeters of nodes or groups of nodes
  # The queue algorithm should check nodes, before marking them as checked.

  groups = []
  comparisons = 0
  nodesChecked = [[0 for col in range(len(board))] for 
    row in range(len(board))]
  for row in range(len(board)):
    for col in range(len(board[row])):
      if nodesChecked[row][col] == 0:
        boundsChecked = [[0 for col in range(len(board))] for 
          row in range(len(board))]
        if board[row][col] == target:
          queue = [(row,col)]
          groups.append([[],[]])
          for i in queue:
            nodesChecked[i[0]][i[1]] = 1

            # Check North
            if ((i[0]-1 > -1 and i[1] > -1) and 
              (i[0]-1 < len(board) and i[1] < len(board))):
              if boundsChecked[i[0]-1][i[1]] == 0:
                if board[i[0]-1][i[1]] == target:
                  boundsChecked[i[0]-1][i[1]] = 1
                  queue.append((i[0]-1,i[1]))
                  groups[-1][0].append((i[0]-1,i[1]))
                else:
                  boundsChecked[i[0]-1][i[1]] = 1
                  groups[-1][1].append((i[0]-1,i[1]))
            
            # Check East
            if ((i[0] > -1 and i[1]+1 > -1) and
                (i[0] < len(board) and i[1]+1 < len(board))):
              if boundsChecked[i[0]][i[1]+1] == 0:
                if board[i[0]][i[1]+1] == target:
                  boundsChecked[i[0]][i[1]+1] = 1
                  groups[-1][0].append((i[0],i[1]+1))
                  queue.append((i[0],i[1]+1))
                else:
                  boundsChecked[i[0]][i[1]+1] = 1
                  groups[-1][1].append((i[0],i[1]+1))
              
            # Check South
            if ((i[0]+1 > -1 and i[1] > -1) and 
              (i[0]+1 < len(board) and i[1] < len(board))):
              if boundsChecked[i[0]+1][i[1]] == 0:
                if board[i[0]+1][i[1]] == target:
                  boundsChecked[i[0]+1][i[1]] = 1
                  groups[-1][0].append((i[0]+1,i[1]))
                  queue.append((i[0]+1,i[1]))
                else:
                  boundsChecked[i[0]+1][i[1]] = 1
                  groups[-1][1].append((i[0]+1,i[1]))

            # Check West
            if ((i[0] > -1 and i[1]-1 > -1) and
                (i[0] < len(board) and i[1]-1 < len(board))):
              if boundsChecked[i[0]][i[1]-1] == 0:
                if board[i[0]][i[1]-1] == target:
                  boundsChecked[i[0]][i[1]-1] = 1
                  groups[-1][0].append((i[0],i[1]-1))
                  queue.append((i[0],i[1]-1))
                else:
                  boundsChecked[i[0]][i[1]-1] = 1
                  groups[-1][1].append((i[0],i[1]-1))
            comparisons += 4
        else:
          nodesChecked[row][col] = 1
  print("Comparisons: "+str(comparisons))
  print("Groups: "+str(len(groups)))
  return groups


def flatten(solved):
  target = [[0 for i in range(dimensions)] for i in range(dimensions)]
  for groups in solved:
    for i in groups[1]:
      target[i[0]][i[1]] = 1
  string = prettyBound(target)
  return string

def pretty(target):
  string = ""
  for i in target:
    for c in i:
      string += printEnt(c) + " "
    string += "\n"
  return string

def prettyBound(target):
  string = ""
  for i in target:
    for c in i:
      string += printBound(c) + " "
    string += "\n"
  return string

def printBound(string):
  if string == 1:
    bound = '😎'
  else:
    bound = '-'
  return bound

def printEnt(string):
  if string == 1:
    ent = '⚫'
  elif string == 2:
    ent = '⚪'
  else:
    ent = '✛'
  return ent

print(flatten(forestFire(1, example1)))

dimensions = 4
example2 = [[0,0,0,0],[0,1,1,0],[0,0,1,0],[0,0,0,0]]

print(flatten(forestFire(1, example2)))

dimensions = 6
example3 = [[0 for col in range(6)] for row in range(6)]
example3[1][1] = 1
example3[4][4] = 1

print(flatten(forestFire(1, example3)))

dimensions = 9
example4 = [[0 for col in range(9)] for row in range(9)]
example4[1][1] = 1
example4[0][1] = 1
example4[0][0] = 1
example4[1][2] = 1
example4[6][5] = 1
example4[6][6] = 1
example4[6][7] = 1
example4[6][8] = 2
example4[4][4] = 2
example4[4][5] = 2
example4[4][6] = 2
print(pretty(example4))
print(flatten(forestFire(1, example4)))
print(flatten(forestFire(2, example4)))
