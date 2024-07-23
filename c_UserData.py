import discord
import c_Database as D
#from replit import db

# Use this method to create the user data
def NewUserData(ctx, userKey):
  userData = {
      'USER':{
        'USER_ID':userKey, 'Level':6, 'User_Exp':0, 'Prestige_Count':0,'Current_Balance':9929390, 'Special_Currency_Amount':50,
        'Total_Fish_Caught':0, 'Total_Common':0,'Total_Uncommon':0,'Total_Rare':0,'Total_Epic':0,'Total_Legendary':0,'Total_Exotic':0,'Total_Ancient':0,'Total_Event':0,
        'Total_Daily':0,'Total_Fish_Caught':0, 'Total_Times_Fished':0, 'Total_Earned_Points':0, 'Total_Points_Spent':0, 
        'Highest_Fish_Count':0, 'Fish_Largest':0, 'Fish_Smallest':0, 'Fish_Heaviest':0, 'Fish_Lightest':0, 'Style_Selected':0#, 'IsFishing':0 
        #'':0, 
      }, 'PRESTIGE_DATA':{
        'BOOSTERS':[], 'ABILITIES':[]
      }, 'ITEMS':{
        'Current_Rod':'Rod_Lucky','Current_Lure':'Lure_Normal',
        'RODS':{
            'Rod_Basic':{
                'Amount':1, 'Rod_Base_Bonus':0.01, 'Price':100, 'Description':'A cheap, basic wooden rod. Nothing special about it.'
            },'Rod_Bamboo':{
                'Amount':0, 'Rod_Base_Bonus':1.15, 'Price':2500,'Description':''
            },'Rod_Advanced':{
                'Amount':0, 'Rod_Base_Bonus':1.25, 'Price':7500,'Description':''
            },'Rod_Fiberglass':{
                'Amount':0, 'Rod_Base_Bonus':1.5, 'Price':15000, 'Description':''
            },'Rod_Triple':{
                'Amount':0, 'Rod_Base_Bonus':1.15, 'Price':33333,'Description':''
            },'Rod_Lucky':{
                'Amount':1, 'Rod_Base_Bonus':3, 'Price':77777,'Description':''
            },'Rod_Masterly':{
                'Amount':0, 'Rod_Base_Bonus':4.5, 'Price':1250000,'Description':''
            }
        }, 'LURES':{
            'Lure_Normal':{
                'Amount':10000, 'Rod_Base_Bonus':0.01, 'Price':100, 'Description':'A cheap, basic lure. Nothing appealing about it.'
            },'Lure_Special':{
                'Amount':0, 'Rod_Base_Bonus':1.15, 'Price':750,'Description':''
            },'Lure_Master':{
                'Amount':0, 'Rod_Base_Bonus':1.25, 'Price':2500,'Description':'Pretty good for finding rare fish'
            },'Lure_Nightly':{
                'Amount':0, 'Rod_Base_Bonus':2.5, 'Price':15000, 'Description':''
            },'Rod_Triple':{
                'Amount':0, 'Rod_Base_Bonus':1.15, 'Price':33333,'Description':''
            },'Rod_Lucky':{
                'Amount':1, 'Rod_Base_Bonus':3, 'Price':77777,'Description':''
            },'Rod_Masterly':{
                'Amount':0, 'Rod_Base_Bonus':4.5, 'Price':1250000,'Description':''
            }
        }, 'BAUBLES': [{'BaubleID':0, "Name":'High-Tension Line', 'Description':'You will never break your line.'}]
        
      }, 'USER_UNLOCKS': {
        'Current_Region':'Region_Lake',
        'REGIONS':{
            'Region_Pond':0, 'Region_Lake':0, 'Region_Tropical':0,'Region_Pirate':0,'Region_Ocean':0, 'Region_Mystical':0,
        }, 'BOATS':{ # Boats are used to go out and fish. When the storage is full, user has to return back to warehouse
            'Boat_Basic': {
                'Current_Boat_Level':1, 'Max_Boat_Level':15, 'Upgrades_Storage':0
            }
        }, 'WAREHOUSES': {
            'Warehouse_Basic': { # Warehouses are used to store massive amounts of fish. Users can sell the fish to make room but also to save space in database
                'Current_Warehouse_Level':1, 'Upgrades_Storage':0
            }
        }

      }, 'QUESTS': { 
        
      },'FISH':{}
      
    }
  print(f"UserData: {userData}")
  return userData

# Use this method to create the user with the data
#def CreateNewUser(ctx):
#  userKey = "U"+str(ctx.author.id)
#  print(f"UserID: {userKey}")
#  try:
#    del db[userKey]
#  except: pass
#  USERKEYS = db.keys()

#  if(userKey in USERKEYS): return
#  print("User not in set")
#  createdUserData = NewUserData(ctx, userKey)
#  db[f"{userKey}"] = createdUserData

  #value = db["key"]

# Essentially tells the user that they need to be regestered before using Fishbot. 
async def NotifyUserForRegistering(ctx):
  generatedEmbed=discord.Embed(title=f'Now Hold On a Second...',description=f"""You might want to setup your account first. It's easy.\n**Use the command** `f-start` and you will be set.""", color=discord.Color.red())
  await ctx.send(embed=generatedEmbed)
  return
  
# Use this method to update the user data. May have to go about doing it by putting 
#   the variables in temp variables, deleting the record then re-creating the record
def ChangeUserBalance(ctx, amount):
  # Grabs the user's Key from the database set
  currBal = D.GrabFromDB(ctx.author.id, 'USERS', 'Current_Balance')
  currBal = D.UpdateDB(ctx.author.id, 'USERS', 'Current_Balance', currBal+amount)
  return currBal

def CheckUserBalance(ctx, amount):
  # Grabs the user's Key from the database set
  currBal = D.GrabFromDB(ctx.author.id, 'USERS', 'Current_Balance')
  if((currBal+amount)>0): return False
  return True
