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
