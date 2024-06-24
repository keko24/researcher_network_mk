import os

import pandas as pd
import requests
from bs4 import BeautifulSoup

from researcher_network_mk.transliteration import transliterate_cyrillic_to_latin
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
        auth=(USERNAME, PASSWORD),
        json=payload,
    )
    response.raise_for_status()
    return response.json()["results"][0]["content"]


def parse_data(researcher):
    anchor_elem = researcher.select("h3")[0]
    researcher_name = " ".join(anchor_elem.get_text().split(" ")[1:])
    researcher_latin_name = researcher_name
    return researcher_latin_name


def main():
    urls = [
        "http://www.fmu.ukim.edu.mk/mk/katedra/Katedra-za-muzichka-teorija-i-pedagogija-muzikologija-kompozicija-i-dirigiranje",
        "http://www.fmu.ukim.edu.mk/mk/katedra/Katedra-za-gudachki-instrumenti-i-gitara",
        "http://www.fmu.ukim.edu.mk/mk/katedra/Katedra-za-baletska-pedagogija",
        "http://www.fmu.ukim.edu.mk/mk/katedra/Katedra-za-duvachki-instrumenti-udirachki-instrumenti-i-solo-peenje",
        "http://www.fmu.ukim.edu.mk/mk/katedra/Katedra-za-klavishni-instrumenti-i-harfa",
    ]
    results_path = os.path.join(
        get_project_root(), "data", "researchers", "ukim", "muzicko"
    )
    data = []
    for url in urls:
        html = get_html_for_page(url)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"class": "page-content"})
        staff = content.find_all("div", {"class": "col-md-9"})
        data.extend([parse_data(researcher) for i, researcher in enumerate(staff)])
    os.makedirs(results_path, exist_ok=True)
    df = pd.DataFrame(data, columns=["name"])
    df["processed"] = False
    df["found"] = False
    df.to_csv(os.path.join(results_path, "researchers.csv"))


if __name__ == "__main__":
    main()
