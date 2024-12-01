# Standard / external libraries
import discord

# External modules

# Internal modules

COLOR_DICT = {
    "BLACK"     : 0x000000,
    "RED"       : 0xFF0000,
    "GREEN"     : 0x00FF00,
    "BLUE"      : 0x0000FF,
    "YELLOW"    : 0xFFFF00,
    "CYAN"      : 0x00FFFF,
    "PURPLE"    : 0xFF00FF,
    "WHITE"     : 0xFFFFFF,
}

def format_msg(msg, title="", color="BLACK"):
    embed = discord.Embed(
        title=title,
        description=msg,
        color=COLOR_DICT.get(color, 0x000000)
    )

    return embed
