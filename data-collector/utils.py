from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import xml.etree.ElementTree as ET
from selenium.webdriver.support.ui import WebDriverWait
import re
import os

RARITIES = [
    "Consumer Grade",
    "Industrial Grade",
    "Mil-Spec",
    "Restricted",
    "Classified",
    "Covert",
    "Contraband"
]

WEAPON_CATEGORIES = [
    "Pistol",
    "SMG",
    "Shotgun",
    "Machine Gun",
    "Sniper Rifle", # ❗❗❗❗ Important that this is before "Rifle", so that the matching works!
    "Rifle",
    "Knife",
    "Equipment",
]

'''
Returns match of a category

Params:
text = scraped text
cats = list of categories
If None, that means no match was found
'''

def locateCategory(text, cats):
    for item in cats:
        if item in text:
            return item
    return None


def getRarity(text):
    i = locateCategory(text, RARITIES)
    if i is None:
        raise ValueError("No match found for the following rarity: ", text)
    return i

def getWeaponCategory(text):
    w = locateCategory(text, WEAPON_CATEGORIES)
    if w is None:
        raise ValueError("No match found for the following weapon category", text)
    return w
    
'''
Grab all URLS from the sitemap XML.
'''
def getAllUrls():
    URL = "https://stash.clash.gg/sitemap.xml"
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    driver.get(URL)
    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    xml = driver.page_source
    file_name = "data-collector/temp-sitemap.xml"

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(xml)
    driver.quit()

    tree = ET.parse(file_name)
    root = tree.getroot()
    namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    all_urls = [url.find("ns:loc", namespace).text for url in root.findall("ns:url", namespace)]
    os.remove(file_name)
    return all_urls


def extractYear(text):
    # Regular expression to match dates in the format "day month year"
    date_pattern = r'\b\d{1,2} \w+ (\d{4})\b'
    match = re.search(date_pattern, text)
    if match:
        return match.group(1)  # Return the captured year
    return None  # Return None if no date is found