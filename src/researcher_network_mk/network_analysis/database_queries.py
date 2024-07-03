def get_number_of_publications_in_year(tx, year):
    result = tx.run(
        """
        MATCH (a)-[r]->(b) 
        WHERE b.year = $year 
        RETURN a, r, b 
        """,
        year=year,
    )
    researchers, publications, relationships = [], [], []
    for record in result:
        researchers.append(record["a"])
        publications.append(record["b"])
        relationships.append(record["r"])

    unique_researchers = list(
        {researcher.id: researcher for researcher in researchers}.values()
    )
    unique_publications = list(
        {publication.id: publication for publication in publications}.values()
    )
    return unique_researchers, unique_publications, relationships


def get_nodes(tx):
    result = tx.run("MATCH (n) RETURN n.name AS name")
    for record in result:
        print(record["name"])


def main():
    pass


if __name__ == "__main__":
    main()
