import requests
from bs4 import BeautifulSoup
USERNAME = "haxorkid" 
PASSWORD = "SerpScraper123"

def get_html_for_page(url):
    payload = {
        "url": url,
        "source": "google",
    }
    response = requests.post(
        "https://realtime.oxylabs.io/v1/queries",
        auth=(USERNAME,PASSWORD),
        json=payload,
    )
    response.raise_for_status()
    return response.json()["results"][0]["content"]

def get_user_profiles(user_profile):
    user_name = user_profile.get_text()
    user_anchor_elem = user_profile.select("a")[0]
    url = user_anchor_elem["href"]
    return {
        "user": user_name,
        "url": url,
    }

def parse_data_from_user_articles(article):
    title_elem = article.find("a", {"class": "gsc_a_at"})
    title = title_elem.get_text()
    url = title_elem["href"]
    article_page = BeautifulSoup(get_html_for_page("https://scholar.google.com" + url), "html.parser")
    article = article_page.find("div", {"id": "gsc_vcpb"})
    print(title)
    return parse_data_from_article(article)
    # return {
    #     "title": title,
    #     "url": url,
    # }

def parse_data_from_article(article):
    title_elem = article.find("a", {"class": "gsc_oci_title_link"})
    print(title_elem)
    title = title_elem.get_text()
    url = title_elem["href"]
    table = article.find("div", {"id": "gsc_oci_table"})
    table_elems = table.find_all("div", {"class": "gs_scl"})
    user_properties = {elem.find("div", {"class": "gsc_oci_field"}).get_text(): elem.find("div", {"class": "gsc_oci_value"}).get_text() for elem in table_elems}
    authors = user_properties["Authors"].split(", ") 
    return {
        "title": title,
        "authors": authors,
        "url": url,
        "publication_date": user_properties["Publication date"],
        "journal": user_properties["Journal"] if "Journal" in user_properties else None
    }

def main():
    url = "https://scholar.google.com/scholar?q=vesna+andova&hl=en&as_sdt=0,5"
    html = get_html_for_page(url)
    soup = BeautifulSoup(html, "html.parser")
    user_profiles_table = soup.find("div", {"class": "gs_r"})
    user_profiles = user_profiles_table.find_all("h4", {"class": {"gs_rt2"}})
    data = [get_user_profiles(user_profile) for user_profile in user_profiles]

    user_page = BeautifulSoup(get_html_for_page("https://scholar.google.com" + data[0]["url"]), "html.parser") 
    article_title_table = user_page.find("div", {"id": {"gsc_a_tw"}})
    articles = article_title_table.find_all("tr", {"class": {"gsc_a_tr"}})
    data = [parse_data_from_user_articles(article) for article in articles]
    
    data = [parse_data_from_article(article) for article in articles]
    print(data)

if __name__ == "__main__":
    main()
