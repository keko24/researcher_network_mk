from transliterate import translit

# Function to transliterate names from Macedonian Cyrillic to Latin
def translate_names_to_latin(names_mk):
    return [translit(name, 'mk', reversed=True) for name in names_mk]

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
data_latin = translate_names_to_latin(data_mk)

# Print the original and transliterated lists
print("Original names in Macedonian Cyrillic:")
print(data_mk)
print("\nTranslated names in Latin letters:")
print(data_latin)
