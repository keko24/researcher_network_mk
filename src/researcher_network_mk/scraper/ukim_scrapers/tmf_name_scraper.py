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
    researcher_name = researcher.get_text()
    researcher_name = researcher_name.replace(u'\xa0', u' ')
    if "М-р" in researcher_name or "Д-р" in researcher_name:
        researcher_name = " ".join(" ".join(researcher_name.split(" ")[1:]).split(", ")[:1])
    else:
        researcher_name = " ".join(" ".join(researcher_name.split(" ")).split(", ")[:1])
    researcher_latin_name = transliterate_cyrillic_to_latin(researcher_name)
    return researcher_latin_name

def main():
    url = "https://www.tmf.ukim.edu.mk/"
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim")
    data = []
    paths = ["редовни-професори", "вонредни-професори", "доценти", "асистенти", "лаборанти", "пензионирани-професори"]
    for i, path in enumerate(paths):
        html = get_html_for_page(url + path)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"id": "page-main-content"})
        staff = content.find_all("p", {"class": "has-black-color has-text-color"})
        data.extend([parse_data(researcher) for researcher in staff])

    os.makedirs(results_path, exist_ok=True)
    pd.DataFrame(data, columns=["name"]).to_csv(os.path.join(results_path, "tehnoloski.csv"))

if __name__ == "__main__":
    main()
