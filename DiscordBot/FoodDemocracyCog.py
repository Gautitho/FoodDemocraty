# Standard / external libraries
import discord
import discord.ext.commands
import discord.ext.tasks
import requests
import json
import toml
import re
import datetime

# External modules
import xpt_utils as xu

# Internal modules
import discord_utils as du

class FoodDemocracyCog(discord.ext.commands.Cog):

    def __init__(self, bot, conf_path="food_democracy.conf"):
        self.bot                    = bot

        conf_dict = toml.load(conf_path)
        self.emoji_list             = conf_dict["emoji_list"]
        self.voting_channel         = self.bot.get_channel(conf_dict["channel_id"])
        self.api_base_url           = conf_dict["api_base_url"]
        self.role_str               = f"<@&{conf_dict['role_id']}>"
        self.voting_sentence_list   = conf_dict["voting_sentence_list"]
        self.counting_sentence_list = conf_dict["counting_sentence_list"]
        self.vote_message_id_list   = []

    #######################################################
    # FoodDemocracy group definition
    #######################################################

    @discord.ext.commands.group(
        name        = "FoodDemocracy",
        aliases     = ["fd"],
        description = "Module permettant d'organiser des votes pour choisir un restaurant.",
    )
    async def food_democracy(self, ctx):
        if ctx.invoked_subcommand is None:
            s = f"Sous commande non reconnue.\n"
            s += "\n"
            s += self.group_help()
            await ctx.send(embed=du.format_msg(s, title="FoodDemocracy", color="BLUE"))

    def group_help(self):
        s = f"[{self.food_democracy.name}]\n"
        s += f"{self.food_democracy.description}\n"
        s += "\n"
        s += f"Voici la liste des commandes de {self.food_democracy.name} :\n"
        for command in self.food_democracy.commands:
            s += f"- {command.name} : {command.description}\n"

        s += "\n"
        s += f"Pour plus d'informations sur chacune des commandes :\n"
        s += f"!fd help [COMMAND_NAME]"

        return s

    #######################################################
    # help
    #######################################################

    @food_democracy.command(
        name        = "help",
        description = "Affiche une aide détaillée pour la commande spécifiée.",
    )
    async def help_command(self, ctx,
        command_name: str = None
    ):
        s = ""
        if (command_name is not None):
            command = self.food_democracy.get_command(command_name)
            if (command is not None):
                s += f"[{self.food_democracy.name}.{command.name}]\n"
                s += f"{command.description}\n"
                s += "\n"
                s += "Usage :\n"
                s += f"{command.name} {' '.join(['[' + name.upper() + ']' for name, param in command.params.items() if (name not in ['self', 'ctx'])])}\n"
            else:
                s += f"Sous commande non reconnue.\n"
                s += "\n"
                s += self.group_help()

        else:
            s += self.group_help()

        await ctx.send(embed=du.format_msg(s, title="FoodDemocracy", color="BLUE"))

    #######################################################
    # list_restaurant
    #######################################################

    @food_democracy.command(
        name        = "list_restaurant",
        description = "Affiche la liste des restaurants la base de données.",
    )
    async def list_restaurant_command(self, ctx):
        api_url = "/".join([self.api_base_url, "restaurant_list"])
        response = requests.get(api_url)

        s = ""
        if (response.status_code == 200):
            restaurant_list = response.json()
            for restaurant in restaurant_list:
                s += f"[{restaurant.get('name', 'Inconnu')}]\n"
                s += f"{restaurant.get('description', 'Pas de description')}\n"
                s += f"Site web : {restaurant.get('website_link', '...')}\n"
                s += f"Position : {restaurant.get('position_link', '...')}\n"
                s += f"Capacité maximum : {restaurant.get('max_table_size', '...')}\n"
                s += f"\n"
            s = s[:-2] if len(s) > 1 else s
        else:
            raise xu.DevException(f"Impossible d'accéder à l'API du backend. Code HTML de retour : {response.status_code}")

        await ctx.send(embed=du.format_msg(s, title="FoodDemocracy", color="BLUE"))

    #######################################################
    # add_restaurant
    #######################################################

    @food_democracy.command(
        name        = "add_restaurant",
        description = "Ajoute un retaurant à la base de données.",
        hidden      = True,
    )
    async def add_restaurant_command(self, ctx,
        name            : str,
        website_link    : str = "",
        position_link   : str = "",
        max_table_size  : int = 0
    ):
        api_url = "/".join([self.api_base_url, "restaurant_list"]) + "/"

        data = {
            "name": name,
            "website_link": website_link,
            "position_link": position_link,
            "max_table_size": max_table_size
        }

        response = requests.post(api_url, json=data)

        s = ""
        if (response.status_code == 201):
            restaurant = response.json()
            s += f"Le restaurant '{restaurant['name']}' a été ajouté avec succès !"
        else:
            raise xu.DevException(f"Impossible d'accéder à l'API du backend. Code HTML de retour : {response.status_code}")

        await ctx.send(embed=du.format_msg(s, title="FoodDemocracy", color="BLUE"))

    #######################################################
    # remove_restaurant
    #######################################################

    # TODO

    #######################################################
    # edit_restaurant
    #######################################################

    # TODO

    #######################################################
    # voting
    #######################################################

    async def voting(self):
        if (len(self.vote_message_id_list) > 0):
            s = f"Précédent vote non cloturé.\n"
            s += f"Impossible d'en démarrer un nouveau.\n"
            s += f"Pour cloturer le précédent vote : `!fd counting`"
            raise xu.DevException(s)

        api_url = "/".join([self.api_base_url, "restaurant_list"])
        response = requests.get(api_url)

        s = ""
        if (response.status_code == 200):
            restaurant_list = response.json()
            s = self.voting_sentence_list[datetime.datetime.now().day%len(self.voting_sentence_list)]
            message = await self.voting_channel.send(embed=du.format_msg(s, title="FoodDemocracy : Scrutin", color="BLUE"))
            for restaurant in restaurant_list:
                message = await self.voting_channel.send(embed=du.format_msg(f"{restaurant.get('name', 'Inconnu')} ({restaurant['description']}) [{restaurant['id']}]", color="BLUE"))

                for emoji in self.emoji_list:
                    await message.add_reaction(emoji)

                self.vote_message_id_list.append(message.id)

            await self.voting_channel.send(self.role_str)

        else:
            raise xu.DevException(f"Impossible d'accéder à l'API du backend. Code HTML de retour : {response.status_code}")

    @food_democracy.command(
        name        = "voting",
        description = "Démarre un scrutin.",
    )
    async def voting_command(self, ctx):
        await self.voting()

    @discord.ext.tasks.loop(seconds=30.0)
    async def voting_task(self, vote_start_hour=12, vote_start_minute=0, vote_duration_minutes=15):
        try:
            now = datetime.datetime.now()
            if (    now.weekday() in [0, 1, 2, 3, 4]
                and now.hour == vote_start_hour
                and now.minute == vote_start_minute
            ):
                await self.voting()
                if not(self.counting_task.is_running()):
                    delay = datetime.timedelta(minutes=vote_duration_minutes)
                    self.counting_task.start(now + delay)
                    await self.voting_channel.send(embed=du.format_msg(f"Le scrutin sera clos dans {vote_duration_minutes} minutes.", color="BLUE"))
                else:
                    raise xu.DevException("Une tâche d'auto-dépouillement est déjà en cours.")

        except Exception as e:
            self.voting_task.stop()
            s = f"Une erreur est survenue dans **voting_task** :\n"
            s += f"{e}\n"
            s += f"La tâche est arrêtée."
            await self.voting_channel.send(embed=du.format_msg(s, title="ERREUR", color="RED"))

    #######################################################
    # counting
    #######################################################

    async def counting(self):
        s = ""

        if not(self.vote_message_id_list):
            s = "Impossible de dépouiller car aucun vote n'a été lancé.\n"
            s += "Pour démarrer un vote : `!fd voting`"
            raise xu.UserException(s)

        user_vote_dict = {} # {user_id : {choice_id : grade}}
        for vote_message_id in self.vote_message_id_list:
            vote_message = await self.voting_channel.fetch_message(vote_message_id)
            choice_id_match = re.search(r'\[(.*?)\]', vote_message.embeds[0].description)
            if choice_id_match:
                choice_id = choice_id_match.group(1)
                for reaction in vote_message.reactions:
                    user_list = [user async for user in reaction.users()]
                    if (reaction.emoji in self.emoji_list):
                        grade = self.emoji_list.index(reaction.emoji)
                        for user in user_list:
                            if (user.id != self.bot.user.id):
                                if not(user.id in user_vote_dict):
                                    user_vote_dict[user.id] = {}
                                if (choice_id in user_vote_dict[user.id]):
                                    user_vote_dict[user.id][choice_id] = -1
                                else:
                                    user_vote_dict[user.id][choice_id] = grade
            else:
                s = "Le message suivant ne contient pas d'ID :\n"
                s += f"{vote_message.embeds[0].description}"
                raise xu.DevException(s)

        if not(user_vote_dict):
            self.vote_message_id_list = [] # Preparing a new vote
            raise xu.DevException("Aucun vote reçu.")

        api_url = "/".join([self.api_base_url, "counting"]) + "/"
        response = requests.post(api_url, json=user_vote_dict)

        if (response.status_code == 201):
            self.vote_message_id_list = [] # Preparing a new vote

            selected_choice_list = response.json()

            s = self.counting_sentence_list[datetime.datetime.now().day%len(self.counting_sentence_list)]
            for selected_choice in selected_choice_list:
                s += f"- {selected_choice['name']} [{selected_choice['id']}] avec un score de {selected_choice['score']}\n"
            s = s[:-1]

            await self.voting_channel.send(embed=du.format_msg(s, title="FoodDemocracy : Dépouillement", color="GREEN"))
            await self.voting_channel.send(self.role_str)

        else:
            raise xu.DevException(f"Impossible d'accéder à l'API du backend. Code HTML de retour : {response.status_code}")


    @food_democracy.command(
        name        = "counting",
        description = "Termine le scurtin en cours et donne le résultat.",
    )
    async def counting_command(self, ctx):
        await self.counting()

    @discord.ext.tasks.loop(seconds=30.0)
    async def counting_task(self, counting_time):
        try:
            if (datetime.datetime.now() >= counting_time):
                await self.counting()
                self.counting_task.stop()

        except Exception as e:
            self.counting_task.stop()
            s = f"Une erreur est survenue dans **counting_task** :\n"
            s += f"{e}\n"
            s += f"La tâche est arrêtée."
            await self.voting_channel.send(embed=du.format_msg(s, title="ERREUR", color="RED"))

    #######################################################
    # enable_auto_voting
    #######################################################

    @food_democracy.command(
        name        = "enable_auto_voting",
        description = "Active le scrutin périodique.",
    )
    async def enable_auto_voting_command(self, ctx, vote_start_hour=12, vote_start_minute=0, vote_duration_minutes=15):
        if not(self.voting_task.is_running()):
            if (len(self.vote_message_id_list) > 0):
                raise xu.DevException("Un scrutin est déjà en cours.")
            else:
                self.voting_task.start(vote_start_hour=vote_start_hour, vote_start_minute=vote_start_minute, vote_duration_minutes=vote_duration_minutes)
                s = f"**Scrutin automatique activé**\n"
                s += f"Heure quotidienne du scrutin : {vote_start_hour:02d}:{vote_start_minute:02d}\n"
                s += f"Durée du scrutin : {vote_duration_minutes} minutes"
                await self.voting_channel.send(embed=du.format_msg(s, color="BLUE"))
        else:
            raise xu.DevException("Le scrutin automatique est déjà activé.")

    #######################################################
    # disable_auto_voting
    #######################################################

    @food_democracy.command(
        name        = "disable_auto_voting",
        description = "Désactive le scrutin périodique.",
    )
    async def disable_auto_voting_command(self, ctx):
        if self.voting_task.is_running():
            self.voting_task.stop()
            await self.voting_channel.send(embed=du.format_msg("**Scrutin automatique désactivé**", color="BLUE"))
        else:
            raise xu.DevException("Le scrutin automatique n'est pas activé.")


async def setup(bot):
    await bot.add_cog(FoodDemocracyCog(bot))
