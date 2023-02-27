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

def parse_job_item(job_item):
    position = job_item.find('a', {'id': compile(r'jotTitle_PIPE-[0-9]{1,}')})
    job_title = position.text
    job_href = position["href"]
    job_link = ''
    job_reference = job_href.split('/')[3]
    department = job_item.find('span', {'class': compile(r'table--advanced-search__role')}).text
    date = job_item.find('span', {'class': compile(r'table--advanced-search__date')}).text
    [month, day, year] = split(r'[ ,]{1,}', date)
    location = job_item.find('span', {'id': compile(r'storeName_container_PIPE-[0-9]{1,}')}).text