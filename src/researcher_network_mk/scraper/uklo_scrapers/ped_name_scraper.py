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

def parse_data(i, researcher):
    anchor_elem = researcher.select("p")
    if i > 22: 
        anchor_elem = anchor_elem[0].get_text().replace(u'\xa0', u' ')
    else:
        anchor_elem = anchor_elem[len(anchor_elem) - 1].get_text().replace(u'\xa0', u' ')
    if "м-р" in anchor_elem or "Дип.инж" in anchor_elem:
        researcher_name = " ".join(anchor_elem.split("\n")[0].split(" ")[1:])
    elif "д-р" in anchor_elem or "Д-р" in anchor_elem:
        researcher_name = " ".join(anchor_elem.split("\n")[0].split(" ")[2:])
    else:
        researcher_name = " ".join(anchor_elem.split("\n")[0].split(" ")[:])
    researcher_latin_name = translit(researcher_name, 'mk', reversed=True)
    return researcher_latin_name

def main():
    urls = ["https://pfbt.uklo.edu.mk/академски-кадар"]
    for url in urls:
        html = get_html_for_page(url)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"class": "post-content"})
        staff = content.find_all("div", {"class": "fusion-text"})
        data = [parse_data(i, researcher) for i, researcher in enumerate(staff) if i != 0]
        print(data)

if __name__ == "__main__":
    main()
