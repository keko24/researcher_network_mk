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
    anchor_elem = researcher.select("a")
    if anchor_elem:
        anchor_elem = anchor_elem[0]
    else:
        anchor_elem = researcher.select("span")[0]
    researcher_name = anchor_elem.get_text().strip("\n")
    print(researcher_name)
    if "Prof. " in researcher_name:
        researcher_name = " ".join(researcher_name.split(" ")[1:-1])
    else:
        researcher_name = " ".join(researcher_name.split(" ")[:-2])
    return researcher_name

def main(): 
    url = "http://www.arh.ukim.edu.mk/index.php/en/structure/people"
    html = get_html_for_page(url)
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", {"class": "item-page"})
    
    data = [parse_data(researcher) for i, researcher in enumerate(staff) if (i != 0 and i < 28) or (i >= 31 and i < 32)]
    print(data)

if __name__ == "__main__":
    main()
