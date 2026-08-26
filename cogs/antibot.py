from asyncio import sleep
from typing import Dict
import time
import discord
from discord import app_commands
from discord.ext import commands
from core import Memory, log, check_hierarchy
from core.handle_command_error import AppTooLowHierarchy
from config import ids_objects, IDs, DISCORD_INVITE, categories, CT_MODERATOR, INFO

BOT_BAN_MESSAGE = (
    f"Beepboop, you were detected as a bot (reason `{{reason}}`)\n"
    f"**in a minute will be able to rejoin using this invite:** {DISCORD_INVITE}"
)


@categories.set_cog_category(CT_MODERATOR)
class AntiBot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.pending_unbans = Memory("pending_unbans", {}, self, save_on_change=True)
        for user_id, unban_at in self.pending_unbans.mem.items():
            self.bot.loop.create_task(
                self._unban_later(int(user_id), float(unban_at))
            )

    # MEMBER/NOT A MEMBER ROLES
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await member.add_roles(ids_objects.ROLES.NOT_MEMBER)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.channel_id != IDs.CHANNELS.NOT_A_BOT:
            return
        member = payload.member
        if member is None or member.bot:
            return
        await member.remove_roles(ids_objects.ROLES.NOT_MEMBER)
        await member.add_roles(ids_objects.ROLES.MEMBER)


    @app_commands.command(name="ban_bot_user", description="Kicks a bot user and notifies them.")
    @app_commands.describe(user="Discord user to kick")
    @app_commands.checks.has_permissions(kick_members=True)
    async def ban_bot_user(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Reason not given"):
        if not await check_hierarchy(interaction.user, user):
            raise AppTooLowHierarchy(target=user)
        await interaction.response.send_message(f"Banning user <@{user.id}> for being a *BOT* ({reason})", ephemeral=True)
        await self._ban_bot(user, f"by a moderator; '{reason}'")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id == IDs.CHANNELS.BIN:
            await self._ban_bot(message.author, "Sent a message in the bin channel")

    async def _ban_bot(self, user: discord.Member, reason):
        # We wont fully ban the user because they might be a normal user
        # The way is to:
        # 1. Message the user thet they were detected as a bot
        #  (include invite link)
        # 2. Ban the user to get rid of their messages
        # 3. After few minutes unban the user so they can rejoin
        try:
            await user.send(BOT_BAN_MESSAGE.format(reason=reason))
        except Exception:
            pass
            # not my problem lmfao
            # if you are reading this, please DM me with a printscreen lol, 13/10/2025-loleczkowo
            # yo 27/03/2026 loleczkowo here, No i wont DM myself. Anyways this is not a great idea but I'm too lazy to find a better one soooo.
            # 26/07/2026 4 months later, copying this code from another repo lol, Also this isint that bad of an idea? wtf were you non-linux loleczkowo on.

        await user.ban(delete_message_seconds=2*60*60, reason=f"(BOT) {reason}")
        # now wait 1 minutes and unban
        unban_at = time.time() + 60
        self.pending_unbans.mem[str(user.id)] = unban_at
        self.pending_unbans.touch()
        self.bot.loop.create_task(self._unban_later(user, 60))
        log(INFO(to_discord=True), f"**ANTI_DC_BOT: BOT BANNED `{user.name}:{user.id}`**\nreason: `{reason}`")

    async def _unban_later(self, user: discord.Member, delay: int):
        await sleep(delay)
        await ids_objects.GUILD.unban(user, reason="unban after bot ban")
        log(INFO(to_discord=True), f"**ANTI_DC_BOT: BOT UNBANNED `{user.name}:{user.id}`**")

