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

def parse_data(i, researcher):
    anchor_elem = researcher.select("p")
    if i > 22: 
        anchor_elem = anchor_elem[0].get_text().replace(u'\xa0', u' ')
    else:
        anchor_elem = anchor_elem[len(anchor_elem) - 1].get_text().replace(u'\xa0', u' ')
    if "м-р" in anchor_elem or "Дип.инж" in anchor_elem:
        researcher_name = " ".join(anchor_elem.split("\n")[0].split(" ")[1:])
    elif "д-р" in anchor_elem or "Д-р" in anchor_elem:
        researcher_name = " ".join(anchor_elem.split("\n")[0].split(" ")[2:])
    else:
        researcher_name = " ".join(anchor_elem.split("\n")[0].split(" ")[:])
    researcher_latin_name = researcher_name
    return researcher_latin_name

def main():
    urls = ["https://pfbt.uklo.edu.mk/академски-кадар"]
    results_path = os.path.join(get_project_root(), "data", "researchers", "uklo", "pedagoski")
    data = []
    for url in urls:
        html = get_html_for_page(url)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"class": "post-content"})
        staff = content.find_all("div", {"class": "fusion-text"})
        data.extend([parse_data(i, researcher) for i, researcher in enumerate(staff) if i != 0])
    os.makedirs(results_path, exist_ok=True)
    df = pd.DataFrame(data, columns=["name"])
    df["processed"] = False
    df.to_csv(os.path.join(results_path, "researchers.csv"))


if __name__ == "__main__":
    main()
