import discord
from discord.ext import commands
from others import gen_code, load_json, save_json
from constants import REG_MESSAGE_CODE, TO_REG_JSON, USERS_DATA_JSON


class RegSys(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="reg")
    @commands.has_permissions(administrator=True)
    async def register(self, ctx: commands.Context):
        userdata = load_json(USERS_DATA_JSON)
        if any(entry['dc'] == ctx.author.id for entry in userdata):
            ctx.send("You are already logged in as ")
            return
        to_reg = load_json(TO_REG_JSON)

        key_to_update = \
            next((k for k, v in to_reg.items()if v == ctx.author.id), None)
        if key_to_update:
            to_reg.pop(key_to_update)

        code = gen_code(6)
        to_reg[code] = ctx.author.id
        await ctx.author.send(REG_MESSAGE_CODE.format(code=code))

        save_json(TO_REG_JSON, to_reg)


async def setup(bot):
    await bot.add_cog(RegSys(bot))
