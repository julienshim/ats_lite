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

def remove_old_jobs(job):
    [y, m, d] = list(map(lambda x: int(x), job[0].split('-')))
    jid = datetime(y, m, d)
    cod = get_date_n_weeks_ago()
    return jid >= cod

def load_previously_imported_jobs():
    with open(csv_output_path) as ref:
        data = [row for row in reader(ref)][1:]
        data = sorted(data, key=lambda x: x[0], reverse=True)
        data = list(filter(remove_old_jobs, data))
        # data = list(map(get_job_ref_date, data))
        return data