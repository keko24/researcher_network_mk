import os

import networkx as nx
import pandas as pd

from researcher_network_mk.utils import (
    get_project_root,
    load_json,
    list_universities,
    list_faculties,
    list_researchers
)

def create_networkx_graph(researchers, publications, edges):
    G = nx.Graph()
    G.add_nodes_from(researchers, bipartite=0)
    G.add_nodes_from(publications, bipartite=1)
    G.add_edges_from(edges)
    return G

def get_researchers():
    data = []
    researchers_path = os.path.join(get_project_root(), "data", "researchers")
    for university in list_universities():
        for faculty in list_faculties(university):
            faculty_researchers_path = os.path.join(researchers_path, university, faculty, "researchers.csv")
            researchers = pd.read_csv(faculty_researchers_path)
            for researcher in researchers.itertuples():
                if researcher.processed:
                    data.append({"name": researcher.name, "university": university, "domain": faculty})
    return data

def get_publications():
    data = []
    researchers_path = os.path.join(get_project_root(), "data", "researchers")
    for university in list_universities():
        for faculty in list_faculties(university):
            for researcher in list_researchers(university, faculty):
                researcher_publications_path = os.path.join(researchers_path, university, faculty, "publications", researcher)
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
                researcher_publications_path = os.path.join(researchers_path, university, faculty, "publications", researcher)
                researcher_publications = load_json(researcher_publications_path)
                for publication in researcher_publications:
                    publication["publication_year"] = 2019
                researchers.append({"name": researcher[:-5].replace('_', ' '), "university": university, "domain": faculty})
                publications.extend(researcher_publications)
    return researchers, publications
