import requests
from bs4 import BeautifulSoup
from transliterate import translit

USERNAME = "andykot24" 
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
    researcher_content = researcher.find("div", {"class": "item-content"})
    anchor_elem = researcher_content.select("a")[0]
    researcher_name = " ".join(anchor_elem.get_text().strip("\n").split(" ")[-2:][::-1])
    researcher_latin_name = translit(researcher_name, 'mk', reversed=True)
    return researcher_latin_name

def main():
    urls = [
            "http://gf.ukim.edu.mk/member/tip_profesor/redoven/",
            "http://gf.ukim.edu.mk/member/tip_profesor/vonreden/",
            "http://gf.ukim.edu.mk/member/tip_profesor/docent/",
            "http://gf.ukim.edu.mk/member/tip_profesor/asistent/"
    ]
    for url in urls:
        html = get_html_for_page(url)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"id": "content"})
        staff = content.find_all("div", {"class": "member-item"})
        data = [parse_data(researcher) for researcher in staff]
        print(data)

if __name__ == "__main__":
    main()
