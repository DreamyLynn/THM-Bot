import asyncio
import json
import time

import aiohttp
import discord
from discord.ext import commands

import libs.config as config
from libs.embedmaker import officialEmbed

####################
# Config variables #
####################

# Strings and images.
s_faq = config.get_string("faq")
img_openvpn = config.get_config("images")["openvpn"]
img_aocfaq = config.get_config("images")["aocfaq"]

############
# COG Body #
############

class FAQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description=s_faq["vpn"][0])
    async def vpn(self, ctx):
        response = officialEmbed()

        response.set_thumbnail(url=(img_openvpn))
        response.add_field(name=s_faq["vpn"][0], value=s_faq["vpn"][1])

        await ctx.send(embed=response)

    @commands.command(name="multivpn", description=s_faq["vpnmulti"][0])
    async def vpn_multi(self, ctx):
        response = officialEmbed(title=s_faq["vpnmulti"][0])

        response.set_thumbnail(url=(img_openvpn))
        
        for i in range(1, len(s_faq["vpnmulti"])):
            response.add_field(name="• Step "+str(i), value=s_faq["vpnmulti"][i])

        await ctx.send(embed=response)

    @commands.command(name="vpnscript", description=s_faq["vpnscript"][0])
    async def vpnscript(self, ctx):
        response = officialEmbed()

        response.set_thumbnail(url=(img_openvpn))
        response.add_field(name=s_faq["vpnscript"][0], value=s_faq["vpnscript"][1])

        await ctx.send(embed=response)

    @commands.command(name="aocfaq", description=s_faq["aocfaq"][0])
    async def aocfaq(self, ctx):
        response = officialEmbed()

        response.set_thumbnail(url=(img_aocfaq))
        response.add_field(name=s_faq["aocfaq"][0], value=s_faq["aocfaq"][1])

        await ctx.send(embed=response)       
def setup(bot):
    bot.add_cog(FAQ(bot))
