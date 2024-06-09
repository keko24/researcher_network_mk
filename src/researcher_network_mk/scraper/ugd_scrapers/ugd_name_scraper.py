import os
import re

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

from researcher_network_mk.utils import get_project_root
from researcher_network_mk.transliteration import transliterate_cyrillic_to_latin

def clean_specific_people(text):
    if "Жан Митрев" in text:
        return "Жан Митрев"
    if "Сашо Стојковиќ" in text:
        return "Сашо Стојковиќ"
    if "Лилјана Илиевска" in text:
        return "Лилјана Илиевска"
    if "Надица Негриевска (Маркоска)" in text:
        return "Надица Негриевска Маркоска"
    return text

def parse_text(text):
    text = clean_specific_people(text)
    if " / " in text:
        text = text.split(" / ")
        if bool(re.search('[а-яА-Я]', text[0])):
            text = text[0]
        else:
            text = text[1]
    elif "/" in text:
        text = text.split("/")
        if bool(re.search('[а-яА-Я]', text[0])):
            text = text[0]
        else:
            text = text[1]
    return text

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
    results_path = os.path.join(get_project_root(), "data", "researchers", "ugd")
    os.makedirs(results_path, exist_ok=True)
    for faculty in data.keys():
        os.makedirs(os.path.join(results_path, faculties[faculty]), exist_ok=True)
        df = pd.DataFrame(data[faculty], columns=["name"])
        df["processed"] = False
        df.to_csv(os.path.join(results_path, faculties[faculty], "researchers.csv"))

if __name__ == "__main__":
    main()
