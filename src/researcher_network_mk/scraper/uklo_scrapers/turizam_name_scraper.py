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
    anchor_elem = researcher.select("p")[0]
    researcher_name = " ".join(anchor_elem.get_text().split("\n")[0].split(" ")[2:])
    researcher_latin_name = translit(researcher_name, 'mk', reversed=True)
    return researcher_latin_name

def main():
    urls = ["https://ftu.uklo.edu.mk/za-fakultetot/osnovni-informacii/kadar/"]
    for url in urls:
        html = get_html_for_page(url)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"class": "post-content"})
        staff = content.find_all("div", {"class": "fusion-text"})
        data = [parse_data(researcher) for researcher in staff]
        print(data)

if __name__ == "__main__":
    main()
