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

def parse_data(researcher, last):
    researcher_name = researcher.get_text().replace(u'\xa0', u' ')
    if last:
        researcher_name = researcher_name[:len(researcher_name) - 14]
    if "д-р " not in researcher_name:
        researcher_name = researcher_name.strip("\t").split("д-р")[1]
    else:
        researcher_name = researcher_name.strip("\t").split("д-р ")[1]
    researcher_latin_name = researcher_name
    return researcher_latin_name

def main():
    url = "https://pfsko.ukim.edu.mk/nastaven-kadar/"
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim", "pedagoski")
    html = get_html_for_page(url)
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("main", {"id": "content"})
    staff = content.find_all("h3", {"class": "module-feature-title"})
    data = [parse_data(researcher, i == len(staff) - 1) for i, researcher in enumerate(staff)]

    os.makedirs(results_path, exist_ok=True)
    df = pd.DataFrame(data, columns=["name"])
    df["processed"] = False
    df.to_csv(os.path.join(results_path, "researchers.csv"))



if __name__ == "__main__":
    main()
