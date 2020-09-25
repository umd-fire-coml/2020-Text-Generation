from bs4 import BeautifulSoup as bs
import requests
import re
import tqdm
import string
import zipfile
import os
import pickle

from eng_dictionary import en_dict, e_word, word_class


def fetch(url, base_dict=None, err_list=None):
    r = requests.get(url)
    s = bs(r.text, "html.parser")

    if base_dict is None:
        base_dict = en_dict()
    if err_list is None:
        err_list = []

    for i in tqdm.tqdm(s.find_all("p")):
        prop_match = re.search(r"<i>.*</i>", str(i))
        word_match = re.search(r"<b>.*</b>", str(i))
        if prop_match is None or word_match is None:
            continue

        prep = get_content(prop_match.group())
        word = get_content(word_match.group())

        t_list = []
        if "n." in prep:
            t_list.append(word_class.N)
        if "v." in prep:
            t_list.append(word_class.VERB)
        if "adj." in prep or "a" in prep:
            t_list.append(word_class.ADJ)
        if "adv." in prep:
            t_list.append(word_class.ADV)
        if "obj." in prep:
            t_list.append(word_class.P)
        if "prep." in prep:
            t_list.append(word_class.PP)
        if "conj." in prep:
            t_list.append(word_class.N)

        if len(t_list) == 0:
            err_list.append([word, prep])
            continue
        else:
            t_word = e_word(word)
            t_word.add_wc(t_list)

        base_dict.add_word(t_word)

    return base_dict, err_list


def get_content(raw: str):
    return raw[3: len(raw)-4]


def dict_downloader():
    b = None
    e = None
    for s in string.ascii_lowercase:
        print(f"Present letter: {s}")
        u = f"http://www.mso.anu.edu.au/~ralph/OPTED/v003/wb1913_{s}.html"
        b, e = fetch(u, base_dict=b, err_list=e)

    return b, e


def dataset_dounloader():
    file_name = "data.zip"
    extract_path = "data"

    if not os.path.isfile(file_name):
        print("Downloading")

        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00260/nysk.xml.zip"
        r = requests.get(url)

        with open(file_name, "wb") as f:
            f.write(r.content)
        print("Downloading finished, starts extracting")
    else:
        print("Compressed file already exists, starts extracting")

    if not os.path.isdir(extract_path):
        zf = zipfile.ZipFile(file_name)
        os.mkdir(extract_path)

        for n in zf.namelist():
            zf.extract(n, f"{extract_path}/")
        zf.close()
        print("Finished")
    else:
        print("Dataset already exists")


def downloader():
    dict_file_name = "en_dict.pickle"
    error_file_name = "error_list.pickle"

    base, error = dict_downloader()

    with open(dict_file_name, "wb") as f:
        pickle.dump(base, f)
    with open(error_file_name, "wb") as f:
        pickle.dump(error, f)

    dataset_dounloader()
    return


if __name__ == "__main__":
    # base, error = dict_downloader()
    downloader()
