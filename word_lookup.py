import os
import sys

from PyDictionary import PyDictionary as pdict
from tqdm import tqdm


class stdout_helper:
    def __init__(self):
        self.orig_out = sys.stdout
        self.alter = open(os.devnull, 'w')

    def suppress(self):
        sys.stdout = self.alter

    def resume(self):
        sys.stdout = self.orig_out

    def finalize(self):
        self.alter.close()


def text_packer(raw: str):
    edt = pdict()
    res = []

    sh = stdout_helper()
    w_list = raw.split(" ")
    for w in tqdm(w_list):
        sh.suppress()
        m = edt.meaning(w.lower())
        sh.resume()
        if m is not None:
            res.append(w.lower())

    return res
