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
    anchor_elem = researcher.select("p")[0]
    researcher_name = " ".join(anchor_elem.get_text().split("\n")[0].split(" ")[2:])
    researcher_latin_name = transliterate_cyrillic_to_latin(researcher_name)
    return researcher_latin_name

def main():
    urls = ["https://eccfp.uklo.edu.mk/za-fakultetot/osnovni-informacii/kadar/redovni-profesori/", "https://eccfp.uklo.edu.mk/za-fakultetot/osnovni-informacii/kadar/vonredni-profesori/", "https://eccfp.uklo.edu.mk/za-fakultetot/osnovni-informacii/kadar/docenti/", "https://eccfp.uklo.edu.mk/za-fakultetot/osnovni-informacii/kadar/asistenti/", "https://eccfp.uklo.edu.mk/za-fakultetot/osnovni-informacii/kadar/penzioniraniprofesori/"]
    data = []
    results_path = os.path.join(get_project_root(), "data", "researchers", "uklo")
    for url in urls:
        html = get_html_for_page(url)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"class": "post-content"})
        staff = content.find_all("div", {"class": "fusion-text"})
        data.extend([parse_data(researcher) for researcher in staff])
    os.makedirs(results_path, exist_ok=True)
    pd.DataFrame(data, columns=["name"]).to_csv(os.path.join(results_path, "ekonomski.csv"))

if __name__ == "__main__":
    main()
