import discord
import asyncio
import datetime
import c_UtilityMethods as UM, c_Database as D, c_ItemValues as IV
#from replit import db

def GrabRodValues():
  rodValues=[]
  
  return rodValues

# You only have to call this method once; Call this method at the start of the program.
# For a new object, copy this instance from the original created method
def ShopItems(ctx):
    usersName=ctx.author
    try:
      usersName=ctx.author.nick
    except: pass
    #USERKEYS = db.keys(); userKeyString = "U"+str(ctx.author.id); userKey=db[userKeyString]
    

    menuItemsArray={
        'Page':{
          'Menu':{
            'Aliases':['Rod','rods', 'rod', 'r'],
            'Header':
              {'title':f"═══════ **Happy {UM.GetDateName()}, {usersName}** ═══════", 
              'description':"Welcome to the Fish Shop. You can buy rods, lures, ~~regions~~, ~~or even boats~~. To view a category, use `fish-shop <category>`. To buy, use `fish-buy <category> <item> <amount>`",
              'color':discord.Color.dark_gold()
              }, 
            'Fields':[{'name':"🐟 Fishing Rods", 'value':"""```fix\nHas all your fishing (rod) needs. [fish-shop rods]```[Hover for details](https://google.com "Basic Fishing Commands.\nX amount of commands")""",'inline':False},
                      {'name':"🇱 Lures", 'value':"""```fish-cmds a```[Hover for details](https://google.com "Commands for those who like to get technical.\nX amount of commands")""",'inline':True},
                      {'name':"~~🇷 Regions~~", 'value':"""```diff\n-Coming Soon```[Hover for details](https://google.com "You like spending your money?\nX amount of commands")""",'inline':True},
                      {'name':"~~🛶 Boats~~", 'value':"""```diff\n-Coming Soon```[Hover for details](https://google.com "Gives you a random hint.\nX amount of commands")""",'inline':True},
                      {'name':"🇩 Daily Deals", 'value':f"""```{UM.GetDateName()} : fish-daily```[Hover for details](https://google.com "Modify or view your settings.\nX amount of commands")""",'inline':True},
                      {'name':"🇼 Weekly Deals", 'value':f"""```diff\n-Coming Soon\n{str(UM.GetDateMonthName("WeekStart"))} - {str(UM.GetDateMonthName("WeekEnd"))}```[Hover for details](https://google.com "[Server Admins Only] Configuration for the server.\nX amount of commands")""",'inline':True},
                      {'name':"❔ What's New", 'value':"""```Fishbot 3.8 build: 062921```[Hover for details](https://github.com/Hyperactvty/fishbot/blob/main/README.md "The Changelog")""",'inline':True},
                      {'name':"🛠 Support the Creator", 'value':"""Also if you want to support the bot creator, click [here](https://www.patreon.com/hyperactvty).""",'inline':True},
                      {'name':"❌ Close Menu", 'value':"""Closes the menu""",'inline':True}], 
            'Footer':{'text':f"""If you require help, feel free to join the [server here](https://discord.gg/kg6Zw8sRjX "Click to join the discord!")""", 'icon_url':f'{ctx.author.avatar_url}'},
            'Emojis': ['🐟','🐠','🛒','❔','🛠','⚙','❌'],
            'Pages': 1, 'CurrentPage':1},
          'Rod':{
            'Aliases':['Rod','rods', 'rod', 'r'],
            'Header':
              {'title':f"═══════ **Rods** ═══════", 
              'description':"To buy **Rods**, use `fish-buy rods <item> <amount || max>`\n*Note: Rods __do__ stack on top of each other for better score*",
              'color':str(discord.Color.dark_gold())
              }, 
            'Fields':[{'name':"1️⃣ Basic", 'value':f"""```bash\n${round(D.GrabFromDB(ctx.author.id, 'USER_ITEM_ROD','Rod_Basic')*100,2)+100}/ rod```"""},
                      {'name':"2️⃣ Bamboo", 'value':f"""```bash\n${round(D.GrabFromDB(ctx.author.id, 'USER_ITEM_ROD','Rod_Bamboo')*2500,2)+2500}/ rod```"""},
                      {'name':"3️⃣ Advanced", 'value':f"""```bash\n${round(D.GrabFromDB(ctx.author.id, 'USER_ITEM_ROD','Rod_Advanced')*7500,2)+7500}/ rod```"""},
                      {'name':"4️⃣ Fiberglass", 'value':f"""```bash\n${round(D.GrabFromDB(ctx.author.id, 'USER_ITEM_ROD','Rod_Fiberglass')*15000,2)+15000}/ rod```"""},
                      {'name':"5️⃣ Triple", 'value':f"""```bash\n${round(D.GrabFromDB(ctx.author.id, 'USER_ITEM_ROD','Rod_Triple')*33333,2)+33333}/ rod```"""},
                      {'name':"6️⃣ Lucky", 'value':f"""```bash\n${round(D.GrabFromDB(ctx.author.id, 'USER_ITEM_ROD','Rod_Lucky')*77777,2)+77777}/ rod```"""},
                      {'name':"7️⃣ Masterly", 'value':f"""```bash\n${round(D.GrabFromDB(ctx.author.id, 'USER_ITEM_ROD','Rod_Masterly')*1250000,2)+1250000}/ rod```"""},
                      {'name':"❌", 'value':"""```fix\nCloses the menu```"""}], 
            'Footer':"""If you require help, feel free to join the [server here](https://discord.gg/kg6Zw8sRjX) "Click to join the discord!" """,
            'Emojis': ['🐟','🐠','🛒','❔','🛠','⚙','❌'],
            'Pages': 1, 'CurrentPage':1},
          }
        }
    return menuItemsArray


def CreateShopFromDict(ctx, arg_ItemType):
  itemsInCategory = IV.GetItemValues(f'{str(arg_ItemType).upper()}S', 'None', True)
  ic= itemsInCategory
  print(ic)

  fields=UM.CreateFieldFromDict(ic,str(arg_ItemType).upper(),ctx)

  SHOPTEMPLATE = {
            'Header':
              {'title':f"═══════ **{str(arg_ItemType).upper()}S** ═══════", 
              'description':"To buy **Rods**, use `fish-buy rods <item> <amount || max>`\n*Note: Rods __do__ stack on top of each other for better score*",
              'color':str(discord.Color.dark_gold())
              }, 
            'Fields':fields,
                       
            'Footer':"""If you require help, feel free to join the [server here](https://discord.gg/kg6Zw8sRjX) "Click to join the discord!" """,
            'Pages': 1, 'CurrentPage':1}
  return SHOPTEMPLATE