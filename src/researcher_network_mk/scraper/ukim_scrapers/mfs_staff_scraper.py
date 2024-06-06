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
    researcher_name = " ".join(anchor_elem.get_text().strip("\n").split(" ")[::-1])
    researcher_latin_name = transliterate_cyrillic_to_latin(researcher_name)
    return researcher_latin_name

def main():
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim")
    data = []
    for i in range(16):
        url = f"https://mf.ukim.edu.mk/mk/academic-staff?page={i}" if i > 0 else "https://mf.ukim.edu.mk/mk/academic-staff"
        html = get_html_for_page(url)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"class": "view-academic-staff"})
        staff = content.find_all("span", {"class": "field-content"})
        page_data = [parse_data(researcher) for researcher in staff]
        data.extend(page_data)
    os.makedirs(results_path, exist_ok=True)
    pd.DataFrame(data, columns=["name"]).to_csv(os.path.join(results_path, "masinski.csv"))


if __name__ == "__main__":
    main()
