from re import match, sub, search
from requests import get
from bs4 import BeautifulSoup

from datetime import datetime, timedelta
from src.settings_results import no_of_weeks_limit

from src.settings_results import search_parameters

def get_soup(url):
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def compress_text(text):
    return sub('\n{1,}', '\n', text.get_text(separator='\n'))

def get_job_posting_details(internal_job_posting_url):
    job_posting_url_reg = r''
    base_pay_reg = r'(\$[\d,.]{1,} and \$[\d,.]{1,})'

    if bool(match(job_posting_url_reg, internal_job_posting_url)):
        public_job_posting_url = ''
        soup = get_soup(public_job_posting_url)

    tmp = {
        'job-summary': None,
        'key-qualifications': None,
        'description': None,
        'education-experience': None,
        'posting-supplement-footer-0': None,
        'base_pay_lower': None,
        'base_pay_upper': None,
        'base_pay_type': None
    }

    for key in list(tmp.keys())[0:5]:
        results = soup.find('div', {'id': f'jd-{key}'})
        if results is not None:
            tmp[key] = compress_text(results)
    
    if tmp['posting-supplement-footer-0'] is not None:
        results = search(base_pay_reg, tmp['posting-supplement-footer-0'])
        if results is not None:
            base_pay = search(base_pay_reg, tmp['posting-supplement-footer-0']).group()
            [base_pay_lower, base_pay_upper] = base_pay.split(' and ') 
            tmp['base_pay_lower'] = base_pay_lower
            tmp['base_pay_upper'] = base_pay_upper[:-1] if base_pay_upper.endswith(',') else base_pay_upper
            tmp['base_pay_type'] = 'hourly' if '.' in base_pay else 'salary'
        
    values = list(tmp.values())
    del values[4]
    return values

def get_target_locations():
    locations = search_parameters['location']
    return '+'.join(locations)

def get_date_n_weeks_ago():
    today = datetime.now()
    delta = timedelta(weeks=no_of_weeks_limit)
    two_weeks_ago = today - delta
    return two_weeks_ago