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
    "ќ": ["kj", "k", "ḱ"],
    "у": ["u"],
    "ф": ["f"],
    "х": ["h"],
    "ц": ["c"],
    "ч": ["ch", "c", "č"],
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
    combinations = trie.get_all_combinations()
    return '|'.join(combinations)

def transliterate_cyrillic_to_latin(names: str | list[str]):
    if isinstance(names, str):
        return translit(names, cyrillic_to_latin_map)
    elif isinstance(names, list):
        return [translit(name, cyrillic_to_latin_map) for name in names if isinstance(name, str)]
    else:
        raise TypeError("Argument names should be a string.")

def main():
    print(transliterate_cyrillic_to_latin("Вања Котевски"))

if __name__ == "__main__":
    main()
