import os
import requests

import pandas as pd
from bs4 import BeautifulSoup
from transliterate import translit
from selenium import webdriver
from selenium.webdriver.common.by import By

from researcher_network_mk.utils import get_project_root

USERNAME = "bube123" 
PASSWORD = "Researchscraper123"

def parse_text(text):
    if " / " in text:
        return text.split(" / ")[1]
    elif "/" in text:
        return text.split("/")[1]
    else:
        return translit(text, 'mk', reversed=True)


def main():
    data = []
    faculties = ["ekonomski-fakultet", "pedagoski-fakultet", "praven-fakultet", "fakultet-za-biznis-administracija", "fakultet-za-zemjodelstvo-i-biotehnologija", "fakultet-za-medicinski-nauki", "fakultet-za-prehranbrena-tehnologija-i-ishrana", "fakultet-za-primeneti-nauki", "fakultet-za-prirodno-matematicki-nauki", "fakultet-za-umetnosti", "fakultet-za-fizicka-kultura", "filozofski-fakultet", "filoloski-fakultet"]
    url = "https://unite.edu.mk/mk/faculty/"
    driver = webdriver.Firefox()
    for faculty in faculties:
        print(faculty)
        driver.get(url + faculty)
        driver.find_element(By.ID, "fusion-tab-Академскикадар").click()
        row = driver.find_elements(By.CLASS_NAME, "container")[1]
        elems = row.find_elements(By.CLASS_NAME, 'col-md-3')
        for elem in elems:
            try:
                text = elem.find_element(By.XPATH, ".//child::a")
            except:
                continue
            text = text.get_attribute("text")
            if '@' in text:
                text = " ".join(elem.get_attribute("innerHTML").split('\n')[1].strip("<br>").split(" ")[3:])
            data.append(text)
            print(text)


if __name__ == "__main__":
    main()
