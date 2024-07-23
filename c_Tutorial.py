import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot
from discord_components import DiscordComponents, Button, ActionRow, SelectOption, Select
import datetime; now = datetime.datetime.now()

class Tutorial(commands.Cog):
  def __init__(self, bot, page):
    self.bot = bot
    self.page = page
      
  def TutorialPages(self, message, page):
    tutorialPages = [{'Page':1, 'Header':
                      {'title':"═══════ **Welcome to Fishbot** ═══════", 
                       'description':f"""Table of Contents
                                        `{str("Getting Started").rjust(14," ")}`\t|\t`{str("The Basics of Fishbot").ljust(25," ")}`
                                        `{str("Shopping").rjust(15," ")}`\t|\t`{str("The lures").ljust(25," ")}`
                                        `{str("Leveling Up").rjust(15," ")}`\t|\t`{str("The regions to fish in").ljust(25," ")}`
                                        `{str("Boats").rjust(13," ")}`\t|\t`{str("The Boats").ljust(25," ")}`
                                        `{str("Baits").rjust(15," ")}`\t|\t`{str("Baits to catch fish").ljust(25," ")}`
                                        `{str("About").rjust(15," ")}`\t|\t`{str("About Fishbot and the creator").ljust(25," ")}`""",
                       'color':str(discord.Color.green())
                       },  'Footer':"Page "+str(self.page)+"/5"}, 
                     {'Page':2, 'Header':
                      {'title':"═══════ **Tutorial: Getting Started** ═══════", 
                       'description':"""__Welcome to **Fishbot**__\nTo start your fishing adventure, use the command `f.fish` in any designated channel and you will start fishing.\nWhen you use the command (`f.fish`), a button with a fish appears. When the button turns blue, click it and you will "catch" a fish.""",
                       'color':str(discord.Color.green())
                       }, 'Fields':[{'name':"__Example__", 'value':"""How to fish:"""}], 'Footer':"Page "+str(self.page)+"/5",
                       'Image':'https://media.giphy.com/media/bzEjUYPfg5TIfY4JMz/giphy.gif'}, 
                     {'Page':3,  'Header':
                      {'title':"═══════ **Tutorial: Shopping** ═══════", 
                       'description':"When you catch fish, you receive points. The points you earn can be used in the shop [`f.shop`] to buy rods, lures, regions, bait, boats, and other things.\nFor detailed explanation on what each item does, click some of the buttons below.\n",
                       'color':str(discord.Color.green())
                       }, 'Fields':[{'name':"Button Values", 'value':f'''`{str("🎣 Rods").rjust(14," ")}`\t|\t`{str("The various rods").ljust(25," ")}`
                                                                         `{str("🇱 Lures").rjust(15," ")}`\t|\t`{str("The lures").ljust(25," ")}`
                                                                         `{str("🇷 Regions").rjust(15," ")}`\t|\t`{str("The regions to fish in").ljust(25," ")}`
                                                                         `{str("🛶 Boats").rjust(13," ")}`\t|\t`{str("The Boats").ljust(25," ")}`
                                                                         `{str("🇧 Baits").rjust(15," ")}`\t|\t`{str("Baits to catch fish").ljust(25," ")}`
                                                                         `{str("🇩 Deals").rjust(15," ")}`\t|\t`{str("The Daily/Weekly Deals").ljust(25," ")}`''','inline':False},
                                    {'name':"__Example__", 'value':"""This example shows you how the shop works""", 'inline':False}], 'Footer':"Page "+str(self.page)+"/5",
                       'Image':'https://media.giphy.com/media/bzEjUYPfg5TIfY4JMz/giphy.gif'}, 
                     {'Page':4, 'Header':
                      {'title':"═══════ **Tutorial: Leveling Up** ═══════", 
                       'description':"The bigger the fish is, the more XP you gain.",
                       'color':str(discord.Color.green())
                       }, 'Fields':[{'name':"__Picture Example__", 'value':"""{Insert Picture Example Here}"""}], 'Footer':"Page "+str(self.page)+"/5",
                       'Image':'https://media.giphy.com/media/bzEjUYPfg5TIfY4JMz/giphy.gif'}, 
                     {'Page':5, 'Header':
                      {'title':"═══════ **Tutorial: Prestige** ═══════", 
                       'description':"If you feel like fishing is too easy of a task, you can risk it all by **prestiging** [`fish-pre c`]. Fishbot will roll a 20-side dice (*yes, it uses it's flippers to roll the dice*) to determine your fate.",
                       'color':str(discord.Color.green())
                       }, 'Fields':[{'name':"__Picture Example__", 'value':"""{Insert Picture Example Here}"""}], 'Footer':"Page "+str(self.page)+"/5",
                       'Image':'https://media.giphy.com/media/bzEjUYPfg5TIfY4JMz/giphy.gif'}, 
                     {'Page':6, 'Header':
                      {'title':"═══════ **Tutorial: Creator Info** ═══════", 
                       'description':"Fishbot was developed by <@287803347388596238>. He enjoys creating Discord bots for the most useless things. \nFishbot was developed using **Python 3.6**",
                       'color':str(discord.Color.green())
                       }, 'Fields':[{'name':"__Picture Example__", 'value':"""{Insert Picture Example Here}"""}], 'Footer':"Page "+str(self.page)+"/5",
                       'Image':'https://media.giphy.com/media/bzEjUYPfg5TIfY4JMz/giphy.gif'}
                     ]
    return tutorialPages[self.page-1]
  
  def changePage(self,page):
    self.page=page
    if(self.page>6): self.page=1
    if(self.page<1): self.page=6

  def TutorialSubcomponents(self, page):
    """
      Add these under the navigation buttons
    """
    components = [ActionRow
                  (
                    Button(label = "Prev Page", style=1, emoji="◀", custom_id="tutorialButton_PREV"),
                    Button(label = "Next Page", style=1, emoji="▶", custom_id="tutorialButton_NEXT"),
                    Button(label = "X", style=4, custom_id="tutorialButton_CLOSE")
                  )
                ]
    if(page==1):
      selectOptionList = [SelectOption(label = f"Getting Started", value=f"select_BASICS_2", description=f"Your Basic Fish Command. Get familiar with it."),
                          SelectOption(label = f"Shop", value=f"select_SHOP_3", description=f"Your shopping goods."),
                          SelectOption(label = f"LEveling Up", value=f"select_LEVELUP4", description=f"How Leveling up affects gameplay."),
                          SelectOption(label = f"Prestige", value=f"select_PRESTIGE5", description=f"What Prestige is and how it works."),
                          SelectOption(label = f"About", value=f"select_ABOUT6", description=f"About the bot and the creator.")
                          ]
      components = [ActionRow
                  (
                    Button(label = "Prev Page", style=1, emoji="◀", custom_id="tutorialButton_PREV"),
                    Button(label = "Next Page", style=1, emoji="▶", custom_id="tutorialButton_NEXT"),
                    Button(label = "X", style=4, custom_id="tutorialButton_CLOSE")
                  ),ActionRow( Select(options=selectOptionList, custom_id="SELECT_ITEM", placeholder=f"Click to go to page" ) )
          ]
    if(page==3):
      components = [ActionRow
            (
              Button(label = "Rods", style=2, emoji="🎣", custom_id="tutorialButton_SHOP_RODS"),
              Button(label = "Lures", style=2, emoji="🇱", custom_id="tutorialButton_SHOP_LURES"),
              Button(label = "Regions", style=2, emoji="🇷", custom_id="tutorialButton_SHOP_REGIONS")
            ), ActionRow
            (
              Button(label = "Boats", style=2, emoji="🛶", custom_id="tutorialButton_SHOP_BOATS"),
              Button(label = "Bait", style=2, emoji="🇧", custom_id="tutorialButton_SHOP_BAIT"),
              Button(label = "Daily/Weekly Deals", style=2, emoji="🇩", custom_id="tutorialButton_SHOP_DEALS")
            ), ActionRow
                  (
                    Button(label = "Prev Page", style=1, emoji="◀", custom_id="tutorialButton_PREV"),
                    Button(label = "Next Page", style=1, emoji="▶", custom_id="tutorialButton_NEXT"),
                    Button(label = "X", style=4, custom_id="tutorialButton_CLOSE")
                  )
          ]
    return components