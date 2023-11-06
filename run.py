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


def create_account():
    SHEET = GSPREAD_CLIENT.open('userdata')
    username = input("username: ")
    password = input("password: ")

    upload = SHEET.worksheet('username')
    upload.append_row([username, password])



    input_username = input("username")
    input_password = input("password")

    data = SHEET.worksheet('username')
    usr = data.get_all_records()
    #print(usr)
    match_found = False
    for record in usr:
        if record[''] == input_username and record[''] == input_password:
            match_found = True
            break
    if match_found:
        print("logged in")
    else:
        print("incorrect")
# def login():
#     username = input("Please enter your username: ")
#     data = SHEET.worksheet('user')
#     usr = data.get_all_values()
#     print(usr)
#     if username.lower() == str(usr):
#         print("Correct credentials!")
#         pwd = input("Please enter your password: ")
#         data = SHEET.worksheet('password')
#         pw = data.get_all_values()
#         print(pw)
#         if pwd == str(pw):
#             print("correct details")
        
#     else:    
#         print("Incorrect credentials.")
#         main()


def main():
    create_account()
    #login()


main()
#login()


