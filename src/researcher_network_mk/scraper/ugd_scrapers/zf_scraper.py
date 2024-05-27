import os
import requests

import pandas as pd
from bs4 import BeautifulSoup
from transliterate import translit

from researcher_network_mk.utils import get_project_root

USERNAME = "bube123" 
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

def get_table(content):
    return content.select("tr")[1]

def main():
    url = "https://scholar.ugd.edu.mk/fakulteti/zf"
    results_path = os.path.join(get_project_root(), "data", "researchers", "feit")
    html = get_html_for_page(url)
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", {"id": "page"})
    content = content.find("div", {"id": "content-column"})
    content = content.find("div", {"class": "field-items"})
    content = content.select("iframe")[0]
    content = content.find_all("div", {"class": "celo"})
    tables = [cnt.select("a")[1] for cnt in content]
    staff = [researcher for table in tables for researcher in table.select("p")]
    data = [parse_data(researcher) for researcher in staff]
    print(data)
    # if os.path.exists(results_path):
    #     os.makedirs(results_path)
    # pd.DataFrame(data, columns=["name"]).to_csv(os.path.join(results_path, "researchers.csv"))

if __name__ == "__main__":
    main()
