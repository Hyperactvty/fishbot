# The Imports
import discord
import asyncio

# You only have to call this method once; Call this method at the start of the program.
# For a new object, copy this instance from the original created method
def MenuItems():
    page=1
    menuItemsArray=[
        {'Page':['Menu', 'm', 'menu', 'home'], 
                    'Header':
                      {'title':"═══════ **Fishbot Menu** ═══════", 
                       'description':"Click on the reaction to go the page",
                       'color':str(discord.Color.dark_gold())
                       }, 
                    'Fields':[{'name':"🐟 Basic Commands", 'value':"""`fish-cmds b`\n[Hover for details](https://google.com "Basic Fishing Commands.\nX amount of commands")"""},
                              {'name':"🐠 Advanced Commands", 'value':"""`fish-cmds a`\n[Hover for details](https://google.com "Commands for those who like to get technical.\nX amount of commands")"""},
                              {'name':"🛒 Shop", 'value':"""`fish-shop`\n[Hover for details](https://google.com "You like spending your money?\nX amount of commands")"""},
                              {'name':"❔ Hints", 'value':"""`fish-hint`\n[Hover for details](https://google.com "Gives you a random hint.\nX amount of commands")"""},
                              {'name':"🛠 Settings", 'value':"""`fish-settings`\n[Hover for details](https://google.com "Modify or view your settings.\nX amount of commands")"""},
                              {'name':"⚙ Config", 'value':"""`fish-config`\n[Hover for details](https://google.com "[Server Admins Only] Configuration for the server.\nX amount of commands")"""},
                              {'name':"❌ Close Menu", 'value':"""Closes the menu"""}], 
                    'Footer':"""If you require help, feel free to join the [server here](https://discord.gg/kg6Zw8sRjX) "Click to join the discord!" """,
                    'Emojis': ['🐟','🐠','🛒','❔','🛠','⚙','❌'],
                    'Pages': 1, 'CurrentPage':1}, 
        {'Page':['B_Commands', 'cmds b', 'commands b', 'cmds'], 
                    'Header':
                      {'title':"═══════ **Basic Fishbot Commands** ═══════", 
                       'description':"\"*Fish are friends, not food.*\"\nClick the emoji for a detailed view.\n__**Here are some basic commands**__",
                       'color':str(discord.Color.green())
                       }, 
                    'Fields':[{'name':"🐟 `fish-start`", 'value':"""    -    Lets you start your fishing journey [**TUTORIAL DOES NOT WORK**]"""},
                              {'name':"🎣 `fish`", 'value':"""\t\t-    You start fishing"""},
                              {'name':"`fish-help`", 'value':"""\t\t-\t\tBring up the help section"""},
                              {'name':"`fish-cmds`", 'value':"""\t\t-\t\tBrings up the commands used for Fishbot"""},
                              {'name':"`fish-lb`", 'value':"""\t\t-\t\tShows the leaderboard"""},
                              {'name':"`fish-list {#}`", 'value':"""\t\t-    Shows all your fish in a neat list."""},
                              {'name':"`fish-show {fish_ID}`", 'value':"""\t\t-    Shows the data of the fish specified"""},
                              {'name':"`fish-list {#}`", 'value':"""\t\t-    Shows all your fish in a neat list."""},
                              {'name':"`fish-list {#}`", 'value':"""\t\t-    Shows all your fish in a neat list."""},
                              {'name':"`fish-list {#}`", 'value':"""\t\t-    Shows all your fish in a neat list."""}], 
                    'Footer':"Page "+str(page)+"/1 | Showing items 1-10 : 10 | 10 per page",
                    'Emojis': ['🏠','🐟','🎣'],
                    'Pages': 1, 'CurrentPage':1}, 
        {'Page':['A_Commands', 'cmds a', 'commands a'],
                    'Header':
                      {'title':"═══════ **Advanced Fishbot Commands** ═══════", 
                       'description':"\"*Fish are friends, not food.*\"\nClick the emoji for a detailed view.\n__**Here are some advanced commands**__",
                       'color':str(discord.Color.green())
                       }, 
                    'Fields':[{'name':"🐟 `fish-start`", 'value':"""    -    Lets you start your fishing journey [**TUTORIAL DOES NOT WORK**]"""},
                              {'name':"🎣 `fish`", 'value':"""\t\t-    You start fishing"""},
                              {'name':"`fish-help`", 'value':"""\t\t-\t\tBring up the help section"""},
                              {'name':"`fish-cmds`", 'value':"""\t\t-\t\tBrings up the commands used for Fishbot"""},
                              {'name':"`fish-lb`", 'value':"""\t\t-\t\tShows the leaderboard"""},
                              {'name':"`fish-list {#}`", 'value':"""\t\t-    Shows all your fish in a neat list."""},
                              {'name':"`fish-show {fish_ID}`", 'value':"""\t\t-    Shows the data of the fish specified"""},
                              {'name':"`fish-list {#}`", 'value':"""\t\t-    Shows all your fish in a neat list."""},
                              {'name':"`fish-list {#}`", 'value':"""\t\t-    Shows all your fish in a neat list."""},
                              {'name':"`fish-list {#}`", 'value':"""\t\t-    Shows all your fish in a neat list."""}], 
                    'Footer':"Page "+str(page)+"/1 | Showing items 1-10 : 10 | 10 per page",
                    'Emojis': ['🏠','🐟','🎣'],
                    'Pages': 1, 'CurrentPage':1}, 
        {'Page':['Shop', 's', 'shop', 'store'],
                    'Header':
                      {'title':"═══════ **Points Shop** ═══════", 
                       'description':"\"*Fish are friends, not food.*\"\nClick the emoji for a detailed view.\n__**Here are some basic commands**__",
                       'color':str(discord.Color.green())
                       }, 
                    'Fields':[{'name':"🐟 `fish-start`", 'value':"""    -    Lets you start your fishing journey [**TUTORIAL DOES NOT WORK**]"""},
                              {'name':"🎣 `fish`", 'value':"""\t\t-    You start fishing"""},
                              {'name':"`fish-help`", 'value':"""\t\t-\t\tBring up the help section"""},
                              {'name':"`fish-cmds`", 'value':"""\t\t-\t\tBrings up the commands used for Fishbot"""},
                              {'name':"`fish-lb`", 'value':"""\t\t-\t\tShows the leaderboard"""},
                              {'name':"`fish-list {#}`", 'value':"""\t\t-    Shows all your fish in a neat list."""},
                              {'name':"`fish-show {fish_ID}`", 'value':"""\t\t-    Shows the data of the fish specified"""},
                              {'name':"`fish-list {#}`", 'value':"""\t\t-    Shows all your fish in a neat list."""},
                              {'name':"`fish-list {#}`", 'value':"""\t\t-    Shows all your fish in a neat list."""},
                              {'name':"`fish-list {#}`", 'value':"""\t\t-    Shows all your fish in a neat list."""}], 
                    'Footer':"Page "+str(page)+"/1 | Showing items 1-10 : 10 | 10 per page",
                    'Emojis': ['🏠','🐟','🎣'],
                    'Pages': 1, 'CurrentPage':1}
               ]
    return menuItemsArray