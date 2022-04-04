import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
import asyncio
import os

import keep_alive

bot = commands.Bot(command_prefix="bj!",intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


async def load_cogs(bot: commands.Bot) -> None:
    for filename in os.listdir("./src/cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            await bot.load_extension(f"src.cogs.{filename[:-3]}")


async def main(bot: commands.Bot) -> None:
    await load_cogs(bot)
    async with bot:
        if os.environ["TEST"] != "1":
            keep_alive.alive()
        await bot.start(os.environ["DISCORD_TOKEN"])


asyncio.run(main(bot))
