import argparse
import csv

from chain_gang.scraper import ChainTextsScraper, ChainEmailsScraper
from chain_gang.predict import LlamaPredictor


def scrape_chain_texts():
    """..."""

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


def benchmark():
    """Return ..."""

    predictor = LlamaPredictor()
    print(predictor.generate("hello"))


def main():
    """..."""

    parser = argparse.ArgumentParser(description="chain")

    subparser = parser.add_subparsers(dest="command", help="subcommand to run")

    scrape_parser = subparser.add_parser("scrape", help="scrape chain texts")
    scrape_parser.add_argument("--texts", action="store_true", help="scrape chain texts")

    _ = subparser.add_parser("benchmark", help="benchmark the model")

    args = parser.parse_args()

    if args.command == "scrape":
        scrape_chain_texts()

    elif args.command == "benchmark":
        benchmark()

    else:
        parser.print_help()
