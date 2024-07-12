from discordai_modelizer.command_line.subparsers import (
    set_openai_help_str,
    set_bot_key_help_str,
)


def setup_bot_start(bot_subcommand):
    bot_cmd_start = bot_subcommand.add_parser("start", help="Start your Discord bot")
    bot_cmd_required_named = bot_cmd_start.add_argument_group(
        "required named arguments"
    )
    bot_cmd_optional_named = bot_cmd_start.add_argument_group(
        "optional named arguments"
    )

    bot_cmd_required_named.add_argument(
        "-d",
        "--discord-token",
        type=str,
        dest="discord_token",
        help=f"The Discord token for your bot. Must either be passed in as an argument or set {set_bot_key_help_str(is_parent=True)}",
    )
    bot_cmd_required_named.add_argument(
        "-o",
        "--openai-key",
        type=str,
        dest="openai_key",
        help=f"The OpenAI API key to use for various OpenAI operations. Must either be passed in as an argument or set {set_openai_help_str(is_parent=True)}",
    )
    bot_cmd_optional_named.add_argument(
        "--sync",
        action="store_true",
        required=False,
        dest="sync",
        help="Sync Discord commands globally on start up",
    )


def setup_add_bot_command(bot_cmd_commands_subcommand):
    add_cmd = bot_cmd_commands_subcommand.add_parser(
        "add",
        help="Add a new slash command for your bot to use a customized model",
    )
    add_cmd_required_named = add_cmd.add_argument_group("required named arguments")
    add_cmd_optional_named = add_cmd.add_argument_group("optional named arguments")

    add_cmd_required_named.add_argument(
        "-c",
        "--command-name",
        type=str,
        required=True,
        dest="command_name",
        help="The name you want to use for the command",
    )
    add_cmd_required_named.add_argument(
        "-m",
        "--model-id",
        type=str,
        required=True,
        dest="model_id",
        help="The ID of the customized model for the slash command to use",
    )
    add_cmd_required_named.add_argument(
        "-o",
        "--openai-key",
        type=str,
        required=False,
        dest="openai_key",
        help=f"The OpenAI API key associated with the model being used.  Must either be passed in as an argument or set {set_openai_help_str(is_parent=True)}",
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
        "-n",
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
        help="Set the stop option to use for completions to True, which will stop completions at the first '.'",
    )
    add_cmd_optional_named.add_argument(
        "--bold_default",
        action="store_true",
        required=False,
        dest="bold_default",
        help="Set the bolden option for prompts to True, which will bolden the prompt portion of a completion",
    )


def setup_delete_bot_command(bot_cmd_commands_subcommand):
    delete_cmd = bot_cmd_commands_subcommand.add_parser(
        "delete", help="Delete a slash command from your bot"
    )
    delete_cmd_required_named = delete_cmd.add_argument_group(
        "required named arguments"
    )
    delete_cmd_optional_named = delete_cmd.add_argument_group(
        "optional named arguments"
    )

    delete_cmd_required_named.add_argument(
        "-c",
        "--command-name",
        type=str,
        required=True,
        dest="command_name",
        help="The name of the slash command you want to delete",
    )

    delete_cmd_optional_named.add_argument(
        "--force",
        action="store_true",
        required=False,
        dest="force",
        help="Skips the deletion confirmation dialogue",
    )


def setup_list_bot_command(bot_cmd_commands_subcommand):
    bot_cmd_commands_subcommand.add_parser(
        "list", help="List all slash commands for your bot"
    )


def setup_update_config(config_subcommand):
    config_command = config_subcommand.add_parser(
        "update", help="Update your DiscordAI config"
    )
    config_command.add_argument(
        "key", help="The key to update: `DISCORD_BOT_TOKEN` | `OPENAI_API_KEY`"
    )
    config_command.add_argument("value", help="The new value for the key")
