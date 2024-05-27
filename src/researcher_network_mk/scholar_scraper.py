import os
import logging

import pandas as pd

from scholarly import scholarly
import time
import random

from researcher_network_mk.utils import (
    get_researcher_paths, 
    save_coauthors
)

def get_publications_info(researcher_name):
    search_query = scholarly.search_author(researcher_name)
    first_author_result = next(search_query)
    author = scholarly.fill(first_author_result)
    publications = []
    for pub in author["publications"]:
        pub = scholarly.fill(pub)
        time.sleep(random.uniform(1, 3))
        publications.append({pub["bib"]["title"]: pub["bib"]["author"].split(" and ")})
    return publications

def get_coauthors_stats(publications):
    coauthors = dict()
    for pub in publications:
        pub_title, pub_authors = next(iter(pub.items()))
        for author in pub_authors:
            if author in coauthors:
                coauthors[author] += 1
            else:
                coauthors[author] = 1
    return coauthors

def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename="scholar_scraper.log", encoding="utf-8", level=logging.DEBUG)
    faculties = get_researcher_paths()
    for (file_path, faculty) in faculties:
        researchers = pd.read_csv(file_path, index_col=0)
        for researcher in researchers.itertuples():
            researcher_name = researcher.name
            try:
                publications = get_publications_info(researcher_name)
                if not publications:
                    logger.info(f"No publications found for {researcher_name}.")
                    continue

                coauthors = get_coauthors_stats(publications)
                save_coauthors(faculty, researcher_name, coauthors)
                logger.info(f"Coauthor network for {researcher_name} has been created.")
            except Exception as e:
                logger.error(f"An error occured for {researcher_name}: {e}")

if __name__ == "__main__":
    main()
