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
    researcher_name = anchor_elem.get_text().strip()
    researcher_latin_name = researcher_name
    if researcher_latin_name[:3] == "d-r" or researcher_latin_name[:3] == "m-r" :
        researcher_latin_name = researcher_latin_name[4:]
    if researcher_latin_name[:4] == "d-r." or researcher_latin_name[:4] == "m-r." :
        researcher_latin_name = researcher_latin_name[5:]
    return researcher_latin_name

def main():
    url = "https://finki.ukim.mk/mk/staff-list/kadar/nastaven-kadar"
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim", "finki")
    html = get_html_for_page(url)
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", {"class": "view-content"})
    staff = content.find_all("div", {"class": "node-teaser"})
    data = [parse_data(researcher) for researcher in staff]

    os.makedirs(results_path, exist_ok=True)
    df = pd.DataFrame(data, columns=["name"])
    df["processed"] = False
    df.to_csv(os.path.join(results_path, "researchers.csv"))


if __name__ == "__main__":
    main()
