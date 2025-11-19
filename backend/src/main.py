'''
Main file for the backend server
'''
import sys
sys.path.append('/home/dominik/.local/lib/python3.10/site-packages')

from typing import Union
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi import FastAPI, BackgroundTasks
from apscheduler.schedulers.background import BackgroundScheduler
from pathlib import Path
import pandas as pd
import json
import asyncio
import modules.gridgen as gridgen
from dotenv import load_dotenv
import mysql.connector
import os
import jq
import modules.utils as utils
import modules.constants as constants
from modules.constants import WeaponCategory
import logging
import datetime

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

app = FastAPI()

scheduler = BackgroundScheduler()
scheduler.start()

# scheduler.add_job(test, 'interval', seconds=2, id='test_job')
# TODO : fix some of the query formatting issues, like with flavor text

# Defining CORS headers
origins = [
    # "http://localhost:5173",
    "http://localhost:3000",
    "http://192.168.0.235:3000",
    # "http://192.168.0.135"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*']
)

# Given the list of pure queries, return a human-readable sentence.
def translateQueryToSentence(query_list):
    output = []
    for q in query_list:
        print("QUERY LIST: ", q)
        cat, key, val = q.split(" ")
        print(constants.LANGUAGE[cat][key] + val)
        try:
            o = constants.LANGUAGE[cat][key] + constants.VALUE_MAPPING[val]
        except KeyError:
            o = constants.LANGUAGE[cat][key] + val
        output.append(o)
    logging.debug(f"QUERY LIST INTO A SENTENCE: ", output)
    return output

def generateBoard():
    '''Use helper functions to generate a new game board for GridGame'''
    rows, cols = gridgen.generateBoard()
    rindex = 0
    
    cindex = 0
    board_fill_queries = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]

    # Given a valid board, get the SQL queries associated with each cell
    for r in rows:
        for c in cols:
            var1, keyword1, val1 = r.split(" ")
            var2, keyword2, val2 = c.split(" ")
            var1 = constants.VAR_MAPPING[var1]
            var2 = constants.VAR_MAPPING[var2]
            query = 'SELECT * '
            # Get the vars that you need
            # add to query
            query += 'FROM skins_data WHERE '
            query += gridgen.queryHelper(val1, keyword1, var1) + ' ' + gridgen.queryHelper(val2, keyword2, var2, first=False)
            print(query)
            print(rindex, cindex)
            
            board_fill_queries[rindex][cindex] = query

            cindex += 1
        cindex = 0
        rindex += 1
    global BOARD_QUERIES
    BOARD_QUERIES = board_fill_queries
    # query += queryHelper(val1, keyword1, var1, first=True) + queryHelper(val2, keyword2, var2, first=False)
    trans_rows = translateQueryToSentence(rows)
    trans_cols = translateQueryToSentence(cols)
    # return getPossibleAnswers(board_fill_queries), trans_rows, trans_cols

    # Before saving the new board, move the old board in with the other old boards
    # NOTE: This will assume that the board currently in the daily board directory is YESTERDAY'S board
    for board_file in os.listdir(constants.DAILY_BOARD_DIR):
            os.rename(os.path.abspath(f'../backend/{constants.DAILY_BOARD_DIR}{board_file}'), os.path.abspath(f'../backend/{constants.PAST_BOARDS_DIR}{board_file}'))
    # Save the board of the day
    with open(utils.get_daily_board_dir(), 'w') as f:
        json.dump([getPossibleAnswers(board_fill_queries), trans_rows, trans_cols], f)

def getBoardOfTheDay():
    try:
        with open(utils.get_daily_board_dir(), 'r') as board:
            return json.load(board)
    except FileNotFoundError:
        logging.warning("Board of the day is missing or not the correct date!")
        try:
            with open(utils.get_board_in_daily_dir(), 'r') as fallback_board:
                    logging.warning("Falling back to file found in daily dir...")
                    return json.load(fallback_board)
        except (FileNotFoundError, TypeError):
            logging.critical("BOARD NOT FOUND")

@app.get('/board/today')
def getTodaysBoard():
    '''Return the name of the board of the day. Front end can decide what to do with it.'''
    try:
        return os.listdir(constants.DAILY_BOARD_DIR)[0]
    except IndexError:
        return "There was a problem retrieving the board of the day, please try again later"

@app.get('/board/all_skins/today')
def getTodaysAllSkins():
    '''Return the all_skins file associated with the daily board'''
    # Extract the date from the daily board file
    day, month, year = utils.extractDate(getTodaysBoard())
    with open(utils.get_all_skins_dir(day, month, year)) as all_skins:
        return json.load(all_skins)

@app.get('/board/past/{year}/{month}/{day}')
def getPastBoard(day, month, year):
    '''Get a board from the past, given a year, month, and day'''
    with open(utils.get_past_board_dir(day, month, year)) as past_board:
        logging.debug("utils: ", utils.get_past_board_dir(day, month, year))
        return json.load(past_board)
    
@app.get('/board/all_skins/past/{year}/{month}/{day}')
def getPastAllSkins(day, month, year):
    '''Return all_skins file associated with a past board, or a board at a specified date'''
    with open(utils.get_all_skins_dir(day, month, year)) as all_skins:
        return json.load(all_skins)
    
@app.get('/board/past/list')
def listPastBoards():
    '''Return a list of all the past boards'''
    boards = os.listdir(constants.PAST_BOARDS_DIR)

    def get_date(board):
        day, month, year = utils.extractDate(board)
        return datetime.date(int(year), int(month), int(day))

    return sorted(boards, key=get_date, reverse=True)

@app.get("/")
def read_root():
    return ""
    # return {"Hello": "World",
    #         # 'all_possible' : getAllPossibleSkins(),
    #         "test_single_item" : getBoardOfTheDay()[0][0][0][0],
    #         "entire_board" : getBoardOfTheDay()} # <- how to get a single item

# TODO: Make it so that if the date of the board that is in the daily slot is "out of date", generate a new board on startup
@app.on_event("startup")
async def startup_event():
    if not os.path.exists(constants.DAILY_BOARD_DIR):
        logging.info("No board on startup, generating...")
        generateBoard()
    # setAllPossibleSkins()

@app.on_event("shutdown")
def shutdown_event():
    print("shutting down!!!!")

@app.get("/board/")
def get_board():
    logging.info("Getting board...")
    return {"board" : getBoardOfTheDay()[0], "row_queries" : getBoardOfTheDay()[1], "col_queries" : getBoardOfTheDay()[2]}

# Generate a new board
# NOTE: This is for testing purposes only. Requires a password.
@app.get("/genboard/}")
def gen_board(password: str = ""):
    if password != os.getenv("SKINSAPI_TEST_PASS"):
        return "You do not have permission to do that."
    logging.info("Generating new board...")
    generateBoard()

# NOTE: This function gave me some pain before because I was importing the crawl-data json instead of just using the database.
def sortWeaponsByPrice(weapon_list, conn_cursor):
    # with open(constants.CRAWL_DATA_DIR) as f:
    #     data = json.load(f)
    prices = {}
    for weapon in weapon_list:
        w, skin = weapon.split(' | ')
        # print("WEAPON: ", w, skin)
        conn_cursor.execute("SELECT prices FROM skins_data WHERE weapon = %s AND skin_name = %s", (w, skin))
        row = conn_cursor.fetchone()

        if row:
            prices_json = row[0].replace('\'', '"').replace("None", "0")  # This is a JSON string
            # print("PRICES.JSON" , prices_json)
            result = json.loads(prices_json)
            # print("Factory New price:", prices.get("Factory New"))
        else:
            print("No matching skin found.")

        max_key, max_value = max(result.items(), key=lambda item: item[1] if item[1] is not None else float('-inf'))
        # Store the weapon in a dict with the price as value
        prices[weapon] = max_value
        # print(max_value)
    # Sort the entire dict, return the KEYS in order
    sorted_prices = dict(sorted(prices.items(), key=lambda item: item[1], reverse=True))
    # print('Heres the dict', sorted_prices)
    logging.debug(f'Sorted weapon names by price for new board: {sorted_prices.keys()}')
    return list(sorted_prices.keys())
        
def getPossibleAnswers(board):
    '''Given a board full of queries, get the names of skins that will work for each square'''
    # Since the board is a 3x3 2D array, we can just loop through, get the query results, and store them in a parallel array
    # Here's what we are going to do: Sort them by max price
    output = [
        [None] * 3,
        [None] * 3,
        [None] * 3,
    ]
    conn = utils.connect_db()
    cursor = conn.cursor()
    rindex, cindex = 0, 0
    for row in board:
        for query in row:
            query = query.replace("*", "weapon, skin_name, id", 1)
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                # global df 
                # df = pd.concat([df, pd.Series(len(results))])
                print(results)
                skin_names = []
                for r in results:
                    skin_names.append(r[0] + " | " + r[1])   
                # Sort by price, put it in the board
                output[rindex][cindex] = sortWeaponsByPrice(skin_names, conn_cursor=cursor)
                # print("Num of answers: ", len(results))
            except mysql.connector.Error as e:
                logging.error('Error occurred when getting possible answers: ', e)
            cindex += 1
        cindex = 0
        rindex += 1
    conn.close()
    return output
            
@app.get("/get_skin_image/{skin_name}")
async def getSkinImage(skin_name):
        matching = skin_name.replace('_', ' ')
        import fnmatch
        print(matching)
        # print(os.listdir())
        def find_files_in_folder(folder_path, match_string):
            matching_files = []
            
            for root, dirs, files in os.walk(folder_path):  # Walk through all subdirectories
                # print(files)
                for file in files:
                    # print(file)
                    if fnmatch.fnmatch(file, f"*{match_string}*"):  # Match files with partial string
                        matching_files.append(os.path.join(root, file))  # Full path to the file
            # print(matching_files)
            
            # print(os.listdir(os.path.join(os.getcwd(), 'images')))
            return matching_files
        print(skin_name)
        logging.critical("WHAT I TRIED: ", os.path.join(os.getcwd(), constants.IMAGE_DIR))
        logging.critical("LISTDIR", os.listdir(os.getcwd()))
        location = find_files_in_folder(os.path.join(os.getcwd(), constants.IMAGE_DIR), matching)[0] # FIXME
        return FileResponse(location)


# TODO : Add the scheduler for making the board each day
scheduler.add_job(gen_board, 'cron', hour=0, minute=5, id='generate_new_daily_board') # FIXME: Specify time zone!

# # FIXME: FOR TEMPORARY TESTING PURPOSES ONLY. DO NOT ALLOW THIS INTO PROD!!!
# @app.get("/import-data/")
# def importData():
#     gridgen.importCrawlData()
