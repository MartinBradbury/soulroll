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

sales = SHEET.worksheet('user')

data = sales.get_all_values()
print(data)
def username():
    username = input("username: ")
    return username.split()

def update_username(user):
    """
    update username on the google sheet
    """
    print("Updating Username....\n")
    upload_un = SHEET.worksheet('user')
    upload_un.append_row(user)
    print("Username accepted")


def main():

    user = username()
    update_username(user)


main()
