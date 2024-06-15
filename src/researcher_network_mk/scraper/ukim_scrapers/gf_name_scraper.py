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
    researcher_content = researcher.find("div", {"class": "item-content"})
    anchor_elem = researcher_content.select("a")[0]
    researcher_name = " ".join(anchor_elem.get_text().strip("\n").split(" ")[-2:][::-1])
    researcher_latin_name = researcher_name
    return researcher_latin_name

def main():
    urls = [
            "http://gf.ukim.edu.mk/member/tip_profesor/redoven/",
            "http://gf.ukim.edu.mk/member/tip_profesor/vonreden/",
            "http://gf.ukim.edu.mk/member/tip_profesor/docent/",
            "http://gf.ukim.edu.mk/member/tip_profesor/asistent/"
    ]
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim", "gradezhen")
    data = []
    for url in urls:
        html = get_html_for_page(url)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"id": "content"})
        staff = content.find_all("div", {"class": "member-item"})
        data = [parse_data(researcher) for researcher in staff]
    os.makedirs(results_path, exist_ok=True)
    df = pd.DataFrame(data, columns=["name"])
    df["processed"] = False
    df["found"] = False
    df.to_csv(os.path.join(results_path, "researchers.csv"))



if __name__ == "__main__":
    main()
