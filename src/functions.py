from re import match, sub, search
from requests import get
from bs4 import BeautifulSoup

from datetime import datetime, timedelta
from src.settings_results import no_of_weeks_limit

from src.settings_results import search_parameters
