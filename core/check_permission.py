from discord import Interaction, app_commands, Member, Guild, NotFound
from discord.ext import commands
from globals import Globals as G


class AppNotOwner(app_commands.CheckFailure): ...
class MissingReference(commands.CheckFailure): ...


class AppTooLowHierarchy(app_commands.CheckFailure):
    def __init__(self, *, target=None):
        self.target = target
        super().__init__()


class TooLowHierarchy(commands.CheckFailure):
    def __init__(self, *, target=None):
        self.target = target
        super().__init__()


async def app_is_owner(interaction: Interaction) -> bool:
    if await G.bot.is_owner(interaction.user):
        return True
    raise AppNotOwner


async def must_be_refering(ctx: commands.Context) -> bool:
    ref = ctx.message.reference
    if ref is not None and ref.message_id is not None:
        return True
    raise MissingReference


async def check_hierarchy(actor: Member | int | None,
                          target: Member | int | None,
                          guild: Guild | None = None):
    if actor is None or target is None:
        return False
    if isinstance(actor, int):
        if not guild:
            return False
        try:
            actor = await guild.fetch_member(actor)
        except NotFound:
            return False
    if isinstance(target, int):
        if not guild:
            return False
        try:
            target = await guild.fetch_member(target)
        except NotFound:
            return False
    if actor.guild.id != target.guild.id:
        return False
    if actor.guild.owner_id == actor.id:
        return True
    if target.guild.owner_id == target.id:
        return False
    return actor.top_role > target.top_role
