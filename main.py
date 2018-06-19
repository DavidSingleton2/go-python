from board import Board
from goAI import goAI
import re
def main():
  if password():
    menu()

def password():
  passwordFile = open("password.txt")
  password = passwordFile.read()
  verify = False
  guesses = 0
  passwordFile.close()
  while verify != True and guesses < 3:
    print("Please enter a licence key")
    attempt = input("Enter key: ")
    if attempt == password:
      verify = True
    else:
      guesses = guesses + 1
      print("Incorrect Licence Key.")
      print("You have "+str(3-guesses)+" licence key entry attempts remaining")
  if verify != True:
    print('You have exhausted your licence key entry attempts.')
  else:
    print("You have successfully entered your licence key.")
    selection = input("Would you like to change your licence key? (Y/N): ")
    selectionPattern = re.compile(r'(^[YN]$)')
    while selectionPattern.match(selection) == False:
      print("The input provided was not valid. Please enter a valid response "
        +"(Y/N)")
      selection = input("Would you like to change your licence key? (Y/N): ")
    if selection == 'Y':
      passwordFile = open('password.txt', 'w')
      newKey = input("Please enter your desired licence key: ")
      passwordFile.write(newKey)
      passwordFile.close()
      print('The licence key has been successfully entered.')
  return verify

def menu():
  logoFile = open('logo.txt','r')
  logo = logoFile.read()
  logoFile.close()
  print('-'*80)
  print('\t'*2 + 'The Go Guru presents')
  print(logo)
  print('-'*80)
  menuInputPattern = re.compile('(^[1-5]$)')
  quit =  False
  while quit != True:
    print("Please make a menu selection: ")
    print("1. Play Now!")
    print("2. Learn to Play!")
    print("3. Rule Set")
    print("4. Leaderboards")
    print("5. Exit the gane :(")
    selection =  input("Please make a menu selection from 1-5: ")
    if menuInputPattern.match(selection):
      selection = int(selection)
      if selection == 1:
        gameplay()
      elif selection == 2:
        tutorial()
      elif selection == 3:
        rulebook()
      elif selection == 4:
        leaderboards()
      else:
        print("Bye!")
        quit = True
    else:
      print("Invalid menu selection. Please try again")

def gameplay():
  print('-'*80)
  print("Who do you want to play against?")
  print("1. A friend!")
  print("2. A machine!")
  opponentSelect = input("Please enter a choice either 1 or 2: ")
  while opponentSelect != '1' and opponentSelect != '2':
    print("Invalid input. Please select either 1 or 2")
    print('1. A friend!')
    print("2. A machine!")
  print('-'*80)
  print('What board size would you like to play on?')
  print('1. 9x9')
  print('2. 13x13')
  print('3. 19x19')
  print('Please choose your desired board size by entering')
  sizeSelect = input('a number between 1-3: ')
  while (sizeSelect != '1' and sizeSelect != '2' 
      and sizeSelect != '3'):
    print('Invalid input. Please select either 1, 2 or 3.')
    print('1. 9x9')
    print('2. 13x13')
    print('3. 19x19')
    sizeSelect = input(sizeSelect)
  sizeSelect = int(sizeSelect)
  if sizeSelect == 1:
    size = 9
  elif sizeSelect == 2:
    size = 13
  else:
    size = 19
  if opponentSelect == 1:
    player(size)
  else:
    difficulty = selectDifficulty()
    computer(size, difficulty)

def selectDifficulty():
  print('-'*80)
  print('Please select a difficulty')
  print('1. Easy')
  print('2. Medium')
  print('3. Hard')
  selection = input('Please enter your desired difficulty from 1-3: ')
  while selection != '1' and selection != '2' and selection != '3':
    print('Invalid input. Please enter either 1, 2 or 3.')
    print('1. Easy')
    print('2. Medium')
    print('3. Hard')
    selection = input('Please enter your desired difficulty from 1-3: ')
  selection = int(selection)
  return selection

def player(size):
  game = Board(size, True)
  while game.win() != True:
    game.player()
    game.opponent()
  

def computer(size, difficulty):
  game = Board(size)
  opponent = goAI(1, size)
  while game.win() != True:
    game.player()
    game.opponent(opponent)

def rulebook():
  ruleFile = open('rules.txt','r')
  ruleArray = ['']
  index = 0
  line = ruleFile.readline()
  while line.strip() != '999':
    if line.strip() == 'ZZZ':
      index += 1 
      ruleArray.append('')
      line = ruleFile.readline()
    else:
      ruleArray[index] += line
      line = ruleFile.readline()
  exit = False
  page = 0
  while exit == False:
    print('-'*80)
    print(ruleArray[page])
    print('-'*80)
    print('You are currently on page '+str(page+1)+ ' of '+str(len(ruleArray))
      + 'pages in the rule book.')
    print('Please select an option:')
    options = 1
    next = -1
    previous = -1
    if page > 0:
      previous = options
      print(str(options)+'. Navigate to the previous page')
      options += 1
    if page < len(ruleArray)-1:
      next = options
      print(str(options) +'. Navigate to the next page')
      options += 1
    print(str(options)+'. Exit')
    exit = options
    selection = input("Please select a number from 1-"+str(options)+': ')
    valid = False
    while valid == False:
      if selection.isdigit() == True:
        if (int(selection)>0 and int(selection)<=options):
          valid = True
        else:
          selection = input("Invalid selection, please enter a digit between "
          +"1-"+ str(options)+': ')
      else:
        selection = input("Invalid selection, please enter a digit between "+
        "1-"+ str(options)+': ')
    selection = int(selection)
    print(selection, next, previous, options, sep=", ")   
    if selection == next:
      page += 1
    if selection == previous:
      page -= 1
    if selection == options:
      exit = True

def leaderboards():
  return 'stub'

def tutorial():
  return 'stub'

main()