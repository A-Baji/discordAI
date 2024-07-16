""""
Copyright © Krypton 2019-2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python programming language.

Version: 5.4.1
"""

from typing import Literal
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from openai import OpenAI


class ImageAI(commands.Cog, name="imageai"):
    models = Literal["dall-e-2", "dall-e-3"]
    sizes = Literal["small", "medium", "large"]
    qualities = Literal["standard", "hd"]
    styles = Literal["vivid", "natural"]

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="imageai",
        description="Create an OpenAI image generation",
    )
    @app_commands.describe(
        prompt="The prompt to pass in",
        model="Default=dall-e-2",
        size="Medium and large sizes for dall-e-3 only swaps orientation: Default=small",
        quality="Only applies to dall-e-3 generations: Default=standard",
        style="Only applies to dall-e-3 generations: Default=vivid",
    )
    async def openai(
        self,
        context: Context,
        prompt: str,
        model: models = "dall-e-2",
        size: sizes = "small",
        quality: qualities = "standard",
        style: styles = "vivid",
    ):
        size_map = {
            "dall-e-2": {"small": "256x256", "medium": "512x512", "large": "1024x1024"},
            "dall-e-3": {
                "small": "1024x1024",
                "medium": "1792x1024",
                "large": "1024x1792",
            },
        }
        params = dict()
        if model == "dall-e-3":
            params = dict(
                quality=quality,
                style=style,
            )
        client = OpenAI(api_key=self.bot.OPENAI_API_KEY)
        await context.defer()
        try:
            response = client.images.generate(
                prompt=prompt, model=model, size=size_map[model][size], **params
            )
            await context.send(response.data[0].url)
        except Exception as error:
            params = dict(
                prompt=prompt,
                model=model,
                size=size,
                quality=quality,
                style=style,
            )
            print(f"Failed to generate image with parameters: {prompt}\nError: {error}")
            await context.send(
                f"Failed to generate image with parameters: {prompt}\nException: {type(error).__name__}\nError: {error}"[
                    :2000
                ]
            )
        client.close()


async def setup(bot):
    await bot.add_cog(ImageAI(bot))
