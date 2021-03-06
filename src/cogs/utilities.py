import discord
from discord.ext import commands


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @commands.command()
    async def ping(self, ctx):
        """
        Test bot's latency
        """
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def credits(self, ctx):
        """
        Credits because yes
        """
        await ctx.send("This bot was made by <@890913140278181909>")

    @commands.command(name="help")
    async def help(self, ctx, command: str = None):
        """Shows help about a command or the bot"""
        print(command)
        if command is None:
            embed = discord.Embed(
                title="Help", description="", color=discord.Color.blue()
            )
            for command in self.bot.commands:
                if command.hidden:
                    continue
                if command.aliases:
                    aliases = " | ".join(command.aliases)
                    embed.add_field(
                        name=f"{command.name} | {aliases}",
                        value=command.help,
                        inline=True,
                    )
                else:
                    embed.add_field(name=command.name, value=command.help, inline=True)
            await ctx.send(embed=embed)

        else:
            command = self.bot.get_command(command)
            if command is None:
                return await ctx.send("That command does not exist.")
            embed = discord.Embed(
                title=f"Help: {command.name}",
                description=command.help,
                color=discord.Color.blue(),
            )
            embed.add_field(name="Usage", value=command.usage)
            embed.add_field(
                name="Aliases",
                value=", ".join(command.aliases) if command.aliases else "None",
            )
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Utilities(bot))
