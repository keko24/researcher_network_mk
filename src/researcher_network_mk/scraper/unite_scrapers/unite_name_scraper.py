import os

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

from researcher_network_mk.transliteration import \
    transliterate_cyrillic_to_latin
from researcher_network_mk.utils import get_project_root


def parse_text(text):
    if " / " in text:
        text = text.split(" / ")[1]
    elif "/" in text:
        text = text.split("/")[1]
    return text

def main():
    faculties = ["ekonomski-fakultet", "pedagoski-fakultet", "praven-fakultet", "fakultet-za-biznis-administracija", "fakultet-za-zemjodelstvo-i-biotehnologija", "fakultet-za-medicinski-nauki", "fakultet-za-prehranbrena-tehnologija-i-ishrana", "fakultet-za-primeneti-nauki", "fakultet-za-prirodno-matematicki-nauki", "fakultet-za-umetnosti", "fakultet-za-fizicka-kultura", "filozofski-fakultet", "filoloski-fakultet"]
    url = "https://unite.edu.mk/mk/faculty/"
    driver = webdriver.Firefox()
    results_path = os.path.join(get_project_root(), "data", "researchers", "unite")
    os.makedirs(results_path, exist_ok=True)
    for faculty in faculties:
        print(faculty)
        data = []
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
            text = parse_text(text)
            data.append(text)
        faculty_path = os.path.join(results_path, faculty)
        os.makedirs(faculty_path, exist_ok=True)
        df = pd.DataFrame(data, columns=["name"])
        df["processed"] = False
        df["found"] = False
        df.to_csv(os.path.join(faculty_path, "researchers.csv"))

if __name__ == "__main__":
    main()
