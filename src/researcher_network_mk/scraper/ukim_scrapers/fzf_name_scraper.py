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
    researcher_name = " ".join(anchor_elem.get_text().strip("\n").split(" ")[1])
    researcher_latin_name = translit(researcher_name, 'mk', reversed=True)
    return researcher_latin_name

def main():
    url = "http://fzf.ukim.edu.mk"
    paths = ["институт-за-филозофија", "институт-за-историја", "инзтитут-за-педагогија", "институт-за-класични-студии", "институт-за-историја-на-уметноста-и-ар", "институт-за-социологија", "институт-за-психологија", "институт-за-безбедност-одбрана-и-мир", "институт-за-социјална-работа-и-соција", "институт-за-специјална-едукација-и-ре", "институт-за-родови-студии", "институт-за-семејни-студии"]
    for path in paths:
        #html = get_html_for_page(url + path)
        headers = { 'accept':'*/*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'en-GB,en;q=0.9,en-US;q=0.8,hi;q=0.7,la;q=0.6',
        'cache-control':'no-cache',
        'dnt':'1',
        'pragma':'no-cache',
        'referer':'https',
        'sec-fetch-mode':'no-cors',
        'sec-fetch-site':'cross-site',
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
         }

        URL = "https://www.crunchbase.com/login"

        response = requests.get(url=url+path, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        content = soup.find("div", {"id": "content"})
        staff = content.find_all("div", {"class": "tg-facultyname"})
        data = [parse_data(researcher) for researcher in staff]
        print(data)

if __name__ == "__main__":
    main()
