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
    anchor_elem = researcher.select("a")[0].get_text()
    if "Науч. " in anchor_elem:
        researcher_name = " ".join(anchor_elem.strip("\n").strip("\t").split(" ")[3:])
    elif "Проф " in anchor_elem or "Проф. " in anchor_elem or "проф. " in anchor_elem or "Виш" in anchor_elem or "ас." in anchor_elem:
        researcher_name = " ".join(anchor_elem.strip("\n").strip("\t").split(" ")[2:])
    else:
        researcher_name = " ".join(anchor_elem.strip("\n").strip("\t").split(" ")[1:])
    researcher_latin_name = translit(researcher_name, 'mk', reversed=True)
    return researcher_latin_name

def main():
    urls = ["https://stomfak.ukim.edu.mk/кадар/наставно-научен-кадар", "https://stomfak.ukim.edu.mk/кадар/научен-кадар", "https://stomfak.ukim.edu.mk/кадар/соработнички-кадар"]
    for url in urls:
        html = get_html_for_page(url)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find_all("div", {"class": "elementor-container"})
        content = content[len(content) - 1]
        staff = content.find_all("div", {"class": "elementor-post__text"})
        data = [parse_data(researcher) for researcher in staff]
        print(data)

if __name__ == "__main__":
    main()
