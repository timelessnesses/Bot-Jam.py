import discord
from discord.ext import commands


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def credits(self, ctx):
        await ctx.send("This bot was made by <@890913140278181909>")


async def setup(bot):
    await bot.add_cog(Utilities(bot))
