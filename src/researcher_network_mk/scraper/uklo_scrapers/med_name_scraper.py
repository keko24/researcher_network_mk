import os

import pandas as pd
import requests
from bs4 import BeautifulSoup

from researcher_network_mk.utils import get_project_root

USERNAME = "bube12_ZULBV"
PASSWORD = "Researchscraper123"


def get_html_for_page(url):
    payload = {
        "url": url,
        "source": "universal",
    }
    response = requests.post(
        "https://realtime.oxylabs.io/v1/queries",
        auth=(USERNAME, PASSWORD),
        json=payload,
    )
    response.raise_for_status()
    return response.json()["results"][0]["content"]


def parse_data(i, researcher):
    if i < 2:
        anchor_elem = researcher.select("p")[1].get_text()
    else:
        anchor_elem = researcher.select("p")[0].get_text()
    if i > 6:
        researcher_name = " ".join(anchor_elem.split("\n")[0].split(" ")[1:])
    else:
        researcher_name = " ".join(anchor_elem.split("\n")[0].split(" ")[2:])
    researcher_latin_name = researcher_name
    return researcher_latin_name


def parse_second_data(researcher):
    researcher_name = researcher.get_text()
    if "м-р " in researcher_name:
        researcher_name = researcher_name.split("м-р ")
    else:
        researcher_name = researcher_name.split("д-р ")
    researcher_name = researcher_name[1].split(" – ")[0]
    researcher_latin_name = researcher_name
    return researcher_latin_name


def main():
    urls = [
        "https://vmsb.uklo.edu.mk/kadar/",
        "https://vmsb.uklo.edu.mk/angazirani-profesori/",
    ]
    data = []
    results_path = os.path.join(
        get_project_root(), "data", "researchers", "uklo", "medicina"
    )
    for i, url in enumerate(urls):
        html = get_html_for_page(url)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"class": "post-content"})
        if i == 0:
            staff = content.find_all("div", {"class": "fusion-text"})
            data.extend(
                [parse_data(j, researcher) for j, researcher in enumerate(staff)]
            )
        else:
            staff = content.select("p")
            data.extend(
                [
                    parse_second_data(researcher)
                    for j, researcher in enumerate(staff)
                    if "м-р" in researcher.get_text() or "д-р" in researcher.get_text()
                ]
            )
    os.makedirs(results_path, exist_ok=True)
    df = pd.DataFrame(data, columns=["name"])
    df["processed"] = False
    df["found"] = False
    df.to_csv(os.path.join(results_path, "researchers.csv"))


if __name__ == "__main__":
    main()
