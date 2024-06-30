def setup_bot_start(bot_subcommand):
    bot_cmd_start = bot_subcommand.add_parser(
        "start", description="Start your discord bot"
    )
    bot_cmd_optional_named = bot_cmd_start.add_argument_group(
        "optional named arguments"
    )

    bot_cmd_optional_named.add_argument(
        "--sync",
        action="store_true",
        required=False,
        dest="sync",
        help="Sync discord commands gloablly on start up",
    )


def setup_add_bot_command(bot_cmd_commands_subcommand):
    add_cmd = bot_cmd_commands_subcommand.add_parser(
        "add",
        description="Add a new slash command for your bot to use a customized model",
    )
    add_cmd_required_named = add_cmd.add_argument_group("required named arguments")
    add_cmd_optional_named = add_cmd.add_argument_group("optional named arguments")

    add_cmd_required_named.add_argument(
        "-n",
        "--command-name",
        type=str,
        required=True,
        dest="command_name",
        help="The name you want to use for the command",
    )
    add_cmd_required_named.add_argument(
        "-i",
        "--model-id",
        type=str,
        required=True,
        dest="model_id",
        help="The ID of the customized model for the slash command to use",
    )
    add_cmd_optional_named.add_argument(
        "-o",
        "--openai-key",
        type=str,
        required=False,
        dest="openai_key",
        help="The openAI key associated with the model being used: DEFAULT=config.OPENAI_API_KEY",
    )
    add_cmd_optional_named.add_argument(
        "-t",
        "--temp-default",
        type=float,
        default=1,
        required=False,
        dest="temp_default",
        help="The default temperature to use for completions: DEFAULT=1",
    )
    add_cmd_optional_named.add_argument(
        "-p",
        "--pres-default",
        type=float,
        default=0,
        required=False,
        dest="pres_default",
        help="The default presence penalty to use for completions: DEFAULT=0",
    )
    add_cmd_optional_named.add_argument(
        "-f",
        "--freq-default",
        type=float,
        default=0,
        required=False,
        dest="freq_default",
        help="The default frequency penalty to use for completions: DEFAULT=0",
    )
    add_cmd_optional_named.add_argument(
        "-m",
        "--max-tokens-default",
        type=int,
        default=125,
        required=False,
        dest="max_tokens_default",
        help="The default max tokens to use for completions: DEFAULT=125",
    )
    add_cmd_optional_named.add_argument(
        "--stop-default",
        action="store_true",
        required=False,
        dest="stop_default",
        help="Set the stop option to use for completions to True",
    )
    add_cmd_optional_named.add_argument(
        "--bold_default",
        action="store_true",
        required=False,
        dest="bold_default",
        help="Set the bolden option for prompts to True",
    )


def setup_delete_bot_command(bot_cmd_commands_subcommand):
    delete_cmd = bot_cmd_commands_subcommand.add_parser(
        "delete", description="Delete a slash command from your bot"
    )
    delete_cmd_required_named = delete_cmd.add_argument_group(
        "required named arguments"
    )

    delete_cmd_required_named.add_argument(
        "-n",
        "--command-name",
        type=str,
        required=True,
        dest="command_name",
        help="The name of the slash command you want to delete",
    )


def setup_update_bot_token(config_subcommand):
    config_bot_token = config_subcommand.add_parser(
        "bot-token", description="Get or set your discord bot token"
    )
    config_bot_token_optional_named = config_bot_token.add_argument_group(
        "optional named arguments"
    )

    config_bot_token_optional_named.add_argument(
        "-t",
        "--set-token",
        type=str,
        required=False,
        dest="new_token",
        help="A new Discord bot token to update the config with",
    )


def setup_update_openai_key(config_subcommand):
    config_openai_key = config_subcommand.add_parser(
        "openai-key", description="Get or set your openaAI API key"
    )
    config_openai_key_optional_named = config_openai_key.add_argument_group(
        "optional named arguments"
    )

    config_openai_key_optional_named.add_argument(
        "-k",
        "--set-key",
        type=str,
        required=False,
        dest="new_key",
        help="A new OpenAI API key to update the config with",
    )
