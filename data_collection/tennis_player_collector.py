from data_collection.helper_functions import *
import csv
import os


def get_tennis_player_links(url):
    browser = init_browser(headless=False)
    browser.get(url)

    # First, load all the players from the season.
    browser.execute_script("cjs.dic.get('Helper_Tab').showMore('#ranking-items"
                           "-per-page_35851', '#ranking-table-results_35851', "
                           "'#ranking-link_35851');")

    # Get the page's html
    html = browser.page_source

    # Close the browser
    browser.close()

    # Create soup from the html
    soup = html_to_soup(html)

    # Get the elements for all players
    player_elements = soup.select("tr[class*=rank-row]")

    # Save the player names and links
    with open("../data/Tennis/player_links.csv", "w") as file:
        writer = csv.writer(file)

        # Get player data for each player
        for pe in player_elements:
            link_element = pe.find('a')
            link = "https://www.scoreboard.com" + link_element.get("href")
            name = link_element.text.strip()
            writer.writerow([link, name])


def get_single_games(url, browser=None):
    url = url + "/results/"
    if browser is None:
        browser = init_browser(headless=True)

    browser.get(url)

    # First, load all the games from the season.
    load_more_button = browser.find_element_by_css_selector("a[onclick*='loadMoreGames(); return false;']")
    while load_more_button.is_displayed():
        loading_img = browser.find_element_by_css_selector("div[id*='preload']")
        if not loading_img.is_displayed():
            browser.execute_script("loadMoreGames()")

    html = browser.page_source
    soup = html_to_soup(html)

    name = soup.find("div", attrs={"class": "team-name"}).text.strip()
    tables = soup.find_all("table", attrs={"class": "tennis"})
    total_games = []

    for t in tables:
        game_type = t.find("span", attrs={"class": "country_part"}).text.strip()
        if game_type == "ATP - SINGLES:":
            game_container = t.find("tbody")
            games = game_container.find_all("tr")
            game_id_list = [game.get("id") for game in games]
            game_id_list = [game.replace("g_2_", "") for game in game_id_list]

            for g in game_id_list:
                total_games.append("https://www.scoreboard.com/en/match/" + g)

    map_name = "../data/Tennis/Players/" + name
    if not os.path.isdir(map_name):
        os.makedirs(map_name)

    # Save the player names and links
    with open("../data/Tennis/Players/"+name+"/single_games.csv", "w") as file:
        writer = csv.writer(file)

        # Get player data for each player
        for game in total_games:
            writer.writerow([game])
    print("{} games parsed.".format(name))


def process_game(url, browser=None):
    if browser is None:
        browser = init_browser()

    browser.get(url)

    html = browser.page_source
    soup = html_to_soup(html)
    print(soup.find_all("span", attrs={"class": "tname"}))


def get_all_single_player_games():
    b = init_browser()
    links = []
    with open("../data/Tennis/player_links.csv", "r") as f:
        reader = csv.reader(f)

        i = 0
        for row in reader:
            if len(row) > 0:
                i += 1
                links.append(row[0])

    i = 0
    for link in links[i:]:
        print("Parsing {}/{}".format(i, len(links)))
        i += 1
        broke = True
        try:
            get_single_games(link, b)
            broke = False
        finally:
            if broke:
                print("Broke at {}".format(i))
                print("Restarting browser")
                b.quit()
                b = init_browser()
                i -= 1


if __name__ == "__main__":
    pass
