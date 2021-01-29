import discord

from discord import guild
from discord.ext import commands

from datetime import datetime

import libs.config as config

import libs.command_manager as command_manager
from libs.command_manager import check, error_response

from libs.embedmaker import officialEmbed

# Look for staff_lounge channel ID
id_staff_lounge = config.get_config("channels")["staff_lounge"]

# Look for Mod role ID from config
id_mod = config.get_config("roles")["mod"]

# Load stored strings
s_pingmods = config.get_string("ping_mods")


class PingMods(commands.Cog, name="Ping Mods"):
    def __init__(self, bot):
        self.bot = bot
    
    # Checks to see if the user is a Mentor and if so, will only send in #staff_lounge
    # Command Manager (CM) does not (yet) have a way of differentiating what part of the check has failed
    # I.e. All conditions in the check must be true for command to work, however any command that is wrong the check will just return false
    # This means that the Command Manager will return the error_response it's been coded to return, where you cannot modify the behaviour of it outside of the CM
    # In this case I wanted the error messages given by the bot to persist in chat.
    @commands.command(name="pingmods", description=s_pingmods["help_desc"], usage="{reason}", hidden=True)
    @check(roles="mentor",
        channels="staff_lounge",
        dm_flag=False)


    async def ping_mods(self, ctx, *reason):

        # If no reason is provided, send "Please provide a reason" but do not delete
        if not reason:
            await command_manager.error_response(ctx, s_pingmods["no_reason"], delete_msg=False, delete_ctx=False)
        
        # Otherwise assume any reason given is a reason for pinging moderators
        else:
            # Load value of moderator role from config into modRole
            modRole = ctx.guild.get_role(id_mod)

            # Create Embed. First the title
            embed = officialEmbed("Pinging Moderators:")

            # Setup embed fields
            timestamp = datetime.now()
            embed.add_field(name="Mentor:", value="{}".format(ctx.author), inline=False)
            embed.add_field(name="Reason:", value=' '.join(reason), inline=False)
            embed.add_field(name="Timestamp:", value=timestamp, inline=False)

            # Send embed
            await ctx.send(embed=embed)

            # Ping Moderators
            await ctx.send(modRole.mention)


def setup(bot):
    bot.add_cog(PingMods(bot))
