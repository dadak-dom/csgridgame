import mysql.connector
import random
import json
import modules.constants as constants
import modules.utils as utils
import logging
import os

'''Helper function to build query'''
def queryHelper(v, k, var, first=True):
    if var == 'rarity' or var == 'finish' or var == 'weapon' or var == 'weapon_category':
        try:
            constants.VALUE_MAPPING[v]
            v = constants.VALUE_MAPPING[v]
        except KeyError:
            pass
    r = ''
    if not first:
        r = ' AND '
    if var != 'prices':
        r += var
    # else:
    #     if var != 'prices':
    #         r = var
    # Add the WHERE clause for variable
    if k == 'under':
        if var == 'prices':
            r += " CAST(REGEXP_SUBSTR(prices, '[0-9]+(\\.[0-9]+)?') AS DECIMAL(10,2)) < " + str(float(v))
        else:
            r += ' < ' + str(float(v))
    elif k == 'over':
        if var == 'prices':
            r += " CAST(REGEXP_SUBSTR(prices, '[0-9]+(\\.[0-9]+)?') AS DECIMAL(10,2)) > " + str(float(v))
        else:
            r += ' > ' + str(float(v))
    elif k == 'has':
        r += ' LIKE ' + f'\'%{v}%\''
    elif k == 'is':
        r += ' = ' + f'\'{v}\''
    elif k == 'canbe':
        r += ' = 1'
    elif k == 'cannotbe':
        r += ' = 0'
    elif k == 'equals':
        if var == 'year_added':
            r += ' = ' + str(int(v))
        else:
            r += ' = ' + str(float(v))
    elif k == 'startswith':
        r += ' LIKE ' + f'\'{v}%\''
    else:
        raise ValueError("Keyword " + k + " has no match in queryHelper()")
    if not first:
        return r + ' AND weapon_category !=  \'Knife\'' + ' AND prices REGEXP \'[0-9]\'' + ';'
    return r

# def setAllPossibleSkins():
#     '''
#      Create the 'all_possible_skins.json' file
#      Should be done each time a new board is generated

#      The purpose of the file is to limit the options that a player is allowed to select from.
#      This way, someone can't guess a skin that has zero chance of appearing as an answer - keeps the game from being too frustrating
#     '''
#     skin_names = []
#     with open(constants.CRAWL_DATA_DIR, 'r', encoding='utf8') as crawl_data:
#         skin_data = json.load(crawl_data)        
#         for skin in skin_data:
#             # Make sure that, for the purposes of the GridGame, we're only allowing non-knives and skins with prices attached
#             if skin['weapon-category'] != constants.WeaponCategory.KNIFE and utils.has_numbers(str(skin['prices'])):
#                 skin_names.append({"weapon_name" : f"{skin['weapon']} | {skin['name']}"})
#     # Delete the old file, if it already exists:
#     # if os.path.exists(constants.SKIN_NAMES_DIR):
#     #     logging.info(f"{constants.SKIN_NAMES_DIR} already exists, DELETING then REGENING...")
#     #     os.remove(constants.SKIN_NAMES_DIR)
#     with open(constants.SKIN_NAMES_DIR, 'w', encoding='utf-8') as f:
#         json.dump(skin_names, f)

def setAllPossibleSkins():
    '''
    Create the 'all_possible_skins.json' file using data from the MySQL database.
    Should be done each time a new board is generated.

    The purpose of the file is to limit the options that a player is allowed to select from.
    This way, someone can't guess a skin that has zero chance of appearing as an answer - keeps the game from being too frustrating.
    '''
    
    skin_names = []

    try:
        # Connect to the database
        conn = mysql.connector.connect(**constants.DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # Query to fetch relevant skins
        query = """
            SELECT weapon, skin_name, prices, weapon_category 
            FROM skins_data
        """
        cursor.execute(query)
        results = cursor.fetchall()

        for skin in results:
            if skin['weapon_category'] != constants.WeaponCategory.KNIFE and utils.has_numbers(str(skin['prices'])):
                skin_names.append({
                    "weapon_name": f"{skin['weapon']} | {skin['skin_name']}"
                })

        # # Optionally delete the existing file
        # if os.path.exists(constants.SKIN_NAMES_DIR):
        #     logging.info(f"{constants.SKIN_NAMES_DIR} already exists, DELETING then REGENING...")
        #     os.remove(constants.SKIN_NAMES_DIR)

        # # Write to JSON file
        # with open(constants.SKIN_NAMES_DIR, 'w', encoding='utf-8') as f:
        #     json.dump(skin_names, f, ensure_ascii=False, indent=2)

        day, month, year = utils.extractDate(utils.get_daily_board_dir())
        logging.debug(f"DAY: {day} MONTH: {month} YEAR: {year} FUNC: {utils.get_all_skins_dir(day, month, year)}")

        with open(utils.get_all_skins_dir(day, month, year), 'w', encoding='utf-8') as f:
            json.dump(skin_names, f, indent=2)

    except mysql.connector.Error as err:
        logging.error(f"MySQL Error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

# FIXME: Make sure that when I'm checking the validity of a board, I'm using skins from the list of POSSIBLE skins, not just the entire DB
def generateBoard():
    '''
    Steps in making a board:
        1. Generate 6 categories randomly - 3 rows, 3 columns
        2. For each cell (9 total), verify that the possible number of answers lies in a reasonable range. (8-20 seems to be a reasonable range)
            Will need to verify what the range is soon.
            If yes, move on to step 3, otherwise repeat step one.
        3. Use database to collect all possible answers for each cell, which will be sent to client
            once they visit the site.
    
    Parser rules breakdown:
    under [NUM]= all prices must be under specified [NUM]
    over = '' over price (same as above)
    has [PROP]= one of the elements of a list must be equal to [PROP] - diffent from IS because it expects a list
    is [PROP]= strings are equal (e.g. the value of a query would return it) - expects a string, compares the two
    canbe [PROP] = PROP expected to be true
    cannotbe [PROP] = PROP expected to be false
    equals [VALUE] = float, expected to be equal to value
    startswith [LETTER]= like '[letter]%'
    '''

    setAllPossibleSkins()

    conn = utils.connect_db()
    cursor = conn.cursor()

    categories = list(constants.QUESTIONS.keys())
    available_cats = categories.copy()

    

    '''Returns a question, as well as the categories used.'''
    def createQuestions(numQuestions=3):

        # print(list(categories))
        # return
        chosen_questions = []
        chosen_categories = []
        # Problem: available categories get modified glboally. This worked when the entire board was made at once, but if we're checking one at a time, we need to make sure that we re-add the category if we don't end up using that particular question
        while len(chosen_questions) < numQuestions:
            chosen_cat = available_cats[random.randint(0, len(available_cats) - 1)]
            available_cats.remove(chosen_cat)
            chosen_categories.append(chosen_cat)
            # Pick a random key and a random index from that key
            # chosen_cat = categories[random.randint(0, len(categories) - 1)]
            # print(chosen_cat)
            # categories
            # chosen_question.append(chosen_cat[random.randint(0, len(chosen_cat) - 1)])
            chosen_questions.append(chosen_cat + " " + constants.QUESTIONS[chosen_cat][random.randint(0, len(constants.QUESTIONS[chosen_cat]) - 1)])
        # print("CHOSEN QUESTIONS: ", chosen_questions)
        return chosen_questions, chosen_categories
    
    # print(createQuestions(3))

    # Now that some questions can be created, we need to create the board, and verify that there are enough solutions for each square

    '''New question generation logic should go here:'''
    row_questions = []
    col_questions = []
    # board_questions = []
    # for i in range(0, 2):
    #     board_questions.append(createQuestions(3))

    VALID_RANGE = [1, 200]
    """This function will query and use helper functions to verify that a given cell is valid"""
    """Returns True if the number of rows is within the VALID_RANGE"""
    def verifyCell(question1, question2):
        print('verifying ', question1, question2)
        # Combine the two questions into a SQL query
        """ 
        In order to do that, need to:
        Map the variable to it's SQL counterpart
        Construct the query based on the categories specified
        """
        # Split the question into its main parts
        var1, keyword1, val1 = question1.split(" ")
        var2, keyword2, val2 = question2.split(" ")
        var1 = constants.VAR_MAPPING[var1]
        var2 = constants.VAR_MAPPING[var2]

        query = 'SELECT * '
        # Get the vars that you need
        # add to query
        query += 'FROM skins_data WHERE '
        
        query += queryHelper(val1, keyword1, var1, first=True) + queryHelper(val2, keyword2, var2, first=False)
        # return query
        print("Query used: ", query)
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            # global df 
            # df = pd.concat([df, pd.Series(len(results))])
            print("DEBUG: RESULTS: ", results)
            print("Num of answers: ", len(results))
        except mysql.connector.Error as e:
            print('ERROROROROROROOR', e)
        return VALID_RANGE[0] <= len(results) <= VALID_RANGE[1]


        # for price checking, I just need to use the following regex: SELECT id, prices FROM skins_data WHERE CAST(REGEXP_SUBSTR(prices, '[0-9]+(\.[0-9]+)?') AS DECIMAL(10,2)) > 100;

        # When actually running the query, what I'll do for this verification step is just ask for the necessary variables - that way, I can parse what I need to, if I need to.
        # Once I'm gathering the answers (after verification), I can run the same queries as before, except this time, just grab the weapon and skin names that are valid answers.

    # verifyCell('MAXWEAR equals 1', 'STATTRAK cannotbe stattrak')
    def flatten_list(l):
        return [item for sublist in l for item in sublist]

    # First, create the rows of questions. These remain static
    rowqs, row_cats = createQuestions(3)
    row_questions.extend(rowqs)

    # Next, 
    # board_cell_questions = [[],[],[]]
    # broken_board = False
    # for r in range(0, 3):
    #     for c in range(0, 3):
    #         # print(c)
    #         # board_cell_questions[r].append(verifyCell(board_questions[0][r], board_questions[1][c]))
    #         if verifyCell(board_questions[0][r], board_questions[1][c]) is False:
    #             broken_board = True
    # print(board_questions)
    ''''''
    # ADD NEW FEATURE: IF the generator fails to make columns over 1000 times, re-gen the rows.
    ''''''
    attempts = 0
    MAX_ATTEMPTS = 100
    while len(col_questions) < 3:
        if attempts > MAX_ATTEMPTS:
            attempts = 0
            print('RESETTING!!!\n\n\n')
            available_cats.extend(row_cats)
            rowqs, row_cats = createQuestions(3)
            row_questions.extend(rowqs)
            col_questions = []
        # print(row_questions)
        # break
        # Generate a possible question
        cq, cats_used = createQuestions(1)
        # Verify that there are enough solutions for each column/row intersection
        goodQuestion = True
        for rq in row_questions:
            if verifyCell(cq[0], rq) is False:
                goodQuestion = False
                print("Questions, ", cq[0], rq, " break the board")
                break
        if goodQuestion:
            print("adding ", cq, "to verified list")
            col_questions.extend(cq)
        else:
            # If the question was not valid, then return the category to the available pool
            print("Adding ", cats_used, ' back to the pool')
            available_cats.extend(cats_used)
        attempts += 1
        print("Number of solid cols: ", len(col_questions), "Attempts:", attempts)
        # import time
        # time.sleep(0.5)
    print(row_questions, col_questions)
    return row_questions, col_questions
    # print(board_cell_questions[0][0])
    # Now, actually query
    questions = flatten_list(board_cell_questions)

good_board = False
i = 0

'''
    Insert data from crawler into database
'''
def importCrawlData():
    def insert_data(conn, skin):
        """Inserts a skin into the DB"""
        id = skin['id']
        url = skin['url']
        url_id = skin['url_id']
        weapon = skin['weapon']
        name = skin['name']
        souvenir = skin['souvenir']
        stattrak = skin['stattrak']
        rarity = skin['rarity']
        minwear = skin['minwear']
        maxwear = skin['maxwear']
        finish = skin['finish-style']
        weapon_cat = skin['weapon-category']
        cases = str(skin['cases'])
        collections = str(skin['collections'])
        colors = str(skin['prominent-colors'])
        prices = str(skin['prices'])
        operation = skin['via-operation']
        year = skin['year']
        valve = skin['made-by-valve']
        text = skin['has-flavor-text']
        query = "INSERT INTO skins_data (id, url, url_id, weapon, skin_name, souvenir, stattrak, rarity, minwear, maxwear, finish, weapon_category, cases, collections, colors, prices, operation, year_added, by_valve, flavor_text) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor = conn.cursor()
        try:
            cursor.execute(query, (id, url, url_id, weapon, name, souvenir, stattrak, rarity, minwear, maxwear, finish, weapon_cat, cases, collections, colors, prices, operation, year, valve, text))
            conn.commit()
            print(f"✅ Added skin ID: {id})")
        except mysql.connector.Error as e:
            print(f"❌ Error inserting data: {e}")
    with open(constants.CRAWL_DATA_DIR, 'r') as file:
        conn = utils.connect_db()
        if conn:
            data = json.load(file)
            for entry in data:
                insert_data(conn=conn, skin=entry)
