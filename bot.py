# coding: cp1252

import discord
from discord.ext import commands
import wikipediaapi
import random
import os
import openai

openai.api_key = "" # Open AI API Key

class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

wiki_wiki = wikipediaapi.Wikipedia('en')
colorDec = random.randint(0, 16777215)

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents = discord.Intents.all())

@bot.command()
async def s(ctx, *, arg):
    textReplace = arg.replace(" ", "_")
    searchQuery = textReplace
    page = wiki_wiki.page(searchQuery)
    text = page.summary

    textLine = text.splitlines()
    repeat = ""
    for i in range (len(textLine)):
        repeat += textLine[i]
        repeat += "\n\n"

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Summarize this: " + repeat,
    temperature=0.7,
    max_tokens=800,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=1
    )

    embedVar = discord.Embed(title=page.title, description=response.choices[0].text, color=colorDec)
    view = Menu()
    view.add_item(discord.ui.Button(label="See More", style=discord.ButtonStyle.link, url=page.fullurl))
    await ctx.send(embed=embedVar, view=view)

@bot.command()
async def rickroll(ctx):
    await ctx.send('never gonna give you up')

@bot.command()
async def a(ctx):
    embedVar = discord.Embed(title="Wikicord 0.0.1", description="by Alcohol#1010", color=colorDec)
    embedVar.add_field(name="Reference", value="OpenAI for summarization\nWikipediaAPI for Wikipedia contents\nDiscord.py for bot coding process")
    await ctx.send(embed=embedVar)

@bot.command()
async def q(ctx):
    helpCommand = "• ``$s + <search query>``: Search a content\n\• ``$q``: Help\n\• ``$a``: About this bot"
    embedVar = discord.Embed(title="Help", description=helpCommand, color=colorDec)
    await ctx.send(embed=embedVar)

TOKEN = '' # Discord bot token
bot.run(TOKEN)





