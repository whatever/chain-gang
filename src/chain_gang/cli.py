import csv

from chain_gang.scraper import ChainTextsScraper, ChainEmailsScraper


def main():

    with open("chain_texts.csv", "w") as f:

        header = ["id", "text", "url", "page", "num"]
        writer = csv.DictWriter(f, header)

        scraper = ChainEmailsScraper()

        for i, post in enumerate(scraper.posts()):
            row = [i] + list(post)
            row = dict(zip(header, row))
            writer.writerow(row)
            print(f"{i} => {post}")

        scraper = ChainTextsScraper()

        for i, post in enumerate(scraper.posts()):
            row = [i] + list(post)
            row = dict(zip(header, row))
            print(f"{i} => {row['page']}")
            writer.writerow(row)
