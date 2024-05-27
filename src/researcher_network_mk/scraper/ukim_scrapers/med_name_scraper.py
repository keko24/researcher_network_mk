import os
import requests

import pandas as pd
from bs4 import BeautifulSoup
from transliterate import translit

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
    if "д-р" in researcher:
        researcher_name = researcher.split("д-р ")
    elif "проф. " in researcher:
        researcher_name = researcher.split("проф. ")
    else:
        researcher_name = researcher.split("сор. ")
    researcher_name = researcher_name[1].strip(" ")
    researcher_latin_name = translit(researcher_name, 'mk', reversed=True)
    return researcher_latin_name

def main():
    url = "http://medf.ukim.edu.mk/"
    paths = ["редовни-професори", "вонредни-професори", "насловни-вонредни-професори", "доценти", "насловни-доценти", "асистенти-според-нов-зво", "виши-научни-соработници", "научни-соработници", "научни-советници", "пензионирани-професори-на-медицинск", "алумни", "in-memoriam"]
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim")
    data = []
    for i, path in enumerate(paths):
        print(path)
        html = get_html_for_page(url + path)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"class": "entry-content"})
        if i == 0 or i == 3 or i == 6:
            staff = content.select("p")
        else:
            content = content.select("ul")[0]
            staff = content.select("li")
        data.extend([parse_data(researcher.get_text().replace(u'\xa0', u' ').strip("\n")) for researcher in staff if researcher.get_text()])
    os.makedirs(results_path, exist_ok=True)
    pd.DataFrame(data, columns=["name"]).to_csv(os.path.join(results_path, "medf.csv"))

if __name__ == "__main__":
    main()
