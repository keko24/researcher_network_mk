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
    anchor_elem = researcher.select("a")[0]
    researcher_name = " ".join(anchor_elem.get_text().strip("\n").split(" ")[1:])
    researcher_latin_name = translit(researcher_name, 'mk', reversed=True)
    return researcher_latin_name

def parse_ass(researcher):
    anchor_elem = researcher.select("a")[0]
    researcher_name = " ".join(anchor_elem.get_text().strip("\n").split(", м-р ")[::-1])
    researcher_latin_name = translit(researcher_name, 'mk', reversed=True)
    return researcher_latin_name

def parse_pen(idx, researcher):
    anchor_elem = researcher.select("a")
    if anchor_elem:
        anchor_elem = anchor_elem[0]
    else:
        anchor_elem = researcher.select("td")[1]
    researcher_name = anchor_elem.get_text().strip().strip("(").strip(")")
    if idx > 67:
        researcher_name = researcher_name.split(" ")[2:]
        researcher_name[0] = researcher_name[0][:-1]
        researcher_name = " ".join(researcher_name[::-1])
    elif idx < 62:
        if "проф. д-р " in researcher_name:
            researcher_name = " ".join(researcher_name.split(" ")[2:])
        else:
            researcher_name = " ".join(researcher_name.split(" ")[1:])
    elif idx == 62:
        researcher_name = " ".join(researcher_name.split(", проф д-р ")[::-1])
    elif idx == 67:
        researcher_name = " ".join(researcher_name.split(", д-р ")[::-1])
    else:
        researcher_name = " ".join(researcher_name.split(" ")[2:][::-1])
    researcher_latin_name = translit(researcher_name, 'mk', reversed=True)
    return researcher_latin_name

def main():
    urls = ["https://pf.ukim.edu.mk/redovni-profesorin/", "https://pf.ukim.edu.mk/vonredni-profesorin/", "https://pf.ukim.edu.mk/doczenti/", "https://pf.ukim.edu.mk/asistenti/", "https://pf.ukim.edu.mk/penzionirani-profesori/"]
    for i, url in enumerate(urls):
        html = get_html_for_page(url)
        soup = BeautifulSoup(html, "html.parser")
        if i == 4:
            content = soup.find("table", {"id": "supsystic-table-242"})
        else:
            content = soup.find("table", {"id": "supsystic-table-" + str(174 + i)})
        content = content.select("tbody")[0]
        staff = content.select("tr")
        if i == 4:
            data = [parse_pen(i, researcher) for i, researcher in enumerate(staff) if i != 0]
        elif i == 3:
            data = [parse_ass(researcher) for researcher in staff]
        else:
            data = [parse_data(researcher) for researcher in staff]
        print(data)

if __name__ == "__main__":
    main()
