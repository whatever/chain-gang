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


class EmojiPastaScraper(object):

    FRONTPAGE_URL = "https://www.reddit.com/r/emojipasta/"
    EXAMPLE_URL = "https://www.reddit.com/r/emojipasta/comments/1ar5x34/request_worst_day_of_my_life/"
    EXAMPLE_URL = "https://www.reddit.com/r/emojipasta/comments/1auoe34/happy_presidents_day/"

    def __init__(self):
        pass


    def scrape_page(self, url: str) -> str:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        div = soup.find("div", class_="text-neutral-content")
        thing = div.find("p")
        return thing.text.strip()

    def post_pages(self, browser, limit=100) -> Iterable[str]:
        """Yield url's of the posts on the front page of the subreddit."""

        count = 0

        html_source_code = browser.execute_script("return document.body.innerHTML;")
        html_soup = BeautifulSoup(html_source_code, 'html.parser')
        
        y = 0
        last = -1
        limit = 2

        hits = set()

        while y != last and count < limit:
            y = browser.execute_script("return document.body.scrollHeight")
            browser.execute_script(f"window.scrollTo(0, {y})")

            html_source_code = browser.execute_script("return document.body.innerHTML;")
            html_soup = BeautifulSoup(html_source_code, 'html.parser')

            for a in html_soup.find_all("a"):
                if not a.get("href", "").startswith("/r/emojipasta/comments/"):
                    continue
                if a["href"] in hits:
                    continue
                hits.add(a["href"])
                yield a["href"]

            time.sleep(1)
            print("scrolliung")
            count += 1

        yield ""

    def posts(self) -> Iterable[Any]:

        driver = webdriver.Firefox()
        driver.get(self.FRONTPAGE_URL)
        print("<<<")

        for url in self.post_pages(driver):
            print(url)

        res = self.scrape_page(self.EXAMPLE_URL)
        yield res
