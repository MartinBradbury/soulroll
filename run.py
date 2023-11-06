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
#from words import word_list


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
    print("Welcome")
    print("[1] Login")
    print("[2] create account")
    print("[3] exit")
    selection = input("What would you like to do?: ")
    if selection in user_selection.keys():
        return user_selection[selection]()
    else:
        welcome()


def create_account():
    system('clear')
    SHEET = GSPREAD_CLIENT.open('userdata')
    print("\nWelcome to account creation.\n")
    print("Please create a username between 3-10 characters and starts with any letter\n")
    username = input("Create a username: ").lower()
    if len(username) < 3:
        print("Username should be between 3 and 10 characters")
        create_account()
    elif len(username) > 10:
        print("Username should be between 3 and 10 characters")
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
        create_account()


    upload = SHEET.worksheet('username')
    upload.append_row([username, hash1])
    welcome()


def login():
    system('clear')
    print("Welcome to Login")
    print("Please Login using your username and password\n")
    input_username = input("username")
    input_password = maskpass.askpass("\npassword")
    auth = input_password.encode()
    auth_hash = hashlib.md5(auth).hexdigest()

    data = SHEET.worksheet('username')
    usr = data.get_all_records()
    match = False
    for record in usr:
        if record['username'] == input_username and record['password'] == auth_hash:
            match = True
            break
    if match:
        print("logged in")
    else:
        print("incorrect")
        login()



def main():
    welcome()


user_selection = dict({
    "1": login,
    "2": create_account,
    "3": exit
    })  



f = Figlet(font='slant')
print(f.renderText('  Welcome'))
print(f.renderText('         To'))
print(f.renderText('  Warcraft'))
print(f.renderText('mini-games'))
main()