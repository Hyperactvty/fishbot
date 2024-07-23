import c_UtilityMethods as UM
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import discord_components
from discord_components import DiscordComponents, Button, ActionRow, InteractionType, Select, SelectOption
from discord_slash import SlashCommand, SlashContext

"""
  Brings up the fish data, how many of that fish has been caught by user, regions, 
  times it comes out, depth, sizing, etc.

  Preferred Bait can maybe be found out by trial and error

  for legendary fish, have spiky orange and yellow thing around fish
"""

async def Fishipedia(ctx, *args):
  try:
    try:
      if(args):
        awaited_generatedEmbed = await ctx.send(embed=createdEmbed,
            components = [ActionRow
              (
                Button(style=1, emoji="◀", custom_id="button_PREV"),
                Button(style=1, emoji="▶", custom_id="button_NEXT"),
                Button(label = "X", style=4, custom_id="button_CLOSE")
              )
            ])

        def check(res):
              return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

        #try:
        #    res = await bot.wait_for("button_click", check=check, timeout=20)
        #    # await ctx.defer()  # Defers the thing to make no error message
        #    await res.respond(type=7, hidden=True,delete_after=0.1)
        #    while True:

        #except: pass
    except: # No Args
      print()
  except Exception as e:
      await ctx.send(
          embed=UM.createErrorMessage(e), delete_after=120
      )
  return