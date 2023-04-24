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

class JobItem:
    global ignore

    def __init__(self, import_date, job_reference_no, job_title, department, location, summary, key_qualifications, description, education_experience, base_pay_lower, base_pay_upper, base_pay_type, job_posting_url, is_previously_imported):
        self.import_date = import_date
        self.job_reference_no = job_reference_no
        self.job_title = job_title
        self.department = department
        self.location = location
        self.summary = summary
        self.key_qualifications = key_qualifications
        self.description = description
        self.education_experience = education_experience
        self.base_pay_lower = base_pay_lower
        self.base_pay_upper = base_pay_upper
        self.base_pay_type = base_pay_type
        self.job_posting_url = job_posting_url
        self.is_previously_imported = is_previously_imported

    def is_irrelevant(self):
        [year, month, day] = list(map(lambda x: int(x), self.import_date.split('-')))
        job_import_datetime = datetime(year, month, day)
        n_weeks_ago_datetime = get_date_n_weeks_ago()
        return job_import_datetime >= n_weeks_ago_datetime and self.department not in ignore['department'] and self.location not in ignore['location']

    def get_write_row(self):
        return [self.import_date, self.job_reference_no, self.job_title, self.department, self.location, self.summary, self.key_qualifications, self.description, self.education_experience, self.base_pay_lower, self.base_pay_upper, self.base_pay_type, self.job_posting_url]

def convert_imported_jobs_to_job_items(data_body, is_previously_imported):
    job_items = []
    for row in data_body:
        [import_date, job_reference_no, job_title, department, location, summary, key_qualifications, description, education_experience, base_pay_lower, base_pay_upper, base_pay_type, job_posting_url] = row
        new_job_item = JobItem(import_date, job_reference_no, job_title, department, location, summary, key_qualifications, description, education_experience, base_pay_lower, base_pay_upper, base_pay_type, job_posting_url, is_previously_imported)
        job_items.append(new_job_item)
    return job_items

def load_previously_imported_jobs():
    with open(csv_output_path) as input_csv:
        data = [row for row in reader(input_csv)]
        # data_header = data[0]
        data_body = data[1:]
        previously_imported_job_items = convert_imported_jobs_to_job_items(data_body, True)
        previously_imported_job_items = sorted(previously_imported_job_items, key=lambda x: x.import_date, reverse=True)
        previously_imported_job_items = list(filter(lambda x: x.is_irrelevant(), previously_imported_job_items)) 
        return previously_imported_job_items

previously_imported_jobs_path = csv_output_path
previously_imported_jobs_path_exists = path.exists(previously_imported_jobs_path)
previously_imported_jobs = [] if not previously_imported_jobs_path_exists else load_previously_imported_jobs()
previously_imported_jobs_len = len(previously_imported_jobs)