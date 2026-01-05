# CSGridGame

## What is this?

This is code for running my trivia game, inspired by the Immaculate Grid format.

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

Install backend deps with

`pip install -r csgridgame/data-collector/requirements.txt`

If you need to add dependencies to the backend, install them normally with pip, then update the requirements file with `pip freeze > requirements.txt`

- Note: Python .venv file in the same directory level as csgridgame (outermost folder)

Run frontend with (from within the `gridgame` directory):

`npm run dev`

- note: if selenium isn't working, try installing chromedriver. Make sure you have whatever browser you need, i.e.
  `chromedriver --version`
  or
  `geckodriver --version`
