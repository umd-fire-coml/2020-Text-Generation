# 2020-Text-Generation
2020-Text-Generation was developed by [Chenyu Zhang](czhang21@terpmail.umd.edu), [Stefan Obradovic](sobrad@umd.edu), [Joseph Chan](jchan123@terpmail.umd.edu), and [Noah Grinspoon](ngrinspoon@gmail.com) in the [Capital One Machine Learning Stream](https://www.fire.umd.edu/coml) for the University of Maryland First-Year Innovation & Research Experience (FIRE) program with help from senior peer mentor [Derek Zhang](dzhang21@terpmail.umd.edu) and overseen by [Dr. Raymond Tu](https://huahongtu.me/).

A [video](https://www.youtube.com/watch?v=-vTMY6ZG2iI) of the project was presented at the College Park [FIRE Summit](https://www.fire.umd.edu/summit) on Monday, November 16, 2020.

# Abstract
As technology continues to advance, it is our job as programmers to figure out how to use and optimize that kind of technology for machine learning. When we talk about machine learning, we look at the way machines operate to perform tasks for advanced security purposes or for every day use. For example, machine learning uses face recognition for added security purposes and can also be used to create self-driving cars using object detection. Machine learning can also be used for detecting and predicting text patterns to help optimize typing time, create chatbots, and automatically generate text. The goal of our research is to create a model that predicts a complete sentence given a text input. We train a Recurrent Neural Network model to learn the English language based on hundreds of news articles (https://archive.ics.uci.edu/ml/datasets/NYSK), and the model considers the order in which words are sequenced in a sentence rather than just the words themselves. All the data gets downloaded and each news article gets parsed into its own txt document, which removes all punctuations and stop words (common words like "the" and "and") and sees if every word is a valid english word by cross-referencing the English dictionary. Every sentence is then converted into a vector representation known as a "bag of words" which shows the frequency of each word. The data generator trains the model on only a couple of text documents to not waste too much memory in RAM. After training, we can give the model a sentence (vector) and it will give a prediction of what the next sentence will be.

# Description
The aim of this project is to create a Machine Learning Model that generates output sentences given an input sentence by training a [Recurrent Neural Network (RNN) Model](https://en.wikipedia.org/wiki/Recurrent_neural_network) on hundreds of news articles about New York v. Strauss-Kahn, a case relating to allegations of sexual assault against the former IMF director Dominique Strauss-Kahn. After training the model, a user can give the model an input sentence and the machine learning model will automatically generate a sentence as output.

Recurrent Neural Networks(RNN) are state of the art deep learning algorithms for sequential data like text. This is because they can remember their previous inputs in memory (using Long-Short Term Memory (LSTM)). As such, we train a model to learn the sequence in which words (encodded as vectors) appear in a sentence and then generate text by sequentially predicting the next best word given the previous sequence of words.

### Model Architecture:
Our model consists of an input layer where each token (character) in the input sentence is used an an input. An LSTM layer that learns the sequence of the tokens (characters) as words. A second input layer, where each learned word is used as an input. A second LSTM layer that learns the sequence of the words. And then a Dense layer with Softmax Activation that transforms the outputs of the model to probability values. 
 

# Getting Started
## Example Notebooks:
* The file `copy_training_USE_THIS_ONE.ipynb` is a python notebook that demonstrates how to use the data generator to download the data and process it as input to train the model. It also tests the trained model by providing input sentences and outputting the generated sentences from the model.

## Running the Project:
* Environment
   * `environment.yml`
   * `env_checker.sh`
   * `PackageChecker.ipynb`

* Data Checker
   * `data_checker_script.py`
   * `file_downloader.py`
   * `word_lookup.py`
   * `validation_script.py`
   * `validation-script.py`
   * `data.zip`
   * `eng_dictionary.py`
   * `Data_Viz.ipynb`

* Data Processor
   * `data_generator.py`

* Model Builder
   * `model.py`

* Training the Model
   * `training.ipynb`

* Testing the Model
   * `copy_training_USE_THIS_ONE.ipynb`
