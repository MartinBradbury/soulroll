import gspread
from google.oauth2.service_account import Credentials
import random
import hashlib
import maskpass
from os import system
from pyfiglet import Figlet
from time import sleep
import pandas as pd
import sys
import time


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


def banner():
    """
    This function displays the game name and provides the user 
    with 4 options. Each option selection is validated.
    """
    clear()
    print(f.renderText('  Welcome To'))
    print(f.renderText('      SoulRoll'))
    print("\n[1] Login")
    print("[2] create account")
    print("[3] Leaderboard")
    print("[4] exit\n")
    selection = input("What would you like to do?: ")
    if selection in banner_select.keys():
        initilising = "Initilising............\n"
        clear()
        print(f"\nYou selected option {selection}\n")
        print_letters(initilising)
        sleep(1)
        return banner_select[selection]()
    else:
        print("\nIncorrect selection, please try again")
        sleep(1)
        banner()


def create_account():
    """
    This function allows the user to create an account. It validates the 
    username chosen to check that it does not exist and comprises of
    no numbers and is between 3 and 10 characters. It allows users to create
    a password which is encoded and stored on google sheets.
    """

    system('clear')
    print(f.renderText('Create Account'))
    SHEET = GSPREAD_CLIENT.open('userdata')
    print("\nWelcome to account creation.\n")
    print("Please create your username")
    print("It should contain 3-10 characters")
    print("It should not contain any numbers")
    print("It will be case sensitive\n")
    username = input("Create a username: ")
    if username_check(username) is False:
        create_account()
    else:
        print("username accepted")
    print("Please create a password")
    print("It will be case sensitive\n")
    password = maskpass.askpass("\nCreate a password: ")
    password_check = maskpass.askpass("\nRe-enter password ")
    if password == password_check:
        print("\nAccount created successfully")
        enc = password_check.encode()
        hash1 = hashlib.md5(enc).hexdigest()
    else:
        print("Passwords do not match")
        sleep(2)
        create_account()
    souls = 20
    upload = SHEET.worksheet('username')
    upload.append_row([username, hash1, souls])
    banner()


def username_check(username):
    """
    This function is used to validate the username created. It checks
    to see if the username has already been taken and if the username
    is within 3 to 10 characters and has no numbers. 
    """
    data = SHEET.worksheet('username')
    usr = data.get_all_records()
    for record in usr:
        if record['username'] == username:
            print("username exists")
            sleep(2)
            create_account()
        else:
            try:
                [str(username) for username in username]
                if len(username) < 3:
                    raise ValueError(f"error")
                if len(username) > 10:
                    raise ValueError(f"error")
                if any(char.isdigit() for char in username):
                    raise ValueError(f"error")
            except ValueError as e:
                print(f"Invalid username: {e},")
                print("It must contain 3 to 10 characters and no numbers\n")
                sleep(2)
                return False
    return True


def user_authentication(input_username, auth_hash):
    """
    This function recieves the username and password input by the
    user and checks google sheets to see if there is a match. 
    """

    data = SHEET.worksheet('username')
    usr = data.get_all_records()
    match = False
    for record in usr:
        if (record['username'] == input_username
                and record['password'] == auth_hash):
            match = True
            break
        if input_username == 'exit'.lower():
            banner()
    if match:
        print("\nLogging in.....\n")
        sleep(1)
        print("Login Successful")
        sleep(1)

    else:
        print("Incorrect username or password. Please try again")
        print("Or type exit for username to exit to main menu.")
        sleep(3)
        main()


def leaderboard():
    """
    This function creates a pandas dataframe from the google sheet
    data and presents the specific columns, username and souls to 
    the terminal. It also hides the index and presents the data 
    with highest score at the top. 
    """

    clear()
    SHEET = GSPREAD_CLIENT.open('userdata').sheet1
    data = SHEET.get_all_records()
    df = pd.DataFrame(data)
    df = df.sort_values(by='souls', ascending=False)
    print(f.renderText('Leaderboard'))
    print(df.to_string(columns=['username', 'souls'], index=False))
    sleep(2)
    input("\nPress enter to return to main menu")
    banner()


def soulroll():
    """
    This function displays the ASCII art and presents the story of 
    the game. 
    """
    system('clear')
    print(f.renderText('SoulRoll'))
    sleep(2)
    system('clear')
    castle = r"""

         +       +++++              +
               +++++                            +
             ++++++
            ++++++                                          +
             +++++                  +
      +        ++++
                +++++


   |--------- /\/\/\__________/\/\/\/\/\/\__________/\/\/\---------|
   |    |    |     |                               |     |    |    |
   | {} | {} |     |          /\/\/\/\/\/\         |     | {} | {} |
   |    |    |  |/\/\|      /-------------\      |/\/\|  |    |    |
   | {} | {} |  /     \    /               \    /     \  | {} | {} |
   |    |    | /   |   \  /     ________    \  /   |   \ |    |    |
   | {} | {} |/   /|\   \|     ||||||||||    |/   /|\   \| {} | {} |
   |         |   |-|-|   |     ||||||||||    |   |-|-|   |         |
   |         |   |_|_|   |     ||||||||||    |   |_|_|   |         |
   |         |           |     |++++++++|    |           |         |
   |_________|___________|-------------------|___________|_________|
                              /__/.../__/
                             /__/.../__/
    """
    print(castle)
    sleep(2)
    story_one = """
Reining supreme in his icy citadel in Deceit
the Lich King Ravnos continues to consume innocent souls.
Any soul claimed by the Lich King would never be able
to leave as they become forever enthralled by his icy grasp.
These souls become bound as lich spirits and destined to
serve him for all eternity.\n
    """
    story_two = """
Until now. . . . . .
    """

    story_three = """\n
Mighty champion,
you have been entrusted with innocent souls to challenge
the Lich King and reclaim the stolen souls.\n
Will you be able to defeat him and return the innocent
souls back to their true resting place?\n
The fate of all Nazimar is in your hands\n
Are your ready for this challenge?\n
    """
    print_letters(story_one)
    sleep(2)
    print_letters(story_two)
    sleep(1)
    print_letters(story_three)
    ready_check()


def ready_check():
    """
    This function validates the users response to allow them to continue
    with the game or exit to main menu.
    """
    begin = input("\nType (y) to see the rules or (n) to quit: ").lower()
    if begin == 'n':
        banner()
    if begin == 'y':
        rules()
    else:
        ready_check()


def rules():
    """
    This function displays the rules of the game to the terminal and
    validats the users response to continue to the game or exit to 
    main menu.
    """
    system('clear')
    print(f.renderText('Rules\n'))
    print("* This is a random dice game of chance.\n")
    print("* You will take it in turn to roll a random number")
    print("  between 1 and 100.\n")
    print("* Each roll after that will be between 1 and the number")
    print("  you last rolled.\n")
    print("* The aim of the game is to NOT roll number 1.\n")
    print("* Should you beat the Lich King you will be")
    print("  rewarded one soul.\n")
    print("* Should you be defeated, you will lose a soul")
    print("  to the Lich King.\n")
    print("Are you ready to face the Lich King?")
    start_game = input("Type (y) to begin or (n) to quit: ").lower()
    if start_game == 'n':
        banner()
    if start_game != 'y':
        print('please type (y/n)')
        rules()
    else:
        print('\nLets begin..........')
        sleep(2)


def random_num(new_souls, input_username):
    """
    This function uses the random number generation to generate
    numbers between 2 and 100 for the first roll and then 1 to 
    whatever the last number rolled was. It will keep generating 
    a random number until number 1 is rolled. At this point the loop
    will stop.
    
    """
    system('clear')
    roll = input("Please type roll to start: ").lower()
    if roll != "roll":
        print("please type roll to begin")
        random_num(new_souls, input_username)
    system('clear')
    rolling = "Rolling . . . . . . .\n"
    print_letters(rolling)
    sleep(1)
    number1 = random.randint(2, 100)
    print(f"\nyou rolled: {number1}\n")
    number2 = random.randint(2, 100)
    sleep(1)
    print("The Lich King makes his move\n")
    print_letters(rolling)
    sleep(1)
    print(f"\nThe Lich King rolled: {number2}\n")
    input("press enter to roll again")
    while (number1 + number2 != 1):
        system('clear')
        number1 = random.randint(1, number1)
        print_letters(rolling)
        print(f"\nyou rolled: {number1}\n")
        sleep(1)
        if (number1 == 1):
            system('clear')
            print("Oh no, the Lich King defeated you!\n")
            print("You have lost a soul to the Lich King")
            new_souls -= 1
            print(f"\n{input_username} you now have {new_souls} souls\n")
            break
        print("The Lich King makes his move\n")
        number2 = random.randint(1, number2)
        print_letters(rolling)
        sleep(1)
        print(f"\nThe Lich King rolled: {number2}\n")
        input("press enter to keep rolling")
        if (number2 == 1):
            system('clear')
            print("The Lich King lost\n")
            print("Congratulations YOU won!")
            print("You have rescued one trapped soul")
            new_souls += 1
            print(f"\n{input_username}, you now have {new_souls} souls\n")
            break
    return new_souls


def print_letters(text):
    """
    This function allos the terminal print statments to be printed
    letter at a time with a 0.05s delay.
    """

    for letters in text:
        print(letters, end='', flush=True)
        time.sleep(0.05)


def clear():
    """
    This function when called clears the terminal in both
    mac and linux OS and windows OS
    """
    if sys.platform.startswith('linux'):
        # For Mac and Linux
        system("clear")
    else:
        # For Windows
        system("cls")


def get_current_souls(input_username):
    """
    This function pulls data from the google sheet for a specific user
    and prints to the terminal how many souls they currently have.
    """

    SHEET = GSPREAD_CLIENT.open('userdata').sheet1
    column_headers = SHEET.row_values(1)
    username_index = column_headers.index('username') + 1
    for i in range(1, SHEET.row_count + 1):
        username = SHEET.cell(i, username_index).value
        if username == input_username:
            souls = SHEET.cell(i, column_headers.index('souls') + 1).value
            system('clear')
            print(f"Well met {username}! you currently have {souls} souls.\n")
            input("\nPress enter to continue")
            return souls


def update_souls(input_username, add_souls):
    """
    This function updates the user score after each random_num played.
    It opens the google sheet userdata, finds the correct user and
    updates their score. 
    """

    SHEET = GSPREAD_CLIENT.open('userdata').sheet1
    column_headers = SHEET.row_values(1)
    username_index = column_headers.index('username') + 1
    value_to_update = add_souls
    row_count = len(SHEET.get_all_values())
    for i in range(1, SHEET.row_count + 1):
        username = SHEET.cell(i, username_index).value
        if username == input_username:
            SHEET.update_cell(i, column_headers.index(
                'souls') + 1, value_to_update)
            return update_souls


def main():
    """
    This function runs from top down and structures the game. It logs the user 
    in, validates their details and and gets their current souls from 
    google sheet data. It runs the game and then asks if the user would 
    like to replay or quit.
    """

    system('clear')
    print(f.renderText('       Login'))
    print("\nWelcome Adventurer,\n")
    input_username = input("Please enter your username: ")
    input_password = maskpass.askpass("\nPlease enter your password: ")
    auth = input_password.encode()
    auth_hash = hashlib.md5(auth).hexdigest()
    user_authentication(input_username, auth_hash)
    souls = get_current_souls(input_username)
    new_souls = int(souls)
    sleep(1)
    soulroll()
    test_souls = random_num(new_souls, input_username)
    sleep(1)
    add_souls = test_souls
    update_souls(input_username, add_souls)
    sleep(2)
    while True:
        print("would you like to play again?\n")
        response = input("Please select (y/n): ").lower()
        if response == 'y':
            print("game restarting.......")
            sleep(2)
            souls = get_current_souls(input_username)
            new_souls = int(souls)
            test_souls = random_num(new_souls, input_username)
            add_souls = test_souls
            update_souls(input_username, add_souls)
        elif response == 'n':
            print("Thankyou for playing!")
            banner()
        else:
            print("invalid choice")
    else:
        print("incorrect")


banner_select = dict({
    "1": main,
    "2": create_account,
    "3": leaderboard,
    "4": banner
})


banner()


if __name__ == "__main__":
    main()
