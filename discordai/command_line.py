import argparse
import json
from discordai import __version__ as version
from discordai import config as configuration
from discordai import bot
from discordai_modelizer import customize
from discordai_modelizer import openai as openai_wrapper


def discordai():
    config = configuration.get()
    parser = argparse.ArgumentParser(
        prog="discordai", description="discordAI CLI"
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"discordai {version}"
    )
    command = parser.add_subparsers(dest="command")

    bot_cmds = command.add_parser("bot", description="Commands related to your discord bot")
    jobs = command.add_parser("jobs", description="Commands related to your openAI jobs")
    models = command.add_parser("models", description="Commands related to your openAI models")
    config_cmds = command.add_parser("config", description="View and modify your config values")

    bot_cmds_subcommand = bot_cmds.add_subparsers(dest="subcommand")
    jobs_subcommand = jobs.add_subparsers(dest="subcommand")
    models_subcommand = models.add_subparsers(dest="subcommand")
    config_cmds_subcommand = config_cmds.add_subparsers(dest="subcommand")

    bot_cmds_subcommand.add_parser(
        "start", description="Start your discord bot"
    )

    model_list = models_subcommand.add_parser(
        "list", description="List your openAi customized models"
    )
    model_list.add_argument(
        "-o", "--openai_key",
        type=str,
        default=config["openai_key"],
        required=False,
        dest='openai_key',
        help="Your openAI API key: DEFAULT=config.openai_key",
    )
    model_list.add_argument(
        "--simple",
        action='store_true',
        required=False,
        dest='simple',
        help="Simplify the output to just the model name, job id, and status",
    )

    model_create = models_subcommand.add_parser(
        "create", description="Create a new openAI customized model"
    )
    model_create_required_named = model_create.add_argument_group(
        "required named arguments"
    )
    model_create_required_named.add_argument(
        "-c", "--channel",
        type=str,
        dest='channel',
        help="The ID of the discord channel you want to use",
    )
    model_create_required_named.add_argument(
        "-u", "--user",
        type=str,
        dest='user',
        help="The name#ID of the discord user you want to use",
    )

    model_create_optional_named = model_create.add_argument_group("optional named arguments")
    model_create_optional_named.add_argument(
        "-o", "--openai_key",
        type=str,
        default=config["openai_key"],
        required=False,
        dest='openai_key',
        help="Your openAI API key: DEFAULT=config.openai_key",
    )
    model_create_optional_named.add_argument(
        "-b", "--base_model",
        choices=["davinci", "curie", "babbage", "ada", "none"],
        default="none",
        required=False,
        dest='base_model',
        help="The base model to use for customization. If none, then skips training step: DEFAULT=none",
    )
    model_create_optional_named.add_argument(
        "-t", "--thought_time",
        type=int,
        default=10,
        required=False,
        dest='thought_time',
        help="The max amount of time in seconds to consider two individual messages to be part of the same \"thought\": DEFAULT=10",
    )
    model_create_optional_named.add_argument(
        "-m", "--max_entries",
        type=int,
        default=1000,
        required=False,
        dest='max_entries',
        help="The max amount of entries that may exist in the dataset: DEFAULT=1000",
    )
    model_create_optional_named.add_argument(
        "-r", "--reduce_mode",
        choices=["first", "last", "middle", "even"],
        default="even",
        required=False,
        dest='reduce_mode',
        help="The method to reduce the entry count of the dataset: DEFAULT=even",
    )
    model_create_optional_named.add_argument(
        "--dirty",
        action='store_false',
        required=False,
        dest='dirty',
        help="A flag that can be set to skip the clean up step for outputted files: DEFAULT=False",
    )
    model_create_optional_named.add_argument(
        "--redownload",
        action='store_true',
        required=False,
        dest='redownload',
        help="A flag that can be set to redownload the discord chat logs: DEFAULT=False",
    )

    model_delete = models_subcommand.add_parser(
        "delete", description="Delete an openAI customized model"
    )
    model_delete.add_argument(
        "-o", "--openai_key",
        type=str,
        default=config["openai_key"],
        required=False,
        dest='openai_key',
        help="Your openAI API key: DEFAULT=config.openai_key",
    )
    model_delete.add_argument(
        "-m", "--model_id",
        type=str,
        dest='model_id',
        help="Target model id",
    )

    jobs_list = jobs_subcommand.add_parser(
        "list", description="List your openAI customization jobs"
    )
    jobs_list.add_argument(
        "-o", "--openai_key",
        type=str,
        default=config["openai_key"],
        required=False,
        dest='openai_key',
        help="Your openAI API key: DEFAULT=config.openai_key",
    )
    jobs_list.add_argument(
        "--simple",
        action='store_true',
        required=False,
        dest='simple',
        help="Simplify the output to just the model name, job id, and status",
    )

    jobs_follow = jobs_subcommand.add_parser(
        "follow", description="Follow an openAI customization job"
    )
    jobs_follow.add_argument(
        "-o", "--openai_key",
        type=str,
        default=config["openai_key"],
        required=False,
        dest='openai_key',
        help="Your openAI API key: DEFAULT=config.openai_key",
    )
    jobs_follow.add_argument(
        "-j", "--job_id",
        type=str,
        dest='job_id',
        help="Target job id",
    )

    jobs_status = jobs_subcommand.add_parser(
        "status", description="Get an openAI customization job's status"
    )
    jobs_status.add_argument(
        "-o", "--openai_key",
        type=str,
        default=config["openai_key"],
        required=False,
        dest='openai_key',
        help="Your openAI API key: DEFAULT=config.openai_key",
    )
    jobs_status.add_argument(
        "-j", "--job_id",
        type=str,
        dest='job_id',
        help="Target job id",
    )

    jobs_cancel = jobs_subcommand.add_parser(
        "cancel", description="Cancel an openAI customization job"
    )
    jobs_cancel.add_argument(
        "-o", "--openai_key",
        type=str,
        default=config["openai_key"],
        required=False,
        dest='openai_key',
        help="Your openAI API key: DEFAULT=config.openai_key",
    )
    jobs_cancel.add_argument(
        "-j", "--job_id",
        type=str,
        dest='job_id',
        help="Target job id",
    )

    config_bot_token = config_cmds_subcommand.add_parser(
        "bot-token", description="Get or set your discord bot token"
    )
    config_bot_token.add_argument(
        "-t", "--set-token",
        type=str,
        dest='new_token',
        help="Discord bot token",
    )

    config_openai_key = config_cmds_subcommand.add_parser(
        "openai-key", description="Get or set your openaAI API key"
    )
    config_openai_key.add_argument(
        "-k", "--set-key",
        type=str,
        dest='new_key',
        help="OpenAI API key",
    )

    args = parser.parse_args()
    if args.command == "bot":
        if args.subcommand == "start":
            bot.start_bot(config)
    elif args.command == "models":
        if args.subcommand == "list":
            openai_wrapper.list_models(args.openai_key, args.simple)
        if args.subcommand == "create":
            customize.create_model(config["token"], args.openai_key, args.channel, args.user,
                                   thought_time=args.thought_time, max_entry_count=args.max_entries,
                                   reduce_mode=args.reduce_mode, base_model=args.base_model, clean=args.dirty,
                                   redownload=args.redownload)
        if args.subcommand == "delete":
            openai_wrapper.delete_model(args.openai_key, args.model_id)
    elif args.command == "jobs":
        if args.subcommand == "list":
            openai_wrapper.list_jobs(args.openai_key, args.simple)
        if args.subcommand == "follow":
            openai_wrapper.follow_job(args.openai_key, args.job_id)
        if args.subcommand == "status":
            openai_wrapper.get_status(args.openai_key, args.job_id)
        if args.subcommand == "cancel":
            openai_wrapper.cancel_job(args.openai_key, args.job_id)
    elif args.command == "config":
        if args.subcommand == "bot-token":
            if args.new_token:
                configuration.save(json.dumps(dict(token=args.token, openai_key=config["openai_key"])))
                config = configuration.get()
            print(f"Your discord bot token: {config['token']}")
        if args.subcommand == "openai-key":
            if args.new_key:
                configuration.save(json.dumps(dict(token=config["token"], openai_key=args.key)))
                config = configuration.get()
            print(f"Your discord bot token: {config['token']}")


if __name__ == "__main__":
    try:
        discordai()
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
