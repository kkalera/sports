from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
import urllib.request


def init_browser(headless=True):
    options = ChromeOptions()
    options.add_argument("--window-size=800,600")
    options.add_argument("--mute-audio")
    if headless:
        options.add_argument("--headless")
    b = Chrome(
        executable_path="c:/program files (x86)/chromedriver/chromedriver.exe",
        options=options)
    return b


def get_html(url):
    return urllib.request.urlopen(url).read()


def html_to_soup(h):
    return BeautifulSoup(h, "html5lib")
    # return BeautifulSoup(h, "html.parser")
