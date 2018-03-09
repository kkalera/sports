import csv
import os
from data_collection.helper_functions import *


def get_players(soup):
    pass

if __name__ == "__main__":
    url = "https://www.scoreboard.com/en/match/SGPa5fvr"
    html = get_html(url)
    get_players(html_to_soup(html))