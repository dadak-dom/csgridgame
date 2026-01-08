# CSGridGame
<img width="562" height="666" alt="image" src="https://github.com/user-attachments/assets/167df38a-bf21-4bc2-9859-48f5ca8aa2c7" />

## What is this?

This is code for running my trivia game, inspired by the Immaculate Grid format.

## How do I play?

This game is a test of the player's knowledge of in-game items in the popular game [Counter-Strike 2](https://www.counter-strike.net/home). The goal of the game is to score as many points on a board as possible. Points are earned by correctly guessing an item that matches both the row and the column category. Most cells will have more than one correct answer; therefore, extra points are awarded for guessing the more expensive answers to a question. The order of points gained, from most to least, is as follows:

💛 -> ❤️ -> 🩷 -> 💜 -> 💙 -> 🩵 -> 🩶

## What technologies were used?

### Data Collection

- Selenium + Python

### Frontend

- Vite + VueJS

### Backend

- MySQL Database
- Python FastAPI

### Deployment

- Nginx
- Docker
- AWS ECS

## Running Locally
### Backend
1. Install backend dependencies with

`pip install -r csgridgame/backend/requirements.txt`

Note: if you need to add dependencies to the backend, install them normally with pip, then update the requirements file with `pip freeze > requirements.txt`

2. Ensure you have a [MySQL](https://www.mysql.com/) database running on your machine. Import the tables found in the `db/exported_db.sql` file. This file contains the information necessary to create the game boards.

3. Create `.env` file within the /backend/ directory
The file should contain the following:
`DB_HOST=location_of_mysql_db (e.g., localhost)
DB_USER=your_mysql_user
DB_PASS=your_mysql_password
DB_NAME=your_db_name
SKINSAPI_TEST_PASS=your_testing_password
`

4. You should now be able to run the backend using `fastapi dev src/main.py`

### Frontend
1. Change your directory to `csgridgame/gridgame`
2. Install dependencies with `npm i`
3. Create .env file that contains the variable `VITE_GRIDGAME_SERVER_URL`. If running locally, use this value: `VITE_GRIDGAME_SERVER_URL=http://localhost:8000/`
4. Run the frontend with `npm run dev`

## Known Issues

- if selenium isn't working when running the data-collector, try installing chromedriver. Make sure you have whatever browser you need, i.e.
  `chromedriver --version`
  or
  `geckodriver --version`
