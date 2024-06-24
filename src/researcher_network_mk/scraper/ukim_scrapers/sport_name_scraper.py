import os

import pandas as pd
import requests
from bs4 import BeautifulSoup

from researcher_network_mk.utils import get_project_root

USERNAME = "bube12_kYa8y"
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


def parse_data(researcher):
    anchor_elem = researcher.select("h4")[0]
    researcher_name = anchor_elem.get_text()
    researcher_latin_name = researcher_name
    return researcher_latin_name


def main():
    url = "https://ffosz.ukim.edu.mk/nastaven-kadar/"
    results_path = os.path.join(
        get_project_root(), "data", "researchers", "ukim", "sport"
    )
    html = get_html_for_page(url)
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", {"class": "main-post-content"})
    staff = content.find_all("div", {"class": "vc_gitem-post-data-source-post_title"})
    data = [parse_data(researcher) for researcher in staff]
    os.makedirs(results_path, exist_ok=True)
    df = pd.DataFrame(data, columns=["name"])
    df["processed"] = False
    df["found"] = False
    df.to_csv(os.path.join(results_path, "researchers.csv"))


if __name__ == "__main__":
    main()
