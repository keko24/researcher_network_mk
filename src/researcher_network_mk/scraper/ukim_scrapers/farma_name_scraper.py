import os
import requests
import time

import pandas as pd
from bs4 import BeautifulSoup
from transliterate import translit
from selenium import webdriver
from selenium.webdriver.common.by import By

from researcher_network_mk.utils import get_project_root

USERNAME = "bube123" 
PASSWORD = "Researchscraper123"

def parse_text(text):
    if "Ас." in text:
        text = " ".join(text.split(" ")[1:])
    else:
        text = " ".join(text.split(" ")[2:])
    return translit(text, 'mk', reversed=True)


def main():
    data = [] 
    url = "http://www.ff.ukim.edu.mk/наставно-научен-и-соработнички-кадар/"
    driver = webdriver.Firefox()
    driver.get(url)
    faculties = ["elementor-tab-title-5102", "elementor-tab-title-5103", "elementor-tab-title-5104", "elementor-tab-title-5105", "elementor-tab-title-5101"]
    for faculty in faculties:
        elems = driver.find_elements(By.CLASS_NAME, 'elementor-image-box-title')
        for elem in elems:
            text = parse_text(elem.text)
            if text:
                print(text)
            data.append(text)
        driver.find_element(By.ID, faculty).click()

if __name__ == "__main__":
    main()
