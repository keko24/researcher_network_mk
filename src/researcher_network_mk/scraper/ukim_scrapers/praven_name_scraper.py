import os
import requests

import pandas as pd
from bs4 import BeautifulSoup

from researcher_network_mk.utils import get_project_root
from researcher_network_mk.transliteration import transliterate_cyrillic_to_latin

USERNAME = "bube12_dKwRX"
PASSWORD = "Researchscraper123"

def get_html_for_page(url):
    payload = {
        "url": url,
        "source": "universal",
    }
    response = requests.post(
        "https://realtime.oxylabs.io/v1/queries",
        auth=(USERNAME,PASSWORD),
        json=payload,
    )
    response.raise_for_status()
    return response.json()["results"][0]["content"]

def parse_data(researcher):
    anchor_elem = researcher.select("a")[0]
    researcher_name = " ".join(anchor_elem.get_text().strip("\n").split(" ")[1:])
    researcher_latin_name = researcher_name
    return researcher_latin_name

def parse_ass(researcher):
    anchor_elem = researcher.select("a")[0]
    researcher_name = " ".join(anchor_elem.get_text().strip("\n").split(", м-р ")[::-1])
    researcher_latin_name = researcher_name
    return researcher_latin_name

def parse_pen(idx, researcher):
    anchor_elem = researcher.select("a")
    if anchor_elem:
        anchor_elem = anchor_elem[0]
    else:
        anchor_elem = researcher.select("td")[1]
    researcher_name = anchor_elem.get_text().strip().strip("(").strip(")")
    if idx > 67:
        researcher_name = researcher_name.split(" ")[2:]
        researcher_name[0] = researcher_name[0][:-1]
        researcher_name = " ".join(researcher_name[::-1])
    elif idx < 62:
        if "проф. д-р " in researcher_name:
            researcher_name = " ".join(researcher_name.split(" ")[2:])
        else:
            researcher_name = " ".join(researcher_name.split(" ")[1:])
    elif idx == 62:
        researcher_name = " ".join(researcher_name.split(", проф д-р ")[::-1])
    elif idx == 67:
        researcher_name = " ".join(researcher_name.split(", д-р ")[::-1])
    else:
        researcher_name = " ".join(researcher_name.split(" ")[2:][::-1])
    researcher_latin_name = researcher_name
    return researcher_latin_name

def main():
    urls = ["https://pf.ukim.edu.mk/redovni-profesorin/", "https://pf.ukim.edu.mk/vonredni-profesorin/", "https://pf.ukim.edu.mk/doczenti/", "https://pf.ukim.edu.mk/asistenti/", "https://pf.ukim.edu.mk/penzionirani-profesori/"]
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim", "praven")
    data = []
    for i, url in enumerate(urls):
        html = get_html_for_page(url)
        soup = BeautifulSoup(html, "html.parser")
        if i == 4:
            content = soup.find("table", {"id": "supsystic-table-242"})
        else:
            content = soup.find("table", {"id": "supsystic-table-" + str(174 + i)})
        content = content.select("tbody")[0]
        staff = content.select("tr")
        if i == 4:
            data.extend([parse_pen(i, researcher) for i, researcher in enumerate(staff) if i != 0])
        elif i == 3:
            data.extend([parse_ass(researcher) for researcher in staff])
        else:
            data.extend([parse_data(researcher) for researcher in staff])
    os.makedirs(results_path, exist_ok=True)
    df = pd.DataFrame(data, columns=["name"])
    df["processed"] = False
    df.to_csv(os.path.join(results_path, "researchers.csv"))



if __name__ == "__main__":
    main()
