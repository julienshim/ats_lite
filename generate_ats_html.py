# nltk
import nltk

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.util import ngrams

## built-in libraries
from csv import reader
from re import IGNORECASE, findall, sub
from json import dump
from os import system

## settings
from src.settings_ats import target_part_of_speech, fdist_count, ngram_number, ngram_min_count, user_defined_stop_words, resume_txt_path
from src.settings_results import csv_output_path
from src.functions import generate_html_doc

def findNgrams(text, n):
    ngs = []
    text = sent_tokenize(text)
    for line in text:
        token = nltk.word_tokenize(line)
        ng = list(ngrams(token, n))
        ngs.extend(ng)
    return ngs

def filter_ngrams(tup):
    for el in tup[0]:
        if el in stop_words:
            return False
    if tup[1] < ngram_min_count:
        return False
    return True