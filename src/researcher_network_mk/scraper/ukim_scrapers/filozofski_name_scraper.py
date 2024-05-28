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
    return translit(text, 'mk', reversed=True)


def main():
    data = [] 
    url = "http://fzf.ukim.edu.mk"
    paths = ["институт-за-филозофија", "институт-за-историја", "инзтитут-за-педагогија", "институт-за-класични-студии", "институт-за-историја-на-уметноста-и-ар", "институт-за-социологија", "институт-за-психологија", "институт-за-безбедност-одбрана-и-мир", "институт-за-социјална-работа-и-соција", "институт-за-специјална-едукација-и-ре", "институт-за-родови-студии", "институт-за-семејни-студии"]
    url = "http://www.ff.ukim.edu.mk/наставно-научен-и-соработнички-кадар/"
    useragentarray = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", 
    driver = webdriver.Firefox()
    for path in paths:
        driver.get(url + path)
        content = driver.find_element(By.ID, 'content')
        elems = content.find_elements(By.CLASS_NAME, 'tg-facultyname')
        for elem in elems:
            text = elem.find_element(By.XPATH, ".//child::a").get_attribute("text")
            text = parse_text(elem.text)
            print(text)
            data.append(text)

if __name__ == "__main__":
    main()
