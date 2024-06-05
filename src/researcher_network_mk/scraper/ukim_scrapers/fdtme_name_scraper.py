from transliterate import translit

# Function to transliterate names from Macedonian Cyrillic to Latin
def translate_names_to_latin(names_mk):
    return [translit(name, 'mk', reversed=True) for name in names_mk]

# List of names in Macedonian Cyrillic
data_mk = [
    "Константин Бахчеванџиев", "Ѓорги Груевски", "Горан Златески", "Борче Илиев",
    "Владимир Каранаков", "Владимир Кољозов", "Живка Мелоска", "Митко Нацевски",
    "Елена Никољски Паневски", "Бранко Рабаџиски", "Нацко Симакоски", 
    "Мира Станкевиќ Шуманска", "Зоран Трпоски", "Виолета Јакимовска Поповска"
]

# Transliterate the names
data_latin = translate_names_to_latin(data_mk)

# Print the original and transliterated lists
print("Original names in Macedonian Cyrillic:")
print(data_mk)
print("\nTranslated names in Latin letters:")
print(data_latin)
