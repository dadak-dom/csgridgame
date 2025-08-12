'''
The purpose of this data-collector is as follows:
1. Scrape necessary data from each skin in the game
2. Organize the data in a way that makes sense
3. Store that data; 

'''

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by  import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from urllib.request import urlretrieve
from collections import Counter
from PIL import Image
from time import sleep
from random import randint
import xml.etree.ElementTree as ET
import datetime
import json
import utils
import logging
# import colors
import os

logging.basicConfig(level=logging.DEBUG)

# Gather all possible URLS on the site.
# TO-DO: Make it so that the script automatically pulls the sitemap, in case the site gets updated.
# tree = ET.parse("data-collector/sitemap.xml")
# root = tree.getroot()
# namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
# all_urls = [url.find("ns:loc", namespace).text for url in root.findall("ns:url", namespace)]# driver = webdriver.Chrome()

# Choose only urls with 'skin' in it
'''
Information of importance for each skin:
    Weapon
    Weapon Category!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ADD THIS, should be doable via the cleanRarity function
    Skin name
    Rarity
    Souvenir available?
    StatTrak available?
    Minimum float
    Maximum float
    Finish style
    Case (if applicable, which one?) (Note: knives can be found in more than 1 case oftentimes. Will need a system for that)
    Collection (if applicable)
    Download the image of the skin; will be good for the frontend, and also can extract colors from it
    Price data (can make a bunch of categories out of this)
    Added via operation? (true/false)
    Year added
    Created by Valve? (true/false)
    Does it have flavor text?

'''

test_urls = [
    "https://stash.clash.gg/skin/1533/AWP-Chromatic-Aberration",
    "https://stash.clash.gg/skin/1525/M249-Downtown",
    "https://stash.clash.gg/skin/82/AK-47-Case-Hardened",
    "https://stash.clash.gg/skin/232/MP9-Rose-Iron",
    "https://stash.clash.gg/skin/13/MP9-Bulldozer",
    "https://stash.clash.gg/skin/690/R8-Revolver-Bone-Mask",
    "https://stash.clash.gg/skin/61/AK-47-Predator",
    "https://stash.clash.gg/skin/475/XM1014-Red-Python",
    "https://stash.clash.gg/skin/1624/Glock-18-Gold-Toof",
    "https://stash.clash.gg/skin/887/AK-47-Orbit-Mk01",
    "https://stash.clash.gg/skin/549/Karambit-Marble-Fade",
    "https://stash.clash.gg/skin/1600/Kukri-Knife-Vanilla",
    "https://stash.clash.gg/skin/289/Flip-Knife-Vanilla",
    "https://stash.clash.gg/skin/60/AK-47-Jungle-Spray",
]

DATA_DIR = "./data-collector/data"
IMAGE_DIR = os.path.join(DATA_DIR, "/images")

# FOR SOME REASON, IT CAN'T FIND THE FUCKING FIREFOX EXEC
def runCrawl(browser="firefox", skip_id=0):
    os.umask(0)
    os.makedirs(DATA_DIR, exist_ok=True, mode=0o777)

    service = Service("/snap/bin/firefox.geckodriver", port=0)
    if browser == "firefox":
        driver = webdriver.Firefox(service=service)
    elif browser == "chrome":
        logging.info("Running Chrome driver...")
        driver = webdriver.Chrome()
    id_number = 0
    all_skins, skin_urls = [], []

    logging.debug("TEST")
    all_urls = utils.getAllUrls(browser=browser)
    # all_urls = test_urls
    for url in all_urls:
        if "/skin/" in url:
            skin_urls.append(url)
    # all_urls = utils.getAllUrls()
    # all_urls = test_urls # For testing purposes
    # skin_urls = test_urls
    # print(skin_urls)
    logging.debug(skin_urls)
    try:
        for url in skin_urls:
            if id_number < skip_id:
                id_number += 1
                continue
            # For each skin URL, create a dictionary that represents the skin (Maybe give the skin an ID or something?)
            skin = {'id': id_number}
            skin["url"] = url
            skin["url_id"] = url.split('/')[4]
            # skin["url_id"] = url.split('/')[]

            # Navigate to the page
            driver.get(url)
            sleep(randint(5, 8))

            # Grab skin info
            skin_info = driver.find_element(By.CSS_SELECTOR, ".skin-misc-details")
            # Check the name and weapon...
            skin["weapon"] = driver.find_element(By.CSS_SELECTOR, "div.well:nth-child(1) > h1:nth-child(1) > a:nth-child(1)").text
            skin["name"] = driver.find_element(By.CSS_SELECTOR, "div.well:nth-child(1) > h1:nth-child(1) > a:nth-child(2)").text
            # Check if stattrack or souvenir is available
            if "Souvenir Available" in driver.page_source:
                skin["souvenir"] = True
            else:
                skin["souvenir"] = False
            if "StatTrak Available" in driver.page_source:
                skin["stattrak"] = True
            else:
                skin["stattrak"] = False

            # Get the rarity
            skin["rarity"] = utils.getRarity(driver.find_element(By.CSS_SELECTOR, ".quality > p:nth-child(1)").text)

            # Check the min and max wear values
            if ("★" not in skin["name"]) and ("Vanilla" not in url):
                skin["minwear"] = driver.find_element(By.CSS_SELECTOR, 'div.marker-wrapper:nth-child(1)').get_attribute("data-wearmin")
                skin["maxwear"] = driver.find_element(By.CSS_SELECTOR, 'div.marker-wrapper:nth-child(2)').get_attribute("data-wearmax")

                # Get finish style
                style = driver.find_element(By.XPATH, "//strong[text()='Finish Style:']/parent::p/span")
                skin["finish-style"] = style.text
            else:
                # In this case, min, max, and finish don't apply to Vanilla knives
                skin["minwear"] = None
                skin["maxwear"] = None
                skin["finish-style"] = None

            # Get weapon category
            skin["weapon-category"] = utils.getWeaponCategory(driver.find_element(By.CSS_SELECTOR, ".quality > p:nth-child(1)").text)

            # Get cases
            # driver.find_element(By.CSS_SELECTOR, "#knife-cases-collapse")
            try:
                driver.find_element(By.CSS_SELECTOR, ".cl-popup-close").click()
                sleep(1)
            except NoSuchElementException as e:
                logging.info(e)
            except ElementNotInteractableException as e:
                logging.info("No popup @", url)
            try:
                driver.find_element(By.CSS_SELECTOR, ".collapse-chevron").click()
                sleep(2)
            except NoSuchElementException as e:
                # logging.info("No case-collapse button @", url)
                print("No case-collapse button @", url)
            casesAndCollections = driver.find_elements(By.CLASS_NAME, "collection-text-label")
            cases, collections, prominent_colors = [], [], []
            for el in casesAndCollections:
                if "Case" in el.text:
                    cases.append(el.text)
                elif "Collection" in el.text:
                    collections.append(el.text)
            skin["cases"] = cases
            skin["collections"] = collections

            # Download the image
            img = driver.find_element(By.CSS_SELECTOR, ".main-skin-img")
            src = img.get_attribute("src")
            if url != 'https://stash.clash.gg/skin/1609/USP-S-027':
                file_end = str(skin['url_id']) + '-' + skin["weapon"] + " " + skin["name"] + '.png'
            else:
                continue
            # os.makedirs(IMAGE_DIR, exist_ok=True, mode=0o777) # Make sure the data/images folder exists, create the images folder if it doesn't
            # TODO: Make a script that will create all necessary directories for the crawler
            urlretrieve(src, 'data-collector/data/images/' + file_end)
            # Get the prominent colors
            skin["prominent-colors"] = ['TO BE REPLACED BY MANUAL LABELING'] #  colors.getProminentColors('data-collector/data/images/' + file_end)

            # Get price data
            prices = {}
            dom_prices = driver.find_element(By.ID, "prices")
            for price_row in dom_prices.find_elements(By.CSS_SELECTOR, ".btn-group-sm.btn-group-justified"):
                # Check if a valid row
                condition = price_row.find_elements(By.CSS_SELECTOR, ".pull-left")
                if len(condition) < 1:
                    continue
                condition_text = ""
                for c in condition:
                    if c.text == "Souvenir" or c.text == "StatTrak":
                        continue
                    else:
                        condition_text = c.text
                stat_price = price_row.find_elements(By.CSS_SELECTOR, ".price-details-st")
                souv_price = price_row.find_elements(By.CSS_SELECTOR, ".price-details-souv")
                price = price_row.find_element(By.CSS_SELECTOR, ".pull-right").text
                if "$" in price:
                    price = float(price.split("$")[1].replace(",", ""))
                else:
                    price = None
                if len(stat_price) == 1:
                    prices[stat_price[0].text + " " + condition_text] = price
                elif len(souv_price) == 1:
                    prices[souv_price[0].text + " " + condition_text] = price
                else:
                    prices[condition_text] = price
            skin["prices"] = prices

            # Check if added via operation
            operation = driver.find_elements(By.PARTIAL_LINK_TEXT, "Operation")
            if len(operation) > 0:
                skin["via-operation"] = True
            else:
                skin["via-operation"] = False

            # Check year added
            # skin["year"] = int(driver.find_element(By.CSS_SELECTOR, ".skin-misc-details > p:nth-child(6) > span:nth-child(2)").text.split(" ")[2])
            skin["year"] = int(utils.extractYear(skin_info.text))
            
            # Check if made by Valve
            '''
            NOTE: Some skins don't seem to have the 'Creator' row on their page. 
            I'm going to leave it like this for now, where if a page doesn't have it, we assume that it wasn't made by Valve.
            Maybe that will bite me in the ass later.
            I added a Bandaid solution where marked with a devil emoji (😈)
            '''
            skin["made-by-valve"] = "Valve" in skin_info.text

            # Check if it has flavor text
            body = driver.find_element(By.TAG_NAME, "body").text
            skin["has-flavor-text"] = "Flavor Text:" in body

            # Once you have all the data, place the skin into a list
            all_skins.append(skin)
            # Write out the list to save progress
            with open("./data-collector/data/skins_temp_data.json", "w") as json_file:
                json.dump(all_skins, json_file, indent=4)
            # Update the ID
            id_number += 1
    except: 
        logging.error("Something has gone wrong")
    finally:
        # When the crawler stops, write out to a file
        with open("./data-collector/data/skins_data" + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + ".json", "w") as json_file:
                json.dump(all_skins, json_file, indent=4)
        driver.quit()

# Note: Skipping USPS | 027, seems to be broken (id 1566)

if __name__ == '__main__':
    # runCrawl(browser="chrome", skip_id=1567)
    # runCrawl(browser="chrome", skip_id=938)
    runCrawl(browser="chrome", skip_id=991)
    # runCrawl(browser="chrome", skip_id=0)