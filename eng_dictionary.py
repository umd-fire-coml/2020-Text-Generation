from enum import Enum, unique


@unique
class word_class(Enum):
    N = "Noun"
    VERB = "Verb"
    ADJ = "Adjective"
    ADV = "Adverb"
    P = "Pronoun"
    PP = "Preposition"
    CONJ = "Conjunction"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other.value


class e_word:
    def __init__(self, w: str):
        self.word = w
        self.wc = []
        self.__dict__ = {"word": self.word, "wc": self.wc}

    def __len__(self):
        return len(self.word)

    def __getitem__(self, item):
        return self.word[item]

    def __str__(self):
        return f"[{self.word}, {self.wc}]"

    def __repr__(self):
        return f"[{self.word}, {self.wc}]"

    def add_wc(self, wc: list):
        for i in wc:
            if i not in self.wc:
                self.wc.append(i)
        self.__dict__["wc"] = self.wc


class en_dict:
    def __init__(self):
        self.d = {}

    def add_word(self, word):
        if type(word) is e_word:
            self.__add_to_dict(self.d, word, 0)
        elif type(word) is list:
            for i in word:
                en_dict.__add_to_dict(self.d, i, 0)

    @staticmethod
    def __add_to_dict(present: dict, temp_word: e_word, pos: int):
        if len(temp_word) == pos:
            if "word" in present.keys():
                present["word"].add_wc(temp_word.wc)
            else:
                present["word"] = temp_word
        else:
            if temp_word[pos] in present.keys():
                en_dict.__add_to_dict(present[temp_word[pos]], temp_word, pos + 1)
            else:
                t = {"word": temp_word}
                for i in range(1, len(temp_word) - pos):
                    t = {temp_word[-i]: t}
                present[temp_word[pos]] = t

    def lookup_word(self, target: str):
        return en_dict.__lookup(self.d, target, 0)

    @staticmethod
    def __lookup(present: dict, word: str, pos: int):
        if pos == len(word):
            if "word" in present.keys():
                return True
            else:
                return False
        else:
            if not word[pos].isalpha():
                return False
            if word[pos] in present.keys():
                return en_dict.__lookup(present[word[pos]], word, pos + 1)
            else:
                return False


if __name__ == "__main__":
    ed = en_dict()
    # ed.add_word(["apple", "bad", "sharp"])
    # ed.add_word([e_word("apple"),
    #              e_word("bad"),
    #              e_word("sharp")])
    print(ed.d)

    print(ed.lookup_word("apple"))
    print(ed.lookup_word("app"))
