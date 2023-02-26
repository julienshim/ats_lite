from requests import get
from bs4 import BeautifulSoup
from re import compile, split
from random import randint
from time import sleep
from os import path
from csv import reader, writer

def get_soup(page_number):
    response = get('')
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup
