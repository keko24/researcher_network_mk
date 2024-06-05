from transliterate import translit

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

# Function to transliterate Macedonian Cyrillic names to Latin letters
def translate_names_to_latin(names_mk):
    return [translit(name, 'mk', reversed=True) for name in names_mk]

# Transliterate the names
data_latin = translate_names_to_latin(data_mk)

# Print the original and transliterated lists
print("Original names in Macedonian Cyrillic:")
print(data_mk)
print("\nTranslated names in Latin letters:")
print(data_latin)
print(f"\nTotal count: {len(data_mk)}")
