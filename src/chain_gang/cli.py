import argparse
import csv
import sys

from chain_gang.logger import get_logger
from chain_gang.scraper import ChainTextsScraper, ChainEmailsScraper, EmojiPastaScraper
from chain_gang.predict import LlamaPredictor


logger = get_logger(__name__)


def scrape_chain_texts(chain_texts, chain_emails, emoji_pasta):
    """..."""


    with open("chain_messages_all.csv", "w") as f:

        header = ["id", "text", "url", "page", "num", "title", "source"]
        writer = csv.DictWriter(f, header)
        writer.writeheader()

        if not any([chain_texts, chain_emails, emoji_pasta]):
            raise ValueError("No scraper specified")

        if emoji_pasta:
            scraper = EmojiPastaScraper()
            for i, post in enumerate(scraper.posts()):
                row = post._asdict()
                row["id"] = i
                writer.writerow(row)
                f.flush()

        if chain_emails:
            scraper = ChainEmailsScraper()
            for i, post in enumerate(scraper.posts()):
                row = post._asdict()
                row["id"] = i
                logger.debug("recording chain email: %s", row["text"][0:10] + "...")
                writer.writerow(row)
                f.flush()

        if chain_texts:
            scraper = ChainTextsScraper()
            for i, post in enumerate(scraper.posts()):
                row = post._asdict()
                row["id"] = i
                logger.debug("recording chain email: %s", row["text"][0:10] + "...")
                writer.writerow(row)
                f.flush()


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
    scrape_parser.add_argument("--chain-texts", action="store_true", help="scrape chain texts")
    scrape_parser.add_argument("--chain-emails", action="store_true", help="scrape chain emails")
    scrape_parser.add_argument("--emoji-pasta", action="store_true", help="scrape emoji pasta")

    _ = subparser.add_parser("benchmark", help="benchmark the model")

    args = parser.parse_args()

    if args.command == "scrape":
        scrape_chain_texts(
            args.chain_texts,
            args.chain_emails,
            args.emoji_pasta,
        )

    elif args.command == "benchmark":
        benchmark()

    else:
        parser.print_help()
