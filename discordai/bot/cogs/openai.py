""""
Copyright © Krypton 2019-2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python programming language.

Version: 5.4.1
"""

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from openai import OpenAI as OpenAI_API
from typing import Literal


class OpenAI(commands.Cog, name="openai"):
    models = Literal["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4o", "gpt-4-turbo"]

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="openai",
        description="Generate an OpenAI chat completion",
    )
    @app_commands.describe(
        prompt="The prompt to pass in",
        model="Listed by cost: Default=gpt-4o-mini",
        temp="Number between 0.0 and 2.0. Higher values means more risks: Min=0.0 Max=2.0 Default=1.0",
        presence_penalty="Number between -2.0 and 2.0. Positive values will encourage new topics: Min=-2.0 Max=2.0 Default=0.0",
        frequency_penalty="Number between -2.0 and 2.0. Positive values will encourage new words: Min=-2.0 Max=2.0 Default=0.0",
        max_tokens="The max number of tokens allowed to be generated. Completion cost scales with token count: Default=300",
    )
    async def openai(
        self,
        context: Context,
        prompt: str,
        model: models = "gpt-4o-mini",
        temp: float = 1.0,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        max_tokens: int = 300,
    ):
        client = OpenAI_API(api_key=self.bot.OPENAI_API_KEY)
        await context.defer()
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temp,
                frequency_penalty=presence_penalty,
                presence_penalty=frequency_penalty,
                max_tokens=max_tokens,
            )
            await context.send(
                f"{prompt}\n\n{response.choices[0].message.content}"[:2000]
            )
        except Exception as error:
            params = dict(
                prompt=prompt,
                model=model,
                temp=temp,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                max_tokens=max_tokens,
            )
            print(
                f"Failed to generate valid response with parameters: {params}\nError: {error}"
            )
            await context.send(
                f"Failed to generate valid response with paramaters: {params}\nException: {type(error).__name__}\nError: {error}"[
                    :2000
                ]
            )
        client.close()


async def setup(bot):
    await bot.add_cog(OpenAI(bot))
