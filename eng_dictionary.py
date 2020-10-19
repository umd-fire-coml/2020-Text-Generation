from enum import Enum, unique
from ModuleException import ModuleException


@unique
class word_class(Enum):
    """ Enums for tracking all word classes """
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


# The class for a word, stores the word itself and the class(es) it belongs to
class e_word:
    """
    The class that stores each English word

    Args:
        word: The string that stores actual word
        wc: The list that stores the possible word class(es) the word belongs to
    """
    def __init__(self, w: str):
        self.word = w
        self.wc = []
        self.__dict__ = {"word": self.word, "wc": self.wc}

    def __len__(self):
        """ return the length of the word"""
        return len(self.word)

    def __getitem__(self, item):
        """ Return the letters at specific indexes """
        return self.word[item]

    def __str__(self):
        """ Overwrites the original __str__ method """
        return f"[{self.word}, {self.wc}]"

    def __repr__(self):
        """ Overwrites the original __repr__ method """
        return f"[{self.word}, {self.wc}]"

    def add_wc(self, wc: list):
        """ Add specific word classes to this word """
        for i in wc:
            # Check if the class already exists
            if i not in self.wc:
                self.wc.append(i)

        # Overwrites its __dict__ property for easier serialization
        self.__dict__["wc"] = self.wc


class en_dict:
    """
    The class of english_dictionary
    Args:
        d: the dictionary object that stores all the words
    """
    def __init__(self):
        self.d = {}

    def add_word(self, word):
        """ Add a word into the dictionary """
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
        """ lookup a word to see if it's in the dictionary """
        return en_dict.__lookup(self.d, target, 0)

    @staticmethod
    def __lookup(present: dict, word: str, pos: int):
        if pos == len(word):
            if "word" in present.keys():
                return present["word"]
            else:
                return None
        else:
            if not word[pos].isalpha():
                return None
            if word[pos] in present.keys():
                return en_dict.__lookup(present[word[pos]], word, pos + 1)
            else:
                return None

    def add_all(self, other):
        """ Add the words from another en_dict object into this one """
        if type(other) is en_dict:
            self.__add_from_other(other.d)
        else:
            raise ModuleException("The argument should be an en_dict object!")

    def __add_from_other(self, other: dict):
        for i in other.keys():
            if i == "word":
                self.add_word(other[i])
            else:
                self.__add_from_other(other[i])
