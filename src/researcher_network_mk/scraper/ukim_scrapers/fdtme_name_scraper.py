import os

import pandas as pd

from researcher_network_mk.utils import get_project_root
from researcher_network_mk.transliteration import transliterate_cyrillic_to_latin

# Function to transliterate names from Macedonian Cyrillic to Latin
def translate_names_to_latin(names_mk):
    return [transliterate_cyrillic_to_latin(name) for name in names_mk]

def main():
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim", "mebel")
    # List of names in Macedonian Cyrillic
    data_mk = [
        "Константин Бахчеванџиев", "Ѓорги Груевски", "Горан Златески", "Борче Илиев",
        "Владимир Каранаков", "Владимир Кољозов", "Живка Мелоска", "Митко Нацевски",
        "Елена Никољски Паневски", "Бранко Рабаџиски", "Нацко Симакоски", 
        "Мира Станкевиќ Шуманска", "Зоран Трпоски", "Виолета Јакимовска Поповска"
    ]

    # Transliterate the names
    data = data_mk

    os.makedirs(results_path, exist_ok=True)
    df = pd.DataFrame(data, columns=["name"])
    df["processed"] = False
    df["found"] = False
    df.to_csv(os.path.join(results_path, "researchers.csv"))



if __name__ == "__main__":
    main()
