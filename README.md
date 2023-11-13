# Warcraft Mini-games

(Developer: Martin Bradbury)

## Live Website

Link to live website: [Warcraft Mini-games](https://warcraft-minigames-58310d7b7a2b.herokuapp.com/)

## Project purpose

LichKing is a Python terminal project game. The game is a story driven random number game where the player competes against the computer, the Lich King. The aim of the game is to reclaim lost souls the Lich King has taken. To do this you need to Lich King to roll the number 1 before you do. The game features a create account feature that stores the users details on google sheets, a login feature which pulls the users data from google sheets and a leaderboard, which displays all the users and their current souls. The game is interactive and provides feedback to the user throughout. All user input has validation functionality and the user can seamlessly play again or return to the main menu. 

## Table of Contense






## Rules of the Game

    • You will take it in turn to roll a random number between 1 and 100.
    • Each roll after that will be between 1 and the number you last rolled.
    • The aim of the game is to NOT roll number 1.
    • Should you beat the Lich King you will be rewarded one soul.
    • Should you be defeated, you will lose a soul to the Lich King.
    • All new accounts start with 20 souls.

## User Experience (UX)

### Key Project Goals

    • To write and develop a Python terminal game that is interactive.
    • The game should be easy to follow and the interface should be easy to navigate.
    • The user should be able to restart, exit or continue playing after logging in.
    • The user will feel part of the story being told.
    • The user will need to create an account username and password which will be stored on google sheets.
    • There will be validation when creating the username and password.
    • A login feature that requires the user to type back in their username and password stored on google sheets.
    • A leaderboard feature which displays the users who have played and their souls remaining.
    • Users can log back into their account at any time to continue playing.

### User Requirements and Expectations

    • A clear and easy to read interface.
    • Clear and intuitive navigation options.
    • Be able to create a unique username that cannot be copied.
    • Be able to create a unique password that is encoded so cannot be seen on google sheets.
    • Be able to look at a leaderboard to see who has the most souls.
    • Have feedback throughout the game of how many souls they have.
    • Have imersion in the story of the game.
    • Be able to take time to read and understand the rules of the game. 
    • Have the opportunity to play again without going back to the main menu. 
    • Be able to exit back to the main menu at the end of a game.

## User Stories

As a site visitor,

    • I want to see the game title when I arrive on the start screen.
    • I want to be able to see the navigation of the game.
    • I want to be able to create a unique username and password.
    • I want to be able to login with my username and password.
    • I want to understand the story of the game.
    • I want to know the rules of the game.
    • I want to be able to play many times without returning to the main menu.
    • I want to know how many souls I have left and if I have won or lost each game. 
    • I want to be able to exit to the main menu and stop points in the game.
    • I want to be able to see my score and username on the leaderboard.

## Features

### Start Screen





## Future Features





## Design Features

### Design Choices

### Typography

### Mock Terminal
positioning of the terminal

## Flow Chart??

## Technology

### Language

- Python

### Framweorks and Tools

- [Heroku](https://www.heroku.com/)
- [GitHub](https://github.com/)
- [CodeAnywhere](https://app.codeanywhere.com/)
- [Lucid Chart](https://www.lucidchart.com/pages/)**
- [Chrome DevTools](https://developer.chrome.com/docs/devtools/)
- [Google Lighthouse](https://chrome.google.com/webstore/detail/lighthouse/blipmdconlkpinefehnmjammfjpmpbjk)
- Code institute's template for the mock terminal was used, but it was styled by centering it and giving it a blue and black theme.
- Code Institutes Python Linter was used to check the Pythn code for errors.

### Python Libraries and Modules

- [google.oauth2.service_account](https://google-auth.readthedocs.io/en/master/reference/google.oauth2.service_account.html) was used to authorize the connection with the Google Sheets API. The Usernames, Passwords and souls were stored here.
- [gspread](https://docs.gspread.org/en/v5.11.3/) was imported and used to access and update data in the spreadsheet.
- [random](https://docs.python.org/3/library/random.html) was imported for generating random numbers.
- [pyfiglet](https://pypi.org/project/pyfiglet/) was imported to render ascii art
- [sys](https://docs.python.org/3/library/sys.html) was imported to clear the terminal on different operating systems.
- [time](https://docs.python.org/3/library/time.html) was imported to allow sleep delays between prompts
- [hashlib](https://docs.python.org/3/library/hashlib.html) was imported to encript and decode the users password before writing to google sheets and when required for login.
- [maskpass](https://pypi.org/project/maskpass/) was used to hide the users input in the terminal when typing in the password.
- [pandas](https://pandas.pydata.org/docs/getting_started/install.html) was used to display the leaderboard in a dataframe.
