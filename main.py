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
csv_write_mode = 'w'

def job_is_previously_imported(target_job_reference_no):
    if len(previously_imported_jobs) == 0:
        return False
    for job_item in previously_imported_jobs:
        if job_item.job_reference_no == target_job_reference_no:
            return True
    return False

def get_soup(page_number):
    locations = get_target_locations()
    response = get(f'')
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def parse_job_item(job_item):

    date_dict = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }

    position = job_item.find('a', {'id': compile(r'jotTitle_PIPE-[0-9]{1,}')})
    job_title = position.text
    job_href = position["href"]
    job_posting_url = f''
    job_reference_no = job_href.split('/')[3]
    department = job_item.find('span', {'class': compile(r'table--advanced-search__role')}).text
    date = job_item.find('span', {'class': compile(r'table--advanced-search__date')}).text
    [month, day, year] = split(r'[ ,]{1,}', date)
    location = job_item.find('span', {'id': compile(r'storeName_container_PIPE-[0-9]{1,}')}).text
    import_date = f'{year}-{date_dict[month]}-{"0" if len(str(day)) == 1 else ""}{day}'
    
    return [import_date, job_reference_no, job_title, department, location, job_posting_url]

def filter_job_items(job_item):
    [import_date, job_reference_no, job_title, department, location, job_posting_url] = job_item
    [year, month, day] = list(map(lambda x: int(x), import_date.split('-')))
    import_date_datetime = datetime(year, month, day)
    n_weeks_ago_datetime = get_date_n_weeks_ago()
    
    return (import_date_datetime >= n_weeks_ago_datetime) and (department not in ignore['department']) and (location not in ignore['location']) and (not job_is_previously_imported(job_reference_no))

def fetch_jobs():
    running = True
    current_page_number = 1
    fetched_jobs = []

    while running:
        soup = get_soup(current_page_number)
        job_items = soup.find_all('tbody', {'id': compile(r'accordion_PIPE-[0-9]{1,}_group')})
        job_items_parsed = list(map(parse_job_item, job_items))
        job_items_parsed_filtered = list(filter(filter_job_items, job_items_parsed))
        job_items_parsed_filtered_len = len(job_items_parsed_filtered)
        if job_items_parsed_filtered_len == 0 :
            running = False
        else :
            print(f'Fetching Page {current_page_number} jobs... {job_items_parsed_filtered_len} jobs found')
            fetched_jobs += job_items_parsed_filtered
            current_page_number += 1
            sleep(seconds_range_between_fetch)
    return fetched_jobs

def convert_fetched_jobs_to_job_items(fetched_jobs, is_previously_imported):
    job_items = []
    for job_item_index, job_item in enumerate(fetched_jobs):
        print(f'- Gather details... {job_item_index + 1} of {len(fetched_jobs)}')
        [import_date, job_reference_no, job_title, department, location, job_posting_url] = job_item
        sleep(seconds_range_between_fetch)
        task = get_job_posting_details(job_posting_url)
        while task is None:
            pass
        [summary, key_qualifications, description, education_experience, base_pay_lower, base_pay_upper, base_pay_type] = task
        new_job_item = JobItem(import_date, job_reference_no, job_title, department, location, summary, key_qualifications, description, education_experience, base_pay_lower, base_pay_upper, base_pay_type, job_posting_url, is_previously_imported)
        job_items.append(new_job_item)
    return job_items

fetched_jobs = fetch_jobs()
fetched_jobs = convert_fetched_jobs_to_job_items(fetched_jobs, False)

with open(previously_imported_jobs_path, csv_write_mode, encoding='utf-8') as f:
    csv_writer = writer(f)

    if csv_write_mode == 'w':
        csv_writer.writerow(['import_date', 'job_reference_no', 'job_title', 'department', 'location', 'summary', 'key_qualifications', 'description', 'education_experience', 'base_pay_lower', 'base_pay_upper', 'base_pay_type', 'job_posting_url'])

    jobs_written_count = 0
    jobs_skipped_count = 0

    job_items_to_write = previously_imported_jobs + fetched_jobs
    job_items_to_write = sorted(job_items_to_write, key=lambda x: x.import_date, reverse=True)

    for job_item_index, job_item in enumerate(job_items_to_write):
        job_item_row = job_item.get_write_row()
        csv_writer.writerow(job_item_row)
        if not job_item.is_previously_imported:
            jobs_written_count += 1

    print(f'Done! {jobs_written_count} new jobs added.')