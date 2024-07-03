""""
Copyright © Krypton 2019-2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.4.1
"""

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from openai import OpenAI


class CustomAI(commands.Cog, name="customai"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="customai",
        description="Generate an OpenAI completion for a fine-tuned model",
    )
    @app_commands.describe(
        model="The id of your custom model",
        prompt='The prompt to pass to your model: Default=""',
        temp="Number between 0.0 and 2.0. Higher values means more risks: Min=0.0 Max=2.0 Default=1.0",
        presence_penalty="Number between -2.0 and 2.0. Positive values will encourage new topics: Min=-2 Max=2 Default=0",
        frequency_penalty="Number between -2.0 and 2.0. Positive values will encourage new words: Min=-2 Max=2 Default=0",
        max_tokens="The max number of tokens allowed to be generated. Completion cost scales with token count: Default=125",
        stop="Whether to stop after the first sentence: Default=false",
        openai_key="The OpenAI key associated with the given model: Default=config.OPENAI_API_KEY",
    )
    async def customai(
        self,
        context: Context,
        model: str,
        prompt: str = "",
        temp: float = 1.0,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        max_tokens: int = 125,
        stop: bool = False,
        openai_key: str = "",
    ):
        client = OpenAI(api_key=openai_key or self.bot.OPENAI_API_KEY)
        await context.defer()
        try:
            response = client.completions.create(
                model=model,
                prompt=prompt,
                temperature=temp,
                frequency_penalty=presence_penalty,
                presence_penalty=frequency_penalty,
                max_tokens=max_tokens,
                echo=True if prompt else False,
                stop="." if stop else None,
            )
            await context.send(
                f"Model: {model}\n{'Prompt: ' + prompt if prompt else ''}\n{response.choices[0].text[:2000]}"
            )
        except Exception as error:
            params = dict(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temp,
                frequency_penalty=presence_penalty,
                presence_penalty=frequency_penalty,
                max_tokens=max_tokens,
                stop="." if stop else None,
            )
            print(
                f"Failed to generate valid response with parameters: {params}\nError: {error}"[
                    :2000
                ]
            )
            await context.send(
                f"Failed to generate valid response with paramaters: {params}\nError: {error}"[
                    :2000
                ]
            )
        client.close()


async def setup(bot):
    await bot.add_cog(CustomAI(bot))
