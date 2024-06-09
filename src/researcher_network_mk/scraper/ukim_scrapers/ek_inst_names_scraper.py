import os

import pandas as pd

from researcher_network_mk.utils import get_project_root
from researcher_network_mk.transliteration import transliterate_cyrillic_to_latin

# Function to transliterate Macedonian Cyrillic names to Latin letters
def translate_names_to_latin(names_mk):
    return [transliterate_cyrillic_to_latin(name) for name in names_mk]

def main():
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim", "ekonomski_institut")
# List of names in Macedonian Cyrillic
    data_mk = [
        "Верица Јанеска",
        "Силвана Мојсовска",
        "Васил Поповски",
        "Снежана Костадиноска-Милошеска",
        "Биљана Ангелова",
        "Климентина Попоска",
        "Татјана Петковска Мирчевска",
        "Неда Петроска–Ангеловска",
        "Наташа Данилоска",
        "Диана Бошковска",
        "Зоран Јаневски",
        "Ирина Пиперкова",
        "Искра Станчева-Гигов",
        "Елизабета Џамбаска",
        "Александра Лозаноска",
        " Катерина Хаџи Наумова Михајловска",
        "Владимир Петковски",
        "Милена Бошкоска Клисароски",
        "Ангела Зафирова",
        "Теа Јосимовска"
    ]

# Transliterate the names
    data = data_mk

    os.makedirs(results_path, exist_ok=True)
    df = pd.DataFrame(data, columns=["name"])
    df["processed"] = False
    df.to_csv(os.path.join(results_path, "researchers.csv"))



if __name__ == "__main__":
    main()
