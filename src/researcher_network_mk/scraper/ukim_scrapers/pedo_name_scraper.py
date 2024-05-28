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

def parse_data(researcher, last):
    researcher_name = researcher.get_text().replace(u'\xa0', u' ')
    if last:
        researcher_name = researcher_name[:len(researcher_name) - 14]
    if "д-р " not in researcher_name:
        researcher_name = researcher_name.strip("\t").split("д-р")[1]
    else:
        researcher_name = researcher_name.strip("\t").split("д-р ")[1]
    researcher_latin_name = translit(researcher_name, 'mk', reversed=True)
    return researcher_latin_name

def main():
    url = "https://pfsko.ukim.edu.mk/nastaven-kadar/"
    html = get_html_for_page(url)
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("main", {"id": "content"})
    staff = content.find_all("h3", {"class": "module-feature-title"})
    data = [parse_data(researcher, i == len(staff) - 1) for i, researcher in enumerate(staff)]
    print(data)

if __name__ == "__main__":
    main()
