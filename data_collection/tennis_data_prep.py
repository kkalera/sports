import os
import csv
from progressbar.bar import ProgressBar
from data_collection.helper_functions import *


def get_all_links():
    player_dir = "../data/Tennis/Players/"
    dirs = [player_dir + name for name in os.listdir(player_dir) if os.path.isdir(player_dir + name)]

    game_links = set()
    players_without_single_games = 0
    for dir in dirs:
        # Read the csv file
        with open(dir+"/single_games.csv", "r") as f:
            reader = csv.reader(f)
            l = []
            for row in reader:
                l.append(str(row))

            if len(l) == 0:
                print("{} has no single games".format(dir))
                players_without_single_games += 1
            else:
                for li in l:
                    #####################
                    # Add the /en link part, since I forgot when importing the links
                    li = li.split("/")
                    li.insert(3, "en")
                    li = "/".join(li)
                    #####################
                    game_links.add(li[2:-2])

    print("{} total games".format(len(game_links)))
    print("{} players without single games".format(players_without_single_games))

    with open("../data/Tennis/game_links.csv", "w") as f:
        writer = csv.writer(f, dialect="excel")
        for link in game_links:
            print(link)
            writer.writerow([link])


def get_game_data(url, browser=None):

    if browser is None:
        browser = init_browser()

    browser.get(url)
    html = browser.page_source

    soup = html_to_soup(html)
    home_team = html_to_soup(soup.select("td[class*=tname-home]")).find("a").get("href")
    print(home_team)


if __name__ == "__main__":
    links = []
    with open("../data/Tennis/game_links.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 0:
                links.append(row[0])

    print(links[0])
    get_game_data(links[0])

    #get_all_links()