import emoji
import requests
import time

from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from selenium import webdriver
from typing import Any, Iterable


class Scraper(ABC):
    """abc for scraping chain texts from a source"""

    @abstractmethod
    def posts(self) -> Iterable[str]:
        """Yield chain texts from the chain texts"""
        pass


class ChainTextsScraper(Scraper):
    """scraper for chain texts from the Chain Texts Tumblr page"""

    URL = "https://chaintexts.tumblr.com"

    PAGES = 35

    def __init__(self):
        pass

    def posts(self) -> Iterable[Any]:
        """Yield chain texts from the Chain Texts Tumblr page."""

        for page in range(1, self.PAGES+1):
            url = f"{self.URL}/page/{page}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            titles = soup.find_all("h2", class_="title")
            for num, t in enumerate(titles):
                yield t.find("a").text, url, page, num


class ChainEmailsScraper(object):

    URL = "https://www.tumblr.com/chainemails"

    def __init__(self):
        pass

    def source(self, browser) -> Iterable[str]:
        html_source_code = browser.execute_script("return document.body.innerHTML;")
        html_soup = BeautifulSoup(html_source_code, 'html.parser')
        for a in html_soup.find_all("article"):
            for p in a.find_all("p"):
                if emoji.emoji_count(p.text) > 3:
                    yield p.text

    def posts(self) -> Iterable[Any]:

        url = self.URL

        browser = webdriver.Firefox()
        browser.get(self.URL)

        last = -1

        y = 0

        while last != y:
            last = y
            y = browser.execute_script("return document.body.scrollHeight")
            browser.execute_script(f"window.scrollTo(0, {y})")
            time.sleep(1)

        for i, p in enumerate(self.source(browser)):
            if emoji.emoji_count(p) > 3:
                yield p, url, -1, i
