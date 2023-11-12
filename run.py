import gspread
from google.oauth2.service_account import Credentials
import random
import hashlib
import maskpass
# pip install maskpass
from os import system
# to clear screen
from pyfiglet import Figlet
# pip3 install pyfiglet
from time import sleep
# time sleep
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
    This function is ran when the terminal loads. It ensures there is a
    clear terminal and prints the title for the game. It gives
    the user a list of options to select which have been stored in
    a dictionary. Once user has selected an option, the will see
    a print message saying initilising and a 3 second pause.
    """

    clear()
    print(f.renderText('       Warcraft'))
    print(f.renderText('     mini-games'))
    print("Welcome")
    print("[1] Login")
    print("[2] create account")
    print("[3] Leaderboard")
    print("[4] exit")
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
    This function clears the current terminal and displays the
    heading 'create account'. It opens the google sheet data
    'userdata' and asks the user to input a username.
    A message is printed detailing the requirements of the username.
    The username is converted to lower case and sent through to
    username check function. If returned True from username check
    a message prints to inform the user it is accepted.
    Users are then asked to create a password and verify the
    password. The password is hidden when typed using maskpass
    and encoded. A score of 0 is declared to the new user and
    the accepted username and encoded password is written
    to google sheets along with their score of 0.
    Users are then sent to the welcome function.
    """

    system('clear')
    print(f.renderText('Create Account'))
    SHEET = GSPREAD_CLIENT.open('userdata')
    print("\nWelcome to account creation.\n")
    print("Please create your username")
    print("It should contain 3-10 characters")
    print("It should not contain any numbers\n")
    username = input("Create a username: ")
    if username_check(username) is False:
        create_account()
    else:
        print("username accepted")
    print("Please create a password")
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
    This function is called from the create account
    function. It checks the username entered by the user
    to make sure it is between 3 and 10 characters and contains
    no numbers. If the username does not meet this creteria
    a valueerror is raised with a print statement reminding the
    user of the username requirements. This remains on the screen
    for 3 seconds before the create account function is called again.
    If the username is accepted no value error is raised and True
    is returned sending the user back to the create account function
    where they will not create a password.
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
    This function take the username input and password input
    from the main function. It opens google sheet userdata
    and gets all records. It looks through the records
    to find a match for the username input and password input.
    If a match is found the loop is broken and returned to the
    main function after a pause where the terminal displays
    logging in and login successful. If no match is found the
    user is returned to the welcome function.
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
        print("Or type exit in username to exit to main menu.")
        sleep(2)
        main()


def leaderboard():
    """
    This function is selected from the welcome function.
    It clears the terminal and opens the google sheet userdata.
    It gets all records from the sheet and stores it as a
    pandas dataframe. It arranges the data from by the score
    column in the google sheet from highest to lowers.
    The heading leaderboard is printed to the terminal. Only the
    usernames and scores are printed to the terminal from highest
    to lowers and the index removed. The is a 5 second delay and
    then a print statment appers under the dataframe informing the
    user to press enter to continue to the welcome function.
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


def deathroll():
    """
    This function clears the terminal and prints the heading
    for the game. Below the heading the rules of the game are
    printed to the terminal. The users are asked to type
    'roll' to start the game. If roll is typed correctly
    the game will begin and the random_num function is called.
    If they do not type roll correctly they are informed what they
    need to type again and their error, a pause for 3 seconds
    and then the deathroll function is called again.
    """

    system('clear')
    castle = """

                 +++++
               +++++
             ++++++
            ++++++
             +++++
               ++++
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
Reining supreme in his icy citadel in Northrend
the Lich King Arthas continues to consume innocent souls.
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
The fate of all Azeroth is in your hands\n
Are your ready for this challenge?\n
    """
    print_letters(story_one)
    sleep(2)
    print_letters(story_two)
    sleep(1)
    print_letters(story_three)
    input("\nPress return to continue to the rules")
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
    input("Press return to continue")


def random_num(new_souls, input_username):
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
    print("The Lich King is rolling\n")
    print_letters(rolling)
    sleep(1)
    print(f"\nthe Lich King rolled: {number2}\n")
    input("press return to keep rolling")
    while (number1 + number2 != 1):
        system('clear')
        # input("press any key to roll again")
        number1 = random.randint(1, number1)
        print_letters(rolling)
        print(f"\nyou rolled: {number1}\n")
        if (number1 == 1):
            print("Oh no, the Lich King defeated you!")
            print("You have lost a soul to the Lich King")
            new_souls -= 1
            print(f"\n {input_username} you now have {new_souls} souls\n")
            break
        input("press any key for Lich Kings roll\n")
        number2 = random.randint(1, number2)
        print_letters(rolling)
        sleep(1)
        print(f"\nThe Lich King rolled: {number2}\n")
        input("press return to keep rolling")
        if (number2 == 1):
            print("The Lich King lost")
            print("Congratulations YOU won!")
            print("You have rescued one trapped soul")
            new_souls += 1
            print(f"\n{input_username}, you now have {new_souls} souls\n")
            break
    return new_souls


def print_letters(text):
    """
    Print the letters in turn with a 0.05s delay
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
    This function is called from the main function. It opens
    the google spreadsheet userdata and checks the username
    input for the login and prints their current score.
    There is an input of enter so the user has time to
    see their current score before moveing on.
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
            input("\nPress the return key to continue")
            return souls


def update_souls(input_username, add_souls):
    """
    This function updates the user score after each random_num played.
    It opens the google sheet userdata, finds the correct user and
    updates their score. It then returns the data update_score.
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
    This function clears the terminal. It is ran when the user
    selects login from the welcome function. It prints log in and
    asks the user to input their username and password. The login
    function is ran with the data inputed by the user and if true
    the get_current_score function is ran. The returned value is
    converted into an int and then the deathrol function is ran.
    when the deathroll function is complete the randon_num function
    is ran using the new_score and input_username data. After the
    random_num has completed the update _score function is ran to
    update the users score. The user is asked if they want to play
    again, if yes is selected the game restarts with their new score,
    if no is selected the welcome function is ran.
    checks are present to make sure the user selects y or n.
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
    deathroll()
    test_souls = random_num(new_souls, input_username)
    sleep(1)
    add_souls = test_souls
    update_souls(input_username, add_souls)
    sleep(2)
    while True:
        print("would you like to play again?")
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
