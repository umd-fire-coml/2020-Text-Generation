# coding = utf-8
import os
import re
import tqdm
import xml.etree.ElementTree as ET


class GeneratorExceptions(Exception):
    """
    The Exception class for tracking all exceptions raised in data generator
    Param
        text: the displayed text
    """
    def __init__(self, text: str):
        self.text = text


class DataGenerator:
    def __init__(self, dataset_file_path : str="data/dataset/nysk.xml", processed_dataset_path: str ="data/processed_dataset/"):
        self.dataset_file_path = dataset_file_path
        self.processed_dataset_path = processed_dataset_path
        self.preprocess_data(override=False)

    def preprocess_data(self, override=False):
        if os.path.isfile(self.dataset_file_path):
            if not os.path.isdir(self.processed_dataset_path):
                os.mkdir(self.processed_dataset_path)

            res = os.listdir(self.processed_dataset_path)

            with open(self.dataset_file_path, "r", encoding="utf-8") as f:
                doc = ET.ElementTree(file=f)

            root = doc.getroot()
            print(len(root))

            for item in tqdm.tqdm(root):
                news_id = item.findtext('docid')
                source = item.findtext('source')
                url = item.findtext('url')
                title = item.findtext('title')
                summary = item.findtext('summary')
                text = item.findtext('text')

                title = re.sub(r"<.*>", "", title)
                title = re.sub(r"\W", "_", title)
                title = f"{news_id}_{title[:10]}"

                fp = f"{self.processed_dataset_path}{title}.txt"
                if not os.path.isfile(fp) or override:
                    with open(fp, 'w', encoding='utf-8') as f:
                        f.write(text)
        else:
            raise GeneratorExceptions("Path doesn't exist")

    def process_data(self):



with open("data/dataset/1.txt", 'w', encoding='utf-8') as f:
    f.write("aaaaa")
dg = DataGenerator()
print(dg.processed_dataset_path)
