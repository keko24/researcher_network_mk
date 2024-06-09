import re

cyrillic_to_latin_map = {
    "а": ["a"],
    "б": ["b"],
    "в": ["v"],
    "г": ["g"],
    "д": ["d"],
    "ѓ": ["gj", "g", "ǵ"],
    "е": ["e"],
    "ж": ["zh", "z", "ž"],
    "з": ["z"],
    "ѕ": ["dz"],
    "и": ["i"],
    "ј": ["j"],
    "к": ["k"],
    "л": ["l"],
    "љ": ["lj", "l"],
    "м": ["m"],
    "н": ["n"],
    "њ": ["nj", "n"],
    "о": ["o"],
    "п": ["p"],
    "р": ["r"],
    "с": ["s"],
    "т": ["t"],
    "ќ": ["kj", "k", "ḱ", "ch", "c", "č"],
    "у": ["u"],
    "ф": ["f"],
    "х": ["h"],
    "ц": ["c"],
    "ч": ["ch", "c", "č", "kj", "k", "ḱ"],
    "џ": ["dz", "dj", "dž", "dzh"],
    "ш": ["sh", "s", "š"],
    "А": ["A"],
    "Б": ["B"],
    "В": ["V"],
    "Г": ["G"],
    "Д": ["D"],
    "Ѓ": ["Gj", "G", "Ǵ"],
    "Е": ["E"],
    "Ж": ["Zh", "Z", "Ž"],
    "З": ["Z"],
    "Ѕ": ["Dz"],
    "И": ["I"],
    "Ј": ["J"],
    "К": ["K"],
    "Л": ["L"],
    "Љ": ["Lj", "L"],
    "М": ["M"],
    "Н": ["N"],
    "Њ": ["Nj", "N"],
    "О": ["O"],
    "П": ["P"],
    "Р": ["R"],
    "С": ["S"],
    "Т": ["T"],
    "Ќ": ["Kj", "K", "Ḱ"],
    "У": ["U"],
    "Ф": ["F"],
    "Х": ["H"],
    "Ц": ["C"],
    "Ч": ["Ch", "C", "Č"],
    "Џ": ["Dz", "Dj", "Dž", "Dzh"],
    "Ш": ["Sh", "S", "Š"],
}

def split_surnames(name):
    if "Хаџи" not in name and "хаџи" not in name:
        name = name.replace(" - ", " ").replace("-", " ")
    else:
        name = name.replace(" - ", "-")
    name_split = name.split(" ")
    if len(name_split) > 2:
        first_name, first_surname, second_surname = name_split
        return [f"{first_name} {first_surname}-{second_surname}", f"{first_name} {second_surname}-{first_surname}", f"{first_name} {first_surname} {second_surname}", f"{first_name} {second_surname} {first_surname}", f"{first_name} {first_surname}", f"{first_name} {second_surname}"]
    else:
        return [name]

def replace_and_strip_spaces(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

class Trie:
    def __init__(self, name: str, map: dict[str, list[str]]) -> None:
        self.map = map
        self.set_trie(name)

    def get_all_combinations(self):
        return self.forward(0)

    def forward(self, idx) -> list[str]:
        if len(self.trie) <= idx: 
            return [""]
        prefixes = self.trie[idx]
        suffixes = self.forward(idx + 1)
        names = ([prefix + suffix for prefix in prefixes for suffix in suffixes])
        return names

    def set_trie(self, name):
        self.trie = [self.map[char] if char in self.map else [char] for char in name]

def translit(name, map):
    trie = Trie(name, map)
    return trie.get_all_combinations()

def transliterate_cyrillic_to_latin(name: str):
    name = replace_and_strip_spaces(name)
    name_variations = split_surnames(name)
    return [item for name_variation in name_variations for item in translit(name_variation, cyrillic_to_latin_map)]

def main():
    print(transliterate_cyrillic_to_latin("Бошко Петров-Чукалиев"))

if __name__ == "__main__":
    main()