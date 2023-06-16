"""
Copyright © Krypton 2019-2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.4.1
"""

import asyncio
import os
import pathlib
import platform
import shutil
import sys
import appdirs
import importlib.util

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context
from discordai import __version__ as version

intents = discord.Intents.default()
intents.message_content = True
bot = Bot(command_prefix=commands.when_mentioned_or(
    '/'), intents=intents, help_command=None)


def start_bot(config, sync=False):
    bot.config = config
    bot.chat_messages = {}
    bot.emoji_map = {}

    @bot.event
    async def on_ready() -> None:
        """
        The code in this even is executed when the bot is ready
        """
        print(f"Logged in as {bot.user.name}")
        print(f"DiscordAi version: {version}")
        print(f"discord.py API version: {discord.__version__}")
        print(f"Python version: {platform.python_version()}")
        print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        if sync:
            print("Syncing commands globally...")
            await bot.tree.sync()
        for guild in bot.guilds:
            for emoji in guild.emojis:
                if emoji.name not in bot.emoji_map:
                    bot.emoji_map[emoji.name] = [emoji.id, emoji.animated]
        print("-------------------")

    @bot.event
    async def on_message(message: discord.Message) -> None:
        """
        The code in this event is executed every time someone sends a message, with or without the prefix

        :param message: The message that was sent.
        """
        if message.author == bot.user or message.author.bot:
            return
        await bot.process_commands(message)

    @bot.event
    async def on_command_completion(context: Context) -> None:
        """
        The code in this event is executed every time a normal command has been *successfully* executed
        :param context: The context of the command that has been executed.
        """
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        if context.guild is not None:
            print(
                f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})")
        else:
            print(
                f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs")

    @bot.event
    async def on_command_error(context: Context, error) -> None:
        """
        The code in this event is executed every time a normal valid command catches an error
        :param context: The context of the normal command that failed executing.
        :param error: The error that has been faced.
        """
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = discord.Embed(
                title="Hey, please slow down!",
                description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Error!",
                description="You are missing the permission(s) `" + ", ".join(
                    error.missing_permissions) + "` to execute this command!",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                title="Error!",
                description="I am missing the permission(s) `" + ", ".join(
                    error.missing_permissions) + "` to fully perform this command!",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Error!",
                # We need to capitalize because the command arguments have no capital letter in the code.
                description=str(error).capitalize(),
                color=0xE02B2B
            )
            await context.send(embed=embed)
        raise error

    async def load_cogs() -> None:
        """
        The code in this function is executed whenever the bot will start.
        """
        if getattr(sys, 'frozen', False):
            # The code is being run as a frozen executable
            cogs_path = pathlib.Path(appdirs.user_data_dir(appname="discordai")) / "discordai" / "bot" / "cogs"
            data_dir = pathlib.Path(sys._MEIPASS)
            og_cogs_path = data_dir / "discordai" / "bot" / "cogs"
            os.makedirs(cogs_path, exist_ok=True)
            for file in og_cogs_path.glob("*"):
                dest_file = cogs_path / file.name
                shutil.copy2(file, dest_file)
            for file in os.listdir(cogs_path):
                if file.endswith(".py"):
                    extension = file[:-3]
                    if extension != "__init__":
                        try:
                            module_path = cogs_path / f'{extension}.py'
                            spec = importlib.util.spec_from_file_location(extension, module_path)
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            await module.setup(bot=bot)
                            print(f"Loaded extension '{extension}'")
                        except Exception as e:
                            exception = f"{type(e).__name__}: {e}"
                            print(f"Failed to load extension {extension}\n{exception}")
        else:
            # The code is being run normally
            bot_dir = pathlib.Path(os.path.dirname(__file__))
            cogs_path = bot_dir / "cogs"
            for file in os.listdir(cogs_path):
                if file.endswith(".py"):
                    extension = file[:-3]
                    if extension != "__init__":
                        try:
                            await bot.load_extension(f".cogs.{extension}", package="discordai.bot")
                            print(f"Loaded extension '{extension}'")
                        except Exception as e:
                            exception = f"{type(e).__name__}: {e}"
                            print(f"Failed to load extension {extension}\n{exception}")

    asyncio.run(load_cogs())
    bot.run(config["token"])
