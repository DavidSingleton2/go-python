def main():
  if password():
    menu()

def password():
  passwordFile = open("password.txt")
  password = passwordFile.read()
  verify = False
  guesses = 0
  while verify != True and guesses <= 3:
    print("Please enter a licence key")
    attempt = input("Enter key: ")
    if attempt == password:
      verify = True
    else:
      print("Incorrect Licence Key.")
      print("You have "+str(3-guesses)+" licence key entry attempts remaining")
      
def menu():
  return "hi"