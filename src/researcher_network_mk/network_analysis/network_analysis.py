import networkx as nx
import numpy as np

from researcher_network_mk.network_analysis.network_utils import get_class_vector


def convert_network_to_one_mode(G):
    researchers = get_researchers(G)
    one_mode = nx.bipartite.projected_graph(G, researchers)

    for researcher_a, researcher_b in one_mode.edges():
        one_mode[researcher_a][researcher_b]["weight"] = 0

    for researcher_a in researchers:
        for researcher_b in researchers:
            if researcher_a != researcher_b:
                common_neighbors = set(G[researcher_a]) & set(G[researcher_b])
                weight = len(common_neighbors)
                if weight > 0:
                    one_mode.add_edge(researcher_a, researcher_b, weight=weight)
    return one_mode


def convert_network_to_one_mode_with_frac_weights(G):
    researchers = get_researchers(G)
    one_mode = nx.bipartite.projected_graph(G, researchers)

    for researcher_a, researcher_b in one_mode.edges():
        one_mode[researcher_a][researcher_b]["weight"] = 0

    for researcher_a in researchers:
        for researcher_b in researchers:
            if researcher_a != researcher_b:
                common_neighbors = set(G[researcher_a]) & set(G[researcher_b])
                weight = 0
                for neighbor in common_neighbors:
                    weight += 1 / (G.nodes[neighbor].get("num_authors") - 1)
                if weight > 0:
                    one_mode.add_edge(researcher_a, researcher_b, weight=weight)
    return one_mode


def get_researchers(G):
    researchers = {n for n, d in G.nodes(data=True) if d["bipartite"] == 0}
    return researchers


def get_publications(G):
    publications = {n for n, d in G.nodes(data=True) if d["bipartite"] == 1}
    return publications


def count_number_of_publications(G):
    return len(get_publications(G))


def count_number_of_researchers(G):
    return len(get_researchers(G))


def count_number_of_publications_by_researcher(G):
    researchers = get_researchers(G)
    adjacency_count = {
        researcher: len(list(G.neighbors(researcher))) for researcher in researchers
    }
    return adjacency_count


def calc_avg_number_of_pubs_per_author(G):
    adjacency_count = count_number_of_publications_by_researcher(G)
    return sum(adjacency_count.values()) / count_number_of_researchers(G)


def count_fractional_number_of_publications_by_researcher(G):
    researchers = get_researchers(G)
    adjacency_count = {researcher: 0 for researcher in researchers}

    for researcher in researchers:
        for pub in G.neighbors(researcher):
            num_authors = G.nodes[pub].get("num_authors")
            adjacency_count[researcher] += 1 / num_authors

    return adjacency_count


def calc_avg_frac_number_of_pubs_per_researcher(G):
    frac_count = count_fractional_number_of_publications_by_researcher(G)
    return sum(frac_count.values()) / count_number_of_researchers(G)


def get_num_authors_per_publication(G):
    publications = get_publications(G)
    num_authors = {
        publication: G.nodes[publication].get("num_authors")
        for publication in publications
    }
    return num_authors


def calc_avg_num_of_coauthors_per_pub(G):
    num_authors = get_num_authors_per_publication(G)
    return sum(num_authors) / len(get_publications(G))


def calc_relative_num_of_solo_pubs(G):
    num_authors = get_num_authors_per_publication(G)
    return sum(num for num in num_authors.values() if num == 1) / len(num_authors)


def calc_avg_num_collaborators_for_researcher(G):
    researchers = get_researchers(G)
    G = convert_network_to_one_mode(G)
    avg_num = 0
    for researcher in researchers:
        avg_num += len(G.neighbors(researcher))
    return avg_num / len(researchers)


def calc_avg_weight_of_edges(G):
    G = convert_network_to_one_mode(G)
    return G.size(weight="weight") / G.number_of_edges()


def calc_avg_frac_weight_of_edges(G):
    G = convert_network_to_one_mode_with_frac_weights(G)
    return G.size(weight="weight") / G.number_of_edges()


def calc_avg_publication_interdisciplinarity(G):
    average_interdisciplinarity = 0
    publications = get_publications(G)
    for publication in publications:
        centroid = get_class_vector(None)
        for researcher in G.neighbors(publication):
            domain = G.nodes[researcher].get("domain")
            centroid += get_class_vector(domain)
        centroid /= G.nodes[publication].get("num_authors")
        average_interdisciplinarity += np.sqrt(
            (1 - np.inner(centroid, centroid)) * 6 / 5
        )
    return average_interdisciplinarity / len(publications)


def calc_avg_researcher_interdisciplinarity(G):
    researchers = get_researchers(G)
    G = convert_network_to_one_mode(G)
    average_interdisciplinarity = 0
    for researcher in researchers:
        centroid = get_class_vector(None)
        for neighbor in G.neighbors(researcher):
            domain = G.nodes[neighbor].get("domain")
            centroid += get_class_vector(domain)
        centroid /= len(G.neighbors(researcher))
        average_interdisciplinarity += np.sqrt(
            (1 - np.inner(centroid, centroid)) * 6 / 5
        )
    return average_interdisciplinarity / len(researchers)


def get_giant_component(G):
    Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
    return G.subgraph(Gcc[0])


def get_characteristic_path_length(G):
    G = convert_network_to_one_mode(G)
    G = get_giant_component(G)
    return nx.average_shortest_path_length(G)


def get_diameter_of_network(G):
    G = convert_network_to_one_mode(G)
    G = get_giant_component(G)
    return nx.diameter(G)


def calc_clustering_coefficient(G):
    clustering_coef = 0
    researchers = get_researchers(G)
    G = convert_network_to_one_mode(G)
    for researcher in researchers:
        coauthors = G.neighbors(researcher)
        num_coauthors = len(coauthors)
        num_edges_between_coauthors = 0
        for coauthor_a, coauthor_b in zip(coauthors, coauthors):
            if coauthor_a != coauthor_b:
                num_edges_between_coauthors += G.number_of_edges(coauthor_a, coauthor_b)
        clustering_coef += (
            2 * num_edges_between_coauthors / (num_coauthors * (num_coauthors - 1))
        )
    return clustering_coef / len(researchers)

def calc_pub_internationality(G):
    publications = get_publications(G)
    avg_pub_internationality = 0
    for publication in publications:
        avg_pub_internationality += 1 - len(G.neighbors(publication)) / G.nodes[publication].get("num_authors")
    return avg_pub_internationality / len(publications)

def calc_researcher_internationality(G):
    researchers = get_researchers(G)
    avg_researcher_internationality = 0
    for researcher in researchers:
        num_coauthors = 0
        num_registered_coauthors = 0
        for publication in G.neighbors(researcher):
            num_coauthors += G.nodes[publication].get("num_authors")
            num_registered_coauthors += len(G.neighbors(publication))
        avg_researcher_internationality += 1 - num_registered_coauthors / num_coauthors
    return avg_researcher_internationality / len(researchers)
