import os

import networkx as nx
import numpy as np
import pandas as pd

from researcher_network_mk.utils import (
    get_project_root,
    list_faculties,
    list_researchers,
    list_universities,
    load_json,
)


def get_class_vector(domain):
    domain_to_class = {
        "Natural Science and Mathematics": 0,
        "Engineering technologies": 1,
        "Social sciences": 2,
        "Humanities": 3,
    }
    class_vector = np.zeros(len(domain_to_class))

    if domain is None:
        return class_vector

    class_vector[domain_to_class[domain]] = 1
    return class_vector


def convert_neo4j_to_networkx(publications, researchers, relationships):
    G = nx.Graph()

    for publication in publications:
        G.add_node(publication.id, **publication._properties, bipartite=0)

    for researcher in researchers:
        G.add_node(researcher.id, **researcher._properties, bipartite=1)

    for rel in relationships:
        G.add_edge(rel.start_node.id, rel.end_node.id, **rel._properties)

    return G


def get_researchers():
    data = []
    researchers_path = os.path.join(get_project_root(), "data", "researchers")
    for university in list_universities():
        for faculty in list_faculties(university):
            faculty_researchers_path = os.path.join(
                researchers_path, university, faculty, "researchers.csv"
            )
            researchers = pd.read_csv(faculty_researchers_path)
            for researcher in researchers.itertuples():
                if researcher.processed:
                    data.append(
                        {
                            "name": researcher.name,
                            "university": university,
                            "domain": faculty,
                        }
                    )
    return data


def get_publications():
    data = []
    researchers_path = os.path.join(get_project_root(), "data", "researchers")
    for university in list_universities():
        for faculty in list_faculties(university):
            for researcher in list_researchers(university, faculty):
                researcher_publications_path = os.path.join(
                    researchers_path, university, faculty, "publications", researcher
                )
                researcher_publications = load_json(researcher_publications_path)
                for publication in researcher_publications:
                    data.append(publication)
    return data


def get_researchers_and_publications():
    researchers = []
    publications = []
    researchers_path = os.path.join(get_project_root(), "data", "researchers")
    for university in list_universities():
        for faculty in list_faculties(university):
            for researcher in list_researchers(university, faculty):
                researcher_publications_path = os.path.join(
                    researchers_path, university, faculty, "publications", researcher
                )
                researcher_publications = load_json(researcher_publications_path)
                for publication in researcher_publications:
                    publication["publication_year"] = 2019
                researchers.append(
                    {
                        "name": researcher[:-5].replace("_", " "),
                        "university": university,
                        "domain": faculty,
                    }
                )
                publications.extend(researcher_publications)
    return researchers, publications
