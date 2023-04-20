from random import randint

csv_output_path = './assets/results.csv'

seconds_range_between_fetch = randint(15, 30)

search_parameters = {
    'location': ['santa-clara-valley-cupertino-SCV']
}

no_of_weeks_limit = 1

ignore = {
    "department": ['Apple Retail'],
    "location": ['Various Locations within  United States ']
}