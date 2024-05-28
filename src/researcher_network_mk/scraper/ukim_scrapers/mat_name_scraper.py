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
    researcher_name = researcher.select("h3")[0].select("a")[0].get_text()
    if "м-р" in researcher_name or "д-р" in researcher_name:
        researcher_name = " ".join(researcher_name.strip("\n").strip().split(" ")[1:])
    researcher_latin_name = ""
    for i, c in enumerate(researcher_name):
        if c.isupper() and i != 0:
            researcher_latin_name += " "
        researcher_latin_name += c
    researcher_latin_name = translit(researcher_latin_name, 'mk', reversed=True)
    return researcher_latin_name.strip()

def main():
    urls = ["https://im.pmf.ukim.edu.mk/titles/view/19", "https://im.pmf.ukim.edu.mk/titles/view/2", "https://im.pmf.ukim.edu.mk/titles/view/17", "https://im.pmf.ukim.edu.mk/titles/view/13", "https://im.pmf.ukim.edu.mk/titles/view/18", "https://im.pmf.ukim.edu.mk/titles/view/12", "https://im.pmf.ukim.edu.mk/titles/view/15", "https://im.pmf.ukim.edu.mk/titles/view/11"]
    for url in urls:
        html = get_html_for_page(url)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"class": "col-md-8"})
        staff = content.find_all("div", {"class": "teachers"})
        data = [parse_data(researcher) for researcher in staff]
        print(data)

if __name__ == "__main__":
    main()

