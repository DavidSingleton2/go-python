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
  while verify != True and guesses <= 3:
    print("Please enter a licence key")
    attempt = input("Enter key: ")
    if attempt == password:
      verify = True
    else:
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

def menu():
  return "hi"

def gameplay():
  game = Board(11)
  opponent = goAI(1, 11)
  while True:
    game.player()
    game.opponent(opponent)

gameplay()