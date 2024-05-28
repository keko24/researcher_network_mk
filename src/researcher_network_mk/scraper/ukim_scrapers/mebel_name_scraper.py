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
    researcher = researcher.select("td")[0]
    anchor_elem = researcher.select("a")[0]
    researcher_name = anchor_elem.get_text().strip()
    researcher_latin_name = translit(researcher_name, 'mk', reversed=True)
    return researcher_latin_name

def main():
    url = "http://www.fdtme.ukim.edu.mk/kadar/index.html"
    html = get_html_for_page(url)
    soup = BeautifulSoup(html, "html.parser")
    content = soup.select("body")[0]
    content = content.select("table")[0]
    content = content.select("table")[1]
    content = content.select("table")[1]
    content = content.select("table")[0]
    staff = content.select("tr")
    data = [parse_data(researcher) for researcher in staff if researcher.select("td")[0].select("a")]
    print(data)

if __name__ == "__main__":
    main()
