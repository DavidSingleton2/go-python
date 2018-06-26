# Imports externally defined board class
from board import Board
# Imports path for checking whether files exist
import os.path
# Imports externally defined goAI class
from goAI import goAI
# Imports regex functionality
import re
# Imports record functionality
from collections import namedtuple
# Imports Hashing functionality for leaderboard
import hashlib

leaderboardRecord = namedtuple('leaderboardRecord',
  ['name','opponent','score','hash'])

# Purpose: To Define the main thread and call other subroutines.
def main():
  # Authenticates user with password / licence key
  if password():
    # Runs menu
    menu()

# Purpose: To Verify the user has obtained a valid licence key and refuse 
# them access to the program should they not have it.
def password():
  # Opens password.txt file as an object and assigns it to passwordFile
  passwordFile = open("password.txt", 'r')
  # Reads the first line of the file
  password = passwordFile.readline().strip()
  # Sets the authentication variable to false
  verify = False
  # Defines integer which stores how many entry attempts the user has made
  guesses = 0
  # Closes the file as to reduce memory overhead
  passwordFile.close()
  # Loop which controls password attempt input
  # Condition specifies that the correct input has not been provided and that
  # the attempts made b the user has not exceeded 3
  while verify != True and guesses < 3:
    # Prints a prompt for the user
    print("Please enter a licence key")
    # Sets variable attempt to user input of attempt
    attempt = input("Enter key: ")
    # Sets verify to true should the attempt be equal to the stored password
    if attempt == password:
      verify = True
    # Executes should the attempt be not equal to the password stored
    else:
      # Increments guess counter
      guesses = guesses + 1
      # Notifies user of incorrect guess and guesses remaining
      print("Incorrect Licence Key.")
      print("You have "+str(3-guesses)+" licence key entry attempts remaining")
  # Prints out error if user has failed to authenticate
  if verify != True:
    print('You have exhausted your licence key entry attempts.')
  else:
    # Prints success message
    print("You have successfully entered your licence key.")
    # Asks user whether they wish to change their licence key
    selection = input("Would you like to change your licence key? (Y/N): ")
    # Reprompts user for selection while their input doesn't match Y or N 
    while selection != 'Y' and selection != 'N':
      print("The input provided was not valid. Please enter a valid response "
        +"(Y/N)")
      selection = input("Would you like to change your licence key? (Y/N): ")
    # If the user is selects that they wish to change their password
    if selection == 'Y':
      # Opens the password file as passwordFile object in write mode
      passwordFile = open('password.txt', 'w')
      # Prompts the user for a new licence key
      newKey = input("Please enter your desired licence key: ")
      # Writes the new licence key to the password file
      passwordFile.write(newKey)
      # Closes the output file
      passwordFile.close()
      # Notifies user of successful password change
      print('The licence key has been successfully entered.')
  return verify

# Purpose: Displays a menu of items from which the user may make a selection,
# after which other subroutines are called.
def menu():
  # The next 3 lines open, read and close a file containing the ASCII logo
  logoFile = open('logo.txt','r')
  logo = logoFile.read()
  logoFile.close()
  # The next 4 lines print the menu
  print('-'*80)
  print('\t'*2 + 'The Go Guru presents')
  print(logo)
  print('-'*80)
  # Creates a regex pattern object only accepting numbers from 1-4
  menuInputPattern = re.compile('(^[1-5]$)')
  # Creates a flag which defines whether the user has opted to exit the 
  # program
  quit =  False
  # While Loop continues to execute while quit does not equal false
  while quit != True:
    # the next 6 lines print out menu selections
    print("Please make a menu selection: ")
    print("1. Play Now!")
    print("2. Learn to Play!")
    print("3. Rule Set")
    print("4. Leaderboards")
    print("5. Exit the gane :(")
    # Prompts the user for a menu selection and stores it in selection var
    selection =  input("Please make a menu selection from 1-5: ")
    # If statement executes only when user input matches regex pattern
    if menuInputPattern.match(selection):
      # Converts the user input from a string into an integer
      selection = int(selection)
      # Pythonic implementation of casewhere statement, uses user input of
      # selection and matches it to an option. Either executes a subprogram
      # or exits the program when matched.
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
    # Informs the user their user input was incorrect
    else:
      print("Invalid menu selection. Please try again")

# Purpose: Creates a new game by asking the user what size board they would
# like to play on, as well as their opponent and opponent's difficulty
def gameplay():
  # Prints a menu asking whether the player wants to compete against a human
  # or machine.
  print('-'*80)
  print("Who do you want to play against?")
  print("1. A friend!")
  print("2. A machine!")
  # Stores users input as opponentSelect variable
  opponentSelect = input("Please enter a choice either 1 or 2: ")
  # Runs a while loop to reprompt the user for input should they enter 
  # incorrect input.
  while opponentSelect != '1' and opponentSelect != '2':
    print("Invalid input. Please select either 1 or 2")
    print('1. A friend!')
    print("2. A machine!")
  # Prints a menu asking what size board the player would like to play on
  print('-'*80)
  print('What board size would you like to play on?')
  print('1. 9x9')
  print('2. 13x13')
  print('3. 19x19')
  print('Please choose your desired board size by entering')
  # Prompts user for which size board they would like
  sizeSelect = input('a number between 1-3: ')
  # Continually prompts user for board size while they have not entered valid
  # input
  while (sizeSelect != '1' and sizeSelect != '2' 
      and sizeSelect != '3'):
    print('Invalid input. Please select either 1, 2 or 3.')
    print('1. 9x9')
    print('2. 13x13')
    print('3. 19x19')
    sizeSelect = input(sizeSelect)
  # Converts the users input into an integer
  sizeSelect = int(sizeSelect)
  # Pythonic Casewhere statement, sets the size of the board based on the
  # users previous selection.
  if sizeSelect == 1:
    size = 9
  elif sizeSelect == 2:
    size = 13
  else:
    size = 19
  # If/Else statement determines whether the player has chosen to play against
  # a human opponent or machine.
  if opponentSelect == '1':
    # Calls Player Subroutine with the selected board size
    player(size)
  else:
    # Calls selectDifficulty subroutine to determine what type of difficulty
    # the player would like to compete against
    difficulty = selectDifficulty()
    # Calls the Computer subroutine with the selected board size and 
    # difficulty
    computer(size, difficulty)

# Purpose: To allow the user to select a difficulty for the GO AI program
def selectDifficulty():
  # Prints a menu displaying possible difficulty options
  print('-'*80)
  print('Please select a difficulty')
  print('1. Easy')
  print('2. Medium')
  print('3. Hard')
  # Prompts user for difficulty selection
  selection = input('Please enter your desired difficulty from 1-3: ')
  # Continues to reprompt user for difficulty while their selection is not 
  # valid
  while selection != '1' and selection != '2' and selection != '3':
    print('Invalid input. Please enter either 1, 2 or 3.')
    print('1. Easy')
    print('2. Medium')
    print('3. Hard')
    selection = input('Please enter your desired difficulty from 1-3: ')
  # Converts selection into an integer
  selection = int(selection)
  # Returns the users selection for computer difficulty
  return selection

# Purpose: To define the main gameplay loop for Player vs Player Gameplay
def player(size):
  # Creates a new board with an opponent
  game = Board(size, True)
  # Continues to execute while the game has not finished
  while game.win() != True:
    # Calls player method which allows user to input a stone
    game.player()
    # Calls opponent method which allows opponent to input a stone
    game.opponent()
  
# Purpose: To define the main gameplay loop for Player vs Computer Gameplay
def computer(size, difficulty):
  # Creates a new board of size with no opponent
  game = Board(size)
  # Defines a new goAI opponent using the size and difficulty
  opponent = goAI(1, size)
  # Continues to execute while the game has not finished
  while game.win() != True:
    # Calls player method which allows user to input a stone
    game.player()
    # Calls opponent method with goAI parameter to generate a new stone 
    # position
    game.opponent(opponent)

# Purpose: To display the rules of the game and allow the user to interact
# with them.
def rulebook():
  # Opens the rule file in read mode
  ruleFile = open('rules.txt','r')
  # Creates an array with one empty string
  ruleArray = ['']
  # Creates an integer for array indexing at 0
  index = 0
  # Reads the first line of the file, a primer read
  line = ruleFile.readline()
  # Continually executes loop while the current line is not the sentinel value
  # or empty
  while line.strip() != '999' and line.strip() != '':
    # Sentinel Value ZZZ denotes the start of a new page. If the sentinel 
    # value is found, the index is iterated and a new line is read
    if line.strip() == 'ZZZ':
      # Iterates index
      index += 1 
      # Appends empty string onto array
      ruleArray.append('')
      # Reads the next file
      line = ruleFile.readline()
    else:
      # Concatenates current line onto the string indexed at index
      ruleArray[index] += line
      # Reads the next line
      line = ruleFile.readline()
  # Sets exit flag to 0
  exit = False
  # Starts the user at page 0
  page = 0
  while exit != True:
    # Prints a border and menu telling the user what page they are on
    print('-'*80)
    print(ruleArray[page])
    print('-'*80)
    print('You are currently on page '+str(page+1)+ ' of '+str(len(ruleArray))
      + ' pages in the rule book.')
    print('Please select an option:')
    # Sets the amount of options to 1, initially
    options = 1
    # Defaults next and previous values to -1, as there is no guarantee that
    # there will be a next/previous page
    next = -1
    previous = -1
    # If the page is greater than 0, meaning that the there is a page before
    # it
    if page > 0:
      # Previous now equals the current value of options
      previous = options
      # Previous is printed out as a menu option
      print(str(options)+'. Navigate to the previous page')
      # The total amount of options is iterated
      options += 1
    # If the page is less than the last page in the array
    if page < len(ruleArray)-1:
      # Next now equals the current value of options
      next = options
      # Next is printed out as a menu option
      print(str(options) +'. Navigate to the next page')
      # Options is iterated
      options += 1
    # A final exit option is printed, denoted by the current value of options
    print(str(options)+'. Exit')
    # The user is prompted to select from one of the available options
    selection = input("Please select a number from 1-"+str(options)+': ')
    # The valid flag is set to false
    valid = False
    # Continues to execute while valid is false. It first checks whether input 
    # is valid, and if not, prompts the user to re enter their option.
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
    # Converts the users selection into an integer
    selection = int(selection)
    # Pythonic Casewhere statement determining whether the users selection is
    # equal to any of the provided options
    if selection == next:
      # Iterates page is user's selection is equal to next
      page += 1
    elif selection == previous:
      # Decrements page if user's selection is equal to previous
      page -= 1
    elif selection == options:
      # Sets exit flag to true if user's selection is equal to the last option
      exit = True

# Purpose: To print, sort and verify leaderboards
def leaderboards():
  # Defines the salt for the hash
  # A salt is a small secret code which is appended to an item which is to be
  # hashed. This makes the hash harder to reproduce.
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
    while current != 'ZZZ':
      # Splits the record into four components
      print(current.split())
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
    # If the leader file does not exist, create an empty array
    leaders = []
  # Set exit flag to False
  exit = False
  # Continues to run while loop while exit flag is equal to false
  while exit == False:
    # Prints a header
    print('-'*80)
    print('\t\t Leaderboards')
    print('-'*80)
    # If/Else statement determines whether the leaders array is empty
    if len(leaders) == 0:
      # Prints that there are no leaders to display
      print("\t\t There are no leaders to display")
      # Prompts the user to return to the menu
      input("Press enter to return to the menu")
      # Sets exit flag to True
      exit = True
    else:
      # Prints a formatted string as a header of leaderboard table
      print('%7s%15s%30s'%('Username','Opponent','Winning Margin'))
      # Iterates index and prints a leader's name, opponent and score
      for index in range(len(leaders)):
        print('%7s%15s%30s'%leaders[index][:-1])
      # Prints a border and menu options
      print('-'*80)
      print('Please select a menu option')
      print('1. Sort Alphabetically')
      print('2. Sort by victory margin')
      print('3. Exit')
      # Prompts user for input stored as selections
      selection = input('Please select an option by entering a ' + 
        ' number from 1-3: ')
      # Continues to reprompt user while selection is not valid
      while selection != '1' and selection != '2' and selection != '3':
        print('Incorrect input, please try again.')
        # Prompts user for input stored as selections
        selection = input('Please select an option by entering a ' + 
          ' number from 1-3: ')
      # Pythonic Casewhere which will either sort the leaderboards or exit
      if selection == '1':
        leaderboardSortAlphabetically(leaders)
      elif selection == '2':
        leaderboardSortMargin(leaders)
      else:
        exit = True
        
# Purpose: Sorts the leaderboard array alphabetically using the leaders' 
# usernames and bubble sort
def leaderboardSortAlphabetically(array):
  # Creates an empty temp variable for swapping
  temp = ''
  # Sets the sorted integer to one. Indicates the progress of the sort when 
  # subtracted from the length of the array.
  sorted = 1
  # Continues to execute until sorted reaches length of the array
  while sorted != len(array):
    # Sets the index to 0
    index = 0
    # Iterates the index until the upperbound of the array is reach
    while index != len(array)-sorted:
      # Swaps the values if the first value is greater than the second
      if array[index][0] > array[index+1][0]:
        temp = array[index+1]
        array[index+1] = array[index]
        array[index] = temp
      # Iterates the index
      index += 1
    # Iterates sorted, in effect decrementing the upper bound.
    sorted +=1

def leaderboardSortMargin(array):
  # Creates an empty temp variable for swapping
  temp = ''
  # Sets the sorted integer to one. Indicates the progress of the sort when 
  # subtracted from the length of the array.
  sorted = 1
  # Continues to execute until sorted reaches length of the array
  while sorted != len(array):
    # Sets the index to 0
    index = 0
    # Iterates the index until the upperbound of the array is reach
    while index != len(array)-sorted:
      # Swaps the values if the first value is greater than the second
      if float(array[index][2]) < float(array[index+1][2]):
        temp = array[index+1]
        array[index+1] = array[index]
        array[index] = temp
      # Iterates the index
      index += 1
    # Iterates sorted, in effect decrementing the upper bound.
    sorted +=1

def tutorial():
  return 'stub'

main()