import os

import pandas as pd

from researcher_network_mk.utils import get_project_root
from researcher_network_mk.transliteration import transliterate_cyrillic_to_latin

# Function to transliterate Macedonian Cyrillic names to Latin letters
def translate_names_to_latin(names_mk):
    return [transliterate_cyrillic_to_latin(name) for name in names_mk]

def main():
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim", "arhitektonski")
# List of names in Macedonian Cyrillic
    data_mk = [
        "Елизабета Аврамовска",
        "Минас Бакалчев", 
        "Мирослав Грчев", 
        "Јасмина Сиљановска", 
        "Митко Хаџи Пуља", 
        "Анета Христова Поповска", 
        "Наташа Милованчев",
        "Михајло Зиноски", 
        "Елизабета Касапова", 
        "Огнен Марина", 
        "Дивна Пенчиќ", 
        "Страхиња Трпевски",
        "Ана Тромбева Гаврилоска",
        "Слободан Велевски",
        "Марија Мано Велевска",
        "Јован Ивановски",
        "Бојан Каранаков",
        "Александар Радевски",
        "Ана Ивановска Дескова",
        "Мери Батакоја",
        "Саша Тасиќ",
        "Димитар Папастеревски",
        "Горан Мицковски",
        "Александар Петровски",
        "Добре Николовски",
        "Благоја Бајковски",
        "Ѓорги Димков",
        "Филип Ценовски",
        "Лилјана Димевска",
        "Михајло Стојановски",
        "Кире Ставров",
        "Марија Петрова",
        "Теодора Михајловска",
        "Сања Аврамовска",
        "Ана Рафаиловска",
        "Елена Арсова",
        "Александар Петановски",
        "Димитар Крстевски",
        "Дарко Драгановски",
        "Теа Дамјановска"
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
