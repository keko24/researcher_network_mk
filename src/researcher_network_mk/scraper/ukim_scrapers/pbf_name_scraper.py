from transliterate import translit

# Function to transliterate names from Macedonian Cyrillic to Latin
def translate_names_to_latin(names_mk):
    return [translit(name, 'mk', reversed=True) for name in names_mk]

# List of names in Macedonian Cyrillic
data_mk = [
    "Ѓоко Ѓорѓевски", "Милан Ѓорѓевиќ", "Дејан Борисов", "Анета Јовковска", 
    "Виктор Недески", "Дарко Анев", "Кирче Трајанов", "Илче Мицевски", 
    "Стефан Гоговски", "Александар Крстаноски", "Марија Гиревска", 
    "Николче Ѓурѓиновски", "Борче Грамбозов"
]

# Transliterate the names
data_latin = translate_names_to_latin(data_mk)

# Print the original and transliterated lists
print("Original names in Macedonian Cyrillic:")
print(data_mk)
print("\nTranslated names in Latin letters:")
print(data_latin)
