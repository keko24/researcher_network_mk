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
    anchor_elem = researcher.select("a")[0].get_text()
    if "Науч. " in anchor_elem:
        researcher_name = " ".join(anchor_elem.strip("\n").strip("\t").split(" ")[3:])
    elif "Проф " in anchor_elem or "Проф. " in anchor_elem or "проф. " in anchor_elem or "Виш" in anchor_elem or "ас." in anchor_elem:
        researcher_name = " ".join(anchor_elem.strip("\n").strip("\t").split(" ")[2:])
    else:
        researcher_name = " ".join(anchor_elem.strip("\n").strip("\t").split(" ")[1:])
    researcher_latin_name = researcher_name
    return researcher_latin_name

def main():
    urls = ["https://stomfak.ukim.edu.mk/кадар/наставно-научен-кадар", "https://stomfak.ukim.edu.mk/кадар/научен-кадар", "https://stomfak.ukim.edu.mk/кадар/соработнички-кадар"]
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim", "stomatoloski")
    data = []
    for url in urls:
        html = get_html_for_page(url)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find_all("div", {"class": "elementor-container"})
        content = content[len(content) - 1]
        staff = content.find_all("div", {"class": "elementor-post__text"})
        data.extend([parse_data(researcher) for researcher in staff])

    os.makedirs(results_path, exist_ok=True)
    df = pd.DataFrame(data, columns=["name"])
    df["processed"] = False
    df.to_csv(os.path.join(results_path, "researchers.csv"))


if __name__ == "__main__":
    main()
