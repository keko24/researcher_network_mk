import os

import pandas as pd

from researcher_network_mk.utils import get_project_root
from researcher_network_mk.transliteration import transliterate_cyrillic_to_latin

# Function to transliterate names from Macedonian Cyrillic to Latin
def translate_names_to_latin(names_mk):
    return [transliterate_cyrillic_to_latin(name) for name in names_mk]

def main():
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim")
# List of names in Macedonian Cyrillic
    data_mk = [
        "Бојана Наумовска",
        "Наташа Габер-Дамјановска",
        "Петар Атанасов",
        "Маријана Марковиќ",
        "Весна Забијакин - Чатлеска",
        "Дритон Маљичи",
        "Ружица Цацаноска",
        "Мирјана Борота Поповска",
        "Славејко Сасајковски",
        "Иван Блажевски",
        "Марија Топузовска Латковиќ",
        "Милка Димитровска",
        "Ганка Цветанова",
        "Драгор Заревски",
        "Горан Јанев",
        "Анета Цекиќ",
        "Мирјана Најчевска",
        "Панде Лазаревски",
        "Јован Близнаковски",
        "Елеонора Серафимовска",
        "Блаже Јосифовски",
        "Теа Конеска-Василевска",
        "Јорде Владимир Јаќимовски",
        "Емилија Симоска"
    ]

# Transliterate the names
    data = translate_names_to_latin(data_mk)

    os.makedirs(results_path, exist_ok=True)
    pd.DataFrame(data, columns=["name"]).to_csv(os.path.join(results_path, "socio_institut.csv"))


if __name__ == "__main__":
    main()
