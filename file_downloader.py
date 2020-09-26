from bs4 import BeautifulSoup as bs
import requests
import re
import tqdm
import string
import zipfile
import os
import pickle

from eng_dictionary import en_dict, e_word, word_class


def fetch(letter: str, base_dict=en_dict(), err_list=None):
    """ Fetch the dictionary for the letter provided

    Args:
        letter: All words started with this letter will be downloaded
        base_dict: The base en_dictionary object
        err_list: The error list that is used to store all words that doesn't have a word class

    Returns:
        return the base en_dictionary object and the error list

    """
    if err_list is None:
        err_list = []

    # Get the HTML response
    url = f"http://www.mso.anu.edu.au/~ralph/OPTED/v003/wb1913_{letter}.html"
    r = requests.get(url)
    s = bs(r.text, "html.parser")

    # Analyze the document and find specific contents using regex
    for i in tqdm.tqdm(s.find_all("p")):
        prop_match = re.search(r"<i>.*</i>", str(i))
        word_match = re.search(r"<b>.*</b>", str(i))
        if prop_match is None or word_match is None:
            continue

        # Get the actual content, without HTML tags
        prep = get_content(prop_match.group())
        word = get_content(word_match.group())

        # Analyze the possible classes of the words and assign it to a list
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

        # if it doesn't have any proper class then add it into the error_list
        if len(t_list) == 0:
            err_list.append([word, prep])
            continue
        # Otherwise create a new e_word object to store it
        else:
            t_word = e_word(word)
            t_word.add_wc(t_list)

        base_dict.add_word(t_word)

    return base_dict, err_list


#
def get_content(raw: str):
    """ Get the actual contents from the HTML element """
    return raw[3: len(raw)-4]


def dict_downloader(overwrite=False):
    """ The downloader for english dictionary

    Args:
        overwrite: When it's True, the function overwrites the original file is the file exists,
                   otherwise it skips that file

    Returns:
        Return the english_dictionaary object (An en_dict object)
    """
    e = None
    data_dir = "data/en_dictionary/"

    # Create the dir if not exist
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)

    # iterate through all letters and download the dictionary
    for s in string.ascii_lowercase:
        f_name = f"{data_dir}dict_{s}.pickle"
        print(f"Present letter: {s}")

        # Check if file exists
        if not os.path.isfile(f_name) or overwrite:
            temp, e = fetch(s, err_list=e)

            with open(f_name, "wb") as f:
                pickle.dump(temp, f)
        else:
            print(f"Dict pickle file '{f_name}' already exist")
    return e


def dataset_downloader(overwrite=False):
    """
    Args:
        overwrite: When it's True, the function overwrites the original file is the file exists,
                   otherwise it skips that file

    Returns:
        Doesn't return anythings
    """
    file_name = "data.zip"
    extract_path = "data/dataset/"

    if not os.path.isdir(extract_path):
        os.mkdir(extract_path)

    if not os.path.isfile(file_name):
        print("Downloading")

        # Get the response and download the file
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00260/nysk.xml.zip"
        r = requests.get(url)

        with open(file_name, "wb") as f:
            f.write(r.content)
        print("Downloading finished, starts extracting")
    else:
        print("Compressed file already exists, starts extracting")

    # Check if target file exists
    if not os.path.isfile(f"{extract_path}{file_name}") or overwrite:
        zf = zipfile.ZipFile(file_name)
        if not os.path.isdir(extract_path):
            os.mkdir(extract_path)

        for n in zf.namelist():
            zf.extract(n, f"{extract_path}/")
        zf.close()
        print("Finished")
    else:
        print("Dataset already exists")


def downloader():
    """ Main method for download all required files """
    error_file_name = "data/en_dictionary/error_list.pickle"

    error = dict_downloader()

    with open(error_file_name, "wb") as f:
        pickle.dump(error, f)

    dataset_downloader()
    return


if __name__ == "__main__":
    downloader()
