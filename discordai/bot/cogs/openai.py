""""
Copyright © Krypton 2019-2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.4.1
"""

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from enum import Enum

import openai

class Models(Enum):
    chatgpt = "gpt-3.5-turbo"
    davinci = "text-davinci-003"
    curie = "text-curie-001"
    babbage = "text-babbage-001"
    ada = "text-ada-001"

class OpenAI(commands.Cog, name="openai"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="openai",
        description="Generate an openAI completion",
    )
    @app_commands.describe(
        prompt="The prompt to pass to openAI: Default=\"\"",
        model=" chatgpt | davinci | curie | babbage | ada:  Default=chatgpt",
        temp="What sampling temperature to use. Higher values means more risks: Min=0 Max=1 Default=1",
        presence_penalty="Number between -2.0 and 2.0. Positive values will encourage new topics: Min=-2 Max=2 Default=0",
        frequency_penalty="Number between -2.0 and 2.0. Positive values will encourage new words: Min=-2 Max=2 Default=0")
    async def openai(self, context: Context, prompt: str = "", model: Models = Models.chatgpt, temp: float = 1.0,
                     presence_penalty: float = 0.0, frequency_penalty: float = 0.0):
        openai.api_key = self.bot.config["openai_key"]
        temp = min(max(temp, 0), 1)
        presPen = min(max(presence_penalty, -2), 2)
        freqPen = min(max(frequency_penalty, -2), 2)

        await context.defer()
        try:
            if model.value == 'gpt-3.5-turbo':
                response = openai.ChatCompletion.create(
                    model=model.value,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temp,
                    frequency_penalty=presPen,
                    presence_penalty=freqPen,
                    max_tokens=325
                )
                await context.send(f"{prompt}\n\n{response['choices'][0]['message']['content']}"[:2000])
            else:
                response = openai.Completion.create(
                    engine=model.value,
                    prompt=prompt,
                    temperature=temp,
                    frequency_penalty=presPen,
                    presence_penalty=freqPen,
                    max_tokens=325,
                    echo=True if prompt else False
                )
                await context.send(response["choices"][0]["text"][:2000])
        except Exception as error:
            print(f"Failed to generate valid response for prompt: {prompt}\nError: {error}")
            await context.send(
                f"Failed to generate valid response for prompt: {prompt}\nError: {error}"
            )


async def setup(bot):
    await bot.add_cog(OpenAI(bot))
