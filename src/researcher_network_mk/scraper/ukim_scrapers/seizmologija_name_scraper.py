import os

import pandas as pd
import requests
from bs4 import BeautifulSoup

from researcher_network_mk.utils import get_project_root

USERNAME = "bube12_elDr7"
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
    researcher_name = researcher.select("td")[1].select("p")[0].get_text()
    researcher_latin_name = researcher_name
    return researcher_latin_name.strip()

def main():
    urls = ["https://seismobsko.pmf.ukim.edu.mk/chronologicalpersonnel"]
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim", "seizmologija")
    data = []
    for url in urls:
        html = get_html_for_page(url)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"class": "col-md-8"})
        content = content.select("table")[0]
        staff = content.select("tr")
        data.extend([parse_data(researcher) for researcher in staff[1:]])
        
    os.makedirs(results_path, exist_ok=True)
    df = pd.DataFrame(data, columns=["name"])
    df["processed"] = False
    df["found"] = False
    df.to_csv(os.path.join(results_path, "researchers.csv"))



if __name__ == "__main__":
    main()

