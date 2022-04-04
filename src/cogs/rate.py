import discord
from discord.ext import commands
import aiofiles
import json
import random, string


class Rate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setup_rate(
        self, ctx, rate_name: str = None, rate_desc: str = "No description provided"
    ):
        if rate_name is None:
            await ctx.send("Please provide a name for the rate!")
            return
        rate_id = "".join(random.choices(string.ascii_letters + string.digits, k=10))
        await ctx.send(
            embed=discord.Embed(
                title="Rate setup",
                description=f"Rate ID: {rate_id}\nRate Name: {rate_name}\nRate Description: {rate_desc}\nYou can delete this with bj!delete_rate {rate_id}",
            )
        )
        await ctx.send("Please continue this process inside Direct Message!")
        user_dm = ctx.user.send
        await user_dm(
            embed=discord.Embed(
                title="Choices for the rate:",
                description="Please send your choices that you wanted in this rate. You can send each of them or split them with comma and you can add the description for choice with:\nExample: choice1,choice2,choice3\nOr\nchoice1\nchoice2\nchoice3\nOr\nchoice1:desc,choice2:desc,choice3:desc\nOr\nchoice1:desc\nchoice2:desc\nchoice3:desc",
            )
        )
        choices = []
        while True:
            choice = await self.bot.wait_for(
                "message", check=lambda m: m.author == ctx.author
            )
            if choice.content == "stop":
                break
            if "," in choice.content:
                if ":" in choice.content:
                    choice_list = choice.content.split(",")
                    for i in choice_list:
                        if ":" in i:
                            choice_list_split = i.split(":")
                            choices.append({choice_list_split[0]: choice_list_split[1]})
                        else:
                            choices.append(i)
                else:
                    choices.extend(choice.content.split(","))
            else:
                choices.append(choice.content)

            await user_dm(
                embed=discord.Embed(
                    title="Added choice",
                    description=f"{choice.content}",
                )
            )
        await user_dm(
            embed=discord.Embed(
                title="Logging channel",
                description="Please send the channel you want to log the votes in! (ID)",
            )
        )
        channel_id = await self.bot.wait_for(
            "message", check=lambda m: m.author == ctx.author
        )
        channel = self.bot.get_channel(int(channel_id.content))
        if channel is None:
            await ctx.send("Channel not found!")
            return
        await user_dm(
            embed=discord.Embed(
                title="Logging channel",
                description=f"Logging channel: {channel.mention}",
            )
        )
        await user_dm(
            embed=discord.Embed(
                title="Your rate is ready!",
                description=f"Rate ID: {rate_id}\nRate Name: {rate_name}\nRate Description: {rate_desc}\nChoices: {choices}\nLogg channel: {channel.mention}",
            )
        )

        await channel.send(
            embed=discord.Embed(
                title="This channel will be used to log the votes for {}!".format(
                    rate_name
                ),
                description=f"Rate ID: {rate_id}\nRate Name: {rate_name}\nRate Description: {rate_desc}\nChoices: {choices}\nLogg channel: {channel.mention}",
            )
        )

        with open("data/rates.json", "r") as f:
            rates = json.load(f)
        rates[rate_id] = {
            "name": rate_name,
            "description": rate_desc,
            "choices": choices,
            "channel": channel.id,
        }
        with open("data/rates.json", "w") as f:
            json.dump(rates, f, indent=4)

    @commands.command()
    async def rate(self, ctx, vote_id: str = None):
        if vote_id == None:
            await ctx.send("Please provide a vote ID")
            return
        async with aiofiles.open("data/votes.json", "r") as f:
            votes = json.load(f)
        if vote_id not in votes:
            await ctx.send("That vote ID does not exist")
            return
        await self.process_rate(ctx, vote_id)

    async def process_rate(self, ctx, vote_id):
        await ctx.send("Please continue this process inside Direct Message!")
        user_dm = ctx.user.send
        await user_dm(
            embed=discord.Embed(title="You're voting for:", description=vote_id)
        )
