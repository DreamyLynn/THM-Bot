import discord
import re

from discord import guild
from discord.ext import commands

import libs.config as config
import libs.database as database

from libs.command_manager import check, error_response

from libs.embedmaker import officialEmbed

# Command specific strings
from libs.thm_api import get_user_by_token

s_lookup = config.get_string("moderation")["lookup"]

# Other variables
id_guild = config.get_config("server")
thm_user_link = config.get_config("url")["user_profile"]
token_regex = re.compile(r"^[0-9a-f]{24}$")
mention_regex = re.compile(r"^<@(?:!|)(\d+)>$")
user_id_regex = re.compile(r"^(?:\d+)$")
user_discrim_regex = re.compile(r"^(?:.+)#(?:\d{4})$")


class Moderation(commands.Cog, name="Moderation commands"):
    def __init__(self, bot):
        self.bot = bot
        self.conn = database.connect_to_db()

    @commands.command(name="lookup", description=s_lookup["help_desc"], usage=s_lookup["usage"], hidden=True)
    @check(roles=["modlead", "admin"], dm_flag=False)
    async def lookup(self, ctx, *arg):
        arg = ' '.join(arg)

        # Token-based search check
        if token_regex.match(arg):
            match_type = 'token'

            db_result = database.get_user_by_thm_token(self.conn, arg)
        else:
            # ID-based search checks
            if mention_regex.match(arg):
                match_type = 'mention'
                user_id = mention_regex.search(arg).group(1)
            elif user_id_regex.match(arg):
                match_type = 'user id'
                user_id = arg
            elif user_discrim_regex.match(arg):
                match_type = 'user#discrim'
                user = self.bot.get_guild(id_guild).get_member_named(arg)
                if user is None:
                    return await ctx.send(f"Failed to find a user with that discriminator")
                user_id = user.id
            else:
                return await ctx.send(s_lookup["match_failed"])

            try:
                db_result = database.get_user_by_discord_uid(self.conn, user_id)
            except:
                return await ctx.send(s_lookup["db_fetch_failed"])

        # Loops over the results (also handles multiple-row results if they occur)
        for row in db_result:
            u_id, u_token = row

            try:
                thm_user = get_user_by_token(u_token)
            except:
                return await ctx.send(s_lookup["thm_fetch_failed"])

            response = officialEmbed("Token match", footer=f"Matched with {match_type}")

            response.add_field(name="Discord mention", value=f"<@{u_id}>")
            response.add_field(name="Discord ID", value=u_id)
            response.add_field(name="THM username", value=thm_user["username"])
            response.add_field(name="THM profile", value=thm_user_link.format(thm_user["username"]))
            response.add_field(name="THM token", value=u_token)

            await ctx.send(embed=response)


def setup(bot):
    bot.add_cog(Moderation(bot))
