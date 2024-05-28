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
    if i > 2:
        anchor_elem = researcher.select("a")[0].get_text().replace(u'\xa0', u' ')
    else: 
        anchor_elem = researcher.select("p")[0].get_text().replace(u'\xa0', u' ')
    if i == 3:
        researcher_name = " ".join(anchor_elem.split("\n")[0].split(" ")[4:])
    elif "м-р" in anchor_elem or "Дип.инж" in anchor_elem:
        researcher_name = " ".join(anchor_elem.split("\n")[0].split(" ")[1:])
    else:
        researcher_name = " ".join(anchor_elem.split("\n")[0].split(" ")[2:])
    researcher_latin_name = translit(researcher_name, 'mk', reversed=True)
    return researcher_latin_name

def main():
    urls = ["https://tfb.uklo.edu.mk/za-fakultetot/osnovni-informacii/kadar/redovni-profesori/", "https://tfb.uklo.edu.mk/za-fakultetot/osnovni-informacii/kadar/vonredni-profesori/", "https://tfb.uklo.edu.mk/za-fakultetot/osnovni-informacii/kadar/asistenti/", "https://tfb.uklo.edu.mk/za-fakultetot/osnovni-informacii/kadar/професори-во-пензија/", "https://tfb.uklo.edu.mk/za-fakultetot/osnovni-informacii/kadar/професори-in-memoriam/"]
    for i, url in enumerate(urls):
        html = get_html_for_page(url)
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"class": "post-content"})
        if i > 2:
            staff = content.find_all("h4", {"class": "entry-title"})
        else:
            staff = content.find_all("div", {"class": "fusion-text"})
        data = [parse_data(i, researcher) for researcher in staff]
        print(data)

if __name__ == "__main__":
    main()
