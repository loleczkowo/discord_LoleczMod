import discord
from discord.ext import commands


class Purge(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, amount: int):
        if amount < 1:
            await ctx.send("Please specify a number greater than 0.")
            return

        if amount > 15 and not ctx.author.guild_permissions.administrator:
            await ctx.send(
                "The max number of messages a mod can delete at once is 15.")
            return

        if amount > 100:
            await ctx.send(
                "too much!")
            return

        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Deleted {len(deleted) - 1} messages.", delete_after=5)

    @commands.command(name="userpurge")
    @commands.has_permissions(manage_messages=True)
    async def userpurge(self, ctx: commands.Context, user: discord.Member,
                        amount: int = 25):
        if amount > 25 and not ctx.author.guild_permissions.administrator:
            await ctx.send(
                "The max number of messages a mod can delete at once is 15.")
            return

        if amount > 250:
            await ctx.send(
                "too much!")
            return

        def check(message):
            return message.author.id == user.id

        deleted = await ctx.channel.purge(limit=amount + 1, check=check)
        await ctx.send(f"Deleted {len(deleted)} messages.", delete_after=5)


async def setup(bot):
    await bot.add_cog(Purge(bot))
