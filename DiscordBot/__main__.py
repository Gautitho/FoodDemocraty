# Standard / external libraries
import sys
import discord
import discord.ext.commands
import discord.ext.tasks
import toml
import traceback

# External modules
sys.path.append("..") # TODO : Use env variable
import xpt_utils as xu

# Internal modules
import discord_utils as du
import FoodDemocracyCog

bot = discord.ext.commands.Bot(command_prefix="!", intents=discord.Intents.all())
discord_conf_dict = toml.load("discord.conf")

@bot.hybrid_command(name="loop_back", aliases=["lb"])
async def loop_back(ctx, msg: str):
    await ctx.send(embed=du.format_msg(msg))

# Not functionnal for now
@bot.hybrid_command()
async def update_command_list(ctx):
    await bot.tree.sync()
    await ctx.send(embed=du.format_msg("Liste des commandes mises à jour.", color="GREEN"))

# This function catch exceptions raised during a command execution
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandNotFound):
        await ctx.send(embed=du.format_msg("Commande non reconnue. Utilise `!help` pour voir les commandes disponibles.", title="ERREUR", color="RED"))
    elif isinstance(error, discord.ext.commands.CommandInvokeError):
        await ctx.send(embed=du.format_msg(error.original, title="ERREUR", color="RED"))
    else:
        await ctx.send(embed=du.format_msg(error, title="ERREUR", color="RED"))

# This function catch all exceptions not previously catched
@bot.event
async def on_error(event_method, *args, **kwargs):
    admin_channel = bot.get_channel(discord_conf_dict["admin_channel_id"])
    error_message = traceback.format_exc()
    await admin_channel.send(embed=du.format_msg(f"Une erreur est survenue dans **{event_method}** :\n{error_message}", title="ERREUR", color="RED"))

@bot.event
async def on_ready():
    await FoodDemocracyCog.setup(bot)

if (__name__ == "__main__"):
    bot.run(token=discord_conf_dict["discord_token"])
