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
    anchor_elem = researcher.select("h4")[0]
    researcher_name = anchor_elem.get_text()
    researcher_latin_name = translit(researcher_name, 'mk', reversed=True)
    return researcher_latin_name

def main():
    url = "https://ffosz.ukim.edu.mk/nastaven-kadar/"
    html = get_html_for_page(url)
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", {"class": "main-post-content"})
    staff = content.find_all("div", {"class": "vc_gitem-post-data-source-post_title"})
    data = [parse_data(researcher) for researcher in staff]
    print(data)

if __name__ == "__main__":
    main()
