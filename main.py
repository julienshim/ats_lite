# built-in libraries
from re import compile, split
from time import sleep
from os import path
from csv import reader, writer
from datetime import datetime

# third-party libraries
from requests import get
from bs4 import BeautifulSoup

# results processing
from src.settings_results import ignore, csv_output_path, seconds_range_between_fetch
from src.functions import get_job_posting_details, get_target_locations, get_date_n_weeks_ago

