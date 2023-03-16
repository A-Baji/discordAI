from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

import openai


class Justin(commands.Cog, name="justin"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="justin",
        description="Generate a completion for justin",
    )
    @app_commands.describe(
        prompt="The prompt to pass to your model: Default=\"\"",
        temp="What sampling temperature to use. Higher values means more risks: Min=0 Max=1 Default=0.5",
        presence_penalty="Number between -2.0 and 2.0. Positive values will encourage new topics: Min=-2 Max=2 Default=0.5",
        frequency_penalty="Number between -2.0 and 2.0. Positive values will encourage new words: Min=-2 Max=2 Default=0.5",
        max_tokens="The max number of tokens to generate. Each token costs credits: Default=75",
        stop="Whether to stop after the first sentence: Default=False",
        bold="Whether to bolden the original prompt: Default=True")
    async def customai(self, context: Context, prompt: str = "", temp: float = 0.5,
                       presence_penalty: float = 0.5, frequency_penalty: float = 0.5, max_tokens: int = 75,
                       stop: bool = False, bold: bool = True):
        temp = min(max(temp, 0), 1)
        presPen = min(max(presence_penalty, -2), 2)
        freqPen = min(max(frequency_penalty, -2), 2)

        await context.defer()
        try:
            openai.api_key = "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"
            response = openai.Completion.create(
                engine="davinci:ft-personal:not-justin-8789-2023-02-23-02-29-05",
                prompt=prompt,
                temperature=temp,
                frequency_penalty=presPen,
                presence_penalty=freqPen,
                max_tokens=max_tokens,
                echo=False,
                stop='.' if stop else None,
            )
            await context.send(f"{'**' if bold and prompt else ''}{prompt}{'**' if bold and prompt else ''}{response['choices'][0]['text'][:2000]}")
        except Exception as error:
            print(f"Failed to generate valid response for prompt: {prompt}\nError: {error}")
            await context.send(
                f"Failed to generate valid response for prompt: {prompt}\nError: {error}"
            )


async def setup(bot):
    await bot.add_cog(Justin(bot))
