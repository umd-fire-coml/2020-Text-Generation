import numpy as np
import sys
from matplotlib import pyplot as plt
import csv

def __init__(self, doc_ids, batch_size=32, shuffle=True):
    'Initialization'
    self.batch_size = batch_size
    self.doc_ids = doc_ids
    self.shuffle = shuffle
    self.generate_doc_ids()
    self.on_epoch_end()

def generate_doc_ids(self):
    

def on_epoch_end(self):
    if self.shuffle == True:
        np.random.shuffle(self.doc_ids)