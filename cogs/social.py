import asyncio
import json
import random
import time

import discord
import requests
from discord.ext import commands

import libs.config as config
import tweepy
from libs.embedmaker import officialEmbed


###################
# Other variables #
###################

# Embeds data.
social = config.get_string("socials")

# Twitter API key.
file_twitter_cred = config.get_config("twitter_creds")

# Socials.
github = social["github"]
twitter = social["twitter"]
reddit = social["reddit"]
website = social["website"]
tweet = social["tweet"]
discord = social["discord"]
blog = social["blog"]
shop = social["shop"]
email = social["email"]

# URLs.
gitURL = github["url"]
twitterURL = twitter["url"]
redditURL = reddit["url"]
websiteURL = website["url"]
discordURL = discord["url"]
blogURL = blog["url"]
shopURL = shop["url"]
emailURL = email["url"]

# Titles.
gitTitle = github["title"]
twitterTitle = twitter["title"]
redditTitle = reddit["title"]
websiteTitle = website["title"]
discordTitle = discord["title"]
blogTitle = blog["title"]
shopTitle = shop["title"]
emailTitle = email["title"]

# Pictures.
gitPic = github["pic"]
twitterPic = twitter["pic"]
redditPic = reddit["pic"]
websitePic = website["pic"]
discordPic = discord["pic"]
blogPic = blog["pic"]
shopPic = shop["pic"]
emailPic = email["pic"]

# Colors
twitterColor = 0x08a0e9
redditColor = 0xff5700
websiteColor = 0x000000
gitColor = 0x0463C4
discordColor = 0x7289da
blogColor = 0x000000
shopColor = 0x000000
emailColor = 0x000000


#############
# Functions #
#############

# Make embeds.
def getEmbedSocial(n, v, t, c):
    """Make the embed able to display a social media infos."""

    response = officialEmbed(n, v, color=c)
    response.set_thumbnail(url=t)
    return response


############
# COG Body #
############

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description=github["help_desc"])
    async def github(self, ctx):
        response = getEmbedSocial(gitTitle, gitURL, gitPic, gitColor)
        await ctx.send(embed=response)

    @commands.command(description=twitter["help_desc"])
    async def twitter(self, ctx):
        response = getEmbedSocial(
            twitterTitle, twitterURL, twitterPic, twitterColor)
        await ctx.send(embed=response)

    @commands.command(description=reddit["help_desc"])
    async def reddit(self, ctx):
        response = getEmbedSocial(
            redditTitle, redditURL, redditPic, redditColor)
        await ctx.send(embed=response)

    @commands.command(description=website["help_desc"])
    async def website(self, ctx):
        response = getEmbedSocial(
            websiteTitle, websiteURL, websitePic, websiteColor)
        await ctx.send(embed=response)
    
    @commands.command(description=discord["help_desc"])
    async def discord(self, ctx):
        response = getEmbedSocial(
            discordTitle, discordURL, discordPic, discordColor)
        await ctx.send(embed=response)

    @commands.command(description=blog["help_desc"])
    async def blog(self, ctx):
        response = getEmbedSocial(
            blogTitle, blogURL, blogPic, blogColor)
        await ctx.send(embed=response)
    
    @commands.command(description=shop["help_desc"])
    async def shop(self, ctx):
        response = getEmbedSocial(
            shopTitle, shopURL, shopPic, shopColor)
        await ctx.send(embed=response)

    @commands.command(description=email["help_desc"])
    async def email(self, ctx):
        response = getEmbedSocial(
            emailTitle, emailURL, emailPic, emailColor)
        await ctx.send(embed=response)

    @commands.command(description=social["help_desc"])
    async def social(self, ctx):
        response = getEmbedSocial(
            twitterTitle, twitterURL, twitterPic, twitterColor)
        await ctx.send(embed=response)

        response = getEmbedSocial(
            redditTitle, redditURL, redditPic, redditColor)
        await ctx.send(embed=response)

        response = getEmbedSocial(
            websiteTitle, websiteURL, websitePic, websiteColor)
        await ctx.send(embed=response)

        response = getEmbedSocial(
            discordTitle, discordURL, discordPic, discordColor)
        await ctx.send(embed=response)    

        response = getEmbedSocial(
            blogTitle, blogURL, blogPic, blogColor)
        await ctx.send(embed=response)

        response = getEmbedSocial(
            shopTitle, shopURL, shopPic, shopColor)
        await ctx.send(embed=response) 

        response = getEmbedSocial(
            emailTitle, emailURL, emailPic, emailColor)
        await ctx.send(embed=response)

    @commands.command(name="tweet", description=tweet["help_desc"])
    async def last_tweet(self, ctx):
        # Secret twitter API key.
        creds = [cred.replace("\n", "") for cred in open(file_twitter_cred, "r")]

        # Auth & get.
        auth = tweepy.OAuthHandler(creds[0], creds[1])
        auth.set_access_token(creds[2], creds[3])
        api = tweepy.API(auth)
        tryhackme_tweets = api.user_timeline(
            screen_name='RealTryHackMe', count=20, include_rts=False)

        # Sends first found tweet. (and not reply.)
        for tweet in tryhackme_tweets:
            if not tweet.in_reply_to_screen_name:
                await ctx.send("https://twitter.com/RealTryHackMe/status/" + str(tweet.id))
                break


def setup(bot):
    bot.add_cog(Social(bot))
