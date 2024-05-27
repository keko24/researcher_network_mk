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
    researcher_name = " ".join(anchor_elem.get_text().strip("\n").split(" ")[::-1])
    researcher_latin_name = translit(researcher_name, 'mk', reversed=True)
    return researcher_latin_name

def main():
    data = []
    for i in range(16):
        url = f"https://mf.ukim.edu.mk/mk/academic-staff?page={i}" if i > 0 else "https://mf.ukim.edu.mk/mk/academic-staff"
        html = get_html_for_page(url)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"class": "view-academic-staff"})
        staff = content.find_all("span", {"class": "field-content"})
        page_data = [parse_data(researcher) for researcher in staff]
        data.extend(page_data)
    print(data)

if __name__ == "__main__":
    main()
