import requests
from bs4 import BeautifulSoup
from transliterate import translit

USERNAME = "haxorkid02" 
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
    anchor_elem = researcher.select("a")[0]
    researcher_name = anchor_elem.get_text().strip()
    researcher_latin_name = translit(researcher_name, 'mk', reversed=True)
    if researcher_latin_name[:3] == "d-r" or researcher_latin_name[:3] == "m-r" :
        researcher_latin_name = researcher_latin_name[4:]
    if researcher_latin_name[:4] == "d-r." or researcher_latin_name[:4] == "m-r." :
        researcher_latin_name = researcher_latin_name[5:]
    return researcher_latin_name

def main():
    url = "https://finki.ukim.mk/mk/staff-list/kadar/nastaven-kadar"
    html = get_html_for_page(url)
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", {"class": "view-content"})
    staff = content.find_all("div", {"class": "node-teaser"})
    data = [parse_data(researcher) for researcher in staff]
    print(data)

if __name__ == "__main__":
    main()
