import json
import random
import string

import aiofiles
import discord
from discord.ext import commands


class Rates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setup_rate(
        self, ctx, rate_name: str = None, rate_desc: str = "No description provided"
    ):
        """
        Setup the rate
        """
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
        """
        Rate the choices
        """
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
            embed=discord.Embed(title="You're voting in: ", description=vote_id)
        )
        async with aiofiles.open("data/rates.json", "r") as f:
            rates = json.load(f)
        rate = rates[vote_id]
        choices = rate["choices"]
        await user_dm(
            embed=discord.Embed(
                title="Choices for the rate:",
                description=f"There is {len(choices)} choices for this rate!",
            )
        )
        answers = {}
        while True:
            await user_dm(
                embed=discord.Embed(
                    title="Choices for the rate:",
                    description="Please select the choice you want to vote for! (Index/Name)",
                )
            )
            choice = await self.bot.wait_for(
                "message", check=lambda m: m.author == ctx.author
            )
            if choice.content == "stop":
                break
            if choice.content.isdigit():
                try:
                    choice_ = choices[int(choice.content)]
                except IndexError:
                    await user_dm(
                        embed=discord.Embed(
                            title="Error",
                            description="That choice does not exist!",
                        )
                    )
                    continue
            else:
                try:
                    choice_ = next(
                        i for i in choices if i.lower() == choice.content.lower()
                    )
                except StopIteration:
                    await user_dm(
                        embed=discord.Embed(
                            title="Error",
                            description="That choice does not exist!",
                        )
                    )
                    continue
            await user_dm(
                embed=discord.Embed(
                    title="Your selection is:",
                    description=f"{choice_}",
                )
            )
            await user_dm(
                embed=discord.Embed(
                    title="Please answer these questions for the rate:",
                )
            )
            for i in rate["questions"]:
                if isinstance(i, dict):  # question has desc
                    for key, val in i.items():
                        await user_dm(
                            embed=discord.Embed(
                                title=key,
                                description=val,
                            )
                        )
                else:
                    await user_dm(
                        embed=discord.Embed(
                            title=i,
                        )
                    )
                await user_dm(
                    embed=discord.Embed(
                        title="Your answer:",
                    )
                )
                answer = await self.bot.wait_for(
                    "message", check=lambda m: m.author == ctx.author
                )
                try:
                    answers[choice_][i] = answer.content
                except KeyError:
                    answers[choice_] = {i: answer.content}
            await user_dm(
                embed=discord.Embed(
                    title="Your answer for {} is:".format(choice_),
                    description=f"{answers}",
                )
            )

        await user_dm(
            embed=discord.Embed(
                title="Thank you for voting!",
                description="Your vote has been logged!",
            )
        )

        log_channel = self.bot.get_channel(int(rate["channel"]))
        embeds = []
        for choice, answer in answers.items():
            embed = discord.Embed(
                title="Rate for {}".format(choice),
                description=f"{answer}",
            )
            for key, val in answer.items():
                embed.add_field(name=key, value=val)
            embeds.append(embed)
        await log_channel.send(embed=discord.Embed(title="New vote!"), embeds=embeds)
        async with aiofiles.open("data/votes.json", "r") as f:
            votes = json.loads(await f.read())
        try:
            votes[vote_id][ctx.author.id]["answers"] = answers
        except KeyError:
            votes[vote_id].update({ctx.author.id: {"answers": answers}})
        async with aiofiles.open("data/votes.json", "w") as f:
            await f.write(json.dumps(votes, indent=4))

    @commands.command()
    async def rates(self, ctx):
        """
        List all rates
        """
        async with aiofiles.open("data/rates.json", "r") as f:
            rates = json.load(f)
        await ctx.send(
            embed=discord.Embed(
                title="Rates:",
                description="\n".join([f"{i}: {rates[i]['name']}" for i in rates]),
            )
        )

    @commands.command()
    async def rates_info(self, ctx, rate_id: str = None):
        """
        Get info about a rate
        """
        if rate_id == None:
            await ctx.send("Please provide a rate ID")
            return
        async with aiofiles.open("data/rates.json", "r") as f:
            rates = json.load(f)
        if rate_id not in rates:
            await ctx.send("That rate ID does not exist")
            return
        rate = rates[rate_id]
        await ctx.send(
            embed=discord.Embed(
                title="Rate info:",
                description=f"{rate['name']}\n{rate['description']}",
            )
        )

    @commands.command()
    async def delete_rate(self, ctx, rate_id: str = None):
        """
        Delete a rate
        """
        if rate_id == None:
            await ctx.send("Please provide a rate ID")
            return
        async with aiofiles.open("data/rates.json", "r") as f:
            rates = json.load(f)
        if rate_id not in rates:
            await ctx.send("That rate ID does not exist")
            return
        await ctx.send(
            embed=discord.Embed(
                title="Are you sure you want to delete this rate?",
                description="This action is irreversible!",
            )
        )
        choice = await self.bot.wait_for(
            "message", check=lambda m: m.author == ctx.author
        )
        if choice.content.lower() == "yes":
            del rates[rate_id]
            await ctx.send(
                embed=discord.Embed(
                    title="Rate deleted!",
                    description="The rate has been deleted!",
                )
            )
            async with aiofiles.open("data/rates.json", "w") as f:
                await f.write(json.dumps(rates, indent=4))
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Rate not deleted!",
                    description="The rate has not been deleted!",
                )
            )

    @commands.command()
    async def edit_rate(self, ctx, rate_id: str = None):
        """
        Edit a rate
        """
        if rate_id == None:
            await ctx.send("Please provide a rate ID")
            return
        async with aiofiles.open("data/rates.json", "r") as f:
            rates = json.load(f)
        if rate_id not in rates:
            await ctx.send("That rate ID does not exist")
            return
        rate = rates[rate_id]
        await ctx.send(
            embed=discord.Embed(
                title="Edit rate:",
                description=f"{rate['name']}\n{rate['description']}",
            )
        )
        await ctx.send(
            embed=discord.Embed(
                title="What do you want to edit?",
                description="\n".join(
                    [
                        "name",
                        "description",
                        "questions",
                        "channel",
                        "stop",
                    ]
                ),
            )
        )
        choice = await self.bot.wait_for(
            "message", check=lambda m: m.author == ctx.author
        )
        if choice.content == "stop":
            return
        if choice.content == "name":
            await ctx.send(
                embed=discord.Embed(
                    title="New name:",
                )
            )
            name = await self.bot.wait_for(
                "message", check=lambda m: m.author == ctx.author
            )
            rate["name"] = name.content
            await ctx.send(
                embed=discord.Embed(
                    title="Name changed!",
                    description="The name has been changed!",
                )
            )
        elif choice.content == "description":
            await ctx.send(
                embed=discord.Embed(
                    title="New description:",
                )
            )
            description = await self.bot.wait_for(
                "message", check=lambda m: m.author == ctx.author
            )
            rate["description"] = description.content
            await ctx.send(
                embed=discord.Embed(
                    title="Description changed!",
                    description="The description has been changed!",
                )
            )
        elif choice.content == "questions":
            await ctx.send(
                embed=discord.Embed(
                    title="New questions:",
                )
            )
            questions = await self.bot.wait_for(
                "message", check=lambda m: m.author == ctx.author
            )
            rate["questions"] = questions.content
            await ctx.send(
                embed=discord.Embed(
                    title="Questions changed!",
                    description="The questions have been changed!",
                )
            )
        elif choice.content == "channel":
            await ctx.send(
                embed=discord.Embed(
                    title="New channel:",
                )
            )
            channel = await self.bot.wait_for(
                "message", check=lambda m: m.author == ctx.author
            )
            rate["channel"] = channel.content
            await ctx.send(
                embed=discord.Embed(
                    title="Channel changed!",
                    description="The channel has been changed!",
                )
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Invalid choice!",
                    description="Please choose a valid choice!",
                )
            )
        async with aiofiles.open("data/rates.json", "w") as f:
            await f.write(json.dumps(rates, indent=4))


async def setup(bot):
    await bot.add_cog(Rates(bot))
