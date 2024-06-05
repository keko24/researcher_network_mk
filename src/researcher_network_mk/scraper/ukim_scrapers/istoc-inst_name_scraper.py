from transliterate import translit

# Function to transliterate names from Macedonian Cyrillic to Latin
def translate_names_to_latin(names_mk):
    return [translit(name, 'mk', reversed=True) for name in names_mk]
data_mk = [
    "Natasha Gjorgovska",
    "Nikola Pacinovski",
    "Nedeljka Nikolova",
    "Bone Palashevski",
    "Natasha Danilovska",
    "Tatjana Petkovska",
    "Tatjana P.-Mircevska",
    "Mirjana Menkovska",
    "Elizabeta Angelova",
    "Bone Palashevski",
    "Nikola Pacinovski",
    "Nedeljka Nikolova",
    "Natasha Gjorgovska",
    "Natasha Mateva",
    "Tosho Kostadinov",
    "Dejan Pendev",
    "Vasil Popovski"
]

data_latin = translate_names_to_latin(data_mk)

# Print the original and transliterated lists
print("Original names in Macedonian Cyrillic:")
print(data_mk)
print("\nTranslated names in Latin letters:")
print(data_latin)
