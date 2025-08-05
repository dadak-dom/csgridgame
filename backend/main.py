'''
Main file for the backend server
'''

from typing import Union
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi import FastAPI
import pandas as pd
import json
import asyncio
import gridgen
from dotenv import load_dotenv
import mysql.connector
import os
import jq
import utils
import constants

BOARD_DIR = 'board.json'
SKIN_NAMES_DIR = 'all_possible_skins.json'

load_dotenv()

app = FastAPI()

# Defining CORS headers
origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
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
    return output

# The board should be global, only updated once per day

# ONly for testing...
BOARD_QUERIES = None
@app.get("/queries/")
def getQs():
    return {"queries" : BOARD_QUERIES}

def generateBoard():
    rows, cols = gridgen.generateBoard()
    rindex = 0
    
    cindex = 0
    board_fill_queries = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]
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
    with open("board.json", 'w') as f:
        json.dump([getPossibleAnswers(board_fill_queries), trans_rows, trans_cols], f)

def getBoard():
    with open(BOARD_DIR, 'r') as board:
        return json.load(board)

@app.get("/all_skins/")
def getAllPossibleSkins():
    output = []
    with open(SKIN_NAMES_DIR, 'r', encoding='utf8') as names:
        weapons = json.load(names)
        for w in weapons:
            output.append(w['weapon_name'])
    return output


@app.get("/")
def read_root():
    return {"Hello": "World",
            'all_possible' : getAllPossibleSkins(),
            "test_single_item" : getBoard()[0][0][0][0],
            "entire_board" : getBoard()} # <- how to get a single item

# async def testing_func():
#     while True:
#         print("Hellow!")
#         await asyncio.sleep(10)

# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(testing_func())

@app.on_event("startup")
async def startup_event():
    if not os.path.exists(BOARD_DIR):
        generateBoard()

@app.on_event("shutdown")
def shutdown_event():
    print("shutting down!!!!")

@app.get("/board/")
def get_board():
    print("Getting board...")
    return {"board" : getBoard()[0], "row_queries" : getBoard()[1], "col_queries" : getBoard()[2]}

@app.get("/genboard/")
def gen_board():
    print("Generating new board...")
    generateBoard()

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

def sortWeaponsByPrice(weapon_list):
    with open("crawl-data.json") as f:
        data = json.load(f)
    
    prices = {}
    for weapon in weapon_list:
        # First, clean the input
        w, skin = weapon.split(' | ')
        query = f'.[] | select(.weapon == \"{w}\" and .name == \"{skin}\") | .prices'
        result = jq.compile(query).input(data).all()[0]
        # max_price = max(result.values())
        max_key, max_value = max(result.items(), key=lambda item: item[1] if item[1] is not None else float('-inf'))
        # Store the weapon in a dict with the price as value
        prices[weapon] = max_value
        print(max_value)
    # Sort the entire dict, return the KEYS in order
    sorted_prices = dict(sorted(prices.items(), key=lambda item: item[1], reverse=True))
    print('Heres the dict', sorted_prices)
    print('Heres the keyes only', sorted_prices.keys())
    return list(sorted_prices.keys())
        

'''Given a board full of queries, get the names of skins that will work for each square.mi'''
def getPossibleAnswers(board):
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
                output[rindex][cindex] = sortWeaponsByPrice(skin_names)
                # print("Num of answers: ", len(results))
            except mysql.connector.Error as e:
                print('ERROROROROROROOR', e)
            cindex += 1
        cindex = 0
        rindex += 1
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
        location = find_files_in_folder(os.path.join(os.getcwd(), 'images'), matching)[0]
        return FileResponse(location)

