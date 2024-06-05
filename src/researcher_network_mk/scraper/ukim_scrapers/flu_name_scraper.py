from transliterate import translit

# Function to transliterate names from Macedonian Cyrillic to Latin
def translate_names_to_latin(names_mk):
    return [translit(name, 'mk', reversed=True) for name in names_mk]

# List of names in Macedonian Cyrillic
data_mk = [
    "Благоја Маневски", "Антони Мазневски", "Жанета Вангели", "Ангел Миов", "Слободанка Стевческа", "Марија Сотировска Богдановска",
    "Беди Ибрахим", "Жарко Башески", "Исмет Рамиќевиќ", "Гоце Наневски", "Валентина Стевановска",
    "Славица Јанешлиева", "Ладислав Цветковски", "Игор Сековски", "Ана Спасова",
    "Јован Шумковски", "Фехим Хусковиќ", "Велимир Жерновски",
    "Натали Рајчиновска-Павлеска", "Роберт Јанкулоски"
]

# Transliterate the names
data_latin = translate_names_to_latin(data_mk)

# Print the original and transliterated lists
print("Original names in Macedonian Cyrillic:")
print(data_mk)
print("\nTranslated names in Latin letters:")
print(data_latin)
