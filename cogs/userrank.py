import asyncio
import json
import random

import aiohttp
import discord
import requests
from discord.ext import commands
from requests.exceptions import HTTPError

import libs.config as config
import libs.database as database
from libs.command_manager import check
from libs.embedmaker import officialEmbed
from libs.utils import sanitize_check
from libs.utils import api_fetch
from libs.thm_api import get_sub_status, get_user_data


####################
# Config variables #
####################

c_api_token = config.get_config("url")["api"]["token"]

#####################
# Strings variables #
#####################

s_userrank = config.get_string("ranks")["userrank"]
s_quotes = config.get_string("quotes")["regular_quotes"]
s_not_sanitized = config.get_string("commands")["not_sanitized"]

#############
# Functions #
#############

def get_moto():
    """Returns a random quote from the list."""

    return s_quotes[random.randint(0, len(s_quotes) - 1)]


############
# COG Body #
############

class Userrank(commands.Cog, name="Rank Commands"):
    def __init__(self, bot):
        self.bot = bot

    async def send_rank(self, ctx, user):
        """Sends the message containing the user's rank."""

        try:
            data = get_user_data(user)

            if data['userRank'] != 0:
                quip = get_moto()
                quip = "*{}*".format(quip)

                user_img = data['avatar']
                points = data['points']
                rank = data['userRank']

                response = officialEmbed("Rank", quip, 0x148f77)

                response.set_thumbnail(url=user_img)
                response.add_field(
                    name="Username:", value=user, inline=True)
                response.add_field(name="Rank:", value=rank, inline=True)
                response.add_field(
                    name="Points:", value=points, inline=True)

                sub = get_sub_status(user)

                response.add_field(name="Subscribed?",
                                    value=sub, inline=True)
            else:
                response = officialEmbed("Rank", s_userrank["user_not_found"], color=0xdc143c)

                user_img = config.get_config("info")["icon"]
                response.set_thumbnail(url=user_img)


            await ctx.send(embed=response)
        except:
            await ctx.send(s_userrank["error"])

    async def rank_from_id(self, ctx, id):
        """Retrieve a user's rank from his ID."""

        db = database.connect_to_db()
        request = database.get_user_by_discord_uid(db, id)

        if len(request) == 0:
            response = officialEmbed("Rank", s_userrank["user_not_found"], color=0xdc143c)

            userImg = config.get_config("info")["icon"]
            response.set_thumbnail(url=userImg)

            await ctx.send(embed=response)
        else:
            user_token = request[0][1]

            data = await api_fetch(c_api_token, user_token)
            user = data["username"]

            await self.send_rank(ctx, user)

    @commands.command(description=s_userrank["help_desc"], usage="[@mention/username]")
    @check(channels="bot_commands")
    async def rank(self, ctx, user=None):
        is_id = False

        # Empty arg, so we retrieve sender's id.
        if user == None:
            await self.rank_from_id(ctx, ctx.author.id)
            return

        # Contains a user.
        ## Is it a mention or THM username?
        ### Mentions.
        if "<@!" in user:
            is_id = True
            user = user[3:len(user)-1]
        elif "<@" in user:
            is_id = True
            user = user[2:len(user)-1]

        # THM Username.
        if sanitize_check(user) == False:
            await ctx.send(s_not_sanitized)
            return
        if is_id:
            await self.rank_from_id(ctx, user)
        else:
            await self.send_rank(ctx, user)


def setup(bot):
    bot.add_cog(Userrank(bot))
