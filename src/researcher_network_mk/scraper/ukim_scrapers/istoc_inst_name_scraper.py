import os

import pandas as pd

from researcher_network_mk.utils import get_project_root
from researcher_network_mk.transliteration import transliterate_cyrillic_to_latin

# Function to transliterate names from Macedonian Cyrillic to Latin
def translate_names_to_latin(names_mk):
    return [transliterate_cyrillic_to_latin(name) for name in names_mk]

def main():
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim", "stocarstvo_institut")
    data_mk = [
        "Natasha Gjorgovska",
        "Nikola Pacinovski",
        "Nedeljka Nikolova",
        "Bone Palashevski",
        "Natasha Danilovska",
        "Tatjana Petkovska",
        "Tatjana P.-Mircevska",
        "Mirjana Menkovska",
        "Elizabeta Angelova",
        "Bone Palashevski",
        "Nikola Pacinovski",
        "Nedeljka Nikolova",
        "Natasha Gjorgovska",
        "Natasha Mateva",
        "Tosho Kostadinov",
        "Dejan Pendev",
        "Vasil Popovski"
    ]

    data = data_mk

    os.makedirs(results_path, exist_ok=True)
    df = pd.DataFrame(data, columns=["name"])
    df["processed"] = False
    df["found"] = False
    df.to_csv(os.path.join(results_path, "researchers.csv"))



if __name__ == "__main__":
    main()
