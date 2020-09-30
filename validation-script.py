import pickle
import string
import xml.etree.ElementTree as ET

from file_downloader import en_dict


def load_dict():
    ed = en_dict()
    path = "data/en_dictionary/"
    for letter in string.ascii_lowercase:
        print(f"now loading letter {letter}")
        f_name = f"{path}dict_{letter}.pickle"
        try:
            with open(f_name, "rb") as f:
                temp_ed  = pickle.load(f)
                ed.add_all(temp_ed)
        except IOError or ImportError:
            print(f"Exception occured at letter {letter}")
            continue
        print(f"finished loading letter {letter}")

    return ed


def load_dataset():
    try:
        print("Loading dataset")
        r = ET.parse("data/dataset/nysk.xml")
        print("Finished")
        return r
    except Exception as e:
        print("Error occurred while loading dataset")
        print(e)
        return None


if __name__ == "__main__":
    load_dict()
    load_dataset()
