import discord
from discord.ext import commands, tasks
import json
import os
import time
from others import convert_time
from constants import (
    MUTED_USERS_FILE, MUTE_ROLE_ID, REPORTS_CHANNEL_ID, MUTE_CHANNEL_ID,
    MUTE_MESSAGE, MUTE_MESSAGE_TIME, REPORT_MUTE_MESSAGE,
    REPORT_TIME_MUTE_MESSAGE, REPORT_UNMUTE_MESSAGE, UNMUTE_MESSAGE
)


class MuteSys(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Loading muted users...")
        self.muted_users = self.load_muted_users()
        self.check_mute_expirations.start()
        bot.add_listener(self.on_join_mutesys, "on_member_join")

    def cog_unload(self):
        self.check_mute_expirations.cancel()

    def load_muted_users(self):
        if os.path.exists(MUTED_USERS_FILE):
            with open(MUTED_USERS_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_muted_users(self, muted_users):
        with open(MUTED_USERS_FILE, "w") as f:
            json.dump(muted_users, f, indent=4)

    # - on join -
    async def on_join_mutesys(self, member: discord.Member):
        if str(member.id) in self.muted_users:
            mute_role = member.guild.get_role(MUTE_ROLE_ID)
            if mute_role:
                try:
                    await member.add_roles(mute_role)
                    try:
                        await member.send(
                            "Rejoining the server won't remove your mute.")
                    except discord.Forbidden:
                        pass
                except discord.Forbidden:
                    print(f"Failed to reassign mute role to {member.name}.")
            else:
                print(f"Mute role with ID {MUTE_ROLE_ID} not found.")

    # - ____________ -
    # - mute command -
    # - ```````````` -
    @commands.command(name="mute")
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member, *, reason_time: str):
        """
        Mutes a member for a specified amount of time or indefinitely.
        Usage: !mute @user [reason] [time] [m/h/d]
        Example: !mute @John spamming 1 h
        """
        args = reason_time.rsplit(' ', 2)

        if len(args) >= 2 and args[-1] in ['m', 'h', 'd']:
            reason = ' '.join(args[:-2])
            try:
                t = float(args[-2])
            except ValueError:
                await ctx.send("Invalid time format! "
                               "Please provide a numeric value for time.")
                return

            timesys = args[-1].lower()
            if timesys == "h":
                pass
            elif timesys == "m":
                t /= 60
            elif timesys == "d":
                t *= 24
            else:
                await ctx.send("Invalid time unit! Use `m`, `h`, or `d`.")
                return
        else:
            reason = reason_time
            t = None

        if not reason:
            reason = "No reason given"

        role = ctx.guild.get_role(MUTE_ROLE_ID)
        if not role:
            await ctx.send("Mute role not found.")
            return

        await member.add_roles(role)

        report_channel = self.bot.get_channel(REPORTS_CHANNEL_ID)

        if t is None:
            # perma-mute
            self.muted_users[str(member.id)] = None
            message = MUTE_MESSAGE.format(
                username=member.mention,
                server_id=ctx.guild.id,
                reason=reason
            )
            await ctx.send(f"`{member.display_name}` has been muted.")
            if report_channel:
                await report_channel.send(
                    REPORT_MUTE_MESSAGE.format(
                        muted_user=member.name,
                        muted_by=ctx.author.name,
                        reason=reason
                    )
                )
        else:
            # Timed mute
            self.muted_users[str(member.id)] = time.time() + (t * 3600)
            ct_t = convert_time(t)
            message = MUTE_MESSAGE_TIME.format(
                username=member.mention,
                time=ct_t,
                server_id=ctx.guild.id,
                reason=reason
            )
            await ctx.send(
                "`{muted_user}` has been muted for {time}.".format(
                   muted_user=member.display_name, time=ct_t))

            if report_channel:
                await report_channel.send(
                    REPORT_TIME_MUTE_MESSAGE.format(
                        muted_user=member.name,
                        muted_time=ct_t,
                        muted_by=ctx.author.name,
                        reason=reason
                    )
                )

        self.save_muted_users(self.muted_users)

        # Attempt to DM the user; if forbidden, send to a mute channel instead
        try:
            await member.send(message)
        except discord.Forbidden:
            mute_channel = self.bot.get_channel(MUTE_CHANNEL_ID)
            if mute_channel:
                await mute_channel.send(message)

    # - ______________ -
    # - unmute command -
    # - `````````````` -
    @commands.command(name="unmute")
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx: commands.Context, member: discord.Member):
        role = ctx.guild.get_role(MUTE_ROLE_ID)
        if not role:
            await ctx.send("Mute role not found.")
            return

        if role not in member.roles:
            await ctx.send(f"`{member.display_name}` is not muted.")
            return

        await member.remove_roles(role)
        report_channel = self.bot.get_channel(REPORTS_CHANNEL_ID)
        if report_channel:
            await report_channel.send(
                REPORT_UNMUTE_MESSAGE.format(
                    unmuted_user=member.name,
                    unmuted_by=ctx.author.name
                )
            )

        self.muted_users.pop(str(member.id), None)
        self.save_muted_users(self.muted_users)

        await ctx.send(f"`{member.display_name}` has been unmuted :D!")
        message = UNMUTE_MESSAGE.format(username=member.mention)
        try:
            await member.send(message)
        except discord.Forbidden:
            mute_channel = self.bot.get_channel(MUTE_CHANNEL_ID)
            if mute_channel:
                await mute_channel.send(message)

    # - ______________ -
    # - HARDCODED MUTE -
    # - `````````````` -
    @commands.command(name="muteid")
    @commands.has_permissions(administrator=True)
    async def hardmute(self, ctx: commands.Context, id):
        if id not in self.muted_users.keys():
            self.muted_users[id] = None
            await ctx.send(f"`{id}` muted.")
        else:
            await ctx.send(f"`{id}` is already muted.")

    # - error handling -
    @mute.error
    @unmute.error
    async def command_error(self, ctx, error):
        """Error handler for the mute/unmute commands."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention a user to mute/unmute.")
        else:
            await ctx.send(f"Something went wrong D: **ERROR; `{error}`**")

    # - _______________ -
    # - auto unmute sys -
    # - ``````````````` -
    @tasks.loop(minutes=1)
    async def check_mute_expirations(self):
        if not self.bot.guilds:
            return

        guild = self.bot.guilds[0]
        role = guild.get_role(MUTE_ROLE_ID)
        if not role:
            return

        current_time = time.time()
        to_remove = []

        for user_id, unmute_time in self.muted_users.items():
            if unmute_time is not None and current_time >= unmute_time:
                member = guild.get_member(int(user_id))
                if member and role in member.roles:
                    await member.remove_roles(role)
                    message = UNMUTE_MESSAGE.format(username=member.mention)
                    try:
                        await member.send(message)
                    except discord.Forbidden:
                        mute_channel = self.bot.get_channel(MUTE_CHANNEL_ID)
                        if mute_channel:
                            await mute_channel.send(message)
                to_remove.append(user_id)

        for user_id in to_remove:
            del self.muted_users[user_id]
        self.save_muted_users(self.muted_users)

    @check_mute_expirations.before_loop
    async def before_check_mute_expirations(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(MuteSys(bot))
