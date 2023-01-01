import argparse
from discordai import __version__ as version
from discordai import config as configuration
from discordai import bot


def discordai():
    parser = argparse.ArgumentParser(
        prog="discordai", description="discordAI CLI"
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"discordai {version}"
    )
    command = parser.add_subparsers(dest="command")

    start = command.add_parser("start", description="Start your discord bot")

    args = parser.parse_args()
    config = configuration.get()
    if args.command == "start":
        bot.start_bot(config)


if __name__ == "__main__":
    discordai()
