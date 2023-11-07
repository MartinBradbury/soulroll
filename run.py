# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

#google gsperad pip3 install gspread google-auth

import gspread
from google.oauth2.service_account import Credentials
import random
import hashlib
import maskpass
#pip install maskpass
from os import system
#to clear screen
from pyfiglet import Figlet
#pip3 install pyfiglet
from time import sleep
#time sleep
#from words import word_list
f = Figlet(font='slant')

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('userdata')



def welcome():
    clear()
    print(f.renderText('  Welcome'))
    print(f.renderText('         To'))
    print(f.renderText('  Warcraft'))
    print(f.renderText('mini-games'))
    print("Welcome")
    print("[1] Login")
    print("[2] create account")
    print("[3] exit")
    selection = input("What would you like to do?: ")
    if selection in welcome_select.keys():
        return welcome_select[selection]()
    else:
        print("\nIncorrect selection, please try again")
        sleep(3)
        welcome_()



    if selection == '1':
        print("Lets log you in")
        sleep(3)
        main()
    elif selection == '2':
        print("lets create an account")
        sleep(3)
        create_account()
    elif selection == '3':
        print("Goodbye")
        exit()
    else:
        print("please select an option")
        welcome()

def create_account():
    system('clear')
    print(f.renderText('Create Account'))
    SHEET = GSPREAD_CLIENT.open('userdata')
    print("\nWelcome to account creation.\n")
    print("Please create a username between 3-10 characters and starts with any letter\n")
    username = input("Create a username: ").lower()
    if len(username) < 3:
        print("Username should be between 3 and 10 characters")
        sleep(3)
        create_account()
    elif len(username) > 10:
        print("Username should be between 3 and 10 characters")
        sleep(3)
        create_account()
    else:   
        print("Username accepted")

    print("Please create a password starting with any letter")
    password = maskpass.askpass("\nCreate a password: ")
    password_check = maskpass.askpass("\nRe-enter password ")
    if password == password_check:
        print("\nAccount created successfully")
        enc = password_check.encode()
        hash1 = hashlib.md5(enc).hexdigest()
    else:
        print("Passwords do not match")
        sleep(3)
        create_account()

    score = 0
    upload = SHEET.worksheet('username')
    upload.append_row([username, hash1, score])
    game_select()


def login(input_username, auth_hash):
    data = SHEET.worksheet('username')
    usr = data.get_all_records()
    match = False
    for record in usr:
        if record['username'] == input_username and record['password'] == auth_hash:
            match = True
            
    if match:
        print("You have sucessfully logged in.....")
        sleep(3)
        return True

    else:
        print("incorrect")
        sleep(3)
        login()

def game_select():
    system('clear')
    print(f.renderText('Mini-Games'))
    print("Which game would you like to play?\n")
    print("[1] DeathRoll")
    print("[2] World of Warcraft Trivia Quiz")
    print("[3] Logout")
    selection = input("What would you like to do?: ")

    if selection in game_selection.keys():
        return game_selection[selection]()
    else:
        print("\nIncorrect selection, please try again")
        sleep(3)
        game_select()

def deathroll():
    system('clear')
    print(f.renderText('Welcome to Deathroll\n'))
    print("In this game you will play against the Lich King!")
    print("\n You will take turns to roll a number between 1 - 100")
    print("your next roll will be between 1 - the number YOU rolled")
    print("You keep taking it in turns until your or the Lick King rolles a 1")
    print("This a game of chance and the object is to not roll 1\n")
    print("To start the game, please type roll\n")
    roll = input(": ")
    if roll.lower() == 'roll':
        
        random_num()
    else:
        print("please type roll to start the game")
        
        deathroll()

def random_num(score):
    system('clear')
    print("rolling.........")
    sleep(1)
    number1 = random.randint(1, 100)
    print(f"\nyou rolled: {number1}")
    number2 = random.randint(1, 100)
    input("press any key for computer roll")
    print(f"the computer rolled: {number2}\n")
    while (number1 + number2 != 1):
        input("press any key to roll again")
        number1 = random.randint(1, number1)
        print(f"\nyou rolled: {number1}")
        
        if (number1 == 1):
            print("Oh no, the Lich King defeated you!")
            print("Congratulations Lich King!")
            print(score)
            sleep(3)
            break
                  

        input("press any key for computer roll")
        number2 = random.randint(1, number2)
        print(f"the computer rolled: {number2}\n")
            
        if (number2 == 1):
            print("The Lich King lost")
            print("Congratulations YOU won!")
            score += 1
            print(score)
            sleep(3)
            break
                    
    else:
        input("error")

    random_num(score)
    game_select()  



def clear():
   # for windows
        system('cls')

   # for mac and linux

        system('clear')

def get_current_score(input_username):
    SHEET = GSPREAD_CLIENT.open('userdata').sheet1
    column_headers = SHEET.row_values(1)
    username_index = column_headers.index('username') + 1
    for i in range(1, SHEET.row_count + 1):
        username = SHEET.cell(i, username_index).value
        if username == input_username:
            score = SHEET.cell(i, column_headers.index('score') + 1).value
            print(f"well done {username} your score is {score}")
            return score


def update_score(input_username, int(score)):
    #open worksheet and sheet1
    SHEET = GSPREAD_CLIENT.open('userdata').sheet1

    #assign a variable to row
    column_headers = SHEET.row_values(1)

    #assign a variable to column headers in username +1 as index
    username_index = column_headers.index('username') + 1

    #value to update
    value_to_update = str(score)

    row_count = len(SHEET.get_all_values())

    for i in range(1, SHEET.row_count + 1):
        username = SHEET.cell(i, username_index).value
        print(username)

        if username == input_username:
            SHEET.update_cell(i, column_headers.index('score') + 1, value_to_update)
            print(f"well done {username} your score is {score}")
            return



def main():
    
    print("Initialising......")
    sleep(2)
    system('clear')
    print(f.renderText('Login'))
    print("\nWelcome Traveller,\n")
    input_username = input("Please enter your username: ")
    input_password = maskpass.askpass("\nPlease enter your password: ")
    auth = input_password.encode()
    auth_hash = hashlib.md5(auth).hexdigest()
    
    if login(input_username, auth_hash):
        True
        #  get_current_score(input_username)
    else:
        print("error")
    

    SHEET = GSPREAD_CLIENT.open('userdata').sheet1
    column_headers = SHEET.row_values(1)
    username_index = column_headers.index('username') + 1
    for i in range(1, SHEET.row_count + 1):
        username = SHEET.cell(i, username_index).value
        if username == input_username:
            score = SHEET.cell(i, column_headers.index('score') + 1).value
            print(f"well done {username} your score is {score}")
            random_num(int(score))
    
    update_score(input_username, int(score))
    
    #game_select(score)
    
    

welcome_select = dict({
    "1": main,
    "2": create_account,
    "3": exit
    })


game_selection = dict({
    "1": deathroll,
    "2": quit,
    "3": welcome
    }) 

welcome()
main()


