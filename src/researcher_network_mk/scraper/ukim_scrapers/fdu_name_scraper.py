import os

import pandas as pd

from researcher_network_mk.transliteration import transliterate_cyrillic_to_latin
from researcher_network_mk.utils import get_project_root


# Function to transliterate names from Macedonian Cyrillic to Latin
def translate_names_to_latin(names_mk):
    return [transliterate_cyrillic_to_latin(name) for name in names_mk]


def main():
    results_path = os.path.join(
        get_project_root(), "data", "researchers", "ukim", "dramski"
    )

    # List of names in Macedonian Cyrillic
    data_mk = [
        "Рефет Абази",
        "Сенка Анастасова",
        "Зоја Бузалковска",
        "Игор Вецовски",
        "Небојша Вилиќ",
        "Ељеса Касо",
        "Сузана Киранџиска",
        "Антонио Митриќески",
        "Сашко Насев",
        "Кренаре Невзати",
        "Лазар Секуловски",
        "Маја Стевановиќ",
        "Тихомир Стојановски",
        "Ана Стојаноска",
        "Синоличка Трпкова Мелес",
        "Горан Трпчевски",
        "Деспина Ангеловска",
        "Валентина Божиновска",
        "Борјан Зафировски",
        "Бесфорт Идризи",
        "Дејан Илиев",
        "Атила Клинче",
        "Сашо Кокаланов",
        "Кристина Леловац",
        "Никола Настоски",
        "Владимир Павловски",
        "Хисмет Рамадани",
        "Илија Циривири",
        "Даниел Велјановски",
        "Ангелчо Илиевски",
        "Милан Тоциновски",
        "Марија Апчевска",
        "Батухан Ибрахим",
        "Ѓорче Ставрески",
        "Христина Цветаноска Станковска",
        "Владимир Блажевски",
        "Русомир Богдановски",
        "Димитар Грбевски",
        "Костадин Дрваров",
        "Јелена Лужина",
        "Владимир Милчин",
        "Мартин Панчевски",
        "Нада Петковска",
        "Стојан Попов",
        "Кирил Ристоски",
        "Златко Славенски",
        "Мими Таневска-Србиновска",
        "Апостол Трпески",
        "Слободан Унковски",
        "Владо Цветановски",
        "Данчо Чеврески",
        "Куштрим Бектеши",
        "Павлина Митева",
        "Маја Бојазиевска",
        "Беди Ибрахим",
        "Дарија Андовска",
        "Бобан Карапејовски",
        "Весна Ѓиновска Илкова",
        "Александар Рашковиќ",
        "Соња Каранџуловска",
        "Александар Степанулески",
        "Мурат Жерка",
        "Шенај Мандак",
        "Деа Пајазити",
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
