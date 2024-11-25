# Standard / external libraries
import discord
import discord.ext.commands
import discord.ext.tasks
import toml

# External modules

# Internal modules
import FoodDemocracyCog

bot = discord.ext.commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.hybrid_command(name="loop_back", aliases=["lb"])
async def loop_back(context, msg: str):
    await context.send(msg)

# Not functionnal for now
@bot.hybrid_command()
async def update_command_list(context):
    await bot.tree.sync()
    await context.send("Liste des commandes mises à jour.")

@bot.event
async def on_command_error(context, error):
    if isinstance(error, discord.ext.commands.CommandNotFound):
        await context.send("Commande non reconnue. Utilise `!help` pour voir les commandes disponibles.")
    else:
        print(f"Erreur : {error}")

@bot.event
async def on_ready():
    discord_conf_dict = toml.load("discord.conf")
    await FoodDemocracyCog.setup(bot, discord_conf_dict["FoodDemocraty_channel_id"], discord_conf_dict["FoodDemocraty_role_id"], discord_conf_dict["FoodDemocraty_api_base_url"])

if (__name__ == "__main__"):
    discord_conf_dict = toml.load("discord.conf")
    bot.run(token=discord_conf_dict["discord_token"])