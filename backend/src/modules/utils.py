import mysql.connector
import modules.constants as constants
import logging
from os import path, listdir
from datetime import datetime

def extractDate(inputString):
    output = inputString.split('.')[0].split('-')
    return [output[1], output[2], output[3]]

def has_numbers(inputString):
    '''Check if a string contains ANY numbers/digits'''
    for char in inputString:
        try:
            int(char)
            return True
        except ValueError:
            continue
    return False

def get_daily_board_dir():
    '''Return the path that the board of the day should be expected at, i.e. the actual .JSON file'''
    day = datetime.now().day
    month = datetime.now().month
    year = datetime.now().year
    return path.join(constants.DAILY_BOARD_DIR, f"board-{day}-{month}-{year}.json")
    # return path.join(constants.DAILY_BOARD_DIR, f"board-{day}-{month}-{year}-{datetime.now().minute}.json")

def get_board_in_daily_dir():
    '''Return the board found in the daily folder. FALLBACK OPTION!'''
    for board_file in listdir(constants.DAILY_BOARD_DIR):
        print(board_file)
        return path.join(constants.DAILY_BOARD_DIR, board_file)
    # return path.join(constants.DAILY_BOARD_DIR, f"board-{day}-{month}-{year}-{datetime.now().minute}.json")

def get_past_board_dir(day, month, year):
    '''Given a date, return the board that was generated on {day, month, year}'''
    p = path.join(constants.PAST_BOARDS_DIR, f"board-{day}-{month}-{year}.json")
    logging.debug("P : ", p)
    if path.exists(p):
        logging.debug("RETURNING P")
        return p
    
def get_all_skins_dir(day, month, year):
    p = path.join(constants.SKIN_NAMES_DIR, f"all_skins-{day}-{month}-{year}.json")
    return p

def connect_db():
    """Connects to MySQL database and returns the connection."""
    try:
        conn = mysql.connector.connect(**constants.DB_CONFIG)
        print("✅ Connected to database successfully!")
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Error connecting to database: {e}")
        return None