from scholarly import scholarly

search_query = scholarly.search_author("Vesna Andova")
first_author_result = next(search_query)
# scholarly.pprint(first_author_result)

author = scholarly.fill(first_author_result)
# scholarly.pprint(author)

first_publication = author["publications"][0]
first_publication_filled = scholarly.fill(first_publication)
publications_authors = [scholarly.fill(pub)["bib"]["author"] for pub in author["publications"]]
print(publications_authors)
# print(first_publication["bib"]["author"])
# scholarly.pprint(first_publication_filled)

# publication_titles = [pub["bib"]["title"] for pub in author["publications"]]
# print(publication_titles)

# citations = [citation["bib"]["title"] for citation in scholarly.citedby(first_publication_filled)]
# print(citations)
