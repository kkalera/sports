import csv
import os
from data_collection.helper_functions import *


def get_season_games_links(url):
    browser = init_browser()
    browser.get(url)

    # First, load all the games from the season.
    load_more_button = browser.find_element_by_css_selector("a[onclick*='loadMoreGames(); return false;']")
    while load_more_button.is_displayed():
        loading_img = browser.find_element_by_css_selector("div[id*='preload']")
        if not loading_img.is_displayed():
            browser.execute_script("loadMoreGames()")

    # Get the html from where we will extract the links
    html = browser.page_source

    # Finally, close the browser
    browser.close()

    # Parse the html with beautifulsoup
    soup = html_to_soup(html)

    # Select all matches
    games = soup.select("tr[class*=stage-finished]")

    # Get all the match id's
    game_id_list = [game.get("id") for game in games]  # Get all the id's
    game_id_list = [game.replace("g_1_", "") for game in game_id_list]  # Trim the id's to use in the link

    # Get the competition name
    competition_name = soup.find("div", attrs={"class": "tournament-name"}).text.strip()
    competition_name = competition_name.replace("/", "-")

    # Create the save directory if it does not exist yet

    map_name = "data/soccer/Premier League - England/{}".format(competition_name)

    if not os.path.isdir(map_name):
        os.makedirs(map_name)

    with open(map_name + "/game_links.csv", "w") as file:
        writer = csv.writer(file)  # Create the writer
        base_url = "https://www.scoreboard.com/en/match/"
        for i in game_id_list:
            writer.writerow([base_url + i])
