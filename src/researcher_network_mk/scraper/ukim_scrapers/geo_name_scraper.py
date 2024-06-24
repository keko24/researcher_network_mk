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
    researcher_name = researcher.select("h3")[0].select("a")[0].get_text()
    if "м-р" in researcher_name or "д-р" in researcher_name:
        researcher_name = " ".join(researcher_name.strip("\n").strip().split(" ")[1:])
    researcher_latin_name = ""
    for i, c in enumerate(researcher_name):
        if c.isupper() and i != 0:
            researcher_latin_name += " "
        researcher_latin_name += c
    researcher_latin_name = researcher_latin_name
    return researcher_latin_name.strip()

def main():
    urls = ["https://ig.pmf.ukim.edu.mk/titles/view/1", "https://ig.pmf.ukim.edu.mk/titles/view/3", "https://ig.pmf.ukim.edu.mk/titles/view/14", "https://ig.pmf.ukim.edu.mk/titles/view/17", "https://ig.pmf.ukim.edu.mk/titles/view/16", "https://ig.pmf.ukim.edu.mk/titles/view/13", "https://ig.pmf.ukim.edu.mk/titles/view/15"]
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim", "geografija")
    data = []
    for url in urls:
        html = get_html_for_page(url)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"class": "col-md-8"})
        staff = content.find_all("div", {"class": "teachers"})
        data.extend([parse_data(researcher) for researcher in staff])
    os.makedirs(results_path, exist_ok=True)
    df = pd.DataFrame(data, columns=["name"])
    df["processed"] = False
    df["found"] = False
    df.to_csv(os.path.join(results_path, "researchers.csv"))



if __name__ == "__main__":
    main()

