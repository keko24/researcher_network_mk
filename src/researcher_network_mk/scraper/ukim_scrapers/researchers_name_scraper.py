import requests
from bs4 import BeautifulSoup
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
    anchor_elem = researcher.select("a")[0]
    researcher_name = " ".join(anchor_elem.get_text().strip("\n").split(" ")[::-1])
    researcher_latin_name = researcher_name
    return researcher_latin_name

def main():
    url = "https://feit.ukim.edu.mk/staff/"
    html = get_html_for_page(url)
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", {"id": "content"})
    staff = content.find_all("div", {"class": "staffArchiveProfessor"})
    data = [parse_data(researcher) for researcher in staff]
    print(data)

if __name__ == "__main__":
    main()
