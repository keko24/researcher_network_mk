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
    anchor_elem = researcher.select("a")
    if anchor_elem:
        anchor_elem = anchor_elem[0]
    else:
        anchor_elem = researcher.select("span")[0]
    researcher_name = anchor_elem.get_text().strip("\n")
    if "Prof. " in researcher_name:
        researcher_name = " ".join(researcher_name.split(" ")[1:-1])
    else:
        researcher_name = " ".join(researcher_name.split(" ")[:-2])
    return researcher_name

def main(): 
    url = "http://www.arh.ukim.edu.mk/index.php/en/structure/people"
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim")
    html = get_html_for_page(url)
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", {"class": "item-page"})
    staff = content.select("p")
    
    data = [parse_data(researcher) for i, researcher in enumerate(staff) if (i != 0 and i < 28) or (i >= 31 and i < 32)]
    os.makedirs(results_path, exist_ok=True)
    pd.DataFrame(data, columns=["name"]).to_csv(os.path.join(results_path, "arhitektonski.csv"))


if __name__ == "__main__":
    main()
