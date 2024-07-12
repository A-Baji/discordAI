import argparse
from discordai import __version__ as version
from discordai import config as configuration
from discordai import template
from discordai import bot
from discordai.command_line import subparsers
from discordai_modelizer.command_line import command_line


def discordai():
    parser = argparse.ArgumentParser(prog="discordai", description="DiscordAI CLI")
    parser.add_argument(
        "-V", "--version", action="version", version=f"discordai {version}"
    )
    command, model_subcommand, job_subcommand = command_line.setup_modelizer_commands(
        parser, is_parent=True
    )

    bot_cmd = command.add_parser("bot", help="Manage your Discord bot")
    config_cmd = command.add_parser("config", help="View your DiscordAI config")

    bot_subcommand = bot_cmd.add_subparsers(dest="subcommand")
    bot_subsubcommand = bot_subcommand.add_parser(
        "command", help="Manage your Discord bot's slash commands"
    ).add_subparsers(dest="subsubcommand")
    config_subcommand = config_cmd.add_subparsers(dest="subcommand")

    subparsers.setup_bot_start(bot_subcommand)
    subparsers.setup_add_bot_command(bot_subsubcommand)
    subparsers.setup_delete_bot_command(bot_subsubcommand)
    subparsers.setup_list_bot_command(bot_subsubcommand)
    subparsers.setup_update_config(config_subcommand)

    args = parser.parse_args()
    config = configuration.get()
    if hasattr(args, "openai_key"):
        args.openai_key = command_line.set_openai_api_key(
            args.openai_key, config, is_parent=True
        )
    if hasattr(args, "discord_token"):
        args.discord_token = command_line.set_bot_token(
            args.discord_token, config, is_parent=True
        )

    if args.command in ["model", "job"]:
        command_line.read_modelizer_args(args, model_subcommand, job_subcommand)
    elif args.command == "bot":
        if args.subcommand == "start":
            bot.start_bot(args.discord_token, args.openai_key, args.sync)
        elif args.subcommand == "command":
            if args.subsubcommand == "list":
                command_line.display(template.list_commands())
            elif args.subsubcommand == "add":
                template.gen_new_command(
                    args.model_id,
                    args.command_name,
                    args.openai_key,
                    args.temp_default,
                    args.pres_default,
                    args.freq_default,
                    args.max_tokens_default,
                    args.stop_default,
                    args.bold_default,
                )
            elif args.subsubcommand == "delete":
                template.delete_command(args.command_name, args.force)
            else:
                raise argparse.ArgumentError(
                    bot_subsubcommand,
                    "Must choose a command from `list`, `add`, or `delete`",
                )
        else:
            raise argparse.ArgumentError(
                bot_subcommand,
                "Must choose a command from `start` or `command`",
            )
    elif args.command == "config":
        if args.subcommand == "update":
            if args.key in config:
                config[args.key] = args.value
                configuration.save(config)
                config = configuration.get()
            else:
                print("Invalid key provided!")
                return
        print(f"{configuration.config_dir / 'config.json'}:")
        command_line.display(config)


if __name__ == "__main__":
    try:
        discordai()
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
