Install backend deps with

`pip install -r csgridgame/data-collector/requirements.txt`

If I need to add dependencies to the backend, install them normally with pip, then update the requirements file with `pip freeze > requirements.txt`

- Note: I have the .venv file in the same level as csgridgame

Run frontend with (from within the `gridgame` directory):

`npm run dev`

- note: if selenium isn't working, try installing chromedriver. Make sure you have whatever browser you need, i.e.
  `chromedriver --version`
  or
  `geckodriver --version`

## Server / Database Notes

I already made a function for importing all crawler JSON data into the database, it's called `importCrawlData` in gridgen.py

# TO-DO NOTES

- Make sure that I have an easy script to set up a production-ready DB
