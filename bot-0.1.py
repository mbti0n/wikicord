# coding: cp1252

import discord
from discord.ext import commands
import wikipediaapi
import random
import os
import openai
import string

openai.api_key = "" # OpenAI token


colorDec = random.randint(0, 16777215)

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='-', intents = discord.Intents.all())



# command -s + <search-query> (with English only)
@bot.command()
async def s(ctx, *, arg):

    # Wikipedia search query
    wiki_wiki = wikipediaapi.Wikipedia('en')
    textReplace = arg.replace(" ", "_")
    searchQuery = textReplace
    page = wiki_wiki.page(searchQuery)

    if page.exists() == True: # generate page data if it exists
        text = page.summary[0:4080] + "..."
        textLine = text.splitlines()
        repeat = ""
        for i in range (len(textLine)):
           repeat += textLine[i]
           repeat += "\n\n"

        # OpenAI model and action configuration
        response = openai.Completion.create(
        model="text-curie-001",
        prompt="Summarize this: " + repeat,
        temperature=0.7,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=1
        )
        
        class Menu(discord.ui.View):
            def __init__(self):
                super().__init__()

            @discord.ui.button(label="See Wikipedia Content", style=discord.ButtonStyle.blurple)
            async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
                embedVar = discord.Embed(title=page.title, description=repeat, color=colorDec)
                view = Menu()
                view.add_item(discord.ui.Button(label="See More", style=discord.ButtonStyle.link, url=page.fullurl))
                await interaction.response.send_message(embed = embedVar, view=view)

                
            @discord.ui.button(label="See GPT Summarization", style=discord.ButtonStyle.blurple)
            async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
                embedVar = discord.Embed(title=page.title, description=response.choices[0].text, color=colorDec)
                view = Menu()
                view.add_item(discord.ui.Button(label="See More", style=discord.ButtonStyle.link, url=page.fullurl))
                await interaction.response.send_message(embed = embedVar, view=view)        

        embedVar = discord.Embed(title=page.title, description=response.choices[0].text, color=colorDec)

        view = Menu()
        view.add_item(discord.ui.Button(label="See More", style=discord.ButtonStyle.link, url=page.fullurl))

        await ctx.send(embed=embedVar, view=view)

    else: # prompt if it does not exist
        embedVar = discord.Embed(title="Page not exists", description="Please try again.", color=colorDec)
        await ctx.send(embed=embedVar)

# command -ss <language> <search-query> (with English only)
@bot.command()
async def ss(ctx, arg1, *, arg2):

    # Wikipedia search query
    wiki_wiki = wikipediaapi.Wikipedia(arg1)
    typeInput = string.capwords(arg2)
    textReplace = typeInput.replace(" ", "_")
    searchQuery = textReplace
    page = wiki_wiki.page(searchQuery)

    if page.exists() == True: # generate page data if it exists
        text = page.summary[0:4080] + "..."
        textLine = text.splitlines()
        repeat1 = ""
        for i in range (len(textLine)):
           repeat1 += textLine[i]
           repeat1 += "\n\n"
        class Menu(discord.ui.View):
            def __init__(self):
                super().__init__()

        '''
        # OpenAI model and action configuration
        response = openai.Completion.create(
        model="text-curie-001",
        prompt="Summarize this: " + repeat1,
        temperature=0.7,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=1
        )
 
        
        

        Disable GPT summarization, because it only shows in English despite having a text content in another language.
            @discord.ui.button(label="See Wikipedia Content", style=discord.ButtonStyle.blurple)
            async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
                embedVar = discord.Embed(title=page.title, description=repeat1, color=colorDec)
                view = Menu()
                view.add_item(discord.ui.Button(label="See More", style=discord.ButtonStyle.link, url=page.fullurl))
                await interaction.response.send_message(embed = embedVar, view=view)

                
            @discord.ui.button(label="See GPT Summarization", style=discord.ButtonStyle.blurple)
            async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
                embedVar = discord.Embed(title=page.title, description=response.choices[0].text, color=colorDec)
                view = Menu()
                view.add_item(discord.ui.Button(label="See More", style=discord.ButtonStyle.link, url=page.fullurl))
                await interaction.response.send_message(embed = embedVar, view=view)

            '''

        embedVar = discord.Embed(title=page.title, description=repeat1, color=colorDec)
        embedVar.set_author(name=f"{arg1}.wikipedia.org")

        view = Menu()
        view.add_item(discord.ui.Button(label="See More", style=discord.ButtonStyle.link, url=page.fullurl))

        await ctx.send(embed=embedVar, view=view)

    else: # prompt if it does not exist
        embedVar = discord.Embed(title="Page not exists", description="Please try again.", color=colorDec)
        await ctx.send(embed=embedVar)        


@bot.command()
async def a(ctx):
    embedVar = discord.Embed(title="Wikicord 0.1.10", description="by Alcohol#1010", color=colorDec)
    embedVar.add_field(name="Reference", value="\
    OpenAI for summarization\n\
    WikipediaAPI for Wikipedia contents\n\
    Discord.py for bot coding process")
    await ctx.send(embed=embedVar)

@bot.command()
async def d(ctx):
    embedVar = discord.Embed(title="Donate", description="Click the gray button below to donate me, using **PayPal**.\n\
    Thank you so much :sparkling_heart:", color=colorDec)
    class Menu(discord.ui.View):
        def __init__(self):
            super().__init__()
    viewDonate = Menu()
    viewDonate.add_item(discord.ui.Button(label="Donate Me!", style=discord.ButtonStyle.link, url="https://paypal.me/mbtion123?country.x=US&locale.x=en_US"))
    await ctx.send(embed=embedVar, view=viewDonate)

@bot.command()
async def q(ctx):
    helpCommand = "\
    • ``-s <search query>``: Search a content\n\
    • ``-ss <language> <search query>``: Search a content\n\
    • ``-q``: Help\n\
    • ``-d``: Donate me\n\
    • ``-a``: About this bot"
    embedVar = discord.Embed(title="Help", description=helpCommand, color=colorDec)
    await ctx.send(embed=embedVar)

TOKEN = '' # Discord bot token
bot.run(TOKEN)





