import pandas as pd

from scholarly import scholarly
import time
import random

from researcher_network_mk.transliteration import transliterate_cyrillic_to_latin
from researcher_network_mk.utils import (
    get_logger,
    get_researcher_paths, 
    save_publications
)

def decode_unicode_escapes(text):
    return text.encode().decode('unicode-escape')

def get_pub_properties(publication):
    pub_bib = publication["bib"]
    if "journal" in pub_bib:
        publication_type = "journal"
    elif "conference" in pub_bib:
        publication_type = "conference"
    elif "book" in pub_bib:
        publication_type = "book"
    else:
        publication_type = "other"
    title = decode_unicode_escapes(pub_bib["title"])
    author = decode_unicode_escapes(pub_bib["author"])
    return {"title": title, "authors": author.split(" and "), "publication_type": publication_type, "num_citations": publication["num_citations"]}

def get_publications_info(researcher_name):
    search_query = scholarly.search_author(researcher_name)
    first_author_result = next(search_query)
    author = scholarly.fill(first_author_result)
    publications = []
    for pub in author["publications"]:
        pub_full = scholarly.fill(pub)
        time.sleep(random.uniform(1, 3))
        publications.append(get_pub_properties(pub_full)) 
    return publications

def get_coauthors_stats(publications):
    coauthors = dict()
    for pub in publications:
        pub_properties = next(iter(pub.items()))
        for author in pub_properties["authors"]:
            if author in coauthors:
                coauthors[author] += 1
            else:
                coauthors[author] = 1
    return coauthors

def main():
    logger = get_logger()
    universities = get_researcher_paths()
    for university in universities:
        for (faculty_name, faculty_path) in universities[university]:
            researchers = pd.read_csv(faculty_path, index_col=0)
            for researcher in researchers.itertuples():
                researcher_names = transliterate_cyrillic_to_latin(researcher.name)
                logger.info(f"Currently processing researcher {researcher_names[0]} from {faculty_name.upper()} at {university.upper()}")
                for researcher_name in researcher_names:
                    try:
                        publications = get_publications_info(researcher_name)
                        if not publications:
                            logger.info(f"No publications found for {researcher_name}.")
                            continue
                        # coauthors = get_coauthors_stats(publications)
                        save_publications(publications, university, faculty_name, researcher_name)
                        logger.info(f"Coauthor network for {researcher_name} has been created.")
                        researcher.processed = True
                        break
                    except Exception as e:
                        logger.error(f"An error occured for {researcher_name}: {e}")
                        time.sleep(random.uniform(0.5, 1))
                if not researcher.processed:
                    logger.error(f"{researcher_names[0]} could not be found.")
                researchers.loc[researcher.Index] = pd.Series({col: getattr(researcher, col) for col in researchers.columns})
                researchers.to_csv(faculty_path)

if __name__ == "__main__":
    main()
