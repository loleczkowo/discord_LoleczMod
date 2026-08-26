from pathlib import Path
from discord import CustomActivity
from core.data_types import LogType, dtEvent, Category
from core.ids_objects import IDsObjects
from core.events import Events
from core.command_category import Categories

# -- MAIN CONFIG --
TEMPLATE_VERSION = "2.6.2"
BOT_VERSION = "1.0.0"
BOT_GITHUB_LINK = "https://github.com/loleczkowo/discord_LoleczMod"
DIR = Path(__file__).parent.resolve()
COMMAND_PREFIX = ":D!"
BOT_ACTIVITY = CustomActivity(name=f"chillin (V{BOT_VERSION})")
DISCORD_INVITE = "https://discord.gg/xAfWgCc48A"

DISCORD_CHAR_LIMIT = 2000
DISCORD_EMBED_LIMIT = 10


# -- IDS CONFIG --
class IDs:
    GUILD: int = 895573181585322005

    class ROLES:
        ADMIN: int      = 897836688326406195
        MEMBER: int     = 1542139803116511362
        NOT_MEMBER: int = 1285949684476547125

    class CHANNELS:
        # the channel where bot logs the console - better to not change name
        CONSOLE_LOGS: int   = 1542142704547405844
        NOT_A_BOT: int      = 1542137270981632070
        BIN: int            = 1542172741216636938

    class USERS:
        # bot ofwner - better to not change name
        OWNER: int = 791000802260811797


ids_objects = IDsObjects(target=IDs)

# -- EVENTS --
events = Events()
EV_STARTUP = dtEvent("startup")
EV_DISCONECT = dtEvent("disconect")
EV_RECCONECT = dtEvent("recconect")
EV_SHUTDOWN = dtEvent("shutdown")


# -- Categories --
CT_MEMBER = Category("Member", sort_priority=0)  # first
CT_MODERATOR = Category("Moderator", sort_priority=-3)  # Third to last
CT_ADMIN = Category("Admin", sort_priority=-2)  # Second to last
CT_BOT_OWNER = Category("Bot Owner", sort_priority=-1)  # Last
categories = Categories(default_category=CT_MEMBER)


# -- LOGS CONFIG --
LOG_DIR = DIR/"logs"
LOG_RETENTION_DAYS = 3
LOG_TO_CONSOLE = True
LOG_TIME_FORMAT = "%H:%M:%S"


# ignore_closed_console does NOT ignore LOG_TO_CONSOLE=false
QINFO:      type[LogType] = LogType("Qinfo",    to_console=False)  # quiet-log.
INFO:       type[LogType] = LogType("INFO")
SUCCESS:    type[LogType] = LogType("SUCCESS")
USER_INPUT: type[LogType] = LogType("USERINP")
RESPONSE:   type[LogType] = LogType("RESPONSE")  # aka console commmand response
WARNING:    type[LogType] = LogType("WARNING",  ignore_closed_console=True)
ERROR:      type[LogType] = LogType("ERROR",    to_discord=True, ignore_closed_console=True, ping=True)
CRITICAL:   type[LogType] = LogType("CRITICAL", to_discord=True, ignore_closed_console=True, ping=True)
ALL_LOG_TYPES = [INFO, SUCCESS, USER_INPUT, RESPONSE, WARNING, ERROR, CRITICAL]
DEFALUT_PING = IDs.ROLES.ADMIN


# -- MEMORY --
MEMORY_DIR = DIR/"memory"
MEMORY_MAIN_FILE = MEMORY_DIR/"memory.json"
MEMORY_AUTOSAVE_TIME = 5*60
