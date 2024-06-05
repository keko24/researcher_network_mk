from transliterate import translit

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
