import json
import discord
from discord.ext import commands
import aiofiles
import string
import random


class Voting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setup_vote(
        self, ctx, channel: discord.TextChannel = None, *, message: str = None
    ):
        if channel is None:
            channel = ctx.channel

        id = "".join(random.sample(string.ascii_letters + string.digits, 10))
        async with aiofiles.open("data/votes.json", "r") as f:
            votes = json.loads(await f.read())
        votes[id] = {
            "channel": channel.id,
            "message": message,
            "choices": [],
            "questions": [],
        }
        async with aiofiles.open("data/votes.json", "w") as f:
            await f.write(json.dumps(votes))

    @commands.command()
    async def add_choices(
        self,
        ctx,
        vote_id: str = None,
        *,
        choice: str = None,
        description: str = "No description provided"
    ):
        if vote_id is None:
            await ctx.send("Please specify a vote id")
            return
        if choice is None:
            await ctx.send("Please specify a choice")
            return
        async with aiofiles.open("data/votes.json", "r") as f:
            votes = json.loads(await f.read())
        if vote_id not in votes:
            await ctx.send("Please specify a valid vote id")
            return
        votes[vote_id]["choices"].append({choice: description})
        async with aiofiles.open("data/votes.json", "w") as f:
            await f.write(json.dumps(votes))

    @commands.command()
    async def remove_choices(self, ctx, vote_id: str = None, *, choice: str = None):
        if vote_id is None:
            await ctx.send("Please specify a vote id")
            return
        if choice is None:
            await ctx.send("Please specify a choice")
            return
        async with aiofiles.open("data/votes.json", "r") as f:
            votes = json.loads(await f.read())
        if vote_id not in votes:
            await ctx.send("Please specify a valid vote id")
            return
        votes[vote_id]["choices"].remove({choice: description})
        async with aiofiles.open("data/votes.json", "w") as f:
            await f.write(json.dumps(votes))

    @commands.command()
    async def remove_vote(self, ctx, vote_id: str = None):
        if vote_id is None:
            await ctx.send("Please specify a vote id")
            return
        async with aiofiles.open("data/votes.json", "r") as f:
            votes = json.loads(await f.read())
        if vote_id not in votes:
            await ctx.send("Please specify a valid vote id")
            return
        del votes[vote_id]
        async with aiofiles.open("data/votes.json", "w") as f:
            await f.write(json.dumps(votes))

    @commands.command()
    async def add_question(self, ctx, vote_id: str = None, question: str = None):
        if vote_id is None:
            await ctx.send("Please specify a vote id")
            return
        if question is None:
            await ctx.send()

    @commands.command()
    async def register_vote(self, ctx):
        pass
