import os

import pandas as pd

from researcher_network_mk.utils import get_project_root
from researcher_network_mk.transliteration import transliterate_cyrillic_to_latin

# Function to transliterate Macedonian Cyrillic names to Latin letters
def translate_names_to_latin(names_mk):
    return [transliterate_cyrillic_to_latin(name) for name in names_mk]

def main():
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim")
# List of names in Macedonian Cyrillic
    data_mk = [
        "Добре Андов",
        "Винко Станоев",
        "Емилија Симеоновска",
        "Бранкица Спасевска",
        "Иво Митрушев",
        "Таска Симоновска",
        "Каролина Карајанкова",
        "Тоше Јорданов",
        "Биљана Дрвошанова",
        "Афродита Ибушовска",
        "Александар Марковски",
        "Ана Селамовска",
        "Виктор Ѓамовски",
        "Јулијана Цветковиќ",
        "Слободан Банџо",
        "Гордана Глаткова",
        "Катерина Банџо Орешковиќ",
        "Климе Белески",
        "Билјана Коруноска",
        "Душко Неделковски",
        "Љупчо Балулоски",
        "Милена Тасеска – Ѓорѓијевски",
        "Горан Миланов",
        "Розе Џољевска Миленковска",
        "Виктор Рајчин",
        "Христина Тришеска",
        "Христина Попоска",
        "Душко Мукаетов",
        "Марјан Андреевски",
        "Радмила Поповска",
        "Марија Ѓошева – Ковачевиќ",
        "Лазо Димитров",
        "Деспина Поповска Стојанов"
    ]

# Transliterate the names
    data = translate_names_to_latin(data_mk)

    os.makedirs(results_path, exist_ok=True)
    pd.DataFrame(data, columns=["name"]).to_csv(os.path.join(results_path, "zemjodelski_institut.csv"))

if __name__ == "__main__":
    main()
