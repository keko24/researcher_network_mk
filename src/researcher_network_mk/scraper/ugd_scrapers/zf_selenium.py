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
    faculties = {"zf": "zemjodelski", "ef": "ekonomski", "pf": "praven", "fon": "obrazovni_nauki", "fmn": "medicinski", "ff": "filoloski", "etf": "elektro", "inf": "informatika", "ma": "muzicko", "fa": "filmska", "la": "likovno", "va": "voena", "mf": "masinski", "ttf": "tehnoloski", "fptn": "prirodno_tehnicki", "ftbl": "turizam", "filip-vtori": "filip_vtori"}
    data = {} 
    url = "https://scholar.ugd.edu.mk/fakulteti/"
    driver = webdriver.Firefox()
    for faculty in faculties.keys():
        print(f"Currently accessing {faculties[faculty]}.")
        data[faculty] = []
        driver.get(url + faculty)
        frame = driver.find_element(By.XPATH, "//iframe")
        driver.switch_to.frame(frame)
        elem = driver.find_elements(By.CLASS_NAME, 'celo')
        for i in range(len(elem)):
            elems = elem[i].find_elements(By.XPATH, ".//child::tr")
            elems = elems[1].find_elements(By.XPATH, ".//child::td")
            for j in range(len(elems)):
                ps = elems[j].find_elements(By.XPATH, ".//child::p")
                for k in range(len(ps)):
                    text = ps[k].find_element(By.XPATH, ".//child::a").get_attribute("text")
                    text = parse_text(text)
                    data[faculty].append(text)
                    print(text)
    for faculty in data.keys():
        results_path = os.path.join(get_project_root(), "data", "researchers", "ugd")
        os.makedirs(results_path, exist_ok=True)
        pd.DataFrame(data[faculty], columns=["name"]).to_csv(os.path.join(results_path, f"{faculties[faculty]}.csv"))

if __name__ == "__main__":
    main()
