import discord
import discord.ext.commands
import discord.ext.tasks
import requests
import json
import re

class FoodDemocracyCog(discord.ext.commands.Cog):

    # List of emojis unicode : https://en.wikipedia.org/wiki/List_of_emojis
    EMOJI_LIST = ["\U0001F92E", "\U0001F922", "\U0001F610", "\U0001F924", "\U0001F60D"]

    # TODO : use config file
    def __init__(self, bot, channel_id, role_id, api_base_url):
        self.bot                    = bot
        self.voting_channel         = self.bot.get_channel(channel_id)
        self.api_base_url           = api_base_url
        self.role_str               = f"<@&{role_id}>"
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
            await ctx.send(f"```{s}```")

    def group_help(self):
        s = f"[{self.food_democracy.name}]\n"
        s += f"{self.food_democracy.description}\n"
        s += "\n"
        s += f"Voici la liste des commandes de {self.food_democracy.name} :\n"
        for command in self.food_democracy.commands:
            s += f"  - {command.name} : {command.description}\n"

        s += "\n"
        s += f"Pour plus d'informations sur chacune des commandes : !fd help [COMMAND_NAME]"

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

        await ctx.send(f"```{s}```")

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
                # s += f"Site web : {restaurant.get('website_link', '...')}\n"
                # s += f"Position : {restaurant.get('position_link', '...')}\n"
                # s += f"Capacité maximum : {restaurant.get('max_table_size', '...')}\n"
                s += f"\n"
            s = s[:-2] if len(s) > 1 else s
        else:
            s += f"Impossible d'accéder à l'API. Vérifie que le serveur Django est en ligne."

        await ctx.send(f"```{s}```")

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
            errors = response.json()
            s += f"Erreur lors de l'ajout : {errors}"

        await ctx.send(f"```{s}```")

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
            s = f"[VOTING] Précédent vote non cloturé. Impossible d'en démarrer un nouveau.\n"
            s += f"[VOTING] Pour cloturer le précédent vote : !fd close_voting"
            await self.voting_channel.send(s)
            return

        api_url = "/".join([self.api_base_url, "restaurant_list"])
        response = requests.get(api_url)

        s = ""
        if (response.status_code == 200):
            restaurant_list = response.json()
            message = await self.voting_channel.send(f"Oyez oyez {self.role_str}, il est temps que le peuple s'exprime. Voici les différentes propositions de restaurants pour ce midi :") # TODO : add different sentences
            for restaurant in restaurant_list:
                message = await self.voting_channel.send(f"```{restaurant.get('name', 'Inconnu')} [{restaurant['id']}]```")

                for emoji in self.EMOJI_LIST:
                    await message.add_reaction(emoji)

                self.vote_message_id_list.append(message.id)

        else:
            await self.voting_channel.send(f"```[VOTING] Impossible d'accéder à l'API. Vérifie que le serveur Django est en ligne.```") # TODO : improve this message

    @food_democracy.command(
        name        = "voting",
        description = "Démarre un scrutin.",
    )
    async def voting_command(self, ctx):
        await self.voting()

    @discord.ext.tasks.loop(seconds=60.0)
    async def voting_task(self):
        await self.voting()

    #######################################################
    # counting
    #######################################################

    async def counting(self):
        s = ""

        if not(self.vote_message_id_list):
            s = "```[COUNTING] Aucun vote lancé.```"
            await self.voting_channel.send(s)
            return

        user_vote_dict = {} # {user_id : {choice_id : grade}}
        for vote_message_id in self.vote_message_id_list:
            vote_message = await self.voting_channel.fetch_message(vote_message_id)
            choice_id_match = re.search(r'\[(.*?)\]', vote_message.content)
            if choice_id_match:
                choice_id = choice_id_match.group(1)
                for reaction in vote_message.reactions:
                    user_list = [user async for user in reaction.users()]
                    if (reaction.emoji in self.EMOJI_LIST):
                        grade = self.EMOJI_LIST.index(reaction.emoji)
                        for user in user_list:
                            if (user.id != self.bot.user.id):
                                if not(user.id in user_vote_dict):
                                    user_vote_dict[user.id] = {}
                                if (choice_id in user_vote_dict[user.id]):
                                    user_vote_dict[user.id][choice_id] = -1
                                else:
                                    user_vote_dict[user.id][choice_id] = grade
            else:
                s += f"```[COUNTING] Le message ({vote_message.content}) ne contient pas d'ID.```"

        if not(user_vote_dict):
            s = "```[COUNTING] Aucun vote reçu.```"
            await self.voting_channel.send(s)

            # Preparing a new vote
            self.vote_message_id_list = []
            return

        api_url = "/".join([self.api_base_url, "counting"]) + "/"
        response = requests.post(api_url, json=user_vote_dict)

        if (response.status_code == 201):
            selected_choice_list = response.json()

            s = f"Oyez oyez {self.role_str}, la majorité a parlé et les restaurants ce midi seront :\n" # TODO : add different sentences
            for selected_choice in selected_choice_list:
                s += f"```  {selected_choice['name']} [{selected_choice['id']}] avec une moyenne de {self.EMOJI_LIST[round(selected_choice['mean'])]}```"

            # Preparing a new vote
            self.vote_message_id_list = []
        else:
            s = f"```[COUNTING] Impossible d'accéder à l'API. Vérifie que le serveur Django est en ligne.```" # TODO : improve this message

        await self.voting_channel.send(s)

    @food_democracy.command(
        name        = "counting",
        description = "Termine le scurtin en cours et donne le résultat.",
    )
    async def counting_command(self, ctx):
        await self.counting()

    @discord.ext.tasks.loop(seconds=60.0)
    async def counting_task(self):
        await self.counting()

    #######################################################
    # enable_auto_voting
    #######################################################

    @food_democracy.command(
        name        = "enable_auto_voting",
        description = "Active le scrutin périodique.",
    )
    async def enable_auto_voting_command(self, ctx):
        if not self.voting_task.is_running():
            if (len(self.vote_message_id_list) > 0):
                pass # TODO
            else:
                self.voting_task.start()
        else:
            pass # TODO

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
        else:
            pass # TODO


async def setup(bot, channel_id, role_id, api_base_url):
    await bot.add_cog(FoodDemocracyCog(bot, channel_id, role_id, api_base_url))