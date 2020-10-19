import numpy as np
import sys
from matplotlib import pyplot as plt
import csv
import xml.etree.ElementTree as ET
#from nysk.xml

def __init__(self, doc_ids, batch_size=32, shuffle=True):
    'Initialization'
    self.batch_size = batch_size
    self.doc_ids = doc_ids
    self.shuffle = shuffle
    self.generate_doc_ids()
    self.on_epoch_end()

def generate_batch(self):
    'Creating a ElementTree with the xml file'
    data_tree = ET.parse('data/dataset/nysk.xml')
    data_root = data_tree.getroot()

    'Opens file for writing'
    word_set = open("WordDataset.txt", "w")

    'Finds all document tags and their corresponding text contents'
    for description in data_root.findall('document'):
        doc_text = description.find('text').text
        'Splits the description string content into individual words in a list'
        split_words = doc_text.split()
        for words in split_words:
            word_set.write(words + "\n")
    word_set.close()

def on_epoch_end(self):
    if self.shuffle == True:
        np.random.shuffle(self.doc_ids)