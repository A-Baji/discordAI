import argparse
from discordai import __version__ as version
from discordai import config as configuration
from discordai import template
from discordai import bot
from discordai.command_line import subparsers
from discordai_modelizer.command_line import command_line


def set_openai_api_key(key: str, config):
    if not key and not config["OPENAI_API_KEY"]:
        raise ValueError(
            "Your OpenAI API key must either be passed in as an argument or set in your config",
        )
    else:
        return key or config["OPENAI_API_KEY"]


def set_bot_token(token: str, config):
    if not token and not config["DISCORD_BOT_TOKEN"]:
        raise ValueError(
            "Your Discord bot token must either be passed in as an argument or set in your config",
        )
    else:
        return token or config["DISCORD_BOT_TOKEN"]


def discordai():
    parser = argparse.ArgumentParser(prog="discordai", description="DiscordAI CLI")
    parser.add_argument(
        "-V", "--version", action="version", version=f"discordai {version}"
    )
    command, model_subcommand, job_subcommand = command_line.setup_modelizer_commands(
        parser, is_parent=True
    )

    bot_cmd = command.add_parser(
        "bot", description="Commands related to your Discord bot"
    )
    config_cmd = command.add_parser("config", description="View and modify your config")

    bot_subcommand = bot_cmd.add_subparsers(dest="subcommand")
    bot_subsubcommand = bot_subcommand.add_parser(
        "command", description="Manage your Discord bot's slash commands"
    ).add_subparsers(dest="subsubcommand")
    config_subcommand = config_cmd.add_subparsers(dest="subcommand")

    subparsers.setup_bot_start(bot_subcommand)
    subparsers.setup_add_bot_command(bot_subsubcommand)
    subparsers.setup_delete_bot_command(bot_subsubcommand)
    subparsers.setup_update_bot_token(config_subcommand)
    subparsers.setup_update_openai_key(config_subcommand)

    args = parser.parse_args()
    config = configuration.get()
    if hasattr(args, "openai_key"):
        args.openai_key = set_openai_api_key(args.openai_key, config)
    if hasattr(args, "discord_token"):
        args.discord_token = set_bot_token(args.discord_token, config)

    if args.command in ["model", "job"]:
        command_line.read_modelizer_args(args, model_subcommand, job_subcommand)
    elif args.command == "bot":
        if args.subcommand == "start":
            bot.start_bot(config, args.sync)
        elif args.subcommand == "command":
            if args.subsubcommand == "new":
                template.gen_new_command(
                    args.model_id,
                    args.command_name,
                    args.temp_default,
                    args.pres_default,
                    args.freq_default,
                    args.max_tokens_default,
                    args.stop_default,
                    args.openai_key,
                    args.bold_default,
                )
            elif args.subsubcommand == "delete":
                template.delete_command(args.command_name)
            else:
                raise argparse.ArgumentError(
                    bot_subsubcommand,
                    "Must choose a command from `new` or `delete`",
                )
        else:
            raise argparse.ArgumentError(
                bot_subcommand,
                "Must choose a command from `start` or `commands`",
            )
    elif args.command == "config":
        if args.subcommand == "bot-token":
            if args.new_token:
                print(f"Old discord bot token: {config['DISCORD_BOT_TOKEN']}")
                configuration.save(
                    dict(
                        DISCORD_BOT_TOKEN=args.new_token,
                        OPENAI_API_KEY=config["OPENAI_API_KEY"],
                    )
                )
                config = configuration.get()
            print(f"Current discord bot token: {config['DISCORD_BOT_TOKEN']}\n")
        elif args.subcommand == "openai-key":
            if args.new_key:
                print(f"Old openAi API key: {config['OPENAI_API_KEY']}")
                configuration.save(
                    dict(
                        DISCORD_BOT_TOKEN=config["DISCORD_BOT_TOKEN"],
                        OPENAI_API_KEY=args.new_key,
                    )
                )
                config = configuration.get()
            print(f"Current openAi API key: {config['OPENAI_API_KEY']}\n")
        else:
            print(f"Current discord bot token: {config['DISCORD_BOT_TOKEN']}")
            print(f"Current openAi API key: {config['OPENAI_API_KEY']}\n")


if __name__ == "__main__":
    try:
        discordai()
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
