import os

import pandas as pd

from researcher_network_mk.utils import get_project_root
from researcher_network_mk.transliteration import transliterate_cyrillic_to_latin

# Function to transliterate Macedonian Cyrillic names to Latin letters
def translate_names_to_latin(names_mk):
    return [transliterate_cyrillic_to_latin(name) for name in names_mk]

def main():
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim")
    data_mk = [
        # From "redovni-profesori"
        "Велимир Стојковски",
        "Тони Довенски",
        "Влатко Илиески",
        "Владимир Петков",
        "Пламен Тројачанец",
        "Зехра Хајрулаи-Муслиу",
        "Ромел Велев",
        "Дине Митров",
        "Игор Улчар",
        "Благица Сековска",
        "Павле Секуловски",
        "Славчо Мреношки",
        "Лазо Пендовски",
        "Јована Стефановска",
        "Флорина Поповска-Перчиниќ",
        "Василка Попоска-Треневска",
        "Деан Јанкулоски",

        # From "vonredni-profesori"
        "Александар Додовски",
        "Трпе Ристоски",
        "Ирена Целеска",
        "Никола Адамов",
        "Бранко Атанасов",
        "Ксенија Илиевска",
        "Игор Џаџовски",
        "Кирил Крстевски",
        "Искра Цветковиќ",
        "Радмила Чрчева-Николовска",
        "Сандра Мојсова",
        "Мирко Проданов",

        # From "docenti"
        "Ивица Ѓуровски",
        "Мартин Николовски",
        "Ристо Узунов",
        "Мирослав Ќосевски",
        "Елена Атанаскова",

        # From "istrazhuvachi"
        "Елизабета Димитриеска Стојковиќ",
        "Катерина Благоевска",
        "Билјана Стојановска Димзоска",
        "Игор Есмеров",
        "Александра Ангелевска",
        "Александар Цветковиќ",
        "Бранко Ангеловски",
        "Љупчо Мицков",

        # From "sorabotnici"
        "Љупчо Ангеловски",
        "Душица Коцева",
        "Катерина Давчева",
        "Љубица Рашиќ",
        "Александар Јаневски",
        "Моника Довенска",
        "Ана Цветановска",
        "Гордана Илиевска",
        "Загорка Попова",
        "Вангелица Енимитева",
        "Снежана Димитровска",
        "Стефанија Маркозанова",
        "Томе Несторовски",
        "Стефан Јованов",
        "Димитар Божиновски",
        "Александар Трајчовски",
        "Филип Тројачанец",
        "Панче Игновски",
        "Зоран Димитровски",
        "Ана Галевска",
        "Лариса Шаќири",

        # From the additional snippet
        "Слободен Чокревски"
    ]

# Transliterate the names
    data = translate_names_to_latin(data_mk)

    os.makedirs(results_path, exist_ok=True)
    pd.DataFrame(data, columns=["name"]).to_csv(os.path.join(results_path, "veterina.csv"))


if __name__ == "__main__":
    main()
