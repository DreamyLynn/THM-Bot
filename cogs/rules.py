import discord
from discord.ext import commands

import libs.config as config
from libs.command_manager import check
from libs.embedmaker import officialEmbed
from libs.utils import sanitize_check

#####################
# Strings variables #
#####################

rules = config.get_string("rules")
s_not_sanitized = config.get_string("commands")["not_sanitized"]


#############
# Functions #
#############

# Sends the rules.
async def send_rules(channel):
    """Makes the embed with all the rules and sends it."""

    # Make embed.
    response = officialEmbed("Rules", color=0xffff00)
    response.set_thumbnail(url=config.get_config("info")["logo"])

    # Load the rules from config.
    i = 0

    # Add each rule.
    for rule in rules:
        response.add_field(name=(str(i+1)+"."), value=rule)
        i = i + 1

    # Send.
    await channel.send(embed=response)


############
# COG Body #
############

class Rules(commands.Cog, name="Rules Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Sends the rules.")
    @check(roles=["trialmod", "mod", "modlead", "admin"], dm_flag=False)
    async def rules(self, ctx):
        await send_rules(ctx.channel)

    @commands.command(description="Sends the requested rule.", usage="{rule}")
    @check(roles=["trialmod", "mod", "modlead", "admin"], dm_flag=False)
    async def rule(self, ctx, ruleNb):

        if not sanitize_check(ruleNb):
            await ctx.send(s_not_sanitized)
            return

        message = "Rule " + ruleNb + " does not exist."

        ruleNb = int(ruleNb)

        if ruleNb >= 1 and ruleNb <= len(rules):
            message = "**__Rule " + str(ruleNb) + ":__** " + rules[ruleNb-1]

        await ctx.send(message)


def setup(bot):
    bot.add_cog(Rules(bot))
