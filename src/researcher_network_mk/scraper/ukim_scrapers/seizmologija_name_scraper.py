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
    researcher_name = researcher.select("td")[1].select("p")[0].get_text()
    researcher_latin_name = translit(researcher_name, 'mk', reversed=True)
    return researcher_latin_name.strip()

def main():
    urls = ["https://seismobsko.pmf.ukim.edu.mk/chronologicalpersonnel"]
    for url in urls:
        html = get_html_for_page(url)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"class": "col-md-8"})
        content = content.select("table")[0]
        staff = content.select("tr")
        data = [parse_data(researcher) for researcher in staff[1:]]
        print(data)

if __name__ == "__main__":
    main()

