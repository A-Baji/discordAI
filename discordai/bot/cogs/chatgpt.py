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


class ChatGPT(commands.Cog, name="chatgpt"):
    models = Literal["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4o", "gpt-4-turbo"]

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="chatgpt",
        description="Generate OpenAI chat conversations",
    )
    @app_commands.describe(
        prompt="The prompt to pass in",
        model="Listed by cost: Default=gpt-4o-mini",
        temp="Number between 0.0 and 2.0. Higher values means more risks: Min=0.0 Max=2.0 Default=1.0",
        presence_penalty="Number between -2.0 and 2.0. Positive values will encourage new topics: Min=-2.0 Max=2.0 Default=0.0",
        frequency_penalty="Number between -2.0 and 2.0. Positive values will encourage new words: Min=-2.0 Max=2.0 Default=0.0",
        max_tokens="The max number of tokens allowed to be generated. Completion cost scales with token count: Default=300",
    )
    async def chatgpt(
        self,
        context: Context,
        prompt: str,
        model: models = "gpt-4o-mini",
        temp: float = 1.0,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        max_tokens: int = 300,
    ):
        client = OpenAI(api_key=self.bot.OPENAI_API_KEY)
        if context.guild.id not in self.bot.chat_messages:
            self.bot.chat_messages[context.guild.id] = [
                {"role": "system", "content": "You are a helpful assistant."}
            ]
        self.bot.chat_messages[context.guild.id].append(
            {"role": "user", "content": prompt}
        )
        messages = self.bot.chat_messages[context.guild.id]

        await context.defer()
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temp,
                frequency_penalty=presence_penalty,
                presence_penalty=frequency_penalty,
                max_tokens=max_tokens,
            )
            message = response.choices[0].message
            await context.send(f"{prompt}\n\n{message.content}"[:2000])
            self.bot.chat_messages[context.guild.id].append(message)
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

    @commands.hybrid_command(
        name="chatreset",
        description="Resets the chat history for ChatGPT conversations",
    )
    async def chatreset(self, context):
        self.bot.chat_messages[context.guild.id] = [
            self.bot.chat_messages[context.guild.id][0]
        ]
        await context.send("Chat history has been reset")

    @commands.hybrid_command(
        name="chatinit",
        description="Initialize ChatGPT's instructional system message",
    )
    @app_commands.describe(
        message="The initialization message. Ex: You are a helpful assistant that speaks with a southern drawl."
    )
    async def chatinit(self, context, message: str):
        if context.guild.id in self.bot.chat_messages:
            if self.bot.chat_messages[context.guild.id][0]["role"] == "system":
                # Overwrite system message
                self.bot.chat_messages[context.guild.id][0] = {
                    "role": "system",
                    "content": message,
                }
            else:
                # Push system message if nonexistant
                self.bot.chat_messages[context.guild.id].insert(
                    {"role": "system", "content": message}, 0
                )
        else:
            # Init guild messages with system message
            self.bot.chat_messages[context.guild.id] = [
                {"role": "system", "content": message}
            ]
        await context.send(f'ChatGPT has been initialized with "{message}"'[:2000])


async def setup(bot):
    await bot.add_cog(ChatGPT(bot))
