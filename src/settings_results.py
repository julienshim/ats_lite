from random import randint

csv_output_path = './assets/results.csv'

seconds_range_between_fetch = randint(15, 30)

search_parameters = {
    'location': ['']
}

no_of_weeks_limit = 2

ignore = {
    "department": [''],
    "location": ['']
}