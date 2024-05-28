import requests
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
    researcher_name = researcher.get_text()
    researcher_name = researcher_name.replace(u'\xa0', u' ')
    if "М-р" in researcher_name or "Д-р" in researcher_name:
        researcher_name = " ".join(" ".join(researcher_name.split(" ")[1:]).split(", ")[:1])
    else:
        researcher_name = " ".join(" ".join(researcher_name.split(" ")).split(", ")[:1])
    researcher_latin_name = translit(researcher_name, 'mk', reversed=True)
    return researcher_latin_name

def main():
    url = "https://www.tmf.ukim.edu.mk/"
    paths = ["редовни-професори", "вонредни-професори", "доценти", "асистенти", "лаборанти", "пензионирани-професори"]
    for i, path in enumerate(paths):
        html = get_html_for_page(url + path)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"id": "page-main-content"})
        staff = content.find_all("p", {"class": "has-black-color has-text-color"})
        data = [parse_data(researcher) for researcher in staff]
        print(data)

if __name__ == "__main__":
    main()
