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

def parse_job_item(job_item):
    position = job_item.find('a', {'id': compile(r'jotTitle_PIPE-[0-9]{1,}')})
    job_title = position.text
    job_href = position["href"]
    job_link = f''
    job_reference = job_href.split('/')[3]
    department = job_item.find('span', {'class': compile(r'table--advanced-search__role')}).text
    date = job_item.find('span', {'class': compile(r'table--advanced-search__date')}).text
    [month, day, year] = split(r'[ ,]{1,}', date)
    location = job_item.find('span', {'id': compile(r'storeName_container_PIPE-[0-9]{1,}')}).text

    dates_dict = {
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

    job_items_dict = {
        'import_date': f'{year}-{dates_dict[month]}-{"0" if len(str(day)) == 1 else ""}{day}',
        'job_title': job_title,
        'job_link': job_link,
        'job_reference': job_reference,
        'department': department,
        'location': location
    }
    
    return job_items_dict

def filter_job_items(job_item):
    import_date = job_item['import_date']
    department = job_item['department']
    location = job_item['location']
    job_reference = job_item['job_reference']
    [year, month, day] = list(map(lambda x: int(x), import_date.split('-')))
    import_date = datetime(year, month, day)
    n_weeks_ago = get_date_n_weeks_ago()
    
    return (import_date >= n_weeks_ago) and (department not in ignore['department']) and (location not in ignore['location']) and (not job_is_previously_imported(job_reference))


def fetch_all_jobs():
    running = True
    current_page_number = 1
    tmp = []

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
            tmp += job_items_parsed_filtered
            current_page_number += 1
            sleep(seconds_range_between_fetch)
    return tmp

all_job_items_fetched = fetch_all_jobs()