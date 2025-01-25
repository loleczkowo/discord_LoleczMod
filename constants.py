import os

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DIR = os.path.dirname(CURRENT_DIR)
BOT_COMMAND_CHANNEL = 1285923235640115344

# - register -
RULE_AGREEMENT_MESSAGE_ID = 1286237932478398535
RULE_AGREE_EMOJI = "🤓"
NOT_MEMBER_ROLE_ID = 1285949684476547125

# - joins -
JOIN_CHANNEL_ID = 1331627791623655424
JOIN_MESSAGE = """\
Hey, {}! **Welcome to the server!**,
We hope you have a great time exploring.
Don't forget to check out <#895573316000178196> to get started!
-# *We now have {} awesome members :D*"""
LEAVE_MESSAGE = """\
Bye `{}`!. *i hope you had fun at my server*.
-# *{} members :/*
"""

# - roles -
ROLE_MESSAGE_ID = 1285942616080253070
EMOJI_ROLE_MAP = {
    "🇵🇱": 1285943447454486580,
    "<:youtube:1285970362399719506>": 1285973181793959946,
    "<:twitch:1285968749773590569>": 1285973268154814556
}

# |--------------------|
# | PHASE II. Commands >
# |--------------------|

# - MUTE -
REPORTS_CHANNEL_ID = 1280858741440516096
MUTE_CHANNEL_ID = 1331939478570274826
MUTE_ROLE_ID = 1331935460888412182
MUTED_USERS_FILE = os.path.join(DIR, "muted_users.json")

MUTE_MESSAGE = (
    "Hello, {{username}}! You have been **muted**.\n"
    "If you think this was a mistake or want to apologize, feel free to "
    "contact the staff: https://discord.com/channels/{{server_id}}/{}\n"
    "**Reason:** `{{reason}}`\n"
    "*We hope to see you back soon*"
).format(MUTE_CHANNEL_ID)

MUTE_MESSAGE_TIME = (
    "Hello, {{username}}! You have been **muted for {{time}}**.\n"
    "If you think this was a mistake or want to apologize, feel free to "
    "contact the staff: https://discord.com/channels/{{server_id}}/{}\n"
    "**Reason:** `{{reason}}`\n"
    "*See you back in {{time}}!*"
).format(MUTE_CHANNEL_ID)

UNMUTE_MESSAGE = (
    "Hey, {username}! **Great news, you've been unmuted!** :D\n"
    "Feel free to chat :D!"
)

REPORT_MUTE_MESSAGE = (
    "||`{muted_user}`|| has been **permanently muted** by ||`{muted_by}`||.\n"
    "**Reason:** `{reason}`."
)

REPORT_TIME_MUTE_MESSAGE = (
    "||`{muted_user}`|| has been **muted for** `{muted_time}` "
    "by ||`{muted_by}`||.\n"
    "**Reason:** `{reason}`."
)

REPORT_UNMUTE_MESSAGE = (
    "||`{unmuted_user}`|| has been **unmuted** by ||`{unmuted_by}`||."
)

# - ACCOUNTS -
REG_MESSAGE_CODE = (
    "Your verification code is ||{code}||.\n"
    "**IMPORTANT: DO NOT SHARE THIS CODE WITH ANYONE.**\n"
    "To register, type \"||`!reg {code}`||\" in Loleczkowo's live chat."
)

REG_MESSAGE = (
    "The YouTube account `{{yt_user}}` has been successfully linked to your "
    "Discord account.\n"
    "**If this isn't you, type `:D! unreg` in https://discord.com/channels/"
    "{{server_id}}/{} immediately!**"
).format(BOT_COMMAND_CHANNEL)

TO_REG_JSON = os.path.join(DIR, "reg_codes.json")
USERS_DATA_JSON = os.path.join(DIR, "users_data.json")
