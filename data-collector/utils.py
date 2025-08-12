from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import xml.etree.ElementTree as ET
from selenium.webdriver.support.ui import WebDriverWait
import re
import os
import logging
from bs4 import BeautifulSoup
import requests
import advertools as adv

logging.basicConfig(level=logging.DEBUG)

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
def getAllUrls(browser="firefox"):

    # def getUrlsOfXml(xml_url):
    #     r = requests.get(xml_url)
    #     xml = r.text
    #     soup = BeautifulSoup(xml)

    #     links_arr = []
    #     for link in soup.findAll('loc'):
    #         linkstr = link.getText('', True)
    #         links_arr.append(linkstr)

    #     return links_arr

    # URL = "https://stash.clash.gg/sitemap.xml"
    URL = "https://stash.clash.gg/sitemaps/skins.xml"

    options = Options()
    

    logging.debug(f"BROWSER={browser}")
    
    if browser == "firefox":
        driver = webdriver.Firefox(options=options, service=Service("/snap/bin/firefox.geckodriver", port=0))
        options.add_argument('-headless')
        logging.debug("Running firefox crawler...")
    elif browser == "chrome":
        logging.info("Running Chrome crawler for sitemap...")
        driver = webdriver.Chrome()
        options.add_argument('--headless')
        logging.debug("Running chrome crawler...")

    # driver = webdriver.Firefox(options=options)
    driver.get(URL)
    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    xml = driver.page_source
    file_name = "data-collector/temp-sitemap.xml"

    # Get rid of the extra HTML and CSS that is throwing off the rest of the code:
    # Find the first instance of "urlset", go back one, and then take the rest of the file
    starting_point = xml.find('<urlset')
    # Magic number '9' because that's the length of </urlset>
    ending_point = xml.find('</urlset>') + 9
    xml = xml[starting_point:ending_point]

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(xml)
    driver.quit()

    tree = ET.parse(file_name)
    root = tree.getroot()
    namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    all_urls = [url.find("ns:loc", namespace).text for url in root.findall("ns:url", namespace)]

    # all_urls = getUrlsOfXml(URL)

    os.remove(file_name)
    return all_urls


def extractYear(text):
    # Regular expression to match dates in the format "day month year"
    date_pattern = r'\b\d{1,2} \w+ (\d{4})\b'
    match = re.search(date_pattern, text)
    if match:
        return match.group(1)  # Return the captured year
    return None  # Return None if no date is found