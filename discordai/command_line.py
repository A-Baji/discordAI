import argparse
from discordai import __version__ as version
from discordai import config as configuration
from discordai import bot
from discordai_modelizer import customize
from discordai_modelizer import openai as openai_wrapper


def discordai():
    parser = argparse.ArgumentParser(
        prog="discordai", description="discordAI CLI"
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"discordai {version}"
    )
    command = parser.add_subparsers(dest="command")

    start = command.add_parser("start", description="Start your discord bot")

    openai = command.add_parser("openai", description="OpenAI model customizer and API wrapper")
    openai_subcommand = openai.add_subparsers(dest="subcommand")

    openai_create = openai_subcommand.add_parser(
        "create", description="Create a new custom openAI model"
    )
    openai_create_required_named = openai_create.add_argument_group(
        "required named arguments"
    )
    openai_create_required_named.add_argument(
        "-c", "--channel",
        type=str,
        dest='channel',
        help="The ID of the discord channel you want to use",
    )
    openai_create_required_named.add_argument(
        "-u", "--user",
        type=str,
        dest='user',
        help="The name#ID of the discord user you want to use",
    )

    openai_create_optional_named = openai_create.add_argument_group("optional named arguments")
    openai_create_optional_named.add_argument(
        "-b", "--base_model",
        choices=["davinci", "curie", "babbage", "ada", "none"],
        default="none",
        required=False,
        dest='base_model',
        help="The base model to use for customization. If none, then skips training step: DEFAULT=none",
    )
    openai_create_optional_named.add_argument(
        "-t", "--thought_time",
        type=int,
        default=10,
        required=False,
        dest='thought_time',
        help="The max amount of time in seconds to consider two individual messages to be part of the same \"thought\": DEFAULT=10",
    )
    openai_create_optional_named.add_argument(
        "-m", "--max_entries",
        type=int,
        default=1000,
        required=False,
        dest='max_entries',
        help="The max amount of entries that may exist in the dataset: DEFAULT=1000",
    )
    openai_create_optional_named.add_argument(
        "-r", "--reduce_mode",
        choices=["first", "last", "middle", "even"],
        default="even",
        required=False,
        dest='reduce_mode',
        help="The method to reduce the entry count of the dataset: DEFAULT=even",
    )
    openai_create_optional_named.add_argument(
        "--dirty",
        action='store_false',
        required=False,
        dest='dirty',
        help="A flag that can be set to skip the clean up step for outputted files: DEFAULT=False",
    )
    openai_create_optional_named.add_argument(
        "--redownload",
        action='store_true',
        required=False,
        dest='redownload',
        help="A flag that can be set to redownload the discord chat logs: DEFAULT=False",
    )

    openai_list_jobs = openai_subcommand.add_parser(
        "list_jobs", description="Get a list of your openAI jobs"
    )
    openai_list_jobs.add_argument(
        "--simple",
        action='store_true',
        required=False,
        dest='simple',
        help="Simplify the output to just the model name, job id, and status",
    )

    openai_list_models = openai_subcommand.add_parser(
        "list_models", description="Get a list of your openAI models"
    )
    openai_list_models.add_argument(
        "--simple",
        action='store_true',
        required=False,
        dest='simple',
        help="Simplify the output to just the model name, job id, and status",
    )

    openai_follow = openai_subcommand.add_parser(
        "follow", description="Follow a custom openAI model job"
    )
    openai_follow.add_argument(
        "-j", "--job_id",
        type=str,
        dest='job_id',
        help="Target job id",
    )

    openai_status = openai_subcommand.add_parser(
        "status", description="Get the status of a custom openAI model job"
    )
    openai_status.add_argument(
        "-j", "--job_id",
        type=str,
        dest='job_id',
        help="Target job id",
    )

    openai_cancel = openai_subcommand.add_parser(
        "cancel", description="Cancel a custom openAI model job"
    )
    openai_cancel.add_argument(
        "-j", "--job_id",
        type=str,
        dest='job_id',
        help="Target job id",
    )

    openai_delete = openai_subcommand.add_parser(
        "delete", description="Delete a custom openAI model"
    )
    openai_delete.add_argument(
        "-m", "--model_id",
        type=str,
        dest='model_id',
        help="Target model id",
    )

    args = parser.parse_args()
    config = configuration.get()
    if args.command == "start":
        bot.start_bot(config)
    elif args.command == "openai":
        if args.subcommand == "create":
            customize.create_model(config["token"], config["openai_key"], args.channel, args.user,
                                   thought_time=args.thought_time, max_entry_count=args.max_entries,
                                   reduce_mode=args.reduce_mode, base_model=args.base_model, clean=args.dirty,
                                   redownload=args.redownload)
        if args.subcommand == "list_jobs":
            openai_wrapper.list_jobs(config["openai_key"], args.simple)
        if args.subcommand == "list_models":
            openai_wrapper.list_models(config["openai_key"], args.simple)
        if args.subcommand == "follow":
            openai_wrapper.follow_job(config["openai_key"], args.job_id)
        if args.subcommand == "status":
            openai_wrapper.get_status(config["openai_key"], args.job_id)
        if args.subcommand == "cancel":
            openai_wrapper.cancel_job(config["openai_key"], args.job_id)
        if args.subcommand == "delete":
            openai_wrapper.delete_model(config["openai_key"], args.model_id)


if __name__ == "__main__":
    discordai()
