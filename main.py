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

previously_imported_jobs_path = csv_output_path
previously_imported_jobs_path_exists = path.exists(previously_imported_jobs_path)
previously_imported_jobs = [] if not previously_imported_jobs_path_exists else load_previously_imported_jobs()
previously_imported_jobs_len = len(previously_imported_jobs)
csv_write_mode = 'w'

def job_is_previously_imported(target_job_reference_no):
    if len(previously_imported_jobs) == 0:
        return False
    
    for item in previously_imported_jobs:
        [import_date, job_reference_no, job_title, department, location, summary, key_qualifications, description, education_experience, base_pay_lower, base_pay_upper, base_pay_type, job_posting_url] = item
        if target_job_reference_no == job_reference_no:
            return True
        
    return False

def get_soup(page_number):
    locations = get_target_locations()
    response = get(f'')
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup
