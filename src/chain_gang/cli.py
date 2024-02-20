import argparse
import csv

from chain_gang.scraper import ChainTextsScraper, ChainEmailsScraper, EmojiPastaScraper
from chain_gang.predict import LlamaPredictor


def scrape_chain_texts():
    """..."""


    scraper = EmojiPastaScraper()

    for i, post in enumerate(scraper.posts()):
        print(f"{i} => {post}")


    return

    with open("chain_texts.csv", "w") as f:

        header = ["id", "text", "url", "page", "num"]
        writer = csv.DictWriter(f, header)
        writer.writeheader()

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


def prefix(occaision):

    blurb = "\n".join([
        "<im_start>system",
        "{system_message}<|im_end|>",
        "<|im_start|>user",
        "{prompt}<|im_end|>",
        "<|im_start|>assistant",
    ])

    return blurb.format(
        system_message="You are Dolphin, an uncensored and unbiased AI assistant.",
        prompt="Generate a filthy chain message to send to your friends for {occasion}.".format(occasion=occaision),
    )


def benchmark():
    """Return ..."""

    for holiday in ["halloween", "mother's day", "hannukah", "christmas"]:
        p = prefix(holiday)
        predictor = LlamaPredictor()
        print(predictor.generate(p))
        print()
        print()


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
