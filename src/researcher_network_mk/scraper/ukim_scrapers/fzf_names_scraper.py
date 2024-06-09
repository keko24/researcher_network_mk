import os

import pandas as pd

from researcher_network_mk.utils import get_project_root
from researcher_network_mk.transliteration import transliterate_cyrillic_to_latin

# Function to transliterate names from Macedonian Cyrillic to Latin
def translate_names_to_latin(names_mk):
    return [transliterate_cyrillic_to_latin(name) for name in names_mk]

def main():
    results_path = os.path.join(get_project_root(), "data", "researchers", "ukim", "filozofski")
# List of names in Macedonian Cyrillic
    data_mk = [
        "Иван Џепароски",
        "Бранислав Саркањац",
        "Ана Димишковска",
        "Дејан Донев",
        "Ристо Солунчев",
        "Вангел Ноневски",
        "Јасмина Поповска",
        "Марија Тодоровска",
        "Александар Атанасовски",
        "Ванчо Ѓорѓиев",
        "Далибор Јовановски",
        "Бобан Петровски",
        "Никола Жежов",
        "Борче Илиевски",
        "Тони Филипоски",
        "Војислав Саракински",
        "Никола Минов",
        "Стефан Пановски",
        "Виолета Ачкоска",
        "Наде Проева",
        "Маргарита Пешевска",
        "Даринка Пачемска Петреска",
        "Коста Аџиевски",
        "Љубен Лапе",
        "Воислав Кушевски",
        "Александар Апостолов",
        "Андрија Лаиновиќ",
        "Бранко Панов",
        "Владимир Алексеевич Мошин",
        "Димитар Димески",
        "Драган Велков – Гане",
        "Душица Петрушевска",
        "Кочо Сидовски",
        "Методија Манојловски",
        "Михајло Миноски",
        "Светозар Наумовски",
        "Славка Фиданова",
        "Стјепан Антолјак",
        "Томо Томоски",
        "Христо Андонов-Полјански",
        "Емил Димитриев",
        "Методија Соколоски",
        "Валериј Софрониевски",
        "Весна Димовска",
        "Весна Томовска",
        "Ратко Дуев",
        "Елена Џукеска",
        "Светлана Кочовска Стевовиќ",
        "Даниела Тошева Николовска",
        "Витомир Митевски",
        "Петар Хр. Илиевски",
        "Михаил Д. Петрушевски",
        "Даница Чадиковска",
        "Елена Колева",
        "Љубинка Басотова",
        "Маргарита Бузалковска-Алексова",
        "Јани Филовски",
        "Елена Зографска",
        "Борка Драгоевиќ-Јосифовска",
        "Елизабета Димитрова",
        "Драги Митревски",
        "Никос Чаусидис",
        "Анета Серафимова",
        "Снежана Филипова",
        "Татјана Филиповска",
        "Марјан Јованов",
        "Виктор Лилчиќ Адамс",
        "Антонио Јакимовски",
        "Ирена Теодора Весевска",
        "Ило Трајковски",
        "Антоанела Петковска",
        "Милева Ѓуровска",
        "Зоран Матевски",
        "Весна Димитриевска",
        "Константин Миноски",
        "Аница Драговиќ",
        "Татјана Стојаноска-Иванова",
        "Марија Дракуловска-Чукалевска",
        "Ивана Гегоска",
        "Емил Димитриев",
        "Виолета Петроска-Бешка",
        "Елена Ачковска-Лешковска",
        "Николина Кениг",
        "Огнен Спасовски",
        "Орхидеја Шурбановска",
        "Ана Фрицханд",
        "Билјана Блажевска Стоилковска",
        "Катерина Наумова",
        "Калина Сотироска Иваноска",
        "Маја Корубин Ќорлука",
        "Васка Лешоска",
        "Зоран Нацев",
        "Билјана Ванковска",
        "Марина Митревска",
        "Лидија Георгиева",
        "Оливер Бакрески",
        "Тони Милески",
        "Зорица Салтировска",
        "Рина Киркова-Танеска",
        "Горан Зенделовски",
        "Тања Милошевска",
        "Сергеј Цветковски",
        "Марјан Ѓуровски",
        "Александар Павлески",
        "Митко Котовчевски",
        "Синиша Даскаловски",
        "Ванчо Кенков",
        "Сунчица Димитријоска",
        "Маја Геровска-Митев",
        "Сузана Борнарова",
        "Иван Трајков",
        "Наташа Богоевска",
        "Светлана Трбојевиќ",
        "Софија Георгиевска",
        "Владимир Илиевски",
        "Јован Пејковски",
        "Мариа Доневска",
        "Дивна Лакинска",
        "Димитрија Трајковски",
        "Даринка Пачемска Петреска",
        "Коста Аџиевски",
        "Љубен Лапе",
        "Воислав Кушевски",
        "Александар Апостолов",
        "Андрија Лаиновиќ",
        "Бранко Панов",
        "Владимир Алексеевич Мошин",
        "Димитар Димески",
        "Драган Велков – Гане",
        "Душица Петрушевска",
        "Кочо Сидовски",
        "Методија Манојловски",
        "Михајло Миноски",
        "Светозар Наумовски",
        "Славка Фиданова",
        "Стјепан Антолјак",
        "Томо Томоски",
        "Христо Андонов-Полјански",
        "Христо Меловски",
        "Методија Соколоски",
        "Денко Скаловски",
        "Сузана Симоновска",
        "Боби Бадаревски",
        "Наташа Таневска",
        "Владимир Давчев",
        "Македонка Радуловиќ",
        "Ирена Авировиќ Бундалевска",
        "Ангелка Кескинова"
    ]

# Transliterate the names
    data = data_mk

    os.makedirs(results_path, exist_ok=True)
    df = pd.DataFrame(data, columns=["name"])
    df["processed"] = False
    df.to_csv(os.path.join(results_path, "researchers.csv"))


if __name__ == "__main__":
    main()