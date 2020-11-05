import random

import numpy
# import sys
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords


class Debug:
    def __init__(self, debug_mode=True):
        self.debug_mode = debug_mode
        self.flag = {}

    def log(self, target, flag=None):
        if self.debug_mode:
            if flag is None:
                print(target)
            else:
                if flag in self.flag.keys():
                    if self.flag[flag]:
                        print(target)

    def set_flag(self, flag: str, val: bool):
        self.flag[flag] = val


def tokenize_words(input_text: str):
    input_text = input_text.lower()

    tz = RegexpTokenizer(r'\w+')
    tokens = tz.tokenize(input_text)

    while True:
        try:
            filtered = filter(token_check, tokens)
            res = " ".join(filtered)
            break
        except LookupError:
            print("Resource 'stopwords' not found. Attempts to download")
            import nltk
            nltk.download('stopwords')
    return res


def token_check(target):
    return target not in stopwords.words('english')


def main_func():
    debug = Debug(False)

    file = open("data/dataset/test.txt").read()

    processed_text = tokenize_words(file)
    debug.log(processed_text)

    chars = sorted(list(set(processed_text)))
    char_to_num = dict((c, i) for i, c in enumerate(chars))

    debug.log(chars)
    debug.log(char_to_num)

    input_len = len(processed_text)
    vocab_len = len(chars)

    debug.log(f"Total number of characters: {input_len}")
    debug.log(f"Total vocab: {vocab_len}")

    seq_length = 100
    x_data = []
    y_data = []

    # loop through inputs, start at the beginning and go until we hit
    # the final character we can create a sequence out of
    for i in range(0, input_len - seq_length, 1):
        # Define input and output sequences
        # Input is the current character plus desired sequence length
        in_seq = processed_text[i:i + seq_length]

        # Out sequence is the initial character plus total sequence length
        out_seq = processed_text[i + seq_length]

        debug.log(processed_text[i:i + seq_length])
        debug.log(processed_text[i + seq_length])
        debug.log("=================")

        # We now convert list of characters to integers based on
        # previously and add the values to our lists
        x_data.append([char_to_num[char] for char in in_seq])
        y_data.append(char_to_num[out_seq])

    debug.log(x_data)
    debug.log(y_data)

    num_patterns = len(y_data)
    debug.log(f"Number of patterns: {num_patterns}")

    processed_x = numpy.reshape(x_data, (num_patterns, seq_length, 1))
    processed_x = processed_x/float(vocab_len)

    debug.log(len(processed_x))
    debug.log(len(processed_x[0]))

    processed_y = np_utils.to_categorical(y_data)

    model = Sequential()
    model.add(LSTM(256, input_shape=(processed_x.shape[1], processed_x.shape[2]), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(256, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(128))
    model.add(Dropout(0.2))
    model.add(Dense(processed_y.shape[1], activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam')

    filepath = "model_weights_saved.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
    desired_callbacks = [checkpoint]

    model.fit(processed_x, processed_y, epochs=2, batch_size=256, callbacks=desired_callbacks)

    num_to_char = dict((i, c) for i, c in enumerate(chars))

    start = random.randint(0, len(x_data) - 1)
    pattern = processed_x[start]
    print("Random Seed:")
    print("\"", ''.join([num_to_char[value] for value in pattern]), "\"")


def test_func():
    pass


if __name__ == '__main__':
    main_func()
