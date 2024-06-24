import os

from neo4j import GraphDatabase
from thefuzz import fuzz, process

from researcher_network_mk.network_utils import get_researchers_and_publications

def normalize_name(name):
    parts = name.split(" ")
    return parts[0][0] + ' ' + ' '.join(parts[1:]) 

def create_researcher_node(tx, researcher):
    tx.run("CREATE (n:Researcher {name: $name, university: $university, domain: $domain})", name=researcher["name"], university=researcher["university"], domain=researcher["domain"])

def create_publication_node(tx, publication):
    tx.run("CREATE (n:Publication {title: $title, publication_type: $publication_type, publication_year: $publication_year, num_authors: $num_authors, num_citations: $num_citations})", title=publication["title"], publication_type=publication["publication_type"], publication_year=publication["publication_year"], num_authors=len(publication["authors"]), num_citations=publication["num_citations"])

def create_authorship_edge(tx, researcher_name, publication_title):
    tx.run("""
        MATCH (a:Researcher {name: $researcher_name}), (b:Publication {title: $publication_title})
        CREATE (a)-[r:AUTHORED]->(b)
    """, researcher_name=researcher_name, publication_title=publication_title)

def get_nodes(tx):
    result = tx.run("MATCH (n) RETURN n.name AS name")
    for record in result:
        print(record["name"])

def find_best_match(researcher_name, existing_researchers):
    normalized_name = normalize_name(researcher_name)
    
    best_match, score = process.extractOne(researcher_name, existing_researchers, scorer=fuzz.token_sort_ratio)
    normalized_best_match, normalized_score = process.extractOne(normalized_name, existing_researchers, scorer=fuzz.token_sort_ratio)
    if score > 80:
        return best_match
    elif normalized_score > 80:
        return normalized_best_match
    else:
        return None

def main():
    uri = "bolt://localhost:7687"
    username = os.environ["NEO4J_USER"]
    password = os.environ["NEO4J_PASS"]

    driver = GraphDatabase.driver(uri, auth=(username, password))

    with driver.session() as session:
        researchers, publications = get_researchers_and_publications()
        researchers_name = [researcher["name"] for researcher in researchers]

        for researcher in researchers:
            session.execute_write(create_researcher_node, researcher)

        for publication in publications:
            session.execute_write(create_publication_node, publication)
            publication_title = publication["title"]
            for author in publication["authors"]:
                researcher_name = find_best_match(author, researchers_name)
                if researcher_name:
                    session.execute_write(create_authorship_edge, researcher_name, publication_title)

    driver.close()

if __name__ == "__main__":
    main()
