import os
import pathlib
import shutil
import sys
import appdirs


template = """from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from openai import OpenAI

import re


def replace_emoji(emoji_name: str, emoji_map):
    emoji = emoji_name.lower()
    if emoji in emoji_map:
        emoji_id = emoji_map[emoji]["id"]
        emoji_name = emoji_map[emoji]["name"]
        is_animated = emoji_map[emoji]["is_animated"]
        return f"<{{'a' if is_animated else ''}}:{{emoji_name}}:{{emoji_id}}>"
    else:
        return f":{{emoji_name}}:"


class {class_name}(commands.Cog, name="{command_name}"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="{command_name}",
        description="Generate a completion for {command_name}",
    )
    @app_commands.describe(
        prompt='The prompt to pass in: Default=\\"\\"',
        temp="Number between 0.0 and 2.0. Higher values means more risks: Min=0.0 Max=2.0 Default={temp_default}",
        presence_penalty="Number between -2.0 and 2.0. Positive values will encourage new topics: Min=-2.0 Max=2.0 Default={pres_default}",
        frequency_penalty="Number between -2.0 and 2.0. Positive values will encourage new words: Min=-2.0 Max=2.0 Default={freq_default}",
        max_tokens="The max number of tokens allowed to be generated. Completion cost scales with token count: Default={max_tokens_default}",
        stop="Whether to stop after the first sentence: Default={stop_default}",
        bold="Whether to bolden the original prompt: Default={bold_default}",
    )
    async def {command_name}(
        self,
        context: Context,
        prompt: str = "",
        temp: float = {temp_default},
        presence_penalty: float = {pres_default},
        frequency_penalty: float = {freq_default},
        max_tokens: int = {max_tokens_default},
        stop: bool = {stop_default},
        bold: bool = {bold_default},
    ):
        client = OpenAI(
            api_key="{openai_key}"
        )
        await context.defer()
        try:
            response = client.completions.create(
                model="{model_id}",
                prompt=f"{username} says: {{prompt}}",
                temperature=temp,
                frequency_penalty=presence_penalty,
                presence_penalty=frequency_penalty,
                max_tokens=max_tokens,
                echo=False,
                stop="." if stop else None,
            )
            prompt = f"**{{prompt}}**" if bold and prompt else prompt
            emojied_response = re.sub(
                r":(\\w+):",
                lambda match: replace_emoji(match.group(1), context.bot.emoji_map),
                f"{{prompt}}{{response.choices[0].text}}",
            )
            await context.send(emojied_response[:2000])
        except Exception as error:
            params = dict(
                prompt=prompt,
                temp=temp,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                max_tokens=max_tokens,
                stop=stop,
                bold=bold,
            )
            print(
                {error}
            )
            await context.send(
                {error}[
                    :2000
                ]
            )
        client.close()


async def setup(bot):
    await bot.add_cog({class_name}(bot))
"""

config_dir = pathlib.Path(appdirs.user_data_dir(appname="discordai"))


def get_cogs_path(update_cogs=False):
    if getattr(sys, "frozen", False):
        # The code is being run as a frozen executable
        data_dir = pathlib.Path(appdirs.user_data_dir(appname="discordai"))
        cogs_path = data_dir / "discordai" / "bot" / "cogs"
        og_data_dir = pathlib.Path(sys._MEIPASS)
        og_cogs_path = og_data_dir / "discordai" / "bot" / "cogs"
        if not cogs_path.exists():
            # Copy files from the bundled location to the user data directory
            shutil.copytree(og_cogs_path, cogs_path, dirs_exist_ok=True)
        elif update_cogs:
            # Recopy the cogs in case of updates
            for file in og_cogs_path.glob("*"):
                dest_file = cogs_path / file.name
                shutil.copy2(file, dest_file)
    else:
        # The code is being run normally
        template_dir = pathlib.Path(os.path.dirname(__file__))
        cogs_path = template_dir / "bot" / "cogs"
    return cogs_path


def gen_new_command(
    model_id: str,
    command_name: str,
    openai_key: str = os.getenv("OPENAI_API_KEY"),
    temp_default: float = 1.0,
    pres_default: float = 0.0,
    freq_default: float = 0.0,
    max_tokens_default: int = 125,
    stop_default: bool = False,
    bold_default: bool = False,
):
    cogs_path = get_cogs_path()
    try:
        username = model_id.split(":")[3].split("-")[0]
    except IndexError:
        username = "bot"
    with open(pathlib.Path(cogs_path, f"{command_name}.py"), "w") as f:
        cogs_path.mkdir(exist_ok=True)
        f.write(
            template.format(
                model_id=model_id,
                openai_key=openai_key,
                username=username,
                command_name=command_name,
                temp_default=float(temp_default),
                pres_default=float(pres_default),
                freq_default=float(freq_default),
                max_tokens_default=max_tokens_default,
                stop_default=stop_default,
                bold_default=bold_default,
                class_name=command_name.capitalize(),
                error='f"Failed to generate valid response with parameters: {params}\\nException: {type(error).__name__}\\nError: {error}"',
            )
        )
        print(
            f"Successfully created new slash command: /{command_name} using model {model_id}"
        )


def delete_command(command_name: str, force=False):
    confirm = (
        "yes"
        if force
        else input(
            "Are you sure you want to delete this command? This action is not reversable. Y/N: "
        )
    )
    if confirm.lower() not in ["y", "yes"]:
        print("Cancelling command deletion...")
        return
    cogs_path = get_cogs_path()
    cmd_file = pathlib.Path(cogs_path, f"{command_name}.py")
    if cmd_file.exists():
        cmd_file.unlink()
        print(f"Successfully deleted command: /{command_name}")
    else:
        print("Failed to delete command: No command with that name was found.")


def list_commands():
    cogs_path = get_cogs_path()
    return [
        f"/{file.stem}"
        for file in cogs_path.glob("*.py")
        if file.stem not in ["__init__", "sync"]
    ]
