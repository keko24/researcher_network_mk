import os

import requests
import pandas as pd
from bs4 import BeautifulSoup
from transliterate import translit
from researcher_network_mk.utils import get_project_root

USERNAME = "andykot24" 
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
    researcher_latin_name = translit(researcher_name, 'mk', reversed=True)
    return researcher_latin_name

def main():
    url = "https://feit.ukim.edu.mk/staff/"
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim")
    html = get_html_for_page(url)
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", {"id": "content"})
    staff = content.find_all("div", {"class": "staffArchiveProfessor"})
    data = [parse_data(researcher) for researcher in staff]

    os.makedirs(results_path, exist_ok=True)
    pd.DataFrame(data, columns=["name"]).to_csv(os.path.join(results_path, "feit.csv"))

if __name__ == "__main__":
    main()
