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
    """
    This function is ran when the terminal loads. It ensures there is a
    clear terminal and prints the title for the game. It gives
    the user a list of options to select which have been stored in
    a dictionary. Once user has selected an option, the will see
    a print message saying initilising and a 3 second pause.
    """

    clear()
    print(f.renderText('  Warcraft'))
    print(f.renderText('mini-games'))
    print("Welcome")
    print("[1] Login")
    print("[2] create account")
    print("[3] Leaderboard")
    print("[4] exit")
    selection = input("What would you like to do?: ")
    if selection in welcome_select.keys():
        print(f"You selected option {selection}, initilising.....")
        sleep(3)
        return welcome_select[selection]()
    else:
        print("\nIncorrect selection, please try again")
        sleep(3)
        welcome()


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
    username = input("Create a username: ").lower()
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
        sleep(3)
        create_account()
    score = 0
    upload = SHEET.worksheet('username')
    upload.append_row([username, hash1, score])
    welcome()


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

    try:
        [str(username) for username in username]
        if len(username) < 3:
            raise ValueError(f"error")
        if len(username) > 10:
            raise ValueError(f"error")
        if any(char.isdigit() for char in username):
            raise ValueError(f"error")
        else:
            return True
    except ValueError as e:
        print(f"Invalid username: {e},")
        print("It must contain 3 to 10 characters and no numbers\n")
        sleep(3)
        return False
    return True


def login(input_username, auth_hash):
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
        if record['username'] == input_username and record['password'] == auth_hash:
            match = True
            break
    if match:
        print("Logging in.....")
        sleep(3)
        print("Login Successful")
        sleep(1)
    else:
        print("Incorrect username or password. Please try again")
        sleep(3)
        welcome()


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
    df = df.sort_values(by='score', ascending=False)
    print(f.renderText('Leaderboard'))
    print(df.to_string(columns=['username', 'score'], index=False))
    sleep(5)
    input("\nPress enter to return to main menu")
    welcome()


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
    print(f.renderText('Welcome to Deathroll\n'))
    print("In this game you will play against the Lich King!")
    print("\n You will take turns to roll a number between 1 - 100")
    print("your next roll will be between 1 - the number YOU rolled")
    print("You keep taking it in turns until your or the Lick King rolles a 1")
    print("This a game of chance and the object is to not roll 1\n")
    print("To start the game, please type roll\n")
    roll = input(": ")
    if roll.lower() == 'roll':
        True
    else:
        print("please type roll to start the game")
        sleep(3)
        deathroll()


def random_num(new_score, input_username):
    system('clear')
    print(new_score)
    print("rolling.........")
    sleep(1)
    number1 = random.randint(2, 100)
    print(f"\nyou rolled: {number1}")
    number2 = random.randint(2, 100)
    input("press any key for computer roll")
    print(f"the computer rolled: {number2}\n")
    while (number1 + number2 != 1):
        input("press any key to roll again")
        number1 = random.randint(1, number1)
        print(f"\nyou rolled: {number1}")
        if (number1 == 1):
            print("Oh no, the Lich King defeated you!")
            print("Congratulations Lich King!")
            new_score += 0
            print(new_score)
            break
        input("press any key for computer roll\n")
        number2 = random.randint(1, number2)
        print(f"the computer rolled: {number2}\n")
        if (number2 == 1):
            print("The Lich King lost")
            print("Congratulations YOU won!")
            new_score += 1
            print(f"Well done {input_username} your new score is {new_score}")
            break
    return new_score


def clear():
    """
    This function when called clears the terminal in both
    mac and linux OS and windows OS
    """

    # for windows
    system('cls')
    # for mac and linux
    system('clear')


def get_current_score(input_username):
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
            score = SHEET.cell(i, column_headers.index('score') + 1).value
            system('clear')
            print(f"Hello {username}! your current score is {score}")
            input("Press the return key to continue")
            return score


def update_score(input_username, add_score):
    """
    This function updates the user score after each random_num played.
    It opens the google sheet userdata, finds the correct user and
    updates their score. It then returns the data update_score.
    """

    SHEET = GSPREAD_CLIENT.open('userdata').sheet1
    column_headers = SHEET.row_values(1)
    username_index = column_headers.index('username') + 1
    value_to_update = add_score
    row_count = len(SHEET.get_all_values())
    for i in range(1, SHEET.row_count + 1):
        username = SHEET.cell(i, username_index).value
        if username == input_username:
            SHEET.update_cell(i, column_headers.index('score') + 1, value_to_update)
            return update_score


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
    print(f.renderText('Login'))
    print("\nWelcome Traveller,\n")
    input_username = input("Please enter your username: ").lower()
    input_password = maskpass.askpass("\nPlease enter your password: \n").lower()
    auth = input_password.encode()
    auth_hash = hashlib.md5(auth).hexdigest()
    login(input_username, auth_hash)
    score = get_current_score(input_username)
    new_score = int(score)
    sleep(1)
    deathroll()
    test_score = random_num(new_score, input_username)
    sleep(1)
    add_score = test_score
    update_score(input_username, add_score)
    sleep(10)
    while True:
        print("would you like to play again?")
        response = input("Please select (y/n): ").lower()
        if response == 'y':
            print("game restarting.......")
            sleep(5)
            score = get_current_score(input_username)
            new_score = int(score)
            test_score = random_num(new_score, input_username)
            add_score = test_score
            update_score(input_username, add_score)
        elif response == 'n':
            print("Thankyou for playing!")
            welcome()
        else:
            print("invalid choice")
    else:
        print("incorrect")


welcome_select = dict({
    "1": main,
    "2": create_account,
    "3": leaderboard,
    "4": exit
    })

welcome()
main()
