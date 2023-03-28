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
import tiktoken

class Roles(Enum):
    system = "system"
    user = "user"
    assistant = "assistant"

class Warnings(Enum):
    low = ""
    medium = "\n:warning:You are nearing the size limit for chatGPT's chat history:warning:"
    high = ":exclamation:You have reached the size limit for chatGPT's chat history. Use the `/resetchat` command to continue using chatGPT:exclamation:"

def num_tokens_from_messages(messages, model):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens

class ChatGPT(commands.Cog, name="chatgpt"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="chatgpt",
        description="Generate an chatGPT completion",
    )
    @app_commands.describe(
        prompt="The prompt to pass to chatGPT: Default=\"\"",
        role=" system | user | asssistant: Default=user",
        temp="What sampling temperature to use. Higher values means more risks: Min=0 Max=1 Default=1",
        presence_penalty="Number between -2.0 and 2.0. Positive values will encourage new topics: Min=-2 Max=2 Default=0",
        frequency_penalty="Number between -2.0 and 2.0. Positive values will encourage new words: Min=-2 Max=2 Default=0")
    async def chatgpt(self, context: Context, prompt: str = "", role: Roles = Roles.user, temp: float = 1.0,
                     presence_penalty: float = 0.0, frequency_penalty: float = 0.0):
        openai.api_key = self.bot.config["openai_key"]
        model = "gpt-3.5-turbo"
        temp = min(max(temp, 0), 1)
        presPen = min(max(presence_penalty, -2), 2)
        freqPen = min(max(frequency_penalty, -2), 2)
        self.bot.messages.append({"role": role.value, "content": prompt})
        messages = self.bot.messages
        token_cost = num_tokens_from_messages(messages, model)
        if 325 <= 4096-token_cost:
            warning = Warnings.low
        elif 4096-token_cost >= 5:
            warning = Warnings.medium
        else:
            warning = Warnings.high

        await context.defer()
        try:
            if warning == Warnings.high:
                await context.send(warning.value)
            else:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    temperature=temp,
                    frequency_penalty=presPen,
                    presence_penalty=freqPen,
                    max_tokens=325 if 325 <= 4096-token_cost else token_cost
                )
                await context.send(f"{prompt}\n{response['choices'][0]['message']['content']}{warning.value}"[:2000])
        except Exception as error:
            print(f"Failed to generate valid response for prompt: {prompt}\nError: {error}")
            await context.send(
                f"Failed to generate valid response for prompt: {prompt}\nError: {error}"
            )

    @commands.hybrid_command(
        name="resetchat",
        description="Resets the chat history for chatGPT completions",
    )
    async def resetchat(self, context):
        self.bot.messages = []
        await context.send("Chat history has been reset")

async def setup(bot):
    await bot.add_cog(ChatGPT(bot))
