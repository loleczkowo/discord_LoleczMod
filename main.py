import os
import discord
from discord.ext import commands
from constants import (
    CURRENT_DIR, RULE_AGREEMENT_MESSAGE_ID, RULE_AGREE_EMOJI,
    NOT_MEMBER_ROLE_ID, ROLE_MESSAGE_ID, EMOJI_ROLE_MAP,
    JOIN_CHANNEL_ID, JOIN_MESSAGE, LEAVE_MESSAGE)

bot = commands.Bot(command_prefix=":D! ", intents=discord.Intents.all())


async def load_cogs():
    for filename in os.listdir(os.path.join(CURRENT_DIR, 'cogs')):
        if filename.endswith('.py') and not filename.startswith('__'):
            print(f"Loading cog: '{filename[:-3]}'")
            await bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    await load_cogs()
    print("Bot is now online and ready.")


@bot.event
async def on_member_join(member):
    """
    Assign the "Not Member" role to every new member
    and send a welcome message in the JOIN_CHANNEL_ID channel.
    """

    # -- 1. Assign "Not Member" role --
    guild = member.guild
    role = guild.get_role(NOT_MEMBER_ROLE_ID)
    if role:
        try:
            await member.add_roles(role)
        except discord.Forbidden:
            print(f"Missing permissions to assign role to {member.name}.")
        except discord.HTTPException as e:
            print(f"HTTP error assigning role to {member.name}: {e}")
    else:
        print(f"Role with ID {NOT_MEMBER_ROLE_ID} not found.")

    # -- 2. Send welcome message --
    channel = bot.get_channel(JOIN_CHANNEL_ID)
    if channel:
        await channel.send(JOIN_MESSAGE.format(member.mention,
                                               member.guild.member_count))
    else:
        print(f"Join channel with ID {JOIN_CHANNEL_ID} not found.")


@bot.event
async def on_member_remove(member):
    """
    Send a goodbye message in the JOIN_CHANNEL_ID channel
    when a user leaves the server.
    """
    channel = bot.get_channel(JOIN_CHANNEL_ID)
    if channel:
        await channel.send(LEAVE_MESSAGE.format(member.name,
                                                member.guild.member_count))
    else:
        print(f"Join channel with ID {JOIN_CHANNEL_ID} not found.")


@bot.event
async def on_raw_reaction_add(payload):
    """
    1. If user reacts to the rules message with the correct emoji,
    remove "Not Member" role.
    2. If user reacts to the role selection message, give them that role.
    """
    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return

    # -- Rule Agreement Check --
    if (payload.message_id == RULE_AGREEMENT_MESSAGE_ID and
       str(payload.emoji) == RULE_AGREE_EMOJI):

        role = guild.get_role(NOT_MEMBER_ROLE_ID)
        member = guild.get_member(payload.user_id)
        if role and member:
            # If they still have the "Not Member" role, remove it
            if role in member.roles:
                await member.remove_roles(role)
            else:
                try:
                    await member.send("You have already been verified :|")
                except Exception as error:
                    print(error)

    # -- Role Selection Check --
    if payload.message_id == ROLE_MESSAGE_ID:
        emoji_str = str(payload.emoji)
        if emoji_str in EMOJI_ROLE_MAP:
            role_id = EMOJI_ROLE_MAP[emoji_str]
            role = guild.get_role(role_id)
            member = guild.get_member(payload.user_id)
            if role and member:
                await member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    """
    If a user removes their reaction from the role selection message,
    remove that corresponding role from them.
    """
    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return

    if payload.message_id == ROLE_MESSAGE_ID:
        emoji_str = str(payload.emoji)
        if emoji_str in EMOJI_ROLE_MAP:
            role_id = EMOJI_ROLE_MAP[emoji_str]
            role = guild.get_role(role_id)
            member = guild.get_member(payload.user_id)
            if role and member:
                await member.remove_roles(role)


token = os.getenv("DISCORD_BOT_TOKEN")
bot.run(token)
