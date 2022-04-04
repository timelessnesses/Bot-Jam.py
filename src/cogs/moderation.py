import datetime
import typing

import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def parse_time(
        self, time: typing.Optional[int, str, datetime.timedelta, datetime.datetime]
    ) -> datetime.datetime:
        if isinstance(time, datetime.timedelta):
            return datetime.datetime.now() + time
        elif isinstance(time, datetime.datetime):
            return time
        elif isinstance(time, int):
            return datetime.datetime.now() + datetime.timedelta(seconds=time)
        elif isinstance(time, str):
            return datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        else:
            raise TypeError("Invalid time type")

    @commands.command()
    async def mute(
        self,
        ctx: commands.Context,
        user: discord.Member = None,
        time: int = None,
        *,
        reason: str = None,
    ):
        if user is None:
            await ctx.send("Please specify a user to mute")
            return
        if time is None:
            await ctx.send(
                'Please specify a time (seconds or "Month/Day Hour/Minutes/Seconds" (due to discord API allow timeout up to 28 days)) to mute'
            )
            return
        if reason is None:
            await ctx.send("Please specify a reason to mute")
            return
        time = self.parse_time(time)
        await user.send(
            embed=discord.Embed(
                title="You have been muted",
                description=f"You have been muted by {ctx.author.mention} for {reason}",
                color=discord.Color.red(),
            )
        )
        await user.timeout(reason=reason, until=time)
        await ctx.send(
            embed=discord.Embed(
                title="Muted",
                description=f"{user.mention} has been muted for {reason} by {ctx.author}",
                color=discord.Color.green(),
            )
        )

    @commands.command()
    async def unmute(self, ctx: commands.Context, user: discord.Member = None):
        if user is None:
            await ctx.send("Please specify a user to unmute")
            return
        await user.send(
            embed=discord.Embed(
                title="You have been unmuted",
                description=f"You have been unmuted by {ctx.author.mention}",
                color=discord.Color.green(),
            )
        )
        await user.timeout(reason="Unmuted", until=None)
        await ctx.send(
            embed=discord.Embed(
                title="Unmuted",
                description=f"{user.mention} has been unmuted by {ctx.author}",
                color=discord.Color.green(),
            )
        )

    @commands.command()
    async def kick(
        self, ctx: commands.Context, user: discord.Member = None, *, reason: str = None
    ):
        if user is None:
            await ctx.send("Please specify a user to kick")
            return
        if reason is None:
            await ctx.send("Please specify a reason to kick")
            return
        await user.send(
            embed=discord.Embed(
                title="You have been kicked",
                description=f"You have been kicked by {ctx.author.mention} for {reason}",
                color=discord.Color.red(),
            )
        )
        await user.kick(reason=reason)
        await ctx.send(
            embed=discord.Embed(
                title="Kicked",
                description=f"{user.mention} has been kicked for {reason} by {ctx.author}",
                color=discord.Color.green(),
            )
        )

    @commands.command()
    async def ban(
        self, ctx: commands.Context, user: discord.Member = None, *, reason: str = None
    ):
        if user is None:
            await ctx.send("Please specify a user to ban")
            return
        if reason is None:
            await ctx.send("Please specify a reason to ban")
            return
        await user.send(
            embed=discord.Embed(
                title="You have been banned",
                description=f"You have been banned by {ctx.author.mention} for {reason}",
                color=discord.Color.red(),
            )
        )
        await user.ban(reason=reason)
        await ctx.send(
            embed=discord.Embed(
                title="Banned",
                description=f"{user.mention} has been banned for {reason} by {ctx.author}",
                color=discord.Color.green(),
            )
        )

    @commands.command()
    async def unban(
        self, ctx: commands.Context, user: discord.Member = None, *, reason: str = None
    ):
        if user is None:
            await ctx.send("Please specify a user to unban")
            return
        if reason is None:
            await ctx.send("Please specify a reason to unban")
            return
        await user.send(
            embed=discord.Embed(
                title="You have been unbanned",
                description=f"You have been unbanned by {ctx.author.mention} for {reason}",
                color=discord.Color.green(),
            )
        )
        await user.unban(reason=reason)
        await ctx.send(
            embed=discord.Embed(
                title="Unbanned",
                description=f"{user.mention} has been unbanned for {reason} by {ctx.author}",
                color=discord.Color.green(),
            )
        )


async def setup(bot):
    await bot.add_cog(Moderation(bot))
