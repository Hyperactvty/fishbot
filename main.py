import discord; client = discord.Client()
import asyncio
import typing, random
import os, sys, traceback
import json,ast, math
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import discord_components
from discord_components import DiscordComponents, Button, ActionRow, InteractionType, Select, SelectOption, Interaction
from discord_slash import SlashCommand, SlashContext
import datetime; now = datetime.datetime.now()
import pyodbc
from functools import reduce

#from replit import db

#The Methods Import
import c_MenuItems, c_UtilityMethods as UM, c_Tutorial, c_Database as D, c_FileReading, Fish as F, c_UserData as UD, c_ShopItems as S, c_WorldEnviroment as WE, c_ItemValues as IV
import c_GenerateFishImage as IMG, c_ImageCreation as IC
# import Classes

global _WE
WORLDENVIROMENT = WE.WorldEnviroment()
WORLDENVIROMENT = WE.ChangeWorldEnviroment(WORLDENVIROMENT)
MENUITEMS = c_MenuItems.MenuItems()

_WE = WORLDENVIROMENT

FISH_OBJECTS = []; usersFishing=[] # For making sure the same user does not fish again while fishing

#FISH_OBJECTS=c_FileReading.SeperateValues(c_FileReading.ReadInputs()); print("Loaded Fish from Text File")
FISH_OBJECTS=D.StartupFishGrab()

FISH_OBJECTS_SBRarity=F.SortFishByRarity(FISH_OBJECTS)

fishLanguages=["pescar", "ribarstvo", "rybolov", "fiskeri", "visvangst", "kalastamine", "kalastus","fishing"] # Put me below when ready
prefixes = "fish-", "f-", "Fish-", "F-", 'f.', 'F.'

def command_prefix(bot, message):
    if message.guild is None:
      return "fish-", "f-", "Fish-", "F-", ""
    else:
      return "fish-", "f-", "Fish-", "F-", 'f.', 'F.'
bot = commands.Bot(command_prefix=command_prefix, ignore_extra=False, case_insensitive=True)
#slash = SlashCommand(bot)

def check_IsChannelFishing(ctx):
    if(ctx.channel in fishLanguages): return True
    return False

@bot.event
async def on_ready():
    DiscordComponents(bot)
    print(f"Logged in as {bot.user}!")
    print("At: ",now)
    print('------')
    ChangeEnviroment.start()
    QuestBoardRefresh.start()
#    command_prefix()

    game = discord.Game(str("In Develop mode"))
    await bot.change_presence(status=discord.Status.online, activity=game)
    usersFishing=[]

@bot.command()
async def ping(ctx):
    await ctx.send('pong  <a:rotatingruby:859191883338219530>')

@tasks.loop(minutes=1)
async def ChangeEnviroment():
  #print('\n\tChanging World Enviroments\n')
  worldEnviroment = WE.ChangeWorldEnviroment(WORLDENVIROMENT)
  _WE=worldEnviroment

@bot.command()
async def update(ctx, *args):
  #await ctx.send(embed=UM.AutoCheckDatabase())
  UM.UpdateUserData(ctx)
  return

#==============================================================================================
""" Settings Area """

#@bot.command(aliases=['sett','pref', 'prefs'])
#async def settings(ctx):
#  try:
#    print("Have the user choose if they want the fist Name, rarity, points (no calc), and image")
#    print("or if they want 3 other templates. Maybe make settings table")
#    #await ctx.send(embed=F.CreateSampleFish())
#  except Exception as e:
#      await ctx.send(
#          embed=UM.createErrorMessage(e), delete_after=120
#      )

@bot.command(aliases=['sett', 'options'], name='settings', description='Lets you view your settings.')
async def settings(ctx, *args):
  try:
    if(D.CheckIfUserExists(ctx.author.id)==False): start(ctx)#UD.NotifyUserForRegistering(ctx); return

    generatedEmbed=discord.Embed(title=f'Settings', description=f"Change your settings here", color=discord.Color.green())
    generatedEmbed.set_footer(text=f'Happy Fishing.', icon_url=str(ctx.author.avatar_url))

    numberButtons=["⚙","💾","🛠","❔","🔐",]
    itemsInCategory=["General", "Preferences", "Mode Select", "Support", "Privacy"]
    itemsDescriptions=[f"`{str('General').center(12, ' ')}`\n`{str('settings').center(12, ' ')}`\n`{str(' ').center(12, ' ')}`", f"`{str('Your').center(12, ' ')}`\n`{str('personalised').center(12, ' ')}`\n`{str('settings').center(12, ' ')}`", f"`{str('To switch').center(12, ' ')}`\n`{str('from PC').center(12, ' ')}`\n`{str('to Mobile').center(12, ' ')}`", f"`{str('Visit the').center(12, ' ')}`\n`{str('support').center(12, ' ')}`\n`{str('server').center(12, ' ')}`", f"`{str('Choose what').center(12, ' ')}`\n`{str('other people').center(12, ' ')}`\n`{str('can see').center(12, ' ')}`"]
    itr=0; iters=0; list_ActionRow=[]; buttonsList=[]
    for item in itemsInCategory:
      generatedEmbed.add_field(name=f"{numberButtons[itr]} {item}", value=f"{str(itemsDescriptions[itr])}", inline=True)
      splitItemName=str(item).replace(' ','')
      buttonObj = Button(style=2, custom_id=f"button_SETTINGS_{str(splitItemName).upper()}", emoji=numberButtons[itr])
      buttonsList.append(buttonObj)
      if(len(buttonsList)%3==0): list_ActionRow.append(buttonsList[len(buttonsList)-3:len(buttonsList)]); print(f'Added New Row: {len(list_ActionRow)}')
      itr+=1

    generatedEmbed.add_field(name=f"❌ Close", value=f"`{str('Closes the').center(12, ' ')}`\n`{str('menu').center(12, ' ')}`\n`{str(' ').center(12, ' ')}`", inline=True)
    buttonsList.append(Button(label = "X", style=4, custom_id="button_CLOSE"))
    if(len(buttonsList)%3==0): list_ActionRow.append(buttonsList[len(buttonsList)-3:len(buttonsList)]); print(f'Added New Row: {len(list_ActionRow)}')
    else: list_ActionRow.append(buttonsList[len(buttonsList)-len(buttonsList)%3:len(buttonsList)]); print(f'Added New Partial Row: {len(list_ActionRow)}')

    awaited_GeneratedEmbed=await ctx.send(embed=generatedEmbed, components = list_ActionRow)

    def buttonCheck(res):
        return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

    try:
        res = await bot.wait_for("button_click", check=buttonCheck, timeout=30)
        print(f"Hit Button {res.custom_id}")
        if res.component.custom_id==("button_CLOSE") :
          print("Deleted Message")
          await awaited_GeneratedEmbed.delete()
          return
        if res.component.custom_id==("button_SETTINGS_MODESELECT") :
          print(res.component.custom_id)
          await res.respond(type=7, hidden=True,delete_after=0.1)

          generatedEmbed=discord.Embed(title=f'What Mode Do You Want To Use?',description=f'Select either **Desktop/PC** or **Mobile**', color=discord.Color.blue())
          #print("E")
          #generatedEmbed.set_footer(text=str(f'TEMP '))
          #shopEmbed=UM.CreateDiscordEmbedFromDict(shopMenu['Page']['Rod'[rodType]])
          #print("SHOP EMBED:")
          PLAYMODE_SELECT= [ActionRow(Select(options=[
                      SelectOption(label = "PC", value="select_PC", description="To have an easier experience on PC"),
                      SelectOption(label = "Mobile", value="select_MOBILE", description="To have an easier experience on mobile")
                      ], custom_id="SELECTS_OBJECT", placeholder="Select your preferred playstyle (can be changed later)"))]
          #awaited_shopEmbed=await ctx.send(
          awaited_GeneratedEmbed=await awaited_GeneratedEmbed.edit(
            embed=generatedEmbed,
            components = PLAYMODE_SELECT
          )

          def check(res):
              return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

          try:
            while True:
              res = await bot.wait_for("select_option", check=check, timeout=30)
              print(f"Selection Hit {res.component[0].value}")
        
              try:
                print("Try")
              except: print("Excpt");extendedItemName = ""
              if res.component[0].value==("select_PC") or res.component[0].value==("select_MOBILE") :
                generatedEmbed=discord.Embed(title=f'Success! You are now set to {res.component[0].label}', color=discord.Color.green())
                generatedEmbed.set_footer(text=f'Mode Selected: {res.component[0].label}', icon_url=str(ctx.author.avatar_url))
                dbLabel=res.component[0].label
                ### D.UpdateDB(ctx.author.id, f'USERS', f'Style_Selected', 'f{str(dbLabel)}')
                D.UpdateDB(ctx.author.id, tableName=f'USERS', thingToSelect=f'Mode_Selected', valuesToUpdate=f"'{str(dbLabel)}'")
                print('169')
                awaited_SelectedEmbed = await ctx.send(
                  embed=generatedEmbed, 
                  delete_after=10,
                  components = [ActionRow(Button(label = "X Close", style=4, custom_id="button_CLOSE"))]
                )
                print('175')
                await res.respond(type=7, hidden=True,delete_after=0.1)
                res = await bot.wait_for("button_click", check=check, timeout=30)
                if res.component.custom_id==("button_CLOSE") :
                  print("Deleted Message")
                  await awaited_SelectedEmbed.delete()
                  return

          except Exception as ex:
              await ctx.channel.send(f'timed out\t{ex}', delete_after=5)
              await awaited_GeneratedEmbed.delete()
              return
        
        if res.component.custom_id==("button_SETTINGS_PRIVACY") :
          print(res.component.custom_id)
          await res.respond(type=7, hidden=True,delete_after=0.1)

          generatedEmbed=discord.Embed(title=f'Do you want to be seen in global leaderboard',description=f'Select either **Yes** or **No**', color=discord.Color.blue())
          PRIVACY_SELECT= [ActionRow(Select(options=[
                      SelectOption(label = "Yes", value="select_YES", description="Your user's name will be shown on the leaderboard"),
                      SelectOption(label = "No", value="select_NO", description="Your username will be private on the leaderboard")
                      ], custom_id="SELECTS_OBJECT", placeholder="Select your leaderboard privacy (can be changed later)"))]
          #awaited_shopEmbed=await ctx.send(
          awaited_GeneratedEmbed=await awaited_GeneratedEmbed.edit(
            embed=generatedEmbed,
            components = PRIVACY_SELECT, delete_after=15
          )

          def check(res):
              return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

          try:
            #while True:
              res = await bot.wait_for("select_option", check=check, timeout=30)
              
              print(f"Selection Hit {res.component[0].value}")
              if res.component[0].value==("select_YES") or res.component[0].value==("select_NO") :
                generatedEmbed=discord.Embed(title=f'Success! You are now set to {res.component[0].label}', color=discord.Color.green())
                generatedEmbed.set_footer(text=f'Privacy Updated: {res.component[0].label}', icon_url=str(ctx.author.avatar_url))
                dbLabel=res.component[0].label
                privacyMode=1
                if(res.component[0].value==("select_YES")): privacyMode=0
                D.UpdateDB(ctx.author.id, tableName=f'USERS', thingToSelect=f'Private_User', valuesToUpdate=privacyMode)
                
                awaited_SelectedEmbed = await ctx.send(
                  embed=generatedEmbed, 
                  delete_after=10,
                  components = [ActionRow(Button(label = "X Close", style=4, custom_id="button_CLOSE"))]
                )
                await res.respond(type=7, hidden=True,delete_after=0.1)
          except Exception as e:
            #await ctx.channel.send(f'timed out\t{e}', delete_after=5)
            #await awaited_GeneratedEmbed.delete()
            return
    except Exception as e:
      await ctx.channel.send(f'timed out\t{e}', delete_after=5)
      await awaited_GeneratedEmbed.delete()
      return

    return   

  except Exception as e:
    await ctx.send(
          content="Error Hit",
          embed=UM.createErrorMessage(e), delete_after=120
      )

#==============================================================================================
""" Store Area """
@bot.command(aliases=['sh', 'store'], name='shop', description='Lets you view the shop and what you can purchase.')
async def shop(ctx, *args):
  try:
    #USERKEYS = db.keys(); userKeyString = "U"+str(ctx.author.id); userKey=db[userKeyString]
    if(D.CheckIfUserExists(ctx.author.id)==False): start(ctx)#UD.NotifyUserForRegistering(ctx); return
    shopMenu=S.ShopItems(ctx)
    shopEmbed=UM.CreateDiscordEmbedFromDict(shopMenu['Page']['Menu'])#discord.Embed(title="Shopping Time!", description="This is a shop embed. if you see this, please let <@287803347388596238> know. Thank you.", color=discord.Color.green())
    global res, resp
    
    arg_ItemType=None; arg_ItemName=None
    loopNum=0
    if True:
      while True:
        if(loopNum>=5):break
        print(f"Loop Num: {loopNum}")
        try:
         if(len(args)>0 or arg_ItemType!=None):
          #arg_ItemType=None
          try: arg_ItemType=args[0]; print(f"\tItem Type: {arg_ItemType}")
          except: pass
          if(str(arg_ItemType)[-1]=='s'): arg_ItemType=arg_ItemType[0:len(arg_ItemType)-1] # Removes the trailing 's' if added
          #arg_ItemName=None
          try: arg_ItemName=args[1]; print(f"\tItem Name: {arg_ItemName}")
          except: pass
          if(str(arg_ItemType).upper() not in ['ROD', 'LURE', 'REGION', 'BAIT']):
            generatedEmbed=discord.Embed(title=f'Error: {str(arg_ItemType)} is not a valid item',description=f'__Valid Items__```\nROD | LURE | REGION | BAIT```', color=discord.Color.red())
            #print("E")
            generatedEmbed.set_footer(text=str(f'For help, enter `f.help` or `f.cmds`'), icon_url=str(ctx.author.avatar_url))
            awaited_Embed = await ctx.channel.send(
              embed=generatedEmbed, delete_after=20
            )
            return

          if (arg_ItemName!=None):
            #if(len(args)>0):
            #    arg_ItemType=args[0] 
            #    if(str(arg_ItemType)[-1]=='s'): arg_ItemType=arg_ItemType[0:len(arg_ItemType)-1] # Removes the trailing 's' if added
                underscoreSplitter = ['button',arg_ItemType,arg_ItemName]#str(res.component.custom_id).split('_')
                itemAmount = D.GrabFromDB(ctx.author.id, f'USER_ITEM_{str(arg_ItemType).upper()}', f'{str(underscoreSplitter[1]).capitalize()}_{str(underscoreSplitter[2]).capitalize()}')
            
                #D.UpdateDB(ctx.author.id, tableName=f'USER_ITEM_{str(arg_ItemType).upper()}', thingToSelect=f'Current_{str(arg_ItemType).capitalize()}', valuesToUpdate=f"'{str(arg_ItemName).capitalize()}'")

                #rodDesc = D.GrabFromDB_WHERE(ctx.author.id, tableName='SHOP_ITEMS', thingToSelect='Item_Desc', where=f"Item_Type='Rod' AND Item_Name='{rodName}'")
                #rodPriceFromDB = D.GrabFromDB_WHERE(ctx.author.id, tableName='SHOP_ITEMS', thingToSelect='Item_Price', where=f"Item_Type='Rod' AND Item_Name='{rodName}'")
                print(f'{str(arg_ItemType).upper()}S\t\t{str(underscoreSplitter[1]).capitalize()}_{str(underscoreSplitter[2]).capitalize()}')
                itemDesc = IV.GetItemValues(f'{str(arg_ItemType).upper()}S',f'{str(underscoreSplitter[1]).capitalize()}_{str(underscoreSplitter[2]).capitalize()}')['Description']
                print(f'{str(underscoreSplitter[1]).capitalize()}_{str(underscoreSplitter[2]).capitalize()}')
                itemPriceFromDB = IV.GetItemValues(f'{str(arg_ItemType).upper()}S',f'{str(underscoreSplitter[1]).capitalize()}_{str(underscoreSplitter[2]).capitalize()}')['Price']
                print(itemDesc)
                print(itemPriceFromDB)
                #rodDesc = str(userKey['ITEMS']['RODS'][rodType]['Description'])
                #rodPrice = round(userKey['ITEMS']['RODS']['Rod_Basic']['Amount']*100,2)+
                print(f'USER_ITEM_{str(underscoreSplitter[1]).upper()}\t{arg_ItemType}')

                itemPrice = round(itemPriceFromDB,2)
                if(str(arg_ItemType).upper()=="ROD"): itemPrice = round(D.GrabFromDB(ctx.author.id, f'USER_ITEM_{str(underscoreSplitter[1]).upper()}',f'{str(underscoreSplitter[1]).capitalize()}_{str(underscoreSplitter[2]).capitalize()}')*itemPriceFromDB,2)+itemPriceFromDB
                    
                currentUserBalance=D.GrabFromDB(ctx.author.id, 'USERS', 'Current_Balance')
                #print(f"BASICALLY THE EMBED:\tTitle: {rodName}\t\tDesc: {rodDesc}```bash\nCost per rod: ${rodPrice}```")
                generatedEmbed=discord.Embed(title=f'{str(underscoreSplitter[2]).capitalize()} {str(underscoreSplitter[1]).capitalize()}',description=f'{itemDesc}```bash\nCost per {str(arg_ItemType).lower()}: ${itemPrice}```', color=discord.Color.blue())
                #print("E")
                generatedEmbed.set_footer(text=str(f'Current Balance: {UM.comma(round(currentUserBalance,2))}'))
                #shopEmbed=UM.CreateDiscordEmbedFromDict(shopMenu['Page']['Rod'[rodType]])
                #print("SHOP EMBED:")
                shopButtons=[ActionRow
                (
                  Button(label="Buy",style=2, emoji="💰", custom_id="shopButton_BUY"),
                  Button(label="Sell",style=2, emoji="💲", custom_id="shopButton_SELL"),
                  Button(label = "X Close", style=4, custom_id="shopButton_CLOSE")
                )]
                #awaited_shopEmbed=await ctx.send(
                awaited_Embed = await ctx.channel.send(
                  embed=generatedEmbed,
                  components = shopButtons
                )

                def check(res):
                    return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

                try:
                    res = await bot.wait_for("button_click", check=check, timeout=30)
                    print(f"Hit Button {res.custom_id}")
                    if res.component.custom_id==("shopButton_CLOSE") :
                      print("Deleted Message")
                      await awaited_shopEmbed.delete()
                      return
                    if res.component.custom_id==("shopButton_BUY") :
                    
                      generatedEmbed=discord.Embed(title=f'How many `{str(underscoreSplitter[2]).capitalize()}` {str(underscoreSplitter[1]).lower()}s do you want to buy? (enter number amount as message)', color=discord.Color.blue())
                      await awaited_Embed.edit(
                        embed=generatedEmbed,
                        components = [ActionRow
                            (
                              #Button(label="1", style=2, custom_id="shopButton_SINGLE", disabled=UD.CheckUserBalance(ctx, -itemPrice*1)),
                              #Button(label="MAX", style=2, custom_id="shopButton_MAX", disabled=UD.CheckUserBalance(ctx, -itemPrice)),
                              Button(label = "Cancel", style=4, custom_id="shopButton_CLOSE")
                            )]
                        )
                      await res.respond(type=7, hidden=True,delete_after=0.1)
                      print("OEUF")
                      #def check(msg):
                      #    print(f'Msg:\t{str(msg.content)}')
                            
                      #    msgType=0
                      #    try: msgType=int(msg.content)
                      #    except: msgType=msg.content
                      #    print(f"Msg Type?\t{type(msgType) in [int, float]}")
                      #    return msg.author == ctx.author and msg.channel == ctx.channel and \
                      #    type(msgType) in [int, float]
                      #try:
                      #  print("Try")
                      #  msg = await bot.wait_for("message", check=check, timeout=30)
                      #  print("Passed wait_for")
                      #  buyAmount=int(msg.content)
                      def check(msg):
                          print(f'Msg:\t{str(msg.content)}')
                            
                          msgType=0
                          try: msgType=int(msg.content)
                          except: msgType=msg.content
                          print(f"Msg Type?\t{type(msgType) in [int, float]}")
                          return msg.author == ctx.author and msg.channel == ctx.channel and \
                          (type(msgType) in [int, float] or str(msgType).lower() == 'max')
                      try:
                        print("Try")
                        msg = await bot.wait_for("message", check=check, timeout=30)
                        print("Passed wait_for")
                        buyAmount=""
                        print(1)
                        
                        print(2)
                        try: 
                          buyAmount=int(msg.content)
                          buyAmount =reduce(lambda a,b : a if a < b else b, [int(buyAmount), amountUserHas])
                        except: 
                          print("Except")
                          if(str(msg.content).lower() == 'max'):
                            buyAmount = amountUserHas
                            print("MAX")
                        print(3)
                        buyPrice=itemPrice*int(buyAmount)
                          
                        print(f'\t__Are you sure that you want to purchase {msg.content}x `{str(underscoreSplitter[2]).capitalize()}` {str(underscoreSplitter[1]).lower()}?__')
                        #print(f'\t__Are you sure that you want to purchase {msg}x `{rodName}` rods?__```fix\nPrice: {buyPrice} = {rodPrice} * {(msg)}```')
                        generatedEmbed=discord.Embed(title=f'Confirmation',description=f'__Are you sure that you want to purchase {buyAmount}x `{str(underscoreSplitter[2]).capitalize()}` {str(underscoreSplitter[1]).lower()}?__```fix\nPrice: {buyPrice} = {itemPrice} * {(msg.content)}```', color=discord.Color.green())
                        print("EED")
                        futureBalance=D.GrabFromDB(ctx.author.id, 'USERS', 'Current_Balance')-buyPrice
                        generatedEmbed.set_footer(text=f'Your balance will be {UM.comma(round(futureBalance,2))}', icon_url=str(ctx.author.avatar_url))
                        await awaited_Embed.edit(
                          embed=generatedEmbed, #CheckUserBalance
                          components = [ActionRow
                          (
                            Button(label = "Yes", style=3, emoji="✅", custom_id="shopButton_CONFIRM", disabled=UD.CheckUserBalance(ctx, -buyPrice)),
                            Button(label = "No", style=4, emoji="❌", custom_id="shopButton_DENY")
                          )]
                        )
                        #await res.respond(type=7, hidden=True,delete_after=0.1)
                        def checkConfirmation(res):
                            return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

                        try:
                            res = await bot.wait_for("button_click", check=checkConfirmation, timeout=30)
                            print(f"Hit Button Confirm {res.custom_id}")
                            if res.component.custom_id==("shopButton_CONFIRM") :
                              currBal=UD.ChangeUserBalance(ctx, -buyPrice)
                              #print("1")
                              generatedEmbed=discord.Embed(title=f'Transaction Success', color=discord.Color.green())
                              #print("2")
                              generatedEmbed.set_footer(text=f'Current balance: {UM.comma(round(currBal,2))}', icon_url=str(ctx.author.avatar_url))

                              #itemType_Str=str(args[0])
                              #if(str(args[0])[-1]=='s'): print("S AT END OF WORD"); itemType_Str=str(args[0])[0:len(args[0])-1]
                                  
                              itemType=arg_ItemType
                              itemType_Str=str(itemType)
                              if(str(itemType)[-1]=='s'): itemType_Str=str(itemType)[0:len(itemType)-1] # Removes trailing 's'

                              #print( f'USER_ITEM_{str(itemType_Str).upper()}')
                              itemTypeForDB=f'{str(underscoreSplitter[1]).capitalize()}_{str(underscoreSplitter[2]).capitalize()}'
                              print(f'{itemTypeForDB}')
                              #print(f"Amt: {int(D.GrabFromDB(ctx.author.id, 'USER_ITEM_ROD',rodType))+int(buyAmount)}")

                              D.UpdateDB(ctx.author.id, f'USER_ITEM_{str(underscoreSplitter[1]).upper()}', f'{itemTypeForDB}', int(D.GrabFromDB(ctx.author.id, f'USER_ITEM_{str(underscoreSplitter[1]).upper()}',itemTypeForDB))+int(buyAmount))
                              #print("4")
                              #userKey['ITEMS'][f'{str(arg_ItemType).upper()}S'][itemType]['Amount']+=int(arg_ItemAmount)
                              await res.respond(type=7, hidden=True,delete_after=0.1)
                              await awaited_Embed.edit(
                                embed=generatedEmbed, #CheckUserBalance
                                delete_after=10,
                                components = [ActionRow(Button(label = "X Close", style=4, custom_id="shopButton_CLOSE"))]
                              )
                              res = await bot.wait_for("button_click", check=checkConfirmation, timeout=10)
                              if res.component.custom_id==("shopButton_CLOSE") :
                                print("Deleted Message")
                                await awaited_Embed.delete()
                                return

                              return
                            if res.component.custom_id==("shopButton_DENY") :
                              generatedEmbed=discord.Embed(title=f'Transaction Cancelled', color=discord.Color.red())
                              await awaited_Embed.delete()
                              await ctx.send(embed=generatedEmbed, delete_after=5); return
                              #await awaited_shopEmbed.edit(embed=generatedEmbed, delete_after=5); return
                        except: return

                      except: await ctx.send("Message Cancelled", delete_after=10); await awaited_Embed.delete(); return

                    if res.component.custom_id==("shopButton_SELL") :
                      
                      generatedEmbed=discord.Embed(title=f'How many `{str(underscoreSplitter[2]).capitalize()}` {str(underscoreSplitter[1]).lower()}s do you want to sell? (enter number amount as message)', color=discord.Color.blue())
                      await awaited_Embed.edit(
                        embed=generatedEmbed,
                        components = [ActionRow
                            (
                              #Button(label="1", style=2, custom_id="shopButton_SINGLE", disabled=UD.CheckUserBalance(ctx, itemPrice*1)),
                              #Button(label="MAX", style=2, custom_id="shopButton_MAX", disabled=UD.CheckUserBalance(ctx, itemPrice)),
                              Button(label = "Cancel", style=4, custom_id="shopButton_CLOSE")
                            )]
                        )
                      await res.respond(type=7, hidden=True,delete_after=0.1)
                      print("OEUF")
                      #def check(msg):
                      #    print(f'Msg:\t{str(msg.content)}')
                            
                      #    msgType=0
                      #    try: msgType=int(msg.content)
                      #    except: msgType=msg.content
                      #    print(f"Msg Type?\t{type(msgType) in [int, float]}")
                      #    return msg.author == ctx.author and msg.channel == ctx.channel and \
                      #    type(msgType) in [int, float]
                      #try:
                      #  print("Try")
                      #  msg = await bot.wait_for("message", check=check, timeout=30)
                      #  print("Passed wait_for")
                      #  buyAmount=int(msg.content)
                      def check(msg):
                          print(f'Msg:\t{str(msg.content)}')
                            
                          msgType=0
                          try: msgType=int(msg.content)
                          except: msgType=msg.content
                          print(f"Msg Type?\t{type(msgType) in [int, float]}")
                          return msg.author == ctx.author and msg.channel == ctx.channel and \
                          (type(msgType) in [int, float] or str(msgType).lower() == 'max')
                      try:
                        print("Try")
                        msg = await bot.wait_for("message", check=check, timeout=30)
                        print("Passed wait_for")
                        buyAmount=""
                        print(1)
                        
                        print(2)
                        try: 
                          buyAmount=int(msg.content)
                          buyAmount =reduce(lambda a,b : a if a < b else b, [int(buyAmount), amountUserHas])
                        except: 
                          print("Except")
                          if(str(msg.content).lower() == 'max'):
                            buyAmount = amountUserHas
                            print("MAX")
                        print(3)
                        buyPrice=(itemPrice*int(buyAmount))*0.66
                          
                        print(f'\t__Are you sure that you want to sell {msg.content}x `{str(underscoreSplitter[2]).capitalize()}` {str(underscoreSplitter[1]).lower()}?__')
                        #print(f'\t__Are you sure that you want to purchase {msg}x `{rodName}` rods?__```fix\nPrice: {buyPrice} = {rodPrice} * {(msg)}```')
                        generatedEmbed=discord.Embed(title=f'Confirmation',description=f'__Are you sure that you want to sell {buyAmount}x `{str(underscoreSplitter[2]).capitalize()}` {str(underscoreSplitter[1]).lower()}?__```fix\nProfit: {buyPrice} = {itemPrice} * {(msg.content)}```', color=discord.Color.green())
                        print("EED")
                        futureBalance=D.GrabFromDB(ctx.author.id, 'USERS', 'Current_Balance')+buyPrice
                        generatedEmbed.set_footer(text=f'Your balance will be {UM.comma(round(futureBalance,2))}', icon_url=str(ctx.author.avatar_url))
                        await awaited_Embed.edit(
                          embed=generatedEmbed, #CheckUserBalance
                          components = [ActionRow
                          (
                            Button(label = "Yes", style=3, emoji="✅", custom_id="shopButton_CONFIRM", disabled=UD.CheckUserBalance(ctx, buyPrice)),
                            Button(label = "No", style=4, emoji="❌", custom_id="shopButton_DENY")
                          )]
                        )
                        #await res.respond(type=7, hidden=True,delete_after=0.1)
                        def checkConfirmation(res):
                            return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

                        try:
                            res = await bot.wait_for("button_click", check=checkConfirmation, timeout=30)
                            print(f"Hit Button Confirm {res.custom_id}")
                            if res.component.custom_id==("shopButton_CONFIRM") :
                              currBal=UD.ChangeUserBalance(ctx, buyPrice)
                              #print("1")
                              generatedEmbed=discord.Embed(title=f'Transaction Success', color=discord.Color.green())
                              #print("2")
                              generatedEmbed.set_footer(text=f'Current balance: {UM.comma(round(currBal,2))}', icon_url=str(ctx.author.avatar_url))

                              #itemType_Str=str(args[0])
                              #if(str(args[0])[-1]=='s'): print("S AT END OF WORD"); itemType_Str=str(args[0])[0:len(args[0])-1]
                              itemType=arg_ItemType
                              itemType_Str=str(itemType)
                              if(str(itemType)[-1]=='s'): itemType_Str=str(itemType)[0:len(itemType)-1] # Removes trailing 's'

                              itemTypeForDB=f'{str(underscoreSplitter[1]).capitalize()}_{str(underscoreSplitter[2]).capitalize()}'
                              print(f'{itemTypeForDB}')
                              #print(f"Amt: {int(D.GrabFromDB(ctx.author.id, 'USER_ITEM_ROD',rodType))+int(buyAmount)}")

                              D.UpdateDB(ctx.author.id, f'USER_ITEM_{str(underscoreSplitter[1]).upper()}', f'{itemTypeForDB}', int(D.GrabFromDB(ctx.author.id, f'USER_ITEM_{str(underscoreSplitter[1]).upper()}',itemTypeForDB))+int(buyAmount))
                              #print("4")
                              #userKey['ITEMS'][f'{str(arg_ItemType).upper()}S'][itemType]['Amount']+=int(arg_ItemAmount)
                              await res.respond(type=7, hidden=True,delete_after=0.1)
                              await awaited_Embed.edit(
                                embed=generatedEmbed, #CheckUserBalance
                                delete_after=10,
                                components = [ActionRow(Button(label = "X Close", style=4, custom_id="shopButton_CLOSE"))]
                              )
                              res = await bot.wait_for("button_click", check=checkConfirmation, timeout=10)
                              if res.component.custom_id==("shopButton_CLOSE") :
                                print("Deleted Message")
                                await awaited_Embed.delete()
                                return

                              return
                            if res.component.custom_id==("shopButton_DENY") :
                              generatedEmbed=discord.Embed(title=f'Transaction Cancelled', color=discord.Color.red())
                              await awaited_Embed.delete()
                              await ctx.send(embed=generatedEmbed, delete_after=5); return
                              #await awaited_shopEmbed.edit(embed=generatedEmbed, delete_after=5); return
                        except: return

                      except: await ctx.send("Message Cancelled", delete_after=10); await awaited_Embed.delete(); return
                    await res.respond(type=7, hidden=True,delete_after=0.1)
                except Exception as e:
                  await ctx.channel.send(f'timed out\t{e}', delete_after=5)
                  #await awaited_SelectEmbed.delete()
                  return


# =========================================================
#   The  None  Option
          if (arg_ItemName==None):
            print("In None")
            itemValues=D.GrabFromDB_WHERE(ctx.author.id, f'USER_ITEM_{str(arg_ItemType).upper()}', '*', f'Discord_ID={ctx.author.id}', 'o')

            itemsInCategory = IV.GetItemValues(f'{str(arg_ItemType).upper()}S', 'None', True)
            print(len(itemsInCategory))
            #buttonsList = []; rows = []# * (math.ceil(len(itemsInCategory)/4))

            numberButtons=["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣",]
            itr=0; iters=0; list_ActionRow=[]; buttonsList=[]
            for item in itemsInCategory:
              splitItemName=str(item).split('_')
              buttonObj = Button(style=2, custom_id=f"button_{str(splitItemName[0]).upper()}_{str(splitItemName[1]).upper()}", emoji=numberButtons[itr])
              buttonsList.append(buttonObj)
              if(len(buttonsList)%4==0): list_ActionRow.append(buttonsList[len(buttonsList)-4:len(buttonsList)]); print(f'Added New Row: {len(list_ActionRow)}')
              itr+=1
          
            buttonsList.append(Button(label = "X", style=4, custom_id="button_CLOSE"))
            if(len(buttonsList)%4==0): list_ActionRow.append(buttonsList[len(buttonsList)-4:len(buttonsList)]); print(f'Added New Row: {len(list_ActionRow)}')
            else: list_ActionRow.append(buttonsList[len(buttonsList)-len(buttonsList)%4:len(buttonsList)]); print(f'Added New Partial Row: {len(list_ActionRow)}')

            #iters=0; list_ActionRow=[None, None]; temp_List=[]
            #for item in buttonsList:
            #  print(f'Name: {item.custom_id}')
            #  temp_List.append(item)
            #  if(len(temp_List)%4==0):list_ActionRow[iters]=(temp_List[len(temp_List)-4:len(temp_List)]);iters+=1
          
        
            creatingFromDict=S.CreateShopFromDict(ctx, arg_ItemType)
            print(creatingFromDict)
            menuEmbed=UM.CreateDiscordEmbedFromDict(creatingFromDict)
            #generatedEmbed=discord.Embed(title=f'{str(splitItemName[0]).upper()}s',description=f'{shopMenu}', color=discord.Color.blue())
            awaited_Embed=await ctx.send(
                #embed=generatedEmbed, components=(ActionRow(buttonsList[0])), delete_after=30
                #embed=generatedEmbed, components=rows[0:len(rows)], delete_after=30
                #embed=generatedEmbed, components=[buttonsList[4-4:4]], delete_after=30
                embed=menuEmbed, components=list_ActionRow, delete_after=30
              )
            def check(res): return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

            try:
              #while True:
                res = await bot.wait_for("button_click", check=check, timeout=30)
                print(f"Button Hit {res.component.custom_id}")
                if res.component.custom_id==("button_CLOSE") :
                  await awaited_SelectEmbed.delete(); return

                await res.respond(type=7, hidden=True,delete_after=0.1)
                underscoreSplitter = str(res.component.custom_id).split('_')
                itemAmount = D.GrabFromDB(ctx.author.id, f'USER_ITEM_{str(arg_ItemType).upper()}', f'{str(underscoreSplitter[1]).capitalize()}_{str(underscoreSplitter[2]).capitalize()}')
            
                #D.UpdateDB(ctx.author.id, tableName=f'USER_ITEM_{str(arg_ItemType).upper()}', thingToSelect=f'Current_{str(arg_ItemType).capitalize()}', valuesToUpdate=f"'{str(arg_ItemName).capitalize()}'")

                #rodDesc = D.GrabFromDB_WHERE(ctx.author.id, tableName='SHOP_ITEMS', thingToSelect='Item_Desc', where=f"Item_Type='Rod' AND Item_Name='{rodName}'")
                #rodPriceFromDB = D.GrabFromDB_WHERE(ctx.author.id, tableName='SHOP_ITEMS', thingToSelect='Item_Price', where=f"Item_Type='Rod' AND Item_Name='{rodName}'")
                print(f'{str(arg_ItemType).upper()}S\t\t{str(underscoreSplitter[1]).capitalize()}_{str(underscoreSplitter[2]).capitalize()}')
                itemDesc = IV.GetItemValues(f'{str(arg_ItemType).upper()}S',f'{str(underscoreSplitter[1]).capitalize()}_{str(underscoreSplitter[2]).capitalize()}')['Description']
                print(f'{str(underscoreSplitter[1]).capitalize()}_{str(underscoreSplitter[2]).capitalize()}')
                itemPriceFromDB = IV.GetItemValues(f'{str(arg_ItemType).upper()}S',f'{str(underscoreSplitter[1]).capitalize()}_{str(underscoreSplitter[2]).capitalize()}')['Price']
                print(itemDesc)
                print(itemPriceFromDB)
                #rodDesc = str(userKey['ITEMS']['RODS'][rodType]['Description'])
                #rodPrice = round(userKey['ITEMS']['RODS']['Rod_Basic']['Amount']*100,2)+
                print(f'USER_ITEM_{str(underscoreSplitter[1]).upper()}\t{arg_ItemType}')

                itemPrice = round(itemPriceFromDB,2)
                if(str(arg_ItemType).upper()=="ROD"): itemPrice = round(D.GrabFromDB(ctx.author.id, f'USER_ITEM_{str(underscoreSplitter[1]).upper()}',f'{str(underscoreSplitter[1]).capitalize()}_{str(underscoreSplitter[2]).capitalize()}')*itemPriceFromDB,2)+itemPriceFromDB
                    
                currentUserBalance=D.GrabFromDB(ctx.author.id, 'USERS', 'Current_Balance')
                #print(f"BASICALLY THE EMBED:\tTitle: {rodName}\t\tDesc: {rodDesc}```bash\nCost per rod: ${rodPrice}```")
                generatedEmbed=discord.Embed(title=f'{str(underscoreSplitter[2]).capitalize()} {str(underscoreSplitter[1]).capitalize()}',description=f'{itemDesc}```bash\nCost per {str(arg_ItemType).lower()}: ${itemPrice}```', color=discord.Color.blue())
                #print("E")
                generatedEmbed.set_footer(text=str(f'Current Balance: {UM.comma(round(currentUserBalance,2))}'))
                #shopEmbed=UM.CreateDiscordEmbedFromDict(shopMenu['Page']['Rod'[rodType]])
                #print("SHOP EMBED:")
                shopButtons=[ActionRow
                (
                  Button(label="Buy",style=2, emoji="💰", custom_id="shopButton_BUY"),
                  Button(label="Sell",style=2, emoji="💲", custom_id="shopButton_SELL"),
                  Button(label = "X Close", style=4, custom_id="shopButton_CLOSE")
                )]
                #awaited_shopEmbed=await ctx.send(
                await awaited_Embed.edit(
                  embed=generatedEmbed,
                  components = shopButtons
                )

                def check(res):
                    return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

                try:
                    res = await bot.wait_for("button_click", check=check, timeout=30)
                    print(f"Hit Button {res.custom_id}")
                    if res.component.custom_id==("shopButton_CLOSE") :
                      print("Deleted Message")
                      await awaited_shopEmbed.delete()
                      return
                    if res.component.custom_id==("shopButton_BUY") :
                    
                      generatedEmbed=discord.Embed(title=f'How many `{str(underscoreSplitter[2]).capitalize()}` {str(underscoreSplitter[1]).lower()}s do you want to buy? (enter number amount as message)', color=discord.Color.blue())
                      await awaited_Embed.edit(
                        embed=generatedEmbed,
                        components = [ActionRow
                            (
                              #Button(label="1", style=2, custom_id="shopButton_SINGLE", disabled=UD.CheckUserBalance(ctx, -itemPrice*1)),
                              #Button(label="MAX", style=2, custom_id="shopButton_MAX", disabled=UD.CheckUserBalance(ctx, -itemPrice)),
                              Button(label = "Cancel", style=4, custom_id="shopButton_CLOSE")
                            )]
                        )
                      await res.respond(type=7, hidden=True,delete_after=0.1)
                      print("OEUF")
                      #def check(msg):
                      #    print(f'Msg:\t{str(msg.content)}')
                            
                      #    msgType=0
                      #    try: msgType=int(msg.content)
                      #    except: msgType=msg.content
                      #    print(f"Msg Type?\t{type(msgType) in [int, float]}")
                      #    return msg.author == ctx.author and msg.channel == ctx.channel and \
                      #    type(msgType) in [int, float]
                      #try:
                      #  print("Try")
                      #  msg = await bot.wait_for("message", check=check, timeout=30)
                      #  print("Passed wait_for")
                      #  buyAmount=int(msg.content)
                      def check(msg):
                          print(f'Msg:\t{str(msg.content)}')
                            
                          msgType=0
                          try: msgType=int(msg.content)
                          except: msgType=msg.content
                          print(f"Msg Type?\t{type(msgType) in [int, float] or str(msgType).lower() == 'max'}")
                          return msg.author == ctx.author and msg.channel == ctx.channel and \
                          (type(msgType) in [int, float] or str(msgType).lower() == 'max')
                      try:
                        print("Try")
                        msg = await bot.wait_for("message", check=check, timeout=30)
                        print("Passed wait_for")
                        buyAmount=""
                        print(1)
                        
                        print(2)
                        try: 
                          buyAmount=int(msg.content)
                          buyAmount =reduce(lambda a,b : a if a < b else b, [int(buyAmount), amountUserHas])
                        except: 
                          print("Except")
                          if(str(msg.content).lower() == 'max'):
                            buyAmount = amountUserHas
                            print("MAX")
                        print(3)
                        buyPrice=itemPrice*int(buyAmount)
                          
                        print(f'\t__Are you sure that you want to purchase {msg.content}x `{str(underscoreSplitter[2]).capitalize()}` {str(underscoreSplitter[1]).lower()}?__')
                        #print(f'\t__Are you sure that you want to purchase {msg}x `{rodName}` rods?__```fix\nPrice: {buyPrice} = {rodPrice} * {(msg)}```')
                        generatedEmbed=discord.Embed(title=f'Confirmation',description=f'__Are you sure that you want to purchase {buyAmount}x `{str(underscoreSplitter[2]).capitalize()}` {str(underscoreSplitter[1]).lower()}?__```fix\nPrice: {UM.comma(round(buyPrice,2))} = {UM.comma(round(itemPrice,2))} * {UM.comma((int(msg.content)))}```', color=discord.Color.green())
                        print("EED")
                        futureBalance=D.GrabFromDB(ctx.author.id, 'USERS', 'Current_Balance')-buyPrice
                        generatedEmbed.set_footer(text=f'Your balance will be {UM.comma(round(futureBalance,2))}', icon_url=str(ctx.author.avatar_url))
                        await awaited_Embed.edit(
                          embed=generatedEmbed, #CheckUserBalance
                          components = [ActionRow
                          (
                            Button(label = "Yes", style=3, emoji="✅", custom_id="shopButton_CONFIRM", disabled=UD.CheckUserBalance(ctx, -buyPrice)),
                            Button(label = "No", style=4, emoji="❌", custom_id="shopButton_DENY")
                          )]
                        )
                        #await res.respond(type=7, hidden=True,delete_after=0.1)
                        def checkConfirmation(res):
                            return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

                        try:
                            res = await bot.wait_for("button_click", check=checkConfirmation, timeout=30)
                            print(f"Hit Button Confirm {res.custom_id}")
                            if res.component.custom_id==("shopButton_CONFIRM") :
                              currBal=UD.ChangeUserBalance(ctx, -buyPrice)
                              #print("1")
                              generatedEmbed=discord.Embed(title=f'Transaction Success', color=discord.Color.green())
                              #print("2")
                              generatedEmbed.set_footer(text=f'Current balance: {UM.comma(round(currBal,2))}', icon_url=str(ctx.author.avatar_url))

                              #itemType_Str=str(args[0])
                              #if(str(args[0])[-1]=='s'): print("S AT END OF WORD"); itemType_Str=str(args[0])[0:len(args[0])-1]
                              itemType=arg_ItemType
                              itemType_Str=str(itemType)
                              if(str(itemType)[-1]=='s'): itemType_Str=str(itemType)[0:len(itemType)-1] # Removes trailing 's'

                              itemTypeForDB=f'{str(underscoreSplitter[1]).capitalize()}_{str(underscoreSplitter[2]).capitalize()}'
                              print(f'{itemTypeForDB}')
                              #print(f"Amt: {int(D.GrabFromDB(ctx.author.id, 'USER_ITEM_ROD',rodType))+int(buyAmount)}")

                              D.UpdateDB(ctx.author.id, f'USER_ITEM_{str(underscoreSplitter[1]).upper()}', f'{itemTypeForDB}', int(D.GrabFromDB(ctx.author.id, f'USER_ITEM_{str(underscoreSplitter[1]).upper()}',itemTypeForDB))+int(buyAmount))
                              #print("4")
                              #userKey['ITEMS'][f'{str(arg_ItemType).upper()}S'][itemType]['Amount']+=int(arg_ItemAmount)
                              await res.respond(type=7, hidden=True,delete_after=0.1)
                              await awaited_Embed.edit(
                                embed=generatedEmbed, #CheckUserBalance
                                delete_after=10,
                                components = [ActionRow(Button(label = "X Close", style=4, custom_id="shopButton_CLOSE"))]
                              )
                              res = await bot.wait_for("button_click", check=checkConfirmation, timeout=10)
                              if res.component.custom_id==("shopButton_CLOSE") :
                                print("Deleted Message")
                                await awaited_Embed.delete()
                                return

                              return
                            if res.component.custom_id==("shopButton_DENY") :
                              generatedEmbed=discord.Embed(title=f'Transaction Cancelled', color=discord.Color.red())
                              await awaited_shopEmbed.delete()
                              await ctx.send(embed=generatedEmbed, delete_after=5); return
                              #await awaited_shopEmbed.edit(embed=generatedEmbed, delete_after=5); return
                        except: return

                      except: await ctx.send("Message Cancelled", delete_after=10); await awaited_Embed.delete(); return
                    
                    if res.component.custom_id==("shopButton_SELL") :
                      itemType=arg_ItemType
                      itemType_Str=str(itemType)
                      if(str(itemType)[-1]=='s'): itemType_Str=str(itemType)[0:len(itemType)-1] # Removes trailing 's'
                      itemTypeForDB=f'{str(underscoreSplitter[1]).capitalize()}_{str(underscoreSplitter[2]).capitalize()}'
                      amountUserHas = int(D.GrabFromDB(ctx.author.id, f'USER_ITEM_{str(underscoreSplitter[1]).upper()}',itemTypeForDB))
                      generatedEmbed=discord.Embed(title=f'How many `{str(underscoreSplitter[2]).capitalize()}` {str(underscoreSplitter[1]).lower()}s do you want to sell? (enter number amount as message)', color=discord.Color.blue())
                      generatedEmbed.set_footer(text=f'Amount of {str(underscoreSplitter[2]).capitalize()} {str(underscoreSplitter[1]).lower()}s: {amountUserHas}', icon_url=str(ctx.author.avatar_url))
                      await awaited_Embed.edit(
                        embed=generatedEmbed,
                        components = [ActionRow
                            (
                              #Button(label="1", style=2, custom_id="shopButton_SINGLE", disabled=UD.CheckUserBalance(ctx, itemPrice*1)),
                              #Button(label="MAX", style=2, custom_id="shopButton_MAX", disabled=UD.CheckUserBalance(ctx, itemPrice)),
                              Button(label = "Cancel", style=4, custom_id="shopButton_CLOSE")
                            )]
                        )
                      await res.respond(type=7, hidden=True,delete_after=0.1)
                      print("OEUF")
                      def check(msg):
                          print(f'Msg:\t{str(msg.content)}')
                            
                          msgType=0
                          try: msgType=int(msg.content)
                          except: msgType=msg.content
                          print(f"Msg Type?\t{type(msgType) in [int, float]}")
                          return msg.author == ctx.author and msg.channel == ctx.channel and \
                          (type(msgType) in [int, float] or str(msgType).lower() == 'max')
                      try:
                        print("Try")
                        msg = await bot.wait_for("message", check=check, timeout=30)
                        print("Passed wait_for")
                        buyAmount=""
                        print(1)
                        
                        print(2)
                        try: 
                          buyAmount=int(msg.content)
                          buyAmount =reduce(lambda a,b : a if a < b else b, [int(buyAmount), amountUserHas])
                        except: 
                          print("Except")
                          if(str(msg.content).lower() == 'max'):
                            buyAmount = amountUserHas
                            print("MAX")
                        print(3)
                        
                        buyPrice=0 # (itemPrice*int(buyAmount))*0.66 # Exploit exists here
                          
                        #print(f'\t__Are you sure that you want to purchase {msg}x `{rodName}` rods?__```fix\nPrice: {buyPrice} = {rodPrice} * {(msg)}```')
                        generatedEmbed=discord.Embed(title=f'Confirmation',description=f'__Are you sure that you want to sell {buyAmount}x `{str(underscoreSplitter[2]).capitalize()}` {str(underscoreSplitter[1]).lower()}?__```fix\n{str(underscoreSplitter[2]).capitalize()} {str(underscoreSplitter[1]).lower()}: {amountUserHas-buyAmount} = {amountUserHas} - {buyAmount}```', color=discord.Color.green())
                        print("EED")
                        futureBalance=D.GrabFromDB(ctx.author.id, 'USERS', 'Current_Balance')+buyPrice
                        generatedEmbed.set_footer(text=f'Your amount of {str(underscoreSplitter[2]).capitalize()} {str(underscoreSplitter[1]).lower()}s will be: {UM.comma(amountUserHas-buyAmount)}', icon_url=str(ctx.author.avatar_url))
                        await awaited_Embed.edit(
                          embed=generatedEmbed, #CheckUserBalance
                          components = [ActionRow
                          (
                            Button(label = "Yes", style=3, emoji="✅", custom_id="shopButton_CONFIRM", disabled=UD.CheckUserBalance(ctx, buyPrice)),
                            Button(label = "No", style=4, emoji="❌", custom_id="shopButton_DENY")
                          )]
                        )
                        #await res.respond(type=7, hidden=True,delete_after=0.1)
                        def checkConfirmation(res):
                            return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

                        try:
                            res = await bot.wait_for("button_click", check=checkConfirmation, timeout=30)
                            print(f"Hit Button Confirm {res.custom_id}")
                            if res.component.custom_id==("shopButton_CONFIRM") :
                              currBal=UD.ChangeUserBalance(ctx, buyPrice)
                              itemType=arg_ItemType
                              itemType_Str=str(itemType)
                              if(str(itemType)[-1]=='s'): itemType_Str=str(itemType)[0:len(itemType)-1] # Removes trailing 's'
                              itemTypeForDB=f'{str(underscoreSplitter[1]).capitalize()}_{str(underscoreSplitter[2]).capitalize()}'
                              print(f'{itemTypeForDB}')

                              generatedEmbed=discord.Embed(title=f'Transaction Success', color=discord.Color.green())
                              generatedEmbed.set_footer(text=f'Current balance: {UM.comma(round(currBal,2))} | Amount of {str(underscoreSplitter[2]).capitalize()} {str(underscoreSplitter[1]).lower()}s: {amountUserHas-buyAmount}', icon_url=str(ctx.author.avatar_url))
                              #print(f"Amt: {int(D.GrabFromDB(ctx.author.id, 'USER_ITEM_ROD',rodType))+int(buyAmount)}")

                              D.UpdateDB(ctx.author.id, f'USER_ITEM_{str(underscoreSplitter[1]).upper()}', f'{itemTypeForDB}', amountUserHas-buyAmount)
                              #print("4")
                              #userKey['ITEMS'][f'{str(arg_ItemType).upper()}S'][itemType]['Amount']+=int(arg_ItemAmount)
                              await res.respond(type=7, hidden=True,delete_after=0.1)
                              await awaited_Embed.edit(
                                embed=generatedEmbed, #CheckUserBalance
                                delete_after=10,
                                components = [ActionRow(Button(label = "X Close", style=4, custom_id="shopButton_CLOSE"))]
                              )
                              res = await bot.wait_for("button_click", check=checkConfirmation, timeout=10)
                              if res.component.custom_id==("shopButton_CLOSE") :
                                print("Deleted Message")
                                await awaited_Embed.delete()
                                return

                              return
                            if res.component.custom_id==("shopButton_DENY") :
                              generatedEmbed=discord.Embed(title=f'Transaction Cancelled', color=discord.Color.red())
                              await awaited_Embed.delete()
                              await ctx.send(embed=generatedEmbed, delete_after=5); return
                              #await awaited_shopEmbed.edit(embed=generatedEmbed, delete_after=5); return
                        except: await ctx.send("Message Closed [CONFIRMATION]", delete_after=10); return

                      except: await ctx.send("Message Cancelled", delete_after=10); await awaited_Embed.delete(); return
                    await res.respond(type=7, hidden=True,delete_after=0.1)
                except Exception as e:
                    await ctx.channel.send(f'timed out [SHOPBUTTON] {e}', delete_after=5)
                    await awaited_Embed.delete()
                    return

                return

            except:
                #await ctx.channel.send(f'timed out', delete_after=5)
                #await awaited_SelectEmbed.delete()
                return
      
         else:
          shopButtons=[ActionRow
            (
              Button(label = "Rods", style=2, emoji="🎣", custom_id="shopButton_RODS"),
              Button(label = "Lures", style=2, emoji="🇱", custom_id="shopButton_LURES"),
              Button(label = "Regions", style=2, emoji="🇷", custom_id="shopButton_REGIONS"),
              Button(label = "Boats", style=2, emoji="🛶", custom_id="shopButton_BOATS")
            ), ActionRow
            (
              Button(label = "Daily Deals", style=2, emoji="🇩", custom_id="shopButton_DAILYDEALS"),
              Button(label = "Weekly Deals", style=2, emoji="🇼", custom_id="shopButton_WEEKLYDEALS"),
              Button(label = "What's New", style=2, emoji="❔", custom_id="shopButton_WHATSNEW")
            ), ActionRow ( Button(label = "Support Creator", style=2, emoji="🛠", custom_id="shopButton_SUPPORTCREATOR"), Button(label = "X Close", style=4, custom_id="shopButton_CLOSE") )
          ]

          usersName=ctx.author.display_name   
          fetchUser= await bot.fetch_user(int(ctx.author.id))
          try: fetchUser=await ctx.guild.fetch_member(int(userToView))
          except: pass
          embedColour=discord.Colour.blurple()
          try: 
            embedColour=fetchUser.colour
            if(str(embedColour)=='#000000'): embedColour=discord.Colour.orange()
          except: pass
          shopMenu = {
            'Header':
              {'title':f"═══════ **Happy {UM.GetDateName()}, {fetchUser.display_name}** ═══════", 
              'description':"Welcome to the Fish Shop. You can buy rods, lures, regions, bait, ~~or even boats~~. To view a category, use `fish-shop <category>`. To buy, use `fish-buy <category> <item> <amount>`",
              'color':embedColour
              }, 
            'Fields':[{'name':"🐟 Fishing Rods", 'value':"""```fix\nHas all your fishing (rod) needs. [f.shop rods]```[Hover for details](https://google.com "Basic Fishing Commands.\nX amount of commands")""",'inline':False},
                      {'name':"🇱 Lures", 'value':"""```f.cmds a```[Hover for details](https://google.com "Commands for those who like to get technical.\nX amount of commands")""",'inline':True},
                      {'name':"🇷 Regions", 'value':"""```diff\nf.shop region```[Hover for details](https://google.com "You like spending your money?\nX amount of commands")""",'inline':True},
                      {'name':"~~🛶 Boats~~", 'value':"""```diff\n-Coming Soon```[Hover for details](https://google.com "Gives you a random hint.\nX amount of commands")""",'inline':True},
                      {'name':"🇩 Daily Deals", 'value':f"""```{UM.GetDateName()} : f.daily **or** f.dailyspin```[Hover for details](https://google.com "Modify or view your settings.\nX amount of commands")""",'inline':True},
                      {'name':"🇼 Weekly Deals", 'value':f"""```diff\n-Coming Soon\n{str(UM.GetDateMonthName("WeekStart"))} - {str(UM.GetDateMonthName("WeekEnd"))}```[Hover for details](https://google.com "[Server Admins Only] Configuration for the server.\nX amount of commands")""",'inline':True},
                      {'name':"❔ What's New", 'value':"""```Fishbot 3.8 build: 062921```[Hover for details](https://github.com/Hyperactvty/fishbot/blob/main/README.md "The Changelog")""",'inline':True},
                      {'name':"🛠 Support the Creator", 'value':"""Also if you want to support the bot creator, click [here](https://www.patreon.com/hyperactvty).""",'inline':True},
                      {'name':"❌ Close Menu", 'value':"""Closes the menu""",'inline':True}], 
            'Footer':{'text':f"""If you require help, feel free to join the [server here](https://discord.gg/kg6Zw8sRjX "Click to join the discord!")""", 'icon_url':f'{ctx.author.avatar_url}'},
            'Emojis': ['🐟','🐠','🛒','❔','🛠','⚙','❌'],
            'Pages': 1, 'CurrentPage':1}
          createdEmbed = UM.CreateDiscordEmbedFromDict(shopMenu)
         
          currentBalance=D.GrabFromDB(ctx.author.id, 'USERS', 'Current_Balance')
          createdEmbed.set_footer(text=f'Current Balance: {UM.comma(round(currentBalance,2))}', icon_url=str(ctx.author.avatar_url))
          awaited_Embed = await ctx.send(embed=createdEmbed, components=shopButtons, delete_after=30)


          def checkConfirmation(res):
              return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

          try:
              res = await bot.wait_for("button_click", check=checkConfirmation, timeout=30)
              print(f"Hit Button Confirm {res.custom_id}")
              buttonName=str(res.custom_id).split('_')
              if res.component.custom_id==("shopButton_CLOSE") :
                print("Deleted Message")
                await awaited_Embed.delete()
                return
              #if res.component.custom_id==(f"shopbutton_{buttonName[1]}") :
              else:
                print("Yep")
                #args.append(str(buttonName[1]).lower()); 
                arg_ItemType=str(buttonName[1]).lower()
                await awaited_Embed.delete()
          except Exception as e:
                await ctx.send(
                  content="Error Hit",
                  embed=UM.createErrorMessage(e), delete_after=120
                )
                #await ctx.channel.send(f'timed out', delete_after=5)
                #await awaited_SelectEmbed.delete()
                return
    
        except Exception as e:
          #await ctx.send(f"Message Cancelled [EXCEPT]\t\t{e}", delete_after=10); 
          await ctx.send(
              content="Error Hit",
              embed=UM.createErrorMessage(e), delete_after=120
          )
          return
        loopNum+=1

  except Exception as e:
    await ctx.send(
          content="Error Hit",
          embed=UM.createErrorMessage(e), delete_after=120
      )
    return

""" Shop Area End """
#==============================================================================================
""" Buy Area """
# TODO: WHEN USER BUYS AN ITEM, HAVE IT WRITE TO A FILE

@bot.command(aliases=['b', 'purchase'], name='buy', description='Lets you buy items in the shop.')
async def buy(ctx, *args):
  try: 
    if(D.CheckIfUserExists(ctx.author.id)==False): start(ctx)#await UD.NotifyUserForRegistering(ctx); return
    shopEmbed=discord.Embed(title="Shopping Time!", description="This is a shop embed. if you see this, please let <@287803347388596238> know. Thank you.",color=discord.Color.green())
    global res, resp

    for a in range(0, len(args)):
      print (args[a])

    if(len(args)<3): 
      shopEmbed=discord.Embed(title="ERROR", description=f"Not enough arguments. Please use the format```fix\n{prefixes}buy <rod|lure|boat|region> <item> <amount|max>```",color=discord.Color.red())
      await ctx.channel.send(embed=shopEmbed, delete_after=20)
      return
    if(len(args)>3): 
      shopEmbed=discord.Embed(title="ERROR", description=f"Too many arguments. Please use the format```fix\n{prefixes}buy <rod|lure|boat|region> <item> <amount|max>```",color=discord.Color.red())
      await ctx.channel.send(embed=shopEmbed, delete_after=20)
      return
    try:
      arg_ItemType=args[0]; arg_ItemName=args[1]; arg_ItemAmount=args[2]
      if(str(arg_ItemType)[-1]=='s'): arg_ItemType=arg_ItemType[0:len(arg_ItemType)-1]
      print(arg_ItemType)
      itemType = f'{str(arg_ItemType).capitalize()}_{str(arg_ItemName).capitalize()}'
      try:
        print(IV.GetItemValues(f'{str(arg_ItemType).upper()}S',itemType)['Price'])
        print("a")
        itemPrice=0
        if(str(arg_ItemType).upper() == 'ROD'):
          itemPrice = round(D.GrabFromDB(ctx.author.id, f'USER_ITEM_{str(arg_ItemType).upper()}', f'{itemType}')*IV.GetItemValues(f'{str(arg_ItemType).upper()}S',itemType)['Price'],2)+IV.GetItemValues(f'{str(arg_ItemType).upper()}S',itemType)['Price']
        if(str(arg_ItemType).upper() == 'LURE'):
          itemPrice = int(IV.GetItemValues(f'{str(arg_ItemType).upper()}S',itemType)['Price'])
        print("b")
        buyPrice=itemPrice*int(arg_ItemAmount)
        print("c")
                            
        print(f'\t__Are you sure that you want to purchase {arg_ItemAmount}x `` rods?__')
        #print(f'\t__Are you sure that you want to purchase {msg}x `{rodName}` rods?__```fix\nPrice: {buyPrice} = {itemPrice} * {(msg)}```')
        generatedEmbed=discord.Embed(title=f'Confirmation',description=f'__Are you sure that you want to purchase {arg_ItemAmount}x `{arg_ItemName}` {arg_ItemType}s?__```fix\nPrice: {buyPrice} = {itemPrice} * {(arg_ItemAmount)}```', color=discord.Color.green())
        futureBalance=D.GrabFromDB(ctx.author.id, f'USER_ITEM_{str(arg_ItemType).upper()}', f'{itemType}')-buyPrice
        generatedEmbed.set_footer(text=f'Your balance will be {UM.comma(round(futureBalance,2))}', icon_url=str(ctx.author.avatar_url))
        awaited_shopEmbed=await ctx.send(
          embed=generatedEmbed, #CheckUserBalance
          components = [ActionRow
          (
            Button(label = "Yes", style=3, emoji="✅", custom_id="shopButton_CONFIRM", disabled=UD.CheckUserBalance(ctx, futureBalance)),
            Button(label = "No", style=4, emoji="❌", custom_id="shopButton_DENY")
          )]
        )
        #await res.respond(type=7, hidden=True,delete_after=0.1)
        def checkConfirmation(res):
            return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

        try:
            res = await bot.wait_for("button_click", check=checkConfirmation, timeout=30)
            print(f"Hit Button {res.custom_id}")
            if res.component.custom_id==("shopButton_CONFIRM") :
              currBal=UD.ChangeUserBalance(ctx, -buyPrice)

              generatedEmbed=discord.Embed(title=f'Transaction Success', color=discord.Color.green())
              
              generatedEmbed.set_footer(text=f'Current balance: {UM.comma(round(currBal,2))}', icon_url=str(ctx.author.avatar_url))

              D.UpdateDB(ctx.author.id, f'USER_ITEM_{str(arg_ItemType).upper()}', f'{itemType}', itemPrice*int(arg_ItemAmount))
              #userKey['ITEMS'][f'{str(arg_ItemType).upper()}S'][itemType]['Amount']+=int(arg_ItemAmount)

              await awaited_shopEmbed.edit(
                embed=generatedEmbed, #CheckUserBalance
                delete_after=10
                #components = [ActionRow
                #(
                  #Button(label = "X Close", style=4, custom_id="shopButton_CLOSE")
                #)]
              )
              return
            if res.component.custom_id==("shopButton_DENY") :
              generatedEmbed=discord.Embed(title=f'Transaction Cancelled', color=discord.Color.red())
              await awaited_shopEmbed.delete()
              await ctx.send(embed=generatedEmbed, delete_after=5); return
              #await awaited_shopEmbed.edit(embed=generatedEmbed, delete_after=5); return
        except: await ctx.send("Message Cancelled [CONFIRMATION]", delete_after=10); return

      except:
        print("INVALID ITEM NAME")
        generatedEmbed=discord.Embed(title=f'ERROR: There is no {str(arg_ItemType).lower()} called `{arg_ItemName}`',description=f'For a list of all purchasable {str(arg_ItemType).lower()}s, do ```fix\n{prefixes}shop {str(arg_ItemType).lower()}```', color=discord.Color.red())
        await ctx.send(embed=generatedEmbed, delete_after=10); return
    except: await ctx.send("Message Cancelled [EXCEPT]", delete_after=10); return

    awaited_shopEmbed=await ctx.send(
      embed=shopEmbed#,
      #components = shopButtons
    )
    

  
    return
  except Exception as e:
    await ctx.send(
          embed=UM.createErrorMessage(e), delete_after=120
      )
    return


""" Buy Area End """
#==============================================================================================
""" Set Area """

@bot.command(aliases=['s'], name='set', description='Lets you set your items.')
async def set(ctx, *args):
  try: 
    if(D.CheckIfUserExists(ctx.author.id)==False): start(ctx)#await UD.NotifyUserForRegistering(ctx); return
    generatedEmbed=discord.Embed(title="Set Command", description="This is the set embed. If you see this, please let <@287803347388596238> know. Thank you.",color=discord.Color.green())
    global res, resp
  
    for a in range(0, len(args)):
      print (args[a])

    if(len(args)<1): 
      generatedEmbed=discord.Embed(title="ERROR", description=f"Not enough arguments. Please use the format```fix\n{prefixes}set <rod|lure|boat|region> <item>```",color=discord.Color.red())
      await ctx.channel.send(embed=generatedEmbed, delete_after=20)
      return
    if(len(args)>2): 
      generatedEmbed=discord.Embed(title="ERROR", description=f"Too many arguments. Please use the format```fix\n{prefixes}set <rod|lure|boat|region> <item>```",color=discord.Color.red())
      await ctx.channel.send(embed=generatedEmbed, delete_after=20)
      return
    try:
      arg_ItemType=args[0] 
      if(str(arg_ItemType)[-1]=='s'): arg_ItemType=arg_ItemType[0:len(arg_ItemType)-1] # Removes the trailing 's' if added
      arg_ItemName=None
      try: arg_ItemName=args[1]
      except: pass
      if (arg_ItemName == None):
        itemValues=D.GrabFromDB_WHERE(ctx.author.id, f'USER_ITEM_{str(arg_ItemType).upper()}', '*', f'Discord_ID={ctx.author.id}', 'o')
        # Sets the emojis for the select options. If the number is 0, then puts a lock emoji on it.
        itemEmojis = [None] * len(itemValues)
        itr=0
        for amt in itemValues[2:len(itemValues)]:
          isNone = lambda lock : lock if lock > 0 else None
          itemEmojis[itr]=isNone(amt)
          if isNone(amt) == None: itemEmojis[itr] = '🔒'
          itr+=1

        itemsInCategory = IV.GetItemValues(f'{str(arg_ItemType).upper()}S', 'None', True)
        print(len(itemsInCategory))
        selectOptionList = []
        itr=0
        for item in itemsInCategory:
          print(item)
          splitItemName=str(item).split('_')
          selectOptionObj = SelectOption(label = f"{splitItemName[1]}", value=f"select_{str(splitItemName[0]).upper()}_{str(splitItemName[1]).upper()}", description=f"{splitItemName[1]} {splitItemName[0]} Amount: {itemValues[itr+2]}", emoji=itemEmojis[itr])
          selectOptionList.append(selectOptionObj)
          itr+=1
        
        #Rod_Basic,Rod_Bamboo,Rod_Advanced,Rod_Fiberglass,Rod_Triple,Rod_Lucky,Rod_Masterly

        SELECT_ITEM = [ActionRow( Select(options=selectOptionList, custom_id="SELECT_ITEM", placeholder=f"Click to set your {arg_ItemType}" ) )]
        
        generatedEmbed=discord.Embed(title=f'Which {arg_ItemType} do you want to select?', color=discord.Color.blurple())
        awaited_SelectEmbed = await ctx.channel.send( embed=generatedEmbed, delete_after=30, components = SELECT_ITEM )
        def check(res): return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

        try:
          while True:
            res = await bot.wait_for("select_option", check=check, timeout=30)
            #print(f"Selection Hit {res.component[0].value}")
            arg_ItemName=res.component[0].label
            underscoreSplitter = str(res.component[0].value).split('_')
            itemAmount = D.GrabFromDB(ctx.author.id, f'USER_ITEM_{str(arg_ItemType).upper()}', f'{str(underscoreSplitter[1]).capitalize()}_{str(underscoreSplitter[2]).capitalize()}')
            if(itemAmount<1): 
              # Return an error saying that the user does not have enough of the item
              generatedEmbed=discord.Embed(title=f'ERROR: Not enough {arg_ItemName} {str(arg_ItemType).lower()}s', color=discord.Color.red())
              await awaited_SelectEmbed.delete()
              await ctx.send(embed=generatedEmbed, delete_after=10); return
            generatedEmbed=discord.Embed(title=f'Successfully set your {str(arg_ItemType).lower()} to `{arg_ItemName}`', color=discord.Color.green())
            generatedEmbed.set_footer(text=f'Happy Fishing!', icon_url=str(ctx.author.avatar_url))
            D.UpdateDB(ctx.author.id, tableName=f'USER_ITEM_{str(arg_ItemType).upper()}', thingToSelect=f'Current_{str(arg_ItemType).capitalize()}', valuesToUpdate=f"'{str(arg_ItemName).capitalize()}'")
         
            await awaited_SelectEmbed.edit( embed=generatedEmbed, delete_after=10, components = [ActionRow(Button(label = "X Close", style=4, custom_id="button_CLOSE"))] )
            await res.respond(type=7, hidden=True,delete_after=0.1)
            res = await bot.wait_for("button_click", check=check, timeout=10)
            if res.component.custom_id==("button_CLOSE") :
              await awaited_SelectEmbed.delete(); return

        except:
            await ctx.channel.send(f'timed out', delete_after=5)
            #await awaited_SelectEmbed.delete()
            return

      else:
        print(arg_ItemType)
        itemType = f'{str(arg_ItemType).capitalize()}_{str(arg_ItemName).capitalize()}'
        try:
          print("a")
          #itemAmount = userKey['ITEMS'][f'{str(arg_ItemType).upper()}S'][itemType]['Amount']
          print(f'USER_ITEM_{str(arg_ItemType).upper()}\t\t{str(arg_ItemType).capitalize()}_{itemType}')
          itemAmount = D.GrabFromDB(ctx.author.id, f'USER_ITEM_{str(arg_ItemType).upper()}',f'{str(arg_ItemType).capitalize()}_{arg_ItemName}')
          print("b")
          if(itemAmount<1): 
            # Return an error saying that the user does not have enough of the item
            generatedEmbed=discord.Embed(title=f'ERROR: Not enough {arg_ItemName} {str(arg_ItemType).lower()}s', color=discord.Color.red())
            await ctx.send(embed=generatedEmbed, delete_after=10); return
          #tableName, thingToSelect, amountOfRods = 
          print(f'Item Type: {str(arg_ItemName).capitalize()}')
          D.UpdateDB(ctx.author.id, tableName=f'USER_ITEM_{str(arg_ItemType).upper()}', thingToSelect=f'Current_{str(arg_ItemType).capitalize()}', valuesToUpdate=f"'{str(arg_ItemName).capitalize()}'")
          print(f"Current_{str(arg_ItemType).capitalize()}\t = {itemType}")
          #print(f'\t__Are you sure that you want to purchase {msg}x `{rodName}` rods?__```fix\nPrice: {buyPrice} = {itemPrice} * {(msg)}```')
          generatedEmbed=discord.Embed(title=f'Successfully set your {str(arg_ItemType).lower()} to `{arg_ItemName}`', color=discord.Color.green())
          generatedEmbed.set_footer(text=f'Happy Fishing!', icon_url=str(ctx.author.avatar_url))
          awaited_shopEmbed=await ctx.send(embed=generatedEmbed, delete_after=10)
          
        except:
          print("INVALID ITEM NAME")
          generatedEmbed=discord.Embed(title=f'ERROR: There is no {str(arg_ItemType).lower()} called `{arg_ItemName}`',description=f'For a list of all purchasable {str(arg_ItemType).lower()}s, do ```fix\n{prefixes}shop {str(arg_ItemType).lower()}```', color=discord.Color.red())
          await ctx.send(embed=generatedEmbed, delete_after=10); return
    except Exception as e: 
      await ctx.send(f"Message Cancelled [EXCEPT]\t\t{e}", delete_after=10); 
      return
    return
  except Exception as e:
    await ctx.send(
          embed=UM.createErrorMessage(e), delete_after=120
      )
    return


""" Set Area End """
#==============================================================================================
""" Phone Area """
"Note; Have a small thin animated banner at the top displaying the time of day, weather, and season"
@bot.command(aliases=['p'], name='Phone', description='Brings up your in-game phone')
async def phone(ctx, *args):
  try: 
    if(D.CheckIfUserExists(ctx.author.id)==False): start(ctx)#await UD.NotifyUserForRegistering(ctx); return
    
    phoneBannerImage=IMG.c_GenerateFishImage.GeneratePhoneBannerAnimation()
    #file_FishSplash = discord.File("FishBotItems/ImagesForTesting/ws_2.gif") # The image in the same folder as the main bot file
    
    file_PhoneBannerImage = discord.File("FishBot_py3.8/ImagesForTesting/phoneBanner.gif") # The image in the same folder as the main bot file
    #file_PhoneBannerImage = discord.File("FishBot_py3.8/ImagesForTesting/phoneBanner.png") # The image in the same folder as the main bot file

    currentTime=datetime.datetime.now()
    str_CurrentTime=currentTime.strftime("%a, %B %d, %Y \t | \t %H:%M")
    str_NowTime=currentTime
    print(currentTime.strftime("%a, %B %d, %Y \t | \t %H:%M"))
    print(WE.GenerateForecastEmbed(_WE))
    cw=_WE['SEASON']['Seasons'][_WE['SEASON']['CurrentSeason']]
    #cTemp=_WE['WEATHER'][_WE['WEATHER']['CurrentWeather']]['CurrentTemp']
    cTemp=15
    print(f'{cw}')
    print(f'{cTemp}')

    # Day ADCFE9 | Dusk ECC1B2 | Dawn E49759 | Midnight 08113B 
    timeColour=discord.Color.green()
    if(_WE['TIME']['Times'][_WE['TIME']['CurrentTime']]=="Day"): timeColour = 'ADCFE9'
    if(_WE['TIME']['Times'][_WE['TIME']['CurrentTime']]=="Dusk"): timeColour = 'ECC1B2'
    if(_WE['TIME']['Times'][_WE['TIME']['CurrentTime']]=="Night"): timeColour = '08113B'
    if(_WE['TIME']['Times'][_WE['TIME']['CurrentTime']]=="Dawn"): timeColour = 'E49759'
    print(int(hex(int(timeColour, 16)), 0))
    phoneEmbed=discord.Embed(title=f"{ctx.author.name}'s Phone", description=f"```{str_CurrentTime}``````fix\n{_WE['SEASON']['Seasons'][_WE['SEASON']['CurrentSeason']]}\t:\t{_WE['TIME']['Times'][_WE['TIME']['CurrentTime']]}```",color=int(hex(int(timeColour, 16)), 0))
    phoneEmbed.add_field(name="Current Weather:", value=f"{cw} - **{cTemp}°c**", inline=True)
    phoneEmbed.add_field(name="Special Events:", value=f"**None Yet**", inline=True)
    #phoneEmbed.add_field(name="Weather Forecast:", value=f"```fix\n{str_NowTime} - **{_WE['WEATHER'][_WE['WEATHER']['CurrentWeather']]['CurrentTemp']}°c```", inline=False)
    phoneEmbed.add_field(name="Weather Forecast:", value=f"{WE.GenerateForecastEmbed(_WE)}", inline=False)
    await ctx.send(embed=phoneEmbed, file=file_PhoneBannerImage) 
    global res, resp

    for a in range(0, len(args)):
      print (args[a])
    
    try:
      arg_ItemType=args[0]; arg_ItemName=args[1]
      if(str(arg_ItemType)[-1]=='s'): arg_ItemType=arg_ItemType[0:len(arg_ItemType)-1]
      print(arg_ItemType)
      itemType = f'{str(arg_ItemType).capitalize()}_{str(arg_ItemName).capitalize()}'
      try:
        print("a")
        itemAmount = userKey['ITEMS'][f'{str(arg_ItemType).upper()}S'][itemType]['Amount']
        print("b")
        if(itemAmount<1): 
          # Return an error saying that the user does not have enough of the item
          generatedEmbed=discord.Embed(title=f'ERROR: Not enough {arg_ItemName}', color=discord.Color.red())
          await ctx.send(embed=generatedEmbed, delete_after=10); return

        userKey['ITEMS'][f'Current_{str(arg_ItemType).capitalize()}']=itemType
        print(f"Current_{str(arg_ItemType).capitalize()}\t = {itemType}")
        #print(f'\t__Are you sure that you want to purchase {msg}x `{rodName}` rods?__```fix\nPrice: {buyPrice} = {itemPrice} * {(msg)}```')
        generatedEmbed=discord.Embed(title=f'Successfully set your {str(arg_ItemType).lower()} to `{arg_ItemName}`', color=discord.Color.green())
        generatedEmbed.set_footer(text=f'Happy Fishing!', icon_url=str(ctx.author.avatar_url))
        awaited_shopEmbed=await ctx.send(embed=generatedEmbed)
        #await res.respond(type=7, hidden=True,delete_after=0.1)
        

      except:
        print("INVALID ITEM NAME")
        generatedEmbed=discord.Embed(title=f'ERROR: There is no {str(arg_ItemType).lower()} called `{arg_ItemName}`',description=f'For a list of all purchasable {str(arg_ItemType).lower()}s, do ```fix\n{prefixes}shop {str(arg_ItemType).lower()}```', color=discord.Color.red())
        await ctx.send(embed=generatedEmbed, delete_after=10); return
    except: await ctx.send("Message Cancelled [EXCEPT]", delete_after=10); return
    return
  except Exception as e:
    await ctx.send(
          embed=UM.createErrorMessage(e), delete_after=120
      )
    return


""" Phone Area End """
#==============================================================================================
""" Quest Area """
import c_Quests as Q
@bot.command(aliases=['q', 'quests'], name='Quest', description='Shows your current quests')
async def quest(ctx, *args):
  try: 
    if(D.CheckIfUserExists(ctx.author.id)==False): start(ctx)#UD.NotifyUserForRegistering(ctx); return
    try:
      if(str(args[0]).lower()=='claim' or str(args[0]).lower()=='c'):
        questObject = Q.CheckQuestClaim(ctx)
        if(len(questObject)<1): return
        if(questObject[0]==True):
          questNums = []
          for item in questObject[1]: questNums.append(item)
          await ctx.channel.send(f"Congratulations, you finished Quest{UM.Str.Plural(questObject)} {UM.Str.ListWithAnd(questNums)}")

          
          for x in questObject[1]:
            userExp=D.GrabFromDB(ctx.author.id, 'USERS', 'User_Exp'); currBal=D.GrabFromDB(ctx.author.id, 'USERS', 'Current_Balance')
            grabbedQuestIDFromDB = D.GrabFromDB_WHERE(ctx.author.id, 'USER_QUESTS', 'QUEST_ID', f'Discord_ID = {ctx.author.id}')
            print(grabbedQuestIDFromDB)
            grabbedQuestFromDB = D.GrabFromDB_WHERE(ctx.author.id, 'USER_QUESTS', 'Quest_Reqs', f'Discord_ID = {ctx.author.id} AND QUEST_ID = {grabbedQuestIDFromDB}')
            #for questItem in grabbedQuestFromDB:
            try: grabbedQuestFromDB['Requirements']
            except: grabbedQuestFromDB = (json.loads(grabbedQuestFromDB))
            D.UpdateDB(ctx.author.id, tableName=f'USERS', thingToSelect=f'Current_Balance', valuesToUpdate=currBal+grabbedQuestFromDB['Award'])
            D.UpdateDB(ctx.author.id, tableName=f'USERS', thingToSelect=f'User_Exp', valuesToUpdate=userExp+grabbedQuestFromDB['Experience'])
            D.DeleteFromDB_WHERE(ctx.author.id, 'USER_QUESTS', f'QUEST_ID = {grabbedQuestIDFromDB}')
    except:
      grabbedQuestFromDB = D.GrabFromDB_WHERE(ctx.author.id, 'USER_QUESTS', 'Quest_Reqs', f'Discord_ID = {ctx.author.id}', 'a')
      print(grabbedQuestFromDB)
      print(len(grabbedQuestFromDB))
      
      usersName=ctx.author
      try: usersName=ctx.author.nick
      except: pass
      currentTime = datetime.datetime.now()
      #checkRemainingHours = 12-currentTime.hour%12; checkRemainingMins = 60-currentTime.minute%60; checkRemainingSecs = 60-currentTime.second%60
      st=UM.ShopTimer()
      checkRemainingHours = st[0]; checkRemainingMins = st[1]; checkRemainingSecs = st[2]
      
      #hourInterval = currentTime+datetime.timedelta(hours=checkRemainingHours)
      #print(f"\tHour Interval: {hourInterval} {checkRemainingMins:02d} {checkRemainingSecs:02d}")
      questEmbed = discord.Embed(title=f"{usersName}'s Quests",description=f"Here are your ongoing quests:", color=discord.Color.blurple())
      if(len(grabbedQuestFromDB)==0):
        print("No Quests for User")
        questEmbed = discord.Embed(title=f"{usersName}'s Quests",description=f"No Quests Available. Check back in `{checkRemainingHours}h` `{checkRemainingMins}m` `{checkRemainingSecs}s`", color=discord.Color.red())
        await ctx.channel.send(embed=questEmbed)
        return

      dict_Quest = (grabbedQuestFromDB)
      for questItem in dict_Quest:
        questItem=(json.loads(questItem))
        print(str(f"{questItem['Type']} ({questItem['Difficulty'][0:2]})"))
        print(f"```{Q.GenerateQuestText(questItem)}```")
        questEmbed.add_field(name=str(f"{questItem['Type']} ({questItem['Difficulty'][0:2]})"), value=f"```{Q.GenerateQuestText(questItem)}```**{checkRemainingHours}h {checkRemainingMins}m {checkRemainingSecs}s left**", inline=False)
      #questEmbed = Q.GenerateNewQuest(ctx)
      questEmbed.set_footer(text=f"Time until quests reset: {checkRemainingHours}h {checkRemainingMins}m {checkRemainingSecs}s")
    
      await ctx.channel.send(embed=questEmbed)
    
    
  except Exception as e:
    await ctx.send(
          embed=UM.createErrorMessage(e), delete_after=120
      )
    return


""" Quest Area End """
#==============================================================================================
""" Quest Board Area """

# Refreshes at 4a and 4p in UTC-5 Time
morningRefresh=datetime.time(hour=4); afternoonRefresh=datetime.time(hour=16)
@tasks.loop(minutes=1)
async def QuestBoardRefresh():
  ct = datetime.datetime.now()
  currentTime = datetime.time(hour=ct.hour, minute=ct.minute)
  tempRefresh=datetime.time(hour=ct.hour, minute=ct.minute)
  print(f"CT : {currentTime}\tMR : {morningRefresh}\tAR : {afternoonRefresh}")
  #if(currentTime==tempRefresh): 
  if(currentTime==morningRefresh or currentTime==afternoonRefresh): 
    print("\n\tRefreshing Time!\n")
    D.DeleteFromDB(None, 'USER_QUESTBOARD', '*')
    D.DeleteFromDB(None, 'USER_QUESTS', '*')
    D.UpdateDB_WHERE(None, 'USERS', 'Quest_Refreshes', 3, 'Quest_Refreshes < 3')
    D.UpdateDB_WHERE(None, 'USERS', 'Has_Refreshed_Quest', 0, 'Has_Refreshed_Quest = 1')

  if(currentTime==morningRefresh):
    # Have the database auto-update

    D.UpdateDB_WHERE(None, 'USERS', 'Daily_Spin', 0, 'Daily_Spin = 1') # Resets those who have done their daily spin back to 0
  
  return

@bot.command(aliases=['qb', 'questBoard'], name='Quest Board', description='Shows the quests available')
async def questboard(ctx, *args):
  try: 
    if(D.CheckIfUserExists(ctx.author.id)==False): start(ctx)#UD.NotifyUserForRegistering(ctx); return
    try:
      if(str(args[0]).lower()=='refresh' or str(args[0]).lower()=='ref' or str(args[0]).lower()=='r'):
        # Check if user has enough free refreshes
        grabbedQuestRefreshesFromDB = D.GrabFromDB_WHERE(ctx.author.id, 'USERS', 'Quest_Refreshes', f'Discord_ID = {ctx.author.id}')
        if(grabbedQuestRefreshesFromDB>0):
          await ctx.channel.send("Refreshing Quests")
          try: D.DeleteFromDB(ctx.author.id, 'USER_QUESTBOARD', '*')
          except: pass
          D.UpdateDB(ctx.author.id, tableName=f'USERS', thingToSelect=f'Quest_Refreshes', valuesToUpdate=grabbedQuestRefreshesFromDB-1)
          D.UpdateDB(ctx.author.id, tableName=f'USERS', thingToSelect=f'Has_Refreshed_Quest', valuesToUpdate=0)
          
          Q.GenerateQuestBoard(ctx)
        await questboard(ctx)
      if(str(args[0]).lower()=='accept' or str(args[0]).lower()=='a'):
        grabbedQuestsFromDB = D.GrabFromDB_WHERE(ctx.author.id, 'USER_QUESTS', 'QUEST_ID', f'Discord_ID = {ctx.author.id}', 'a')
        grabbedPremLevelFromDB = D.GrabFromDB_WHERE(ctx.author.id, 'USERS', 'Premium_Level', f'Discord_ID = {ctx.author.id}')
        if(len(grabbedQuestsFromDB)>=3+(grabbedPremLevelFromDB*2)): 
          generatedEmbed=discord.Embed(title="Quest Limit Reached", description=f"You have reached your **quest limit** ({len(grabbedQuestsFromDB)}/{3+(grabbedPremLevelFromDB*2)}).\nPlease complete some quests or purchase more quest slots.",color=discord.Color.red())
          await ctx.channel.send(embed=generatedEmbed, delete_after=20)
          return
        if(len(args)<2): 
          generatedEmbed=discord.Embed(title="ERROR", description=f"Not enough arguments. Please use the format```fix\n{prefixes}questboard <accept> <1-7>```",color=discord.Color.red())
          await ctx.channel.send(embed=generatedEmbed, delete_after=20)
          return
        if(len(args)>2): 
          generatedEmbed=discord.Embed(title="ERROR", description=f"Too many arguments. Please use the format```fix\n{prefixes}questboard <accept> <1-7>```",color=discord.Color.red())
          await ctx.channel.send(embed=generatedEmbed, delete_after=20)
          return
        if(int(args[1]) in range(1,8)):
          print("Yeah, we in, bro")
          grabbedQuestFromDB = D.GrabFromDB_WHERE(ctx.author.id, 'USER_QUESTBOARD', f'Q{int(args[1])}', f'Discord_ID = {ctx.author.id}')
          dict_Quest = (json.loads(grabbedQuestFromDB))
          if(f"Accepted" in (dict_Quest)['Type']): 
            generatedEmbed=discord.Embed(title="ERROR", description=f"You already accepted this quest.",color=discord.Color.red())
            await ctx.channel.send(embed=generatedEmbed, delete_after=20)
            return
          currentTime = datetime.datetime.now()
          checkRemainingHours = 12-currentTime.hour%12; checkRemainingMins = 60-currentTime.minute%60; checkRemainingSecs = 60-currentTime.second%60
          questEmbed = discord.Embed(title=f"Successfully accepted **Quest {args[1]}**: {(dict_Quest)['Type']} ({(dict_Quest)['Difficulty'][0:2]})",description=f"{Q.GenerateQuestText(dict_Quest)}\nXP: **{dict_Quest['Experience']}**\t|\tAward: **{dict_Quest['Award']}**", color=discord.Color.green())
          #questEmbed.add_field(name=str(f"{(dict_Quest)['Type']} ({(dict_Quest)['Difficulty'][0:2]})"), value=f"XP: **{dict_Quest['Experience']}**\t|\tAward: **{dict_Quest['Award']}**", inline=True)
          questEmbed.set_footer(text=f"Time until quests reset: {checkRemainingHours}h {checkRemainingMins}m {checkRemainingSecs}s")
          str_Quest = str(dict_Quest).replace("'",'"')
          D.InsertIntoDB(ctx.author.id, tableName='USER_QUESTS', 
                   columnsToUpdate=f'''Discord_ID, Difficulty, Quest_Type, Quest_Reqs''', 
                   valuesToInsert= f'''{ctx.author.id}, '{dict_Quest['Difficulty']}', '{dict_Quest['Type']}', '{str_Quest}\'''')
          
          # Update the text in the table column so include 'Claimed'
          updatedName=f"{(dict_Quest)['Type']} - Accepted"
          dict_Quest['Type'] = updatedName
          str_Quest = str(dict_Quest).replace("'",'"')
          D.UpdateDB(ctx.author.id, tableName=f'USER_QUESTBOARD', thingToSelect=f'Q{int(args[1])}', valuesToUpdate=f"'{str_Quest}'")#f"'{str_UpdatedName}'")
          
          await ctx.channel.send(embed=questEmbed, delete_after=20)
    except Exception as e:
      print(e)
      grabbedQuestsFromDB = D.GrabFromDB_WHERE(ctx.author.id, 'USER_QUESTS', 'QUEST_ID', f'Discord_ID = {ctx.author.id}', 'a')
      grabbedQuestRefreshesFromDB = D.GrabFromDB_WHERE(ctx.author.id, 'USERS', 'Quest_Refreshes', f'Discord_ID = {ctx.author.id}')
      #currentTime = datetime.datetime.now()
      #checkRemainingHours = (12-currentTime.hour%12); checkRemainingMins = 60-currentTime.minute%60; checkRemainingSecs = 60-currentTime.second%60

      ct = datetime.datetime.now()
      currentTime = datetime.datetime(ct.year, ct.month, ct.day, hour=ct.hour, minute=ct.minute, second=ct.second)
      future = datetime.datetime(ct.year, ct.month, ct.day, 4, 0, 0)
      if(ct.hour<4): future = datetime.datetime(ct.year, ct.month, ct.day, 4, 0, 0)
      elif(ct.hour>=4 and ct.hour<16): future = datetime.datetime(ct.year, ct.month, ct.day, 16, 0, 0)
      elif(ct.hour>=16): future = datetime.datetime(ct.year, ct.month, ct.day, 4, 0, 0)
      difference = future - currentTime 
      
      checkRemainingHours=difference.seconds//3600; checkRemainingMins = (difference.seconds//60)%60; checkRemainingSecs=difference.seconds%60
      print(f"No Quests Available. Check back in `{difference.seconds//3600}h` `{(difference.seconds//60)%60}m` `{difference.seconds%60}s`")
      #checkRemainingHours = int((12-currentTime.hour%12)/3); checkRemainingMins = 60-currentTime.minute%60; checkRemainingSecs = 60-currentTime.second%60
      #hourInterval = currentTime+datetime.timedelta(hours=checkRemainingHours)
      questEmbed = discord.Embed(title=f"Quests Available",description=f"No Quests Available. Check back in `{checkRemainingHours}h` `{checkRemainingMins}m` `{checkRemainingSecs}s`", color=discord.Color.red())
      
      questEmbed = Q.GenerateQuestBoard(ctx)
      questEmbed.set_footer(text=f"Quest Refreshes Available: {grabbedQuestRefreshesFromDB}/3  |  Current Quests: {len(grabbedQuestsFromDB)}/3  |  Time until quests reset: {checkRemainingHours}h {checkRemainingMins}m {checkRemainingSecs}s")
    
      await ctx.channel.send(embed=questEmbed)
    
    
  except Exception as e:
    await ctx.send(
          embed=UM.createErrorMessage(e), delete_after=120
      )
    return


""" Quest Board Area End """
#==============================================================================================
""" Trophywall Area """

  #async with ctx.typing():
  #  # do expensive stuff here
  #  await ctx.send('done!')

@bot.command(aliases=['tw', 'twall'], name='Trophy Wall', description="Lets you view your or other people's trophy walls.")
async def trophywall(ctx, *args):
  KEYWORDS=['set','remove']
  # Set will bring up an embed with numbers to the areas to set fish
  try:
    isKeyword = [ele for ele in KEYWORDS if(ele in args)]
    print(isKeyword)
    if(bool(isKeyword)):
      numberButtons=["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣",]
      if(str(args[0])=='set'):
        usersName=""
        try: usersName= ctx.author.display_name
        except Exception as e: usersName = ctx.author.split('#')[0]; print(f"Error: {e}")
        embedColour=discord.Colour.blurple()
        try: embedColour=ctx.author.colour; print(f"User Colour: {embedColour}")
        except: pass

        generatedEmbed=discord.Embed(title=f"Which area do you want to set?", color=embedColour)
        USER_TROPHYWALL = D.GrabFromDB_ALL(ctx.author.id, "USER_TROPHYWALL","*",'o')
        itr=0; TITLES = ["Featured Fish", "Slot 2", "Slot 3", "Slot 4", "Slot 5", "Slot 6", "Slot 7"]
        INLINES = [False, True, True, True, True, True, True]

        list_ActionRow=[]; buttonsList=[]
        

        # generatedEmbed.add_field(name=f"{numberButtons[itr]} {TITLES[itr]}", value=f"```fix\nName:\tDate Caught:\nSize:\t%:\nPoints:```", inline=False)
        for column in USER_TROPHYWALL[1:len(USER_TROPHYWALL)]:
          #if(column == None): pass
          #else:
          generatedEmbed.add_field(name=f"{numberButtons[itr]} {TITLES[itr]}", value=f"```cr\n{column}```", inline=INLINES[itr])
          buttonObj = Button(style=2, custom_id=f"button_{itr}", emoji=numberButtons[itr])
          buttonsList.append(buttonObj)
          if(len(buttonsList)%4==0): list_ActionRow.append(buttonsList[len(buttonsList)-4:len(buttonsList)]); print(f'Added New Row: {len(list_ActionRow)}')
          itr+=1

        buttonsList.append(Button(label = "X", style=4, custom_id="button_CLOSE"))
        if(len(buttonsList)%4==0): list_ActionRow.append(buttonsList[len(buttonsList)-4:len(buttonsList)]); print(f'Added New Row: {len(list_ActionRow)}')
        else: list_ActionRow.append(buttonsList[len(buttonsList)-len(buttonsList)%4:len(buttonsList)]); print(f'Added New Partial Row: {len(list_ActionRow)}')
        awaited_GeneratedEmbed=await ctx.channel.send(embed=generatedEmbed,components=list_ActionRow)

        def check(res): return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

        try:
          while True:
            res = await bot.wait_for("button_click", check=check, timeout=30)
            print(f"Button Hit {res.component.custom_id}")
            if res.component.custom_id==("button_CLOSE") :
              #break
              await awaited_GeneratedEmbed.delete(); return

            await res.respond(type=7, hidden=True,delete_after=0.1)
            print(f"Hit Button Confirm {res.custom_id}")
            generatedEmbed=discord.Embed(title=f"Please enter the `Fish ID` of the fish you want to show", color=embedColour)
            generatedEmbed.set_footer(text=f"To get a list of all your fish, do f.list <page#>", icon_url=str(ctx.author.avatar_url))
            awaited_GeneratedEmbed=await awaited_GeneratedEmbed.edit(embed=generatedEmbed,components=[Button(label = "X", style=4, custom_id="button_CLOSE")])
            def checkMsg(msg):
                msgType=0
                try: msgType=int(msg.content)
                except: msgType=msg.content
                print(f"Msg Type?\t{type(msgType) in [int]}")
                return msg.author == ctx.author and msg.channel == ctx.channel and \
                type(msgType) in [int]
            try:
              print("Try")
              msg = await bot.wait_for("message", check=checkMsg, timeout=30)
              print("Passed wait_for")
              fishID=int(msg.content)
            except: await awaited_GeneratedEmbed.delete(); return
          
        except: 
          pass
    else:  
      userToView = ctx.author
      try:
        if(len(args)>0): userToView = args[0]
        userToView=userToView.strip("<@!").strip(">")
      except: userToView = ctx.author.id
      try:
        if(type(int(userToView))!=int or len(userToView)!=18):
          generatedEmbed=discord.Embed(title=f"Error: Please use a valid user mention or ID", color=discord.Color.red())
          awaited_SelectEmbed=await ctx.channel.send(embed=generatedEmbed, delete_after=30)
          return
      except Exception as e:
        if("invalid literal for int() with base 10:" in str(e)):
          generatedEmbed=discord.Embed(title=f"Error: Please use a valid user mention or ID", color=discord.Color.red())
          awaited_SelectEmbed=await ctx.channel.send(embed=generatedEmbed, delete_after=30)
          return
      if(D.CheckIfUserExists(userToView)==False): 
        generatedEmbed=discord.Embed(title=f'Error',description=f'User **{userToView}** does not exist yet.', color=discord.Color.red())
        awaited_SelectEmbed=await ctx.channel.send(embed=generatedEmbed, delete_after=30)
        return
      else:
        #fetchUser=await ctx.guild.fetch_member(int(userToView))
        fetchUser= await bot.fetch_user(int(userToView)); usersName=""
        try: fetchUser=await ctx.guild.fetch_member(int(userToView)); usersName= fetchUser.display_name
        except Exception as e: usersName = str(fetchUser).split('#')[0]; print(f"Error: {e}")
        embedColour=discord.Colour.random()
        try: embedColour=fetchUser.colour; print(f"User Colour: {embedColour}")
        except: pass
        # Have next page, uh, featured as false inline adn probs 3-5 lines tall
        generatedEmbed=discord.Embed(title=f"{usersName}{UM.Str.Apostrophe(usersName)} Trophy Wall",description=f"**{usersName}{UM.Str.Apostrophe(usersName)} Featured Fish**", color=embedColour)
        USER_TROPHYWALL = D.GrabFromDB_ALL(userToView, "USER_TROPHYWALL","*",'o')
        print(USER_TROPHYWALL[1:len(USER_TROPHYWALL)])

        if(USER_TROPHYWALL[1:len(USER_TROPHYWALL)]==[None,None,None,None,None,None,None]):generatedEmbed=discord.Embed(title=f"{usersName}{UM.Str.Apostrophe(usersName)} Trophy Wall",description=f"{usersName} has nothing to share ¯\\_(ツ)_/¯", color=embedColour)
        else: 
          for row in USER_TROPHYWALL:
            print(row)
        generatedEmbed.set_footer(icon_url=str(ctx.author.avatar_url))
        awaited_SelectEmbed=await ctx.channel.send(embed=generatedEmbed, delete_after=120)

  except Exception as e:
    await ctx.send(
          content="Error Hit",
          embed=UM.createErrorMessage(e), delete_after=120
      )

""" Trophywall Area End """
#==============================================================================================
""" List Area """

@bot.command(aliases=['li', 'l'], name='List', description='Lists all of your fish')
async def list(ctx, *args):
  try: 
    if(D.CheckIfUserExists(ctx.author.id)==False): start(ctx)#UD.NotifyUserForRegistering(ctx); return
    

    usersFishList=D.GrabFromDB_WHERE(ctx.author.id, "USER_FISH","Fish_Name, FishNumber, Fish_Rarity, Fish_Weight", f'Discord_ID={ctx.author.id}','all');fishNumber=len(usersFishList)
    pageCount = 20; page=1
    # If the user inputs a number for the page
    #try: page=int(args[0])
    try: page=reduce(lambda a,b : a if a < b else b, [int(args[0]), math.ceil(fishNumber/pageCount)])
    # If the user DOESNT input a page number
    except: page=1

    
    pageStart = ((page - 1) * pageCount) + 1
    pageEnd = page * pageCount # Number of items per page (pageCount)
    bookEnd=math.ceil(fishNumber/20)# To round up to nearest 20
    bookStart=page
    #(fishNumber-pageEnd)%20
    print("ps:"+str(pageStart)+" pe:"+str(pageEnd)+" be:"+str(bookEnd))

    print(f"fishNumber: {fishNumber//20}\t|\tpageStart: {20*pageStart}")
    usersName=ctx.author.display_name
                                
    userFishDisplay="" #For the user's fish display
    userFishArray=[] #The array where the fish may lay peacefully
    embedColour=discord.Colour.blurple()
    try: 
      embedColour=ctx.author.colour;
      if(str(embedColour)=='#000000'): embedColour=discord.Colour.blurple()
    except: pass
    generatedEmbed=discord.Embed(title=f"__**{usersName}{UM.Str.Apostrophe(usersName)} Fish:**__", description="", color=embedColour)      
    userFishDisplay=f'`{str("Name of Fish").ljust(24," ")}`\t| `{str("Fish ID").ljust(8," ")}`\t|\t`{str("Rarity").ljust(10," ")}`\t|\t`{str("Weight (lbs)").rjust(16," ")}`'
    userFishArray.append(userFishDisplay)
    if(fishNumber>=(pageEnd)):
        pageEnd = page * pageCount #Number of itmes per page (pageCount)
        for fishLine in range(pageStart-1,pageEnd):
            #userFishDisplay=f'\n'.join(["**"+usersFishList[fishLine][0]+"** | Number: "+str(usersFishList[fishLine][1])+" | Rarity: "+usersFishList[fishLine][2]+" | Weight: "+str(usersFishList[fishLine][3])+"lbs"])
            fishName=str(usersFishList[fishLine][0])
            if(len(fishName)>24):
              fishName=str(usersFishList[fishLine][0])[:21]+"..."
            # Have trimmed name, like to 15 maybe..? with eg: fishman...
            #userFishDisplay=f'`{str(usersFishList[fishLine][0]).ljust(16," ")}`\t| Number: {str(usersFishList[fishLine][1])} | Rarity: {usersFishList[fishLine][2]} | Weight: {str(usersFishList[fishLine][3])}lbs'
            userFishDisplay=f'`{str(fishName).ljust(24," ")}`\t|\t`{str(usersFishList[fishLine][1]).ljust(8," ")}`\t|\t`{str(usersFishList[fishLine][2]).ljust(10," ")}`\t|\t`{str(usersFishList[fishLine][3]).rjust(12," ")} lbs`'
            userFishArray.append(userFishDisplay)

    ##if(fishNumber!=pageEnd):#(20*pageStart)):
    #if(fishNumber<=(20*pageStart)):
    else:
        pageEnd=int((pageStart-1)+(fishNumber%20))
        print("ye "+str(pageEnd))
        for fishLine in range(pageStart-1,int((pageStart-1)+(fishNumber%20))):
            fishName=str(usersFishList[fishLine][0])
            if(len(fishName)>24):
              fishName=str(usersFishList[fishLine][0])[:21]+"..."
            # Have trimmed name, like to 15 maybe..? with eg: fishman...
            #userFishDisplay=f'`{str(usersFishList[fishLine][0]).ljust(16," ")}`\t| Number: {str(usersFishList[fishLine][1])} | Rarity: {usersFishList[fishLine][2]} | Weight: {str(usersFishList[fishLine][3])}lbs'
            userFishDisplay=f'`{str(fishName).ljust(24," ")}`\t|\t`{str(usersFishList[fishLine][1]).ljust(8," ")}`\t|\t`{str(usersFishList[fishLine][2]).ljust(10," ")}`\t|\t`{str(usersFishList[fishLine][3]).rjust(12," ")} lbs`'
            userFishArray.append(userFishDisplay)
                                    
    #else:print("There is an error here")
                                    
    userFishDisplay='\n'.join(userFishArray)#The final step to print the list of the user's fish data
    generatedEmbed.description=str(userFishDisplay)#"**Fish Name**\n"
                            
    generatedEmbed.set_footer(text="Showing Fish:"+str(pageStart)+"-"+str(pageEnd)+" of "+str(fishNumber)+" | Page: "+str(bookStart)+" of "+str(bookEnd), icon_url=str(ctx.author.avatar_url))
    #generatedEmbed.set_footer(icon_url=str(ctx.author.avatar_url))
    await ctx.send(embed=generatedEmbed)#Returns the embedded Message
    
    
  except Exception as e:
    await ctx.send(embed=UM.createErrorMessage(e), delete_after=120)
    return


""" List Area End """
#==============================================================================================
""" Leaderboard Area """

# Have every 5-10 mins update the leaderboard, like maybe check if the time is x5 or x10 within a constant loop?
# The program will list all the user's by points and then will have the program check what place in the list the user's discord number is and that's what place they are worldwide in the leaderbaod
async def UpdateLeaderboard():
  return

@bot.command(aliases=['lb'], name='Leaderboard', description='Shows the Global Leaderboard')
async def leaderboard(ctx, *args):
  #return
  try:
    if(D.CheckIfUserExists(ctx.author.id)==False): start(ctx)#UD.NotifyUserForRegistering(ctx); return
  #NOTE: Add "fullstats"
    KEYWORDS = ['level', 'lvl', 'bal', 'balance', 'points', 'pts', 'prestige', 'totalfish', 'fishcaught', 'common', 'uncommon', 'rare', 'epic', 'legendary', 'exotic', 'ancient']
    globalKeywords=['global', '-g'] # For showing the global leaderboard for users
    
    if(len(args)!=0): 
      args = [ele.lower() for ele in args]
      isKeyword = [ele for ele in KEYWORDS if(ele in args)]
      isNotKeyword=False
      try:
        #for item in [ele for ele in args if(ele not in KEYWORDS)]: 
        for item in [ele for ele in args if(ele not in globalKeywords and ele not in KEYWORDS)]: 
          if(int(item)): pass
      except: isNotKeyword=True
      print([ele for ele in args if(ele not in globalKeywords and ele not in KEYWORDS)])
      if(isNotKeyword):
        invalidKeys = ""
        for item in [ele for ele in args if(ele not in globalKeywords and ele not in KEYWORDS)]: invalidKeys+=item.join(", ")
        generatedEmbed=discord.Embed(title=f"__{invalidKeys[1:]}__ is not a keyword", description=f"The following are keywords```fix\n{KEYWORDS}```", color=discord.Color.red())
        generatedEmbed.set_footer(text=f"For help on commands, try f.help", icon_url=str(ctx.author.avatar_url))  
        await ctx.send(embed=generatedEmbed, delete_after=30)
        return
      if(isKeyword):
        isGlobal=False # For fetching the global amount.
        if([ele for ele in globalKeywords if(ele in args)]): isGlobal=True
        print([ele for ele in KEYWORDS if(ele in args)])
        
        tableToGrab=""; orderBy=""
        if(args[0]=='level' or args[0]=='lvl'): tableToGrab = 'User_Level'; orderBy='User_Level DESC, User_Exp DESC'
        if([ele for ele in ['bal', 'balance', 'points', 'pts'] if(ele in args)]): tableToGrab = 'Current_Balance'; orderBy='Current_Balance DESC'
        if(args[0]=='prestige'): tableToGrab = 'Prestige_Count'; orderBy='Prestige_Count DESC, User_Level DESC, User_Exp DESC'
        if(args[0]=='totalfish'): tableToGrab = 'Total_Times_Fished'; orderBy='Total_Times_Fished DESC, Total_Fish_Caught DESC'
        if(args[0]=='fishcaught'): tableToGrab = 'Total_Fish_Caught'; orderBy='Total_Fish_Caught DESC, Total_Times_Fished DESC'
        if(args[0]=='common'): tableToGrab = 'Total_Common'; orderBy='Total_Common DESC, Total_Fish_Caught DESC'
        if(args[0]=='uncommon'): tableToGrab = 'Total_Uncommon'; orderBy='Total_Uncommon DESC, Total_Fish_Caught DESC'
        if(args[0]=='rare'): tableToGrab = 'Total_Rare'; orderBy='Total_Rare DESC, Total_Fish_Caught DESC'
        if(args[0]=='epic'): tableToGrab = 'Total_Epic'; orderBy='Total_Epic DESC, Total_Fish_Caught DESC'
        if(args[0]=='legendary'): tableToGrab = 'Total_Legendary'; orderBy='Total_Legendary DESC, Total_Fish_Caught DESC'
        if(args[0]=='exotic'): tableToGrab = 'Total_Exotic'; orderBy='Total_Exotic DESC, Total_Fish_Caught DESC'
        if(args[0]=='ancient'): tableToGrab = 'Total_Ancient'; orderBy='Total_Ancient DESC, Total_Fish_Caught DESC'
        

        leaderboardList=D.GrabFromDB_ALL(ctx.author.id, "USERS",f"Discord_ID, ROW_NUMBER() OVER(ORDER BY {tableToGrab} DESC) AS Rank_Number, {tableToGrab}, Private_User",'all', 'order', f'{orderBy} DESC'); print(f"\n\tUser List\n\t{leaderboardList}\n")
        amountOfUsers=len(leaderboardList)

        page=1; pageCount = 20
        # If the user inputs a number for the page (If larger than total pages, sets page to last page available)
        try: page=reduce(lambda a,b : a if a < b else b, [int(args[1]), math.ceil(amountOfUsers/pageCount)])
        # If the user DOESNT input a page number
        except: page=1
        
        usersNames=[]; dbIter=0
        for u in leaderboardList:
          if(u[3]==0): # Checks to see if user is private
            fetchUser= await bot.fetch_user(int(u[0]))
            try: fetchUser=await ctx.guild.fetch_member(int(u[0]))
            except: pass
            usersNames.append(fetchUser.name)
          else: usersNames.append("Private User")
        print(f"User's Names:\n\t{usersNames}")
        # aHighestLevel= [column[0] for column in gHighestLevel.fetchall()]
        pageStart = ((page - 1) * pageCount) + 1
        pageEnd = page * pageCount # Number of items per page (pageCount)
        bookEnd=math.ceil(amountOfUsers/20)# To round up to nearest 20
        bookStart=page
        #(fishNumber-pageEnd)%20
        print("ps:"+str(pageStart)+" pe:"+str(pageEnd)+" be:"+str(bookEnd))

        print(f"fishNumber: {amountOfUsers//20}\t|\tpageStart: {20*pageStart}")
        usersName=ctx.author.display_name
                                
        leaderboardDisplay="" #For the user's fish display
        leaderboardArray=[] #The array where the fish may lay peacefully
        embedColour=discord.Colour.blurple()
        try: 
          embedColour=ctx.author.colour;
          if(str(embedColour)=='#000000'): embedColour=discord.Colour.blurple()
        except: pass
        generatedEmbed=discord.Embed(title=f'__**Leaderboard for {str(tableToGrab).replace("_"," ")}**__', description="", color=embedColour)      
        leaderboardDisplay=f'`{str("Rank").rjust(12," ")}`\t|\t`{str("User Name").ljust(24," ")}`\t|\t`{str(str(tableToGrab).replace("_"," ")).ljust(26," ")}`'
        leaderboardArray.append(leaderboardDisplay)
        if(amountOfUsers>=(pageEnd)):
            pageEnd = page * pageCount #Number of itmes per page (pageCount)
            for lbLine in range(pageStart-1,pageEnd):
                userNameForLB=str(usersNames[lbLine])
                if(len(userNameForLB)>24):
                  userNameForLB=str(usersNames[lbLine])[:21]+"..."
                # Have trimmed name, like to 15 maybe..? with eg: fishman...
                leaderboardDisplay=f'`{str(UM.Str.Rank(leaderboardList[lbLine][1])).rjust(12," ")}`\t|\t`{str(userNameForLB).ljust(24," ")}`\t|\t`{str(UM.comma(round(leaderboardList[lbLine][2], 2))).ljust(26," ")}`'
                leaderboardArray.append(leaderboardDisplay)

        ##if(fishNumber!=pageEnd):#(20*pageStart)):
        #if(fishNumber<=(20*pageStart)):
        else:
            pageEnd=int((pageStart-1)+(amountOfUsers%20))
            print("ye "+str(pageEnd))
            for lbLine in range(pageStart-1,int((pageStart-1)+(amountOfUsers%20))):
                userNameForLB=str(usersNames[lbLine])
                if(len(userNameForLB)>24):
                  userNameForLB=str(usersNames[lbLine])[:21]+"..."
                # Have trimmed name, like to 15 maybe..? with eg: fishman...
                leaderboardDisplay=f'`{str(UM.Str.Rank(leaderboardList[lbLine][1])).rjust(12," ")}`\t|\t`{str(userNameForLB).ljust(24," ")}`\t|\t`{str(UM.comma(round(leaderboardList[lbLine][2], 2))).ljust(26," ")}`'
                leaderboardArray.append(leaderboardDisplay)
                                    
        #else:print("There is an error here")
                                    
        leaderboardDisplay='\n'.join(leaderboardArray)#The final step to print the list of the user's fish data
        generatedEmbed.description=str(leaderboardDisplay)#"**Fish Name**\n"
                            
        generatedEmbed.set_footer(text="Showing User: "+str(pageStart)+"-"+str(pageEnd)+" of "+str(amountOfUsers)+" | Page: "+str(bookStart)+" of "+str(bookEnd), icon_url=str(ctx.author.avatar_url))
        #generatedEmbed.set_footer(icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=generatedEmbed)#Returns the embedded Message



    else: # Maybe have the local by fetching all the users in a certain guild..?
      with pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=FishbotDatabase') as conn:
        conn.autocommit = True;cursor = conn.cursor();user=ctx.author.id#The user's ID
      
        grabTotalUsersFromDB=cursor.execute("""SELECT Discord_ID FROM USERS""");TOTAL_USERS=len(grabTotalUsersFromDB.fetchall())
        #gHighestLevel=cursor.execute("""SELECT Discord_ID FROM USERS ORDER BY User_Level DESC, User_Exp DESC""");highestLevel=(gHighestLevel.fetchone())[0]
        gHighestLevel=cursor.execute("""SELECT Discord_ID FROM USERS ORDER BY User_Level DESC, User_Exp DESC""");aHighestLevel= [column[0] for column in gHighestLevel.fetchall()]
        gCurrentBalance=cursor.execute("""SELECT Discord_ID FROM USERS ORDER BY Current_Balance DESC""");aCurrentBalance= [column[0] for column in gCurrentBalance.fetchall()]
        gHighestPrestige=cursor.execute("""SELECT Discord_ID FROM USERS ORDER BY Prestige_Count DESC, User_Level DESC, User_Exp DESC""");aHighestPrestige= [column[0] for column in gHighestPrestige.fetchall()]
        gTotalFishCaught=cursor.execute("""SELECT Discord_ID FROM USERS ORDER BY Total_Fish_Caught DESC, Total_Times_Fished DESC""");aMostFishCaught= [column[0] for column in gTotalFishCaught.fetchall()]
        gTotalTimesFished=cursor.execute("""SELECT Discord_ID FROM USERS ORDER BY Total_Times_Fished DESC, Total_Fish_Caught DESC""");aMostTimesFished= [column[0] for column in gTotalTimesFished.fetchall()]
        gCommonFish=cursor.execute("""SELECT Discord_ID FROM USERS ORDER BY Total_Common DESC, Total_Fish_Caught DESC""");aCommonFish= [column[0] for column in gCommonFish.fetchall()]
        gUncommonFish=cursor.execute("""SELECT Discord_ID FROM USERS ORDER BY Total_Uncommon DESC, Total_Fish_Caught DESC""");aUncommonFish= [column[0] for column in gUncommonFish.fetchall()]
        gRareFish=cursor.execute("""SELECT Discord_ID FROM USERS ORDER BY Total_Rare DESC, Total_Fish_Caught DESC""");aRareFish= [column[0] for column in gRareFish.fetchall()]
        gEpicFish=cursor.execute("""SELECT Discord_ID FROM USERS ORDER BY Total_Epic DESC, Total_Fish_Caught DESC""");aEpicFish= [column[0] for column in gEpicFish.fetchall()]
        gLegendaryFish=cursor.execute("""SELECT Discord_ID FROM USERS ORDER BY Total_Legendary DESC, Total_Fish_Caught DESC""");aLegendaryFish= [column[0] for column in gLegendaryFish.fetchall()]
        gExoticFish=cursor.execute("""SELECT Discord_ID FROM USERS ORDER BY Total_Exotic DESC, Total_Fish_Caught DESC""");aExoticFish= [column[0] for column in gExoticFish.fetchall()]
        gAncientFish=cursor.execute("""SELECT Discord_ID FROM USERS ORDER BY Total_Ancient DESC, Total_Fish_Caught DESC""");aAncientFish= [column[0] for column in gAncientFish.fetchall()]

        # The Highest percent user with least loss %( must have over 100 fish)
        #grabHighestFishPercentFromDB=cursor.execute("""SELECT Discord_ID FROM USERS ORDER BY Total_Fish_Caught DESC, Total_Fish_Caught DESC""");highestFishPercent=grabHighestFishPercentFromDB.fetchall();theIndex=str(totalCommon).split("', ), ('");rank_Common=theIndex.index(str(user));print("C_Rank: "+str(rank_Common))
      
        cursor.close()
      
        usersName=ctx.author.display_name   
        fetchUser= await bot.fetch_user(int(ctx.author.id))
        try: fetchUser=await ctx.guild.fetch_member(int(userToView))
        except: pass
        embedColour=discord.Colour.blurple()
        try: 
          embedColour=fetchUser.colour
          if(str(embedColour)=='#000000'): embedColour=discord.Colour.blurple()
        except: pass
        returnMessage=discord.Embed(title=f"{usersName}{UM.Str.Apostrophe(usersName)} Leaderboard Ranks", description="Here are your leaderboard stats.", color=embedColour)
        #returnMessage.set_thumbnail(url=ctx.author.avatar_url)
        """  Get user ID by the top user, then check if they are a private user by checking database  """
        returnMessage.add_field(name="Highest Level", value=f"```fix\nLvl:{D.GrabFromDB(ctx.author.id,'USERS','User_Level')}\n{str((UM.Str.Rank(aHighestLevel.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        returnMessage.add_field(name="Highest Prestige", value=f"```fix\nPrestige:{D.GrabFromDB(ctx.author.id,'USERS','Prestige_Count')}\n{str((UM.Str.Rank(aHighestPrestige.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        try:returnMessage.add_field(name="Most Fish w/o Miss", value=f"```fix\n{D.GrabFromDB(ctx.author.id,'USERS','Total_Fish_Caught') / D.GrabFromDB(ctx.author.id,'USERS','Total_Times_Fished')}%\n{str((UM.Str.Rank(gTotalFishCaught.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        except:returnMessage.add_field(name="Most Fish w/o Miss", value=f"```fix\nN/A```", inline=True)
        returnMessage.add_field(name="Common Caught", value=f"```fix\n{D.GrabFromDB(ctx.author.id,'USERS','Total_Common')} Fish\n{str((UM.Str.Rank(aCommonFish.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        returnMessage.add_field(name="Uncommon Caught", value=f"```fix\n{D.GrabFromDB(ctx.author.id,'USERS','Total_Uncommon')} Fish\n{str((UM.Str.Rank(aUncommonFish.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        returnMessage.add_field(name="Rare Caught", value=f"```fix\n{D.GrabFromDB(ctx.author.id,'USERS','Total_Rare')} Fish\n{str((UM.Str.Rank(aRareFish.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        returnMessage.add_field(name="Epic Caught", value=f"```fix\n{D.GrabFromDB(ctx.author.id,'USERS','Total_Epic')} Fish\n{str((UM.Str.Rank(aEpicFish.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        returnMessage.add_field(name="Legendary Caught", value=f"```fix\n{D.GrabFromDB(ctx.author.id,'USERS','Total_Legendary')} Fish\n{str((UM.Str.Rank(aLegendaryFish.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        returnMessage.add_field(name="Exotic Caught", value=f"```fix\n{D.GrabFromDB(ctx.author.id,'USERS','Total_Exotic')} Fish\n{str((UM.Str.Rank(aExoticFish.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        returnMessage.add_field(name="Ancient Caught", value=f"```fix\n{D.GrabFromDB(ctx.author.id,'USERS','Total_Ancient')} Fish\n{str((UM.Str.Rank(aAncientFish.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        returnMessage.add_field(name="Total Fish Caught", value=f"```fix\n{UM.comma(D.GrabFromDB(ctx.author.id,'USERS','Total_Fish_Caught'))} Fish\n{str((UM.Str.Rank(aMostFishCaught.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        returnMessage.add_field(name="Current Balance", value=f"```fix\n{UM.comma(round(D.GrabFromDB(ctx.author.id,'USERS','Current_Balance'),2))} pts\n{str((UM.Str.Rank(aCurrentBalance.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        #returnMessage.add_field(name="All-Time Balance", value="```fix\n"+str((number_PointsEarned[rank_PointsEarned]))+" ("+str("%d%s" % (rank_PointsEarned,"tsnrhtdd"[(math.floor(rank_PointsEarned/10)%10!=1)*(rank_PointsEarned%10<4)*rank_PointsEarned%10::4]))+")```", inline=True)
        #returnMessage.add_field(name="Times Fished", value="```fix\n"+number_TimesFished[rank_TimesFished]+" ("+str("%d%s" % (rank_TimesFished,"tsnrhtdd"[(math.floor(rank_TimesFished/10)%10!=1)*(rank_TimesFished%10<4)*rank_TimesFished%10::4]))+")```", inline=True)

        returnMessage.set_footer(text=f"Rank is out of {TOTAL_USERS} users", icon_url=str(ctx.author.avatar_url))
                            
        await ctx.send(embed=returnMessage, delete_after=30)

  except Exception as e:
    await ctx.send(embed=UM.createErrorMessage(e), delete_after=120)
    return


""" Leaderboard Area End """
#==============================================================================================
""" Badges Area """

@bot.command(aliases=['badge'], name='Badges', description="Shows your or other user's badges")
async def badges(ctx, *args):
  #return
  try:
        if(D.CheckIfUserExists(ctx.author.id)==False): start(ctx)#UD.NotifyUserForRegistering(ctx); return
  #NOTE: Add "fullstats"
        
      
        usersName=ctx.author.display_name   
        fetchUser= await bot.fetch_user(int(ctx.author.id))
        try: fetchUser=await ctx.guild.fetch_member(int(userToView))
        except: pass
        embedColour=discord.Colour.blurple()
        try: 
          embedColour=fetchUser.colour
          if(str(embedColour)=='#000000'): embedColour=discord.Colour.blurple()
        except: pass
        returnMessage=discord.Embed(title=f"{usersName}{UM.Str.Apostrophe(usersName)} Leaderboard Ranks", description="Here are your leaderboard stats.", color=embedColour)
        #returnMessage.set_thumbnail(url=ctx.author.avatar_url)
        """  Get user ID by the top user, then check if they are a private user by checking database  """
        returnMessage.add_field(name="Highest Level", value=f"```fix\nLvl:{D.GrabFromDB(ctx.author.id,'USERS','User_Level')}\n{str((UM.Str.Rank(aHighestLevel.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        returnMessage.add_field(name="Highest Prestige", value=f"```fix\nPrestige:{D.GrabFromDB(ctx.author.id,'USERS','Prestige_Count')}\n{str((UM.Str.Rank(aHighestPrestige.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        try:returnMessage.add_field(name="Most Fish w/o Miss", value=f"```fix\n{D.GrabFromDB(ctx.author.id,'USERS','Total_Fish_Caught') / D.GrabFromDB(ctx.author.id,'USERS','Total_Times_Fished')}%\n{str((UM.Str.Rank(gTotalFishCaught.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        except:returnMessage.add_field(name="Most Fish w/o Miss", value=f"```fix\nN/A```", inline=True)
        returnMessage.add_field(name="Common Caught", value=f"```fix\n{D.GrabFromDB(ctx.author.id,'USERS','Total_Common')} Fish\n{str((UM.Str.Rank(aCommonFish.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        returnMessage.add_field(name="Uncommon Caught", value=f"```fix\n{D.GrabFromDB(ctx.author.id,'USERS','Total_Uncommon')} Fish\n{str((UM.Str.Rank(aUncommonFish.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        returnMessage.add_field(name="Rare Caught", value=f"```fix\n{D.GrabFromDB(ctx.author.id,'USERS','Total_Rare')} Fish\n{str((UM.Str.Rank(aRareFish.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        returnMessage.add_field(name="Epic Caught", value=f"```fix\n{D.GrabFromDB(ctx.author.id,'USERS','Total_Epic')} Fish\n{str((UM.Str.Rank(aEpicFish.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        returnMessage.add_field(name="Legendary Caught", value=f"```fix\n{D.GrabFromDB(ctx.author.id,'USERS','Total_Legendary')} Fish\n{str((UM.Str.Rank(aLegendaryFish.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        returnMessage.add_field(name="Exotic Caught", value=f"```fix\n{D.GrabFromDB(ctx.author.id,'USERS','Total_Exotic')} Fish\n{str((UM.Str.Rank(aExoticFish.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        returnMessage.add_field(name="Ancient Caught", value=f"```fix\n{D.GrabFromDB(ctx.author.id,'USERS','Total_Ancient')} Fish\n{str((UM.Str.Rank(aAncientFish.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        returnMessage.add_field(name="Total Fish Caught", value=f"```fix\n{UM.comma(D.GrabFromDB(ctx.author.id,'USERS','Total_Fish_Caught'))} Fish\n{str((UM.Str.Rank(aMostFishCaught.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        returnMessage.add_field(name="Current Balance", value=f"```fix\n{UM.comma(round(D.GrabFromDB(ctx.author.id,'USERS','Current_Balance'),2))} pts\n{str((UM.Str.Rank(aCurrentBalance.index(ctx.author.id)+1))+' / '+str(str(TOTAL_USERS)+' Users')).center(18)}```", inline=True)
        #returnMessage.add_field(name="All-Time Balance", value="```fix\n"+str((number_PointsEarned[rank_PointsEarned]))+" ("+str("%d%s" % (rank_PointsEarned,"tsnrhtdd"[(math.floor(rank_PointsEarned/10)%10!=1)*(rank_PointsEarned%10<4)*rank_PointsEarned%10::4]))+")```", inline=True)
        #returnMessage.add_field(name="Times Fished", value="```fix\n"+number_TimesFished[rank_TimesFished]+" ("+str("%d%s" % (rank_TimesFished,"tsnrhtdd"[(math.floor(rank_TimesFished/10)%10!=1)*(rank_TimesFished%10<4)*rank_TimesFished%10::4]))+")```", inline=True)

        returnMessage.set_footer(text=f"Rank is out of {TOTAL_USERS} users", icon_url=str(ctx.author.avatar_url))
                            
        await ctx.send(embed=returnMessage, delete_after=30)

  except Exception as e:
    await ctx.send(embed=UM.createErrorMessage(e), delete_after=120)
    return


""" Badges Area End """
#==============================================================================================
""" x Area """

@bot.command(aliases=['info', 'v', 'i'], name='view', description='Lets you view fish according to name or ID')
async def view(ctx, *fish):
    tempfish=""
    for args in range(0, len(fish)):
      if((len(fish)>1) and args > 0): tempfish+=" "
      tempfish+=fish[args]
    print(tempfish)
    fish = tempfish
    try:
      fishEmbed=discord.Embed(title="empty value",description="empty value", color=discord.Color.red())
      try:
        print(int(fish))
        fish=int(fish)
        if((int(fish))):
          for item in FISH_OBJECTS:
            print(f"id: {item['FISH_ID']}\t|\t{fish} == {item['FISH_ID']}")
            if int(fish) == int(item['FISH_ID']):
                #do_something(item[fish])
                print("In")
                print("Found Fish "+str(item['Name']))
                fishEmbed = F.CreateFishViewEmbed(item)
                break
          #FISH_OBJECTS['Name']
          print("Calling fish by number")
     
      except: print("Not Int")
      try:
        if(type(fish)==str):
          for item in FISH_OBJECTS:
            print(f"item\t{item['Name'].lower()}\tid: {item['FISH_ID']}\t|\t{fish.lower()} == {item['Name'].lower()}")
            if fish.lower() == item['Name'].lower():
                #do_something(item[fish])
                print("In")
                print("Found Fish "+str(item['Name']))
                fishEmbed = F.CreateFishViewEmbed(item)
                break
          #FISH_OBJECTS['Name']
          print("Calling fish by name")
          
      except: print("Not String")
    
      await ctx.send(
          embed=fishEmbed
      )

    except Exception as e:
      await ctx.send(
          embed=UM.createErrorMessage(e), delete_after=120
      )
    

@bot.event
async def on_raw_interaction_create(ctx):
    await ctx.defer()
    print("Interaction interacted")

@bot.command()
async def dailySpin(ctx):
  try:
    if(D.CheckIfUserExists(ctx.author.id)==False): start(ctx)#await UD.NotifyUserForRegistering(ctx); return
    dailySpinAmount=D.GrabFromDB(ctx.author.id, f'USERS', f'Daily_Spin')
    dailySpinMultiplier=D.GrabFromDB(ctx.author.id, f'USERS', f'Daily_Spin_Double')
    if(dailySpinAmount==0): 
      ct = datetime.datetime.now()
      currentTime = datetime.datetime(ct.year, ct.month, ct.day, hour=ct.hour, minute=ct.minute, second=ct.second)
      future = datetime.datetime(ct.year, ct.month, ct.day, 4, 0, 0)
      difference = future - currentTime 
      
      checkRemainingHours=difference.seconds//3600; checkRemainingMins = (difference.seconds//60)%60; checkRemainingSecs=difference.seconds%60
      print(f"No Quests Available. Check back in `{difference.seconds//3600}h` `{(difference.seconds//60)%60}m` `{difference.seconds%60}s`")
      generatedEmbed=discord.Embed(title=f"Error", description=f"You have already claimed your daily wheelspin. Check back in `{difference.seconds//3600}h` `{(difference.seconds//60)%60}m` `{difference.seconds%60}s`", color=discord.Color.red())
      generatedEmbed.set_footer(text=f"Check back in {difference.seconds//3600}h {(difference.seconds//60)%60}m {difference.seconds%60}s", icon_url=str(ctx.author.avatar_url))
      await ctx.send(embed=generatedEmbed, delete_after=30)
      return
    print("Have the user spina  wheel, and whatever it lands on the user gets.")
    print("Prizes Include: Rods, Lures, Points, XP booster, Special points")
    print("Daily Spin")
    D.UpdateDB(ctx.author.id, f'USERS', f'Daily_Spin', dailySpinAmount-1)

    wheelSpinChance = [random.randint(0,360) for RNG in range(10)] # Grabs 10 random numbers ranging from 0-360

    RNGesus = random.choice(wheelSpinChance)
    #RNGesus = (dailySpinAmount%20)*18
    print(f"\tRNGesus: {RNGesus}")
    generatedEmbed=discord.Embed(title=f"{ctx.author.name}'s Daily Spin", color=discord.Color.random())
    #generatedEmbed.set_image(url=f'https://imgur.com/qhJ1Qvp')

    # Have images spin like 10 times, then slow down to the middle of the selected Pie Part
    colour=""
    if   (RNGesus >= 342): colour=("Rose")#; generatedEmbed.set_image(url=f'https://imgur.com/qhJ1Qvp')
    elif (RNGesus >= 324): colour=("Hot Pink")
    elif (RNGesus >= 306): colour=("Pink"); generatedEmbed.set_image(url=f'https://media.giphy.com/media/fSIXY9jKORcABgnOne/giphy.gif')
    elif (RNGesus >= 288): colour=("Flamingo"); generatedEmbed.set_image(url=f'https://media.giphy.com/media/7oaZOyDHhJYyUtiRS8/giphy.gif')
    elif (RNGesus >= 270): colour=("Purble"); generatedEmbed.set_image(url=f'https://media.giphy.com/media/zrhRC0iTzoGpbm2Zqd/giphy.gif')
    elif (RNGesus >= 252): colour=("Grape"); generatedEmbed.set_image(url=f'https://media.giphy.com/media/kKBYOvLKs3xjGO5CfR/giphy.gif')
    elif (RNGesus >= 234): colour=("Blue"); generatedEmbed.set_image(url=f'https://media.giphy.com/media/pJMGi6OT7Hhrpt5Ve9/giphy.gif')
    elif (RNGesus >= 216): colour=("Denim Blue")
    elif (RNGesus >= 198): colour=("Sky Blue")
    elif (RNGesus >= 180): colour=("Cyan") # Mid
    elif (RNGesus >= 162): colour=("Aquamarine") # Mid
    elif (RNGesus >= 144): colour=("Mint Green")
    elif (RNGesus >= 126): colour=("Very Green")
    elif (RNGesus >= 108): colour=("Lime Green")
    elif (RNGesus >= 90 ): colour=("Green")
    elif (RNGesus >= 72 ): colour=("Yellow-Green")
    elif (RNGesus >= 54 ): colour=("Yellow"); generatedEmbed.set_image(url=f'https://media.giphy.com/media/CehdoJgxgLYEXmH5Ec/giphy.gif')
    elif (RNGesus >= 36 ): colour=("Mango")
    elif (RNGesus >= 18 ): colour=("Orange")#; generatedEmbed.set_image(url=f'https://imgur.com/rmsDQ3B')
    else: colour=("Red") # Lucky
    print(colour)

    #makeEndImages = IC.GenerateWheelspinEnd()
    #wheelSpinMethod = IC.GenerateWheelspin(math.floor(RNGesus/20))
    
    file_WHEELSPINCHOSEN = discord.File(f'FishBot_py3.8/images/Wheelspin_Labeled/ws_{colour}.gif')
    #file_WHEELSPINEND = discord.File(f'FishBot_py3.8/images/Wheelspin_Labeled/EndImages/ws_{colour}.gif')

    #generatedEmbed=discord.Embed(title=f"{ctx.author.name}'s Daily Spin", description=f"{wheelSpinChance}\n**__{RNGesus}__\t{colour}**", color=discord.Color.random())
    #generatedEmbed=discord.Embed(title=f"{ctx.author.name}'s Daily Spin", color=discord.Color.random())
    generatedEmbed.set_image(url=f'attachment://ws_{colour}.gif') # Because GIFs from GIPHY and IMGUR loop
    awaited_GeneratedEmbed=await ctx.send(embed=generatedEmbed, file=file_WHEELSPINCHOSEN) 
    await asyncio.sleep(10)
    await awaited_GeneratedEmbed.delete()
    generatedEmbed=discord.Embed(title=f"{ctx.author.name}'s Daily Spin", description=f"{wheelSpinChance}\n**__{RNGesus}__\t{colour}**", color=discord.Color.random())

    if(colour==("Rose")):
      currBal = D.GrabFromDB(ctx.author.id, f'USERS', f'Special_Currency_Amount')
      D.UpdateDB(ctx.author.id, f'USERS', f'Special_Currency_Amount', currBal+(5*dailySpinMultiplier))
      generatedEmbed.add_field(name="Your Reward", value=f"{(5*dailySpinMultiplier)}x **Special Points**: `{currBal} -> {currBal+(5*dailySpinMultiplier)}`", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/hVz0QAC.gif')
    if(colour==("Hot Pink")):
      amountOfLures = D.GrabFromDB(ctx.author.id, f'USER_ITEM_LURE', f'Lure_Master')
      D.UpdateDB(ctx.author.id, f'USER_ITEM_LURE', f'Lure_Master', amountOfLures+(20*dailySpinMultiplier))
      generatedEmbed.add_field(name="Your Reward", value=f"{(20*dailySpinMultiplier)}x **Masterly Lures**: `{amountOfLures} -> {amountOfLures+(20*dailySpinMultiplier)}`", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/3IAQHFE.gif')
    if(colour==("Pink")):
      amountOfRods = D.GrabFromDB(ctx.author.id, f'USER_ITEM_ROD', f'Rod_Basic')
      D.UpdateDB(ctx.author.id, f'USER_ITEM_ROD', f'Rod_Basic', amountOfRods+(5*dailySpinMultiplier))
      generatedEmbed.add_field(name="Your Reward", value=f"{(5*dailySpinMultiplier)}x **Basic Rod**: `{amountOfRods} -> {amountOfRods+(5*dailySpinMultiplier)}`", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/GG58c53.gif')
    if(colour==("Flamingo")):
      grabbedQuestRefreshesFromDB = D.GrabFromDB_WHERE(ctx.author.id, 'USERS', 'Quest_Refreshes', f'Discord_ID = {ctx.author.id}')
      D.UpdateDB(ctx.author.id, tableName=f'USERS', thingToSelect=f'Quest_Refreshes', valuesToUpdate=grabbedQuestRefreshesFromDB+(1*dailySpinMultiplier))
      generatedEmbed.add_field(name="Your Reward", value=f"{(1*dailySpinMultiplier)}x **Quest Refreshes**: `{grabbedQuestRefreshesFromDB} -> {grabbedQuestRefreshesFromDB+(1*dailySpinMultiplier)}`", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/1rSkbBp.gif')
    if(colour==("Purble")):
      D.UpdateDB(ctx.author.id, f'USERS', f'Daily_Spin', dailySpinAmount+(1*dailySpinMultiplier))
      generatedEmbed.add_field(name="Your Reward", value=f"{(1*dailySpinMultiplier)}x **Free Spin**: `{dailySpinAmount} -> {dailySpinAmount+(1*dailySpinMultiplier)}`", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/VAHCbFJ.gif')
    if(colour==("Grape")):
      amountOfLures = D.GrabFromDB(ctx.author.id, f'USER_ITEM_LURE', f'Lure_Special')
      D.UpdateDB(ctx.author.id, f'USER_ITEM_LURE', f'Lure_Special', amountOfLures+(20*dailySpinMultiplier))
      generatedEmbed.add_field(name="Your Reward", value=f"{(20*dailySpinMultiplier)}x **Special Lures**: `{amountOfLures} -> {amountOfLures+(20*dailySpinMultiplier)}`", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/qhJ1Qvp.gif')
    if(colour==("Blue")):
      currExp = D.GrabFromDB(ctx.author.id, f'USERS', f'User_Exp')
      D.UpdateDB(ctx.author.id, f'USERS', f'User_Exp', currExp+(1500*dailySpinMultiplier))
      generatedEmbed.add_field(name="Your Reward", value=f"+{(1500*dailySpinMultiplier)} **Exp**: `{round(currExp,2)} -> {round(currExp+(1500*dailySpinMultiplier),2)}`", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/LBGgNWF.gif')
    if(colour==("Denim Blue")):
      amountOfLures = D.GrabFromDB(ctx.author.id, f'USER_ITEM_LURE', f'Lure_Master')
      D.UpdateDB(ctx.author.id, f'USER_ITEM_LURE', f'Lure_Master', amountOfLures+(5*dailySpinMultiplier))
      generatedEmbed.add_field(name="Your Reward", value=f"{(5*dailySpinMultiplier)}x **Masterly Lures**: `{amountOfLures} -> {amountOfLures+(5*dailySpinMultiplier)}`", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/cSZ1CPr.gif')
    if(colour==("Sky Blue")):
      amountOfLures = D.GrabFromDB(ctx.author.id, f'USER_ITEM_LURE', f'Lure_Special')
      D.UpdateDB(ctx.author.id, f'USER_ITEM_LURE', f'Lure_Special', amountOfLures+(10*dailySpinMultiplier))
      generatedEmbed.add_field(name="Your Reward", value=f"{(10*dailySpinMultiplier)}x **Special Lures**: `{amountOfLures} -> {amountOfLures+(10*dailySpinMultiplier)}`", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/opxgFQJ.gif')
    if(colour==("Cyan")):
      currBal = D.GrabFromDB(ctx.author.id, f'USERS', f'Current_Balance')
      D.UpdateDB(ctx.author.id, f'USERS', f'Current_Balance', currBal+(1500*dailySpinMultiplier))
      generatedEmbed.add_field(name="Your Reward", value=f"{(50*dailySpinMultiplier)}x **Normal Lures**: `{amountOfLures} -> {amountOfLures+(50*dailySpinMultiplier)}`", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/91ePmtU.gif')
    if(colour==("Aquamarine")):
      amountOfLures = D.GrabFromDB(ctx.author.id, f'USER_ITEM_LURE', f'Lure_Normal')
      D.UpdateDB(ctx.author.id, f'USER_ITEM_LURE', f'Lure_Normal', amountOfLures+(20*dailySpinMultiplier))
      generatedEmbed.add_field(name="Your Reward", value=f"{(20*dailySpinMultiplier)}x **Normal Lures**: `{amountOfLures} -> {amountOfLures+(20*dailySpinMultiplier)}`", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/fBvfz9m.gif')
    if(colour==("Mint Green")):
      grabbedQuestRefreshesFromDB = D.GrabFromDB_WHERE(ctx.author.id, 'USERS', 'Quest_Refreshes', f'Discord_ID = {ctx.author.id}')
      D.UpdateDB(ctx.author.id, tableName=f'USERS', thingToSelect=f'Quest_Refreshes', valuesToUpdate=grabbedQuestRefreshesFromDB+(1*dailySpinMultiplier))
      generatedEmbed.add_field(name="Your Reward", value=f"{(1*dailySpinMultiplier)}x **Quest Refreshes**: `{grabbedQuestRefreshesFromDB} -> {grabbedQuestRefreshesFromDB+(1*dailySpinMultiplier)}`", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/xnDXMT5.gif')
    if(colour==("Very Green")):
      D.UpdateDB(ctx.author.id, f'USERS', f'Daily_Spin', dailySpinAmount+(1*dailySpinMultiplier))
      generatedEmbed.add_field(name="Your Reward", value=f"Not yet implemented, have another spin", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/cFFQQqF.gif')
    if(colour==("Lime Green")):
      generatedEmbed.add_field(name="Your Reward", value="https://www.youtube.com/watch?v=abvH1f4JHmM \n https://www.youtube.com/watch?v=JfpzXrmvtEI", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/SlmfsQp.gif')
    if(colour==("Green")):
      currExp = D.GrabFromDB(ctx.author.id, f'USERS', f'User_Exp')
      D.UpdateDB(ctx.author.id, f'USERS', f'User_Exp', currExp+(2500*dailySpinMultiplier))
      generatedEmbed.add_field(name="Your Reward", value=f"+{(2500*dailySpinMultiplier)} **Exp**: `{round(currExp,2)} -> {round(currExp+(2500*dailySpinMultiplier),2)}`", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/1EoKYU3.gif')
    if(colour==("Yellow-Green")):
      amountOfLures = D.GrabFromDB(ctx.author.id, f'USER_ITEM_LURE', f'Lure_Special')
      D.UpdateDB(ctx.author.id, f'USER_ITEM_LURE', f'Lure_Special', amountOfLures+(20*dailySpinMultiplier))
      generatedEmbed.add_field(name="Your Reward", value=f"{(20*dailySpinMultiplier)}x **Special Lures**: `{amountOfLures} -> {amountOfLures+(20*dailySpinMultiplier)}`", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/EVfXQGS.gif')
    if(colour==("Yellow")):
      D.UpdateDB(ctx.author.id, f'USERS', f'Daily_Spin_Double', 2)
      D.UpdateDB(ctx.author.id, f'USERS', f'Daily_Spin', dailySpinAmount+(1*dailySpinMultiplier))
      generatedEmbed.add_field(name="Your Reward", value=f"{(1*dailySpinMultiplier)}x **Free Spin + __Double for next spin!__**: `{dailySpinAmount} -> {dailySpinAmount+(1*dailySpinMultiplier)}`", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/3hrbUf4.gif')
    if(colour==("Mango")):
      currBal = D.GrabFromDB(ctx.author.id, f'USERS', f'Current_Balance')
      D.UpdateDB(ctx.author.id, f'USERS', f'Current_Balance', currBal+(25000*dailySpinMultiplier))
      generatedEmbed.add_field(name="Your Reward", value=f"{(25000*dailySpinMultiplier)}x **Points**: `{currBal} -> {currBal+(25000*dailySpinMultiplier)}`", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/rmsDQ3B.gif')
    if(colour==("Orange")):
      amountOfLures = D.GrabFromDB(ctx.author.id, f'USER_ITEM_LURE', f'Lure_Normal')
      D.UpdateDB(ctx.author.id, f'USER_ITEM_LURE', f'Lure_Normal', amountOfLures+(50*dailySpinMultiplier))
      generatedEmbed.add_field(name="Your Reward", value=f"{(50*dailySpinMultiplier)}x **Normal Lures**: `{amountOfLures} -> {amountOfLures+(50*dailySpinMultiplier)}`", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/LteuUh0.gif')
    if(colour==("Red")):
      randomRod = str(random.choice(list(IV.GetItemValues('RODS', 'ROD', True))))[4:]
      amountOfRods = D.GrabFromDB(ctx.author.id, f'USER_ITEM_ROD', f'Rod_{randomRod}')
      D.UpdateDB(ctx.author.id, f'USER_ITEM_ROD', f'Rod_{randomRod}', amountOfRods+(1*dailySpinMultiplier))
      generatedEmbed.add_field(name="Your Reward", value=f"{1*dailySpinMultiplier}x **Random Rod**: `{randomRod} {amountOfRods} -> {amountOfRods+(1*dailySpinMultiplier)}`", inline=False)
      generatedEmbed.set_image(url=f'https://i.imgur.com/vWyfKKt.gif')

      
      
    
    #generatedEmbed.set_image(url=f'attachment://FishBot_py3.8/images/Wheelspin_Labeled/EndImages/ws_{colour}.gif')
    #awaited_GeneratedEmbed=await awaited_GeneratedEmbed.edit(embed=generatedEmbed, file=file_WHEELSPINEND) 
    if(dailySpinMultiplier!=1): D.UpdateDB(ctx.author.id, f'USERS', f'Daily_Spin_Double', 1)
    awaited_GeneratedEmbed=await ctx.send(embed=generatedEmbed, delete_after=120)#, file=file_WHEELSPINEND) 
    

  except Exception as e:
      await ctx.send(
          embed=UM.createErrorMessage(e), delete_after=120
      )
@bot.command(aliases=['milestone','lvl'], name='level', description='Lets you view your fishing level and future rewards')
async def level(ctx):
  try:
    if(D.CheckIfUserExists(ctx.author.id)==False): start(ctx)#await UD.NotifyUserForRegistering(ctx); return
    userLevel=D.GrabFromDB(ctx.author.id, 'USERS', 'User_Level'); userExp=D.GrabFromDB(ctx.author.id, 'USERS', 'User_Exp')
    userLevelUpMath=(userLevel*50)+((userLevel*50)+(userLevel*50))+50
    UM.GenerateProgressBar(userExp, userLevelUpMath,userLevel, userLevel+1)
    file_ProgressBar = discord.File("FishBot_py3.8/ImagesForTesting/progressbar.png") # The image in the same folder as the main bot file
    phoneEmbed=discord.Embed(title=f"{ctx.author.name}'s Level", description=f"Here is your level progress.\nCurrent Level:`{userLevel}`",color=discord.Color.random())
    phoneEmbed.set_image(url='attachment://progressbar.png')
    await ctx.send(embed=phoneEmbed, file=file_ProgressBar) 
  except Exception as e:
      await ctx.send(
          embed=UM.createErrorMessage(e), delete_after=120
      )

#def checkB(i: Interaction):
#    res = (i.message.id == message.id)# and (i.custom_id in self.control_labels or i.custom_id.split(" ")[1] in valid)

#    #if len(users) > 0:
#    #    res = res and i.user.id in [u1.id for u1 in users]

#    return res

#def checkM(msg: Select):
#    print(msg)
#    #if len(users) > 0:
#    #    res = msg.author.id in [u1.id for u1 in users] and msg.content.lower() in valid
#    res = msg.user.id
#    return res

@bot.command()
async def tst(ctx):
  return
  #if isinstance(result.component, component.Button):
  #  components=[my_select]
  #  print(components[0].options[0].label)  # Not None
  #  print(components[0].options[0].value)  # Not None

  #  await result.respond(components=components)
  
  #elif isinstance(result.component, component.SelectOption):
  #  print(result.component.label)  # Not None
  #  print(result.component.value) # None

  #  await result.respond(content="...")   
  message=ctx
  newTutorialObject = c_Tutorial.Tutorial(bot, 1)
  createdEmbed=UM.CreateDiscordEmbedFromDict(newTutorialObject.TutorialPages(message, newTutorialObject.page))
  awaited_TutorialEmbed = await ctx.author.send(embed=createdEmbed,
      components = [ActionRow
        (
          Button(label = "Prev Page", style=1, emoji="◀", custom_id="tutorialButton_PREV"),
          Button(label = "Next Page", style=1, emoji="▶", custom_id="tutorialButton_NEXT"),
          Button(label = "X", style=4, custom_id="tutorialButton_CLOSE")
        )
      ])

  click = client.wait_for('button_click', check=checkB, timeout=5)
  msg = client.wait_for('select_option', check=checkM, timeout=5)

  tasks = [click, msg]
  while tasks:
      try:
          print(f"Tasks: {tasks}")
          print("Waffles")
          done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
          for x in done:
              result = x.result()
              if result:
                  #if isinstance(result, Interaction):
                  if isinstance(result, Button):
                      id = result.custom_id
                      max_index = len(self.pages) - 1  # index for the last page

                      

                      await result.respond(type=7, embed=UM.createErrorMessage("EGG"), delete_after=120, components=buttons)

                      current_page_index = load_page_index

                      for future in pending:
                          future.cancel()

                      click = client.wait_for('button_click', check=checkB, timeout=5)
                      msg = client.wait_for('select_option', check=checkM, timeout=5)

                      tasks = [msg, click]
                  #elif isinstance(result, discord.message.Message):
                  elif isinstance(result, Select):
                      await self.message.delete()
                      try:
                          await result.delete()
                      except:
                          pass
                      for future in pending:
                          future.cancel()
                      return result.content
              print("Waffles")
          print("Waffles")
      except Exception as e: 
        await ctx.send(embed=UM.createErrorMessage(e), delete_after=120)
        return
      except asyncio.TimeoutError:
          
          await self.message.delete()
          return
      
  
  return

@bot.command()
async def starte(ctx):
  return
  if(False):
    selectOptionList=[]
    selectOptionObj = SelectOption(label = f"One", value=f"ValOne", description=f"Desc")
    selectOptionList.append(selectOptionObj)
    selectOptionObj = SelectOption(label = f"Two", value=f"ValTwo", description=f"Desc")
    selectOptionList.append(selectOptionObj)
        
    #Rod_Basic,Rod_Bamboo,Rod_Advanced,Rod_Fiberglass,Rod_Triple,Rod_Lucky,Rod_Masterly

    SELECT_ITEM = [ActionRow( Select(options=selectOptionList, custom_id="SELECT_ITEM", placeholder=f"Click to set your Button" ) )]

  def checkB(i: Interaction):
    res = True#(i.message.id == ctx.message.id)# and (i.custom_id in self.control_labels or i.custom_id.split(" ")[1] in valid)

    #if len(users) > 0:
    #    res = res and i.user.id in [u1.id for u1 in users]

    return res

  def checkM(msg: Select):
      print(msg)
      #if len(users) > 0:
      #    res = msg.author.id in [u1.id for u1 in users] and msg.content.lower() in valid
      res = msg.user.id == ctx.author.id
      return res

  try:
    message = ctx; userKeyString = ctx.author.id
    if(D.CheckIfUserExists(userKeyString)==False): D.CreateNewUser(userKeyString)
    
    # Skipping the question and going stright to the tutorial
    if(False):
      #UD.CreateNewUser(ctx)
      confirmationMessage=discord.Embed(title="You're All Set!", description="You're ready to go, "+str(message.author.mention)+".\nUse `fish-help` to see how to fish. For commands, use `fish-cmds`. Be sure to let Admin know if you have any problems.**Happy Fishing :)**\n~Hyper", color=discord.Color.green())
      awaitedConfirmationMessage=await ctx.author.send(embed=confirmationMessage, delete_after=20)

      tutorialQuestionMessage=discord.Embed(title="Do you want the Tutorial", description="", color=discord.Color.green())
  #    awaitedTutorialMessage=await message.channel.send(embed=tutorialQuestionMessage, delete_after=20) #have reactions to this

      awaited_tutQMessage= await ctx.author.send(
          embed=tutorialQuestionMessage, delete_after=20,
          components = [ActionRow
            (
              Button(label = "Yes", style=3, emoji="✅", custom_id="tutorialButton_CONFIRM"),
              Button(label = "No", style=4, emoji="❌", custom_id="tutorialButton_DENY")
            )
          ]
      )

      def check(res):
          return res.user.id == ctx.author.id

      try:
          res = await bot.wait_for("button_click", check=check, timeout=20)
          if res.component.custom_id!=("tutorialButton_CONFIRM") :
            print("Deleted Message")
            await awaitedConfirmationMessage.delete()
            await awaited_tutQMessage.delete()
            return
          await res.respond(content = "Welcome to Fishbot")
        
      except:
          #await message.channel.send('timed out', delete_after=5)
          await awaitedConfirmationMessage.delete()
          await awaited_tutQMessage.delete()
          return
        
      await awaitedConfirmationMessage.delete()
      await awaited_tutQMessage.delete()

    
  #await settings(ctx)
    newTutorialObject = c_Tutorial.Tutorial(bot, 1)
    createdEmbed=UM.CreateDiscordEmbedFromDict(newTutorialObject.TutorialPages(message, newTutorialObject.page))
    awaited_TutorialEmbed = await ctx.author.send(embed=createdEmbed,
        components = newTutorialObject.TutorialSubcomponents(newTutorialObject.page))
        #[ActionRow
        #  (
        #    Button(label = "Prev Page", style=1, emoji="◀", custom_id="tutorialButton_PREV"),
        #    Button(label = "Next Page", style=1, emoji="▶", custom_id="tutorialButton_NEXT"),
        #    Button(label = "X", style=4, custom_id="tutorialButton_CLOSE")
        #  )
        #])
    
    try:
        while True:

          if(False):
            click = bot.wait_for('button_click', check=checkB, timeout=5)
            msg = bot.wait_for('select_option', check=checkM, timeout=5)

            tasks = [click, msg]
          
            try:
                print(f"Tasks: {tasks}")
                print("Waffles")
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                print(done)
                if(done): print("DOne is yes")
                for x in done:
                    result = x.result()
                    if isinstance(result, Interaction):
                      try: print(f"IntID:\t{Interaction.interaction_id}")
                      except: pass
                      print(f"result.interacted_component:\n\t{result.interacted_component}")
                      print(f"result.component:\n\t{result.component}")
                      print(f"result.custom_id:\n\t{result.custom_id}")
                      if(result.custom_id=='SELECT_ITEM'):
                        print(f"result.component:\n\t{result.component[0].label}")
                        print(f"result.component:\n\t{result.component[0].value}")
                      
                      #print(f"result.interacted_component.slots:\n\t{result.interacted_component.__slots__[1]}")
                      print(f"Hi Ho\t{result}\t|\t{Interaction}")
            except: print("AHHH")
# The Working one, don;t ruin it.
          def check(resp):
              return resp.user.id == ctx.author.id

          try:
              resp = await bot.wait_for("button_click", check=check, timeout=30)
              if (resp.component.custom_id == ("tutorialButton_CLOSE")): await awaited_TutorialEmbed.delete(); break
              print("In Buttons of TUT")
              if resp.component.custom_id==("tutorialButton_NEXT") :
                SUBCOMPONENTS = newTutorialObject.TutorialPages(message, newTutorialObject.page)
                print("Hit next")
                newTutorialObject.changePage(newTutorialObject.page+1)
                createdEmbed=UM.CreateDiscordEmbedFromDict(newTutorialObject.TutorialPages(message, newTutorialObject.page))
                edited_TutorialMessageEmbed=createdEmbed
                await awaited_TutorialEmbed.edit(embed=edited_TutorialMessageEmbed)

                # This sends the Discord-API that the interaction has been received and is being "processed"
                #await resp.defer()  # Defers the thing to make no error message
                print(InteractionType)

                await resp.respond(
                            type=7,
                            embed=edited_TutorialMessageEmbed,
                            components=newTutorialObject.TutorialSubcomponents(newTutorialObject.page)
                        )
                #await resp.respond(
                #            type=7,
                #            embed=edited_TutorialMessageEmbed,
                #            components=[ActionRow
                #          (
                #            Button(label = "Prev Page", style=1, emoji="◀", custom_id="tutorialButton_PREV"),
                #            Button(label = "Next Page", style=1, emoji="▶", custom_id="tutorialButton_NEXT"),
                #            Button(label = "X", style=4, custom_id="tutorialButton_CLOSE")
                #          ),newTutorialObject.TutorialSubcomponents(newTutorialObject.page)
                #        ]
                #        )

                #await resp.respond(content="Egg")
              if resp.component.custom_id==("tutorialButton_PREV") :
                print("Hit prev")
                newTutorialObject.changePage(newTutorialObject.page-1)
                createdEmbed=UM.CreateDiscordEmbedFromDict(newTutorialObject.TutorialPages(message, newTutorialObject.page))
                edited_TutorialMessageEmbed=createdEmbed
                await awaited_TutorialEmbed.edit(embed=edited_TutorialMessageEmbed)
                #await resp.defer()  # Defers the thing to make no error message
                await resp.respond(
                            type=7,
                            embed=edited_TutorialMessageEmbed,
                            components=newTutorialObject.TutorialSubcomponents(newTutorialObject.page)
                            #[ActionRow
                            #  (
                            #    Button(label = "Prev Page", style=1, emoji="◀", custom_id="tutorialButton_PREV"),
                            #    Button(label = "Next Page", style=1, emoji="▶", custom_id="tutorialButton_NEXT"),
                            #    Button(label = "X", style=4, custom_id="tutorialButton_CLOSE")
                            #  )
                            #]
                        )
                #await resp.respond(content='error description', hidden=False,delete_after=0.1)
              
              # The Shopping page (have select as well)
                #res = await bot.wait_for("select_option", check=check, timeout=30)
                #arg_ItemName=res.component[0].label
                
          except Exception as e:
              print(f"Exc: {e}")
              await message.channel.send('Happy Fishing', delete_after=5)
              await awaited_TutorialEmbed.delete()
              return
        
    except:
        await message.channel.send('Happy Fishing', delete_after=5)
        await awaited_TutorialEmbed.delete()
        return
    
  except Exception as e:
    await ctx.send(
        embed=UM.createErrorMessage(e), delete_after=120
    )

@bot.command()
async def start(ctx):
  message = ctx; userKeyString = ctx.author.id
  if(D.CheckIfUserExists(userKeyString)==False): D.CreateNewUser(userKeyString)
  def checkB(i: Interaction):
    return i.user.id == ctx.author.id

  def checkM(msg: Select):
      res = msg.user.id == ctx.author.id
      return res

  try:
    message = ctx; userKeyString = ctx.author.id
    if(D.CheckIfUserExists(userKeyString)==False): D.CreateNewUser(userKeyString)
    
   
    newTutorialObject = c_Tutorial.Tutorial(bot, 1)
    createdEmbed=UM.CreateDiscordEmbedFromDict(newTutorialObject.TutorialPages(message, newTutorialObject.page))
    awaited_TutorialEmbed = await ctx.author.send(embed=createdEmbed, components = newTutorialObject.TutorialSubcomponents(newTutorialObject.page))
    
    try:
        while True:

          if(True):
            click = bot.wait_for('button_click', check=checkB, timeout=30)
            msg = bot.wait_for('select_option', check=checkM, timeout=30)

            tasks = [click, msg]
          
            #try:
            print(f"Tasks: {tasks}")
            print("Waffles")
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            print(done)
            if(done): print("DOne is yes")
            for x in done:
              result = x.result()
              if isinstance(result, Interaction):
                #try: print(f"IntID:\t{Interaction.interaction_id}")
                #except: pass
                #print(f"result.interacted_component:\n\t{result.interacted_component}")
                #print(f"result.component:\n\t{result.component}")
                #print(f"result.custom_id:\n\t{result.custom_id}")
                if(result.custom_id=='SELECT_ITEM'):
                  #print(f"result.component:\n\t{result.component[0].label}")
                  #print(f"result.component:\n\t{result.component[0].value}")
                  print(int((result.component[0].value)[-1]))
                  newTutorialObject.changePage(int((result.component[0].value)[-1]))
                  createdEmbed=UM.CreateDiscordEmbedFromDict(newTutorialObject.TutorialPages(message, newTutorialObject.page))
                  edited_TutorialMessageEmbed=createdEmbed
                  await awaited_TutorialEmbed.edit(embed=edited_TutorialMessageEmbed)
                  await result.respond(
                            type=7,
                            embed=edited_TutorialMessageEmbed,
                            components=newTutorialObject.TutorialSubcomponents(newTutorialObject.page)
                        )
              resp = result        
              if (resp.custom_id == ("tutorialButton_CLOSE")): 
                await awaited_TutorialEmbed.delete(); return
              print("In Buttons of TUT")
              if resp.custom_id==("tutorialButton_NEXT") :
                SUBCOMPONENTS = newTutorialObject.TutorialPages(message, newTutorialObject.page)
                print("Hit next")
                newTutorialObject.changePage(newTutorialObject.page+1)
                createdEmbed=UM.CreateDiscordEmbedFromDict(newTutorialObject.TutorialPages(message, newTutorialObject.page))
                edited_TutorialMessageEmbed=createdEmbed
                await awaited_TutorialEmbed.edit(embed=edited_TutorialMessageEmbed)

                # This sends the Discord-API that the interaction has been received and is being "processed"
                #await resp.defer()  # Defers the thing to make no error message
                print(InteractionType)

                await resp.respond(
                            type=7,
                            embed=edited_TutorialMessageEmbed,
                            components=newTutorialObject.TutorialSubcomponents(newTutorialObject.page)
                        )
                #await resp.respond(
                #            type=7,
                #            embed=edited_TutorialMessageEmbed,
                #            components=[ActionRow
                #          (
                #            Button(label = "Prev Page", style=1, emoji="◀", custom_id="tutorialButton_PREV"),
                #            Button(label = "Next Page", style=1, emoji="▶", custom_id="tutorialButton_NEXT"),
                #            Button(label = "X", style=4, custom_id="tutorialButton_CLOSE")
                #          ),newTutorialObject.TutorialSubcomponents(newTutorialObject.page)
                #        ]
                #        )

                #await resp.respond(content="Egg")
              if resp.custom_id==("tutorialButton_PREV") :
                print("Hit prev")
                newTutorialObject.changePage(newTutorialObject.page-1)
                createdEmbed=UM.CreateDiscordEmbedFromDict(newTutorialObject.TutorialPages(message, newTutorialObject.page))
                edited_TutorialMessageEmbed=createdEmbed
                await awaited_TutorialEmbed.edit(embed=edited_TutorialMessageEmbed)
                #await resp.defer()  # Defers the thing to make no error message
                await resp.respond(
                            type=7,
                            embed=edited_TutorialMessageEmbed,
                            components=newTutorialObject.TutorialSubcomponents(newTutorialObject.page))
                           
                
          #except Exception as e:
          #    print(f"Exc: {e}")
          #    await message.channel.send('Happy Fishing', delete_after=5)
          #    await awaited_TutorialEmbed.delete()
          #    return
        
    except Exception as e:
        print(f"Exc: {e}")
        await message.channel.send('Happy Fishing', delete_after=5)
        await awaited_TutorialEmbed.delete()
        return
    
  except Exception as e:
    await ctx.send(
        embed=UM.createErrorMessage(e), delete_after=120
    )

@bot.event
async def on_command_error(ctx, error):
    try: 
      if(type(int(ctx.message.content)) in [int,float]): return
    except: pass
    
    # find what in quotes
    findErrorInQuotes = str(error).split('"')
    #print(str(findErrorInQuotes[1]))
    try: 
      if(str(findErrorInQuotes[1]).lower() == 'max'): return
    except: pass
    try:
      print("Err: "+str(findErrorInQuotes[1]))
    except: pass
    
    await ctx.send(
        embed=UM.createErrorMessage(error), delete_after=120
    )
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing a required argument.  Do >help")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the appropriate permissions to run this command.")
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I don't have sufficient permissions!")
    else:
        print("error not caught")
        print(error) 



#fish = commands.Bot(command_prefix='', ignore_extra=False, case_insensitive=True)
#@fish.command()
#async def fish(ctx):
#  print("You're now fishing")
@bot.command()
async def testfish(ctx):
  await ctx.channel.send("Not in service"); return
  try:
    fishedFish = F.GrabFishFromRarity("Exotic",FISH_OBJECTS_SBRarity[5])
    generatedFish=F.GenerateNewUserFish(fishedFish, False, ctx)
  
    fishEmbed=F.CreateFishEmbed(generatedFish, False, ctx)
    #IMG.GenerateFishOutputImage(generatedFish)
  
    fishEmbed.set_image(url='attachment://generatedFishStatsImage.png')
    #fishEmbed.set_image(url='attachment://pillow_imagedrawe.gif')
    fishEmbed.color=generatedFish['RarityColour']
    #file_Fish = discord.File("FishBot_py3.8\\ImagesForTesting\\fbLayout.png") # The image in the same folder as the main bot file
    file_Fish = discord.File("FishBot_py3.8\\ImagesForTesting\\generatedFishStatsImage.png") # The image in the same folder as the main bot file
    #file_Fish = discord.File("FishBot_py3.8\ImagesForTesting\pillow_imagedrawe.gif") # The image in the same folder as the main bot file
    #awaited_EmbedData=await message.channel.send(embed=embedData, file=file_Fish, delete_after=8)
    await ctx.send(
          embed=fishEmbed,file=file_Fish
    )
  except Exception as e:
    await ctx.send(
        embed=UM.createErrorMessage(e), delete_after=120
    )

@bot.command(aliases=['cl','chgl'])
async def changelog(ctx):
  print("Opening Changelog")
  print("Please include buffs of items and fish andwhatnot. Thanks :)")

import c_Fishipedia as FPDA
@bot.command()
async def fishipedia(ctx, *args):
  try: await FPDA.Fishipedia(ctx, args)
  except: await FPDA.Fishipedia(ctx)
  return

@bot.command(aliases=fishLanguages)
#@commands.cooldown(1, userKey['USER']['IsFishing'], commands.BucketType.user)
@commands.cooldown(1, 6, commands.BucketType.user)
async def fish(ctx):
  try:
    # Grabs the user's Key from the database set
    userKeyString=ctx.author.id
    if(D.CheckIfUserExists(userKeyString)==False): start(ctx)#await UD.NotifyUserForRegistering(ctx); return
    if(userKeyString in usersFishing): 
      try: await ctx.message.delete()
      except: pass
      return
    if(False):usersFishing.append(userKeyString)

    # check_IsChannelFishing(ctx)


    #selectedLure = userKey['ITEMS']['Current_Lure']
    selectedLure = D.GrabFromDB(ctx.author.id, 'USER_ITEM_LURE','Current_Lure')

    # Test against the amount of lures the user has (might want to put near bottom incase of error to prevent data loss)
    #remainingLures = userKey['ITEMS']['LURES'][selectedLure]['Amount']
    remainingLures = D.GrabFromDB(ctx.author.id, 'USER_ITEM_LURE',f'Lure_{selectedLure}')

    print(f"\nLURES:\n\tLure:\t{selectedLure} : {remainingLures}")

    if (remainingLures<1): raise Exception(f"_outOfLures(). please use `{prefixes}start` to get more lures"); return
    currentRegion=D.GrabFromDB(ctx.author.id, 'USER_ITEM_REGION','Current_Region')

    timesFished=D.GrabFromDB(ctx.author.id, 'USERS','Total_Times_Fished')
    D.UpdateDB(ctx.author.id, f'USERS', f'Total_Times_Fished', timesFished+1)

    #userKey['USER']['IsFishing']=10
    #print(f"\tFishing Time: \t{userKey['USER']['IsFishing']}")
    awaited_fishButton= await ctx.send(
        content="You begin to fish.", delete_after=20,
        components = [ActionRow ( Button(style=2, emoji="🐟", custom_id="fishButton") ) ]
    )

    fishWaitTime=random.uniform(3,8) #For the random fish time
    await asyncio.sleep(fishWaitTime)
    awaited_caughtFishButton = await awaited_fishButton.edit(
      content="You feel a tugging at your line...",
      components = [ActionRow
          (
            Button(style=1, emoji="🎣", custom_id="fishButton")
          )
        ]
    )

    # Grab Rod while fish is loading
    currentRod=D.GrabFromDB(ctx.author.id, 'USER_ITEM_ROD','Current_Rod')

    def emj(res):
      #return (res.user.id)
      return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

    try:
        res = await bot.wait_for("button_click", check=emj, timeout=4)       
        await awaited_fishButton.delete()       
        
    except:
        print("No")
        await awaited_fishButton.delete()
        if(False):usersFishing.remove(userKeyString)
        # Resets the user's streak
        D.UpdateDB(ctx.author.id, f'USERS', f'Highest_Fish_Count', 0)
        return

    if(False):usersFishing.remove(userKeyString)
    
    # Have Baubles, Luck Boosters, and Prestige Boosts here, and if any are luck boosters, have them applied here
    # Note: Regions

    # Roll random number
    percentRarity=random.uniform(1,100)
    percentSecondaryRarity=random.randint(1,20)#For the ancient or smthn.
    isAncient=False

    # Adds one to the user's streak
    fishStreak=D.GrabFromDB(ctx.author.id, 'USERS','Highest_Fish_Count')
    D.UpdateDB(ctx.author.id, f'USERS', f'Highest_Fish_Count', fishStreak+1)

    currentBait=D.GrabFromDB(ctx.author.id, 'USER_ITEM_BAIT','Current_Bait')
    
    totalFishCaught=D.GrabFromDB(ctx.author.id, 'USERS','Total_Fish_Caught')
    D.UpdateDB(ctx.author.id, f'USERS', f'Total_Fish_Caught', totalFishCaught+1)

    # Removes a lure from the amount
    #userKey['ITEMS']['LURES'][selectedLure]['Amount'] = remainingLures-1
    D.UpdateDB(ctx.author.id, 'USER_ITEM_LURE', f'Lure_{selectedLure}', remainingLures-1)

    fishedFish, isAncient = F.DetermingFishingVariables(ctx, currentRegion, currentRod, currentBait, percentRarity, percentSecondaryRarity, FISH_OBJECTS_SBRarity)

    if(False):
      fishedFish={}
      if(percentRarity>=0 and percentRarity<=50):
        print("Common Fish")
        fishedFish = F.GrabFishFromRarity("Common", FISH_OBJECTS_SBRarity[0])
      elif(percentRarity>50 and percentRarity<=75):
        print("Uncommon Fish")
        fishedFish = F.GrabFishFromRarity("Uncommon",FISH_OBJECTS_SBRarity[1])
      elif(percentRarity>75 and percentRarity<=90):
        print("Rare Fish")
        fishedFish = F.GrabFishFromRarity("Rare",FISH_OBJECTS_SBRarity[2])
      elif(percentRarity>90 and percentRarity<=97.5):
        print("Epic Fish")
        fishedFish = F.GrabFishFromRarity("Epic",FISH_OBJECTS_SBRarity[3])
      elif(percentRarity>97.5 and percentRarity<=99):
        print("Legendary Fish")
        fishedFish = F.GrabFishFromRarity("Legendary",FISH_OBJECTS_SBRarity[4])
      elif(percentRarity>99 and percentRarity<=110):
        print("Exotic Fish")
        fishedFish = F.GrabFishFromRarity("Exotic",FISH_OBJECTS_SBRarity[5])
      else:
        print("Rare Fish [OVERFLOW]")
        fishedFish = F.GrabFishFromRarity(FISH_OBJECTS_SBRarity[2])
    
      if percentSecondaryRarity==6:#Ancient
        isAncient=True
    
    generatedFish=F.GenerateNewUserFish(fishedFish, isAncient, ctx)
    #print(f"\n Generated Fish:\t{str(generatedFish)}")
    fishEmbed=F.CreateFishEmbed(generatedFish, isAncient, ctx)
    print(generatedFish['RarityColour'])   
    
    # For no image
    doImage=False
    if(doImage):
      IMG.c_GenerateFishImage.GenerateFishAnimation(str(generatedFish['Name']))
      imageMode="Standard"
      if(imageMode=="Standard"):
        fishEmbed.set_image(url='attachment://pillow_imagedrawe.gif')
        file_Fish = discord.File("FishBot_py3.8\ImagesForTesting\pillow_imagedrawe.gif") # The image in the same folder as the main bot file
      else:
        #IMG.GenerateFishOutputImage(generatedFish)
        fishEmbed.set_image(url='attachment://generatedFishStatsImage.png')
        file_Fish = discord.File("FishBot_py3.8\\ImagesForTesting\\generatedFishStatsImage.png") # The image in the same folder as the main bot file
    fishEmbed.color=generatedFish['RarityColour']
    
    
    #awaited_EmbedData=await message.channel.send(embed=embedData, file=file_Fish, delete_after=8)
    await ctx.send(
          embed=fishEmbed#,file=file_Fish
    )

    # Checks the fish quests that the User has.
    checkFish = Q.CheckQuestReqs_FISH(ctx, generatedFish)
    if(checkFish!=None):
      #completedQuests = str(str(checkFish).replace("[", "")).replace("]","")
      completedQuests = UM.Str.ConvertListToItem(checkFish)
      k = completedQuests.rfind(",")
      completedQuests = completedQuests[:k] + " and" + completedQuests[k+1:]
      isAre=UM.Str.IsAre(checkFish)
      
      embed = discord.Embed(title=f"✨Quest{UM.Str.Plural(checkFish)} Complete!✨", description=f"Quest{UM.Str.Plural(checkFish)} **{completedQuests}** {isAre} complete. Claim your reward{UM.Str.Plural(checkFish)} before the reset. ```fix\n{prefixes} quest claim #```",color=discord.Color.dark_gold())
      await ctx.send(embed=embed)
  except Exception as e:
      await ctx.send(
          embed=UM.createErrorMessage(e), delete_after=120
      )

if(False):
  slash = SlashCommand(bot, sync_commands=False, sync_on_cog_reload=False)

  bot.load_extension("cog")

  @slash.slash(name="fish", description="You start fishing")
  async def _fish(ctx: SlashContext):
      await fish(ctx)
    

  @slash.slash(name="testFish", description="Sends a test message.")
  async def _testFish(ctx: SlashContext):
      embed = discord.Embed(title="Here's an embed.",
                            color=0xeb4034)
      await ctx.send(3, content="This is a test. Only you can see this.",
                     embeds=[embed], hidden=True)



#import requests


#url = "https://discord.com/api/v8/applications/<my_application_id>/commands"

#json = {
#    "name": "blep",
#    "description": "Send a random adorable animal photo",
#    "options": [
#        {
#            "name": "animal",
#            "description": "The type of animal",
#            "type": 3,
#            "required": True,
#            "choices": [
#                {
#                    "name": "Dog",
#                    "value": "animal_dog"
#                },
#                {
#                    "name": "Cat",
#                    "value": "animal_cat"
#                },
#                {
#                    "name": "Penguin",
#                    "value": "animal_penguin"
#                }
#            ]
#        },
#        {
#            "name": "only_smol",
#            "description": "Whether to show only baby animals",
#            "type": 5,
#            "required": False
#        }
#    ]
#}

# For authorization, you can use either your bot token
#headers = {
#    "Authorization": os.environ['discordBotID']
#}

## or a client credentials token for your app with the applications.commands.update scope
#headers = {
#    "Authorization": "Bearer abcdefg"
#}

#r = requests.post(url, headers=headers, json=json)

#@client.event
#async def on_message(message):
#  print(str(message))
#  if (str(message.channel) in fishLanguages or str(message.channel)== "fishing-area"):
#    message.content=message.content.lower() # Converts all the words to lower case
#    
#    if(message.content in fishLanguages): # Checks the words in different languages for the word "fish"
#      user=message.author.id
#      print("User "+str(user)+" said "+str(message.content))
#    
#  else: return

#import pprint
#env_var = os.environ
 
## Print the list of user's
## environment variables
#print("User's Environment variable:")
#pprint.pprint(dict(env_var), width = 1)

os.environ['stingrayBotID'] = '<secret>'
os.environ['FishBotID'] = '<secret>'
bot.run(os.environ['FishBotID'])
#bot.run(os.environ['stingrayBotID'])