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
        'import_date': f'{year}-{dates_dict[month]}-{day}',
        'job_title': job_title,
        'job_link': job_link,
        'job_reference': job_reference,
        'department': department,
        'location': location
    }
    
    return job_items_dict

def filter_year(job_item):
    import_date = job_item['import_date']
    [year, month, day] = import_date.split('-')
    return year == '2023'

def fetch_all_jobs():
    running = True
    current_page_number = 1
    tmp = []

    while running:
        soup = get_soup(current_page_number)
        job_items = soup.find_all('tbody', {'id': compile(r'accordion_PIPE-[0-9]{1,}_group')})
        job_items_parsed = list(map(parse_job_item, job_items))
        job_items_parsed_filtered = list(filter(filter_year, job_items_parsed))
        job_items_parsed_filtered_len = len(job_items_parsed_filtered)

        if job_items_parsed_filtered_len == 0:
            running = False
        else :
            print(f'Fetching Page {current_page_number} jobs... {job_items_parsed_filtered_len} jobs found')
            tmp += job_items_parsed_filtered
            current_page_number += 1
            rand_num = randint(3, 7)
            sleep(rand_num)

    return tmp

def get_job_ref_date(row):
    pass
    [import_date, job_reference_no, job_title, department, location, job_posting_url, status, notes] = row
    tmp = {
        'job_reference_no': job_reference_no,
        'import_date': import_date
    }
    return tmp

def load_previously_imported_jobs():
    with open('') as ref:
        data = [row for row in reader(ref)][1:]
        data = list(map(get_job_ref_date, data))
        return data

all_job_items_fetched = fetch_all_jobs()
previously_imported_jobs_path = ''
previously_imported_jobs_path_exists = path.exists(previously_imported_jobs_path)
previously_imported_jobs = load_previously_imported_jobs() if previously_imported_jobs_path_exists else []
previously_imported_jobs_len = len(previously_imported_jobs)
csv_write_mode = 'a' if previously_imported_jobs_path_exists else 'w'

def job_is_previously_imported(job_reference_no):
    if previously_imported_jobs_len > 0:
        for job_item in previously_imported_jobs:
            if job_item['job_reference_no'] == job_reference_no:
                return job_item
    tmp = {'job_reference_no': '', 'import_date': ''}
    return tmp

with open(previously_imported_jobs_path, csv_write_mode, encoding='utf-8') as f:
    csv_writer = writer(f)
    if csv_write_mode == 'w':
        csv_writer.writerow(['import_date', 'job_reference_no', 'job_title', 'department', 'location', 'job_posting_url', 'status', 'notes'])

    jobs_written_count = 0
    jobs_skipped_count = 0

    for job_item in all_job_items_fetched:
        job_title = job_item['job_title']
        job_posting_url = job_item['job_link']
        job_reference_no = job_item['job_reference']
        department = job_item['department']
        location = job_item['location']
        import_date = job_item['import_date']

        import_status = job_is_previously_imported(job_reference_no)
        import_job_reference_no = import_status["job_reference_no"]
        import_import_date = import_status["import_date"]

        if import_job_reference_no and import_import_date:
            jobs_skipped_count += 1
        else:
            job_item_row = [import_date, job_reference_no, job_title, department, location, job_posting_url, '', '']
            csv_writer.writerow(job_item_row)
            jobs_written_count += 1

    print(f'Done! {jobs_written_count} new jobs added.')