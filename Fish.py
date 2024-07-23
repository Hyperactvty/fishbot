import discord
#from replit import db
import math, random
import c_UtilityMethods as UM, c_UserData as UD, c_Database as D, c_ItemValues as IV, c_GenerateFishImage as IMG
import datetime

def GetAllFish():
  fishData=[
        {
          'FISH_ID':0, 'Name':'Bass', 'Type':'Fish', 'Rarity':'Common', 'Set':None, 'Regions':['Lake', 'Pond', 'Ocean'], 
          'MIN_WEIGHT':10, 'MAX_WEIGHT':20,'MIN_LENGTH':40, 'MAX_LENGTH':80, 'MIN_WIDTH':0.3, 'MAX_WIDTH':7.8,
          'Trophy_Sizes':{'Bronze':60, 'Silver':75, 'Gold':85, 'Platinum':90, 'Ruby':95, 'Diamond':97.5}}
        
        
        ]
  return fishData

def PutFishIntoDict( FISH_ID: int, name: str, fish_type: str, rarity: str, fish_set: str, regions: [], 
                     MIN_WEIGHT: float, MAX_WEIGHT: float, MIN_LENGTH: float, MAX_LENGTH: float, MIN_WIDTH: float, MAX_WIDTH: float,
                     trophy_Sizes: {}, preferred_Bait, nocturnal, seasonal):
  fishDict = {'FISH_ID':FISH_ID, 'Name':name, 'Type':fish_type, 'Rarity':rarity, 'Set':fish_set, 'Regions':regions, 
  'MIN_WEIGHT':MIN_WEIGHT, 'MAX_WEIGHT':MAX_WEIGHT,'MIN_LENGTH':MIN_LENGTH, 'MAX_LENGTH':MAX_LENGTH, 'MIN_WIDTH':MIN_WIDTH, 'MAX_WIDTH':MAX_WIDTH,
  'Trophy_Sizes':trophy_Sizes, 'Preferred_Bait':preferred_Bait, 'Nocturnal':nocturnal, 'Seasonal':seasonal}
  
  return fishDict


def GrabFishDynamically(FISH_OBJECTS_SBRarity: []):
  randomFishList = [random.choice(FISH_OBJECTS_SBRarity) for fish in range(10)]
  print(f"Random Fish List: {randomFishList}")


def DetermingFishingVariables(ctx, currentRegion, currentRod, currentBait, percentRarity, percentSecondaryRarity, SortedRarity_FishList):
  """
    Use for determining the fish fished.
  """
  FISH_OBJECTS_SBRarity=SortedRarity_FishList
  FISH_IN_REGION = []
  for rarity in SortedRarity_FishList:
    RARITYLIST=[]
    for fish in rarity:
      #print(f"FISH: {fish}")
      if(currentRegion in fish['Regions']):
        #if(fish['Seasonal']==CurrentSeason)
        if(fish['Nocturnal']==0):
          randomRollForBait=random.randint(0,100)
          if(randomRollForBait>=15 and randomRollForBait <= 40):
            if(currentBait==fish['Preferred_Bait']):
              print(f"Added fish due to preferred bait: {fish['Name']}")
              RARITYLIST.append(fish)
          RARITYLIST.append(fish)
        #print(f"\tADDED FISH: {fish['Name']}")
    FISH_IN_REGION.append(RARITYLIST)

  FISH_OBJECTS_SBRarity=FISH_IN_REGION
  fishedFish={}; isAncient=False

  # Have a random chance, like 15-30% for fish who have preferred_bait, and have them

  # Have a list of 10 generated fish, depending on the type of bait used, some fish may appear more (15-35% more)
  
  
  if(currentRod=='Basic'):
    if(percentRarity>=0 and percentRarity<=50): fishedFish = GrabFishFromRarity(ctx, "Common", FISH_OBJECTS_SBRarity[0])
    elif(percentRarity>50 and percentRarity<=75):fishedFish = GrabFishFromRarity(ctx, "Uncommon",FISH_OBJECTS_SBRarity[1])
    elif(percentRarity>75 and percentRarity<=90):fishedFish = GrabFishFromRarity(ctx, "Rare",FISH_OBJECTS_SBRarity[2])
    elif(percentRarity>90 and percentRarity<=97.5):fishedFish =GrabFishFromRarity(ctx, "Epic",FISH_OBJECTS_SBRarity[3])
    elif(percentRarity>97.5 and percentRarity<=99):fishedFish =GrabFishFromRarity(ctx, "Legendary",FISH_OBJECTS_SBRarity[4])
    elif(percentRarity>99 and percentRarity<=110):fishedFish = GrabFishFromRarity(ctx, "Exotic",FISH_OBJECTS_SBRarity[5])
    else:
      print("Rare Fish [OVERFLOW]")
      fishedFish = F.GrabFishFromRarity(ctx, FISH_OBJECTS_SBRarity[2])
  if(currentRod=='Advanced'):
    if(percentRarity>=0 and percentRarity<=40): fishedFish = GrabFishFromRarity(ctx, "Common", FISH_OBJECTS_SBRarity[0])
    elif(percentRarity>40 and percentRarity<=65):fishedFish = GrabFishFromRarity(ctx, "Uncommon",FISH_OBJECTS_SBRarity[1])
    elif(percentRarity>65 and percentRarity<=90):fishedFish = GrabFishFromRarity(ctx, "Rare",FISH_OBJECTS_SBRarity[2])
    elif(percentRarity>90 and percentRarity<=95):fishedFish =GrabFishFromRarity(ctx, "Epic",FISH_OBJECTS_SBRarity[3])
    elif(percentRarity>95 and percentRarity<=99):fishedFish =GrabFishFromRarity(ctx, "Legendary",FISH_OBJECTS_SBRarity[4])
    elif(percentRarity>99 and percentRarity<=110):fishedFish = GrabFishFromRarity(ctx, "Exotic",FISH_OBJECTS_SBRarity[5])
    else:
      print("Rare Fish [OVERFLOW]")
      fishedFish = F.GrabFishFromRarity(ctx, FISH_OBJECTS_SBRarity[2])
  if(currentRod=='Masterly'):
    if(percentRarity>=0 and percentRarity<=20): fishedFish = GrabFishFromRarity(ctx, "Common", FISH_OBJECTS_SBRarity[0])
    elif(percentRarity>20 and percentRarity<=35):fishedFish = GrabFishFromRarity(ctx, "Uncommon",FISH_OBJECTS_SBRarity[1])
    elif(percentRarity>35 and percentRarity<=60):fishedFish = GrabFishFromRarity(ctx, "Rare",FISH_OBJECTS_SBRarity[2])
    elif(percentRarity>60 and percentRarity<=80):fishedFish =GrabFishFromRarity(ctx, "Epic",FISH_OBJECTS_SBRarity[3])
    elif(percentRarity>80 and percentRarity<=92.5):fishedFish =GrabFishFromRarity(ctx, "Legendary",FISH_OBJECTS_SBRarity[4])
    elif(percentRarity>92.5 and percentRarity<=110):fishedFish = GrabFishFromRarity(ctx, "Exotic",FISH_OBJECTS_SBRarity[5])
    else:
      print("Rare Fish [OVERFLOW]")
      fishedFish = F.GrabFishFromRarity(ctx, FISH_OBJECTS_SBRarity[2])
  else:
    if(percentRarity>=0 and percentRarity<=50): fishedFish = GrabFishFromRarity(ctx, "Common", FISH_OBJECTS_SBRarity[0])
    elif(percentRarity>50 and percentRarity<=75):fishedFish = GrabFishFromRarity(ctx, "Uncommon",FISH_OBJECTS_SBRarity[1])
    elif(percentRarity>75 and percentRarity<=90):fishedFish = GrabFishFromRarity(ctx, "Rare",FISH_OBJECTS_SBRarity[2])
    elif(percentRarity>90 and percentRarity<=97.5):fishedFish =GrabFishFromRarity(ctx, "Epic",FISH_OBJECTS_SBRarity[3])
    elif(percentRarity>97.5 and percentRarity<=99):fishedFish =GrabFishFromRarity(ctx, "Legendary",FISH_OBJECTS_SBRarity[4])
    elif(percentRarity>99 and percentRarity<=110):fishedFish = GrabFishFromRarity(ctx, "Exotic",FISH_OBJECTS_SBRarity[5])
    else:
      print("Rare Fish [OVERFLOW]")
      fishedFish = F.GrabFishFromRarity(ctx, FISH_OBJECTS_SBRarity[2])
    
  if percentSecondaryRarity==6:#Ancient
    isAncient=True
    updateFishCount=D.GrabFromDB(ctx.author.id, 'USERS',f'Total_Ancient')
    D.UpdateDB(ctx.author.id, f'USERS', f'Total_Ancient', updateFishCount+1)
  return fishedFish, isAncient

def formatCell(data: str):
  try:
    data=str(data)
    data=(data).replace('{','').replace('}','')
    #print(data)
    
    line='\_'
    cell = ""
    buffer=0
    fmt_len=len(str(data))
    #print(fmt_len)
    for space in range(0,11):
      #print(cell)
      if(space < math.floor((11-fmt_len)/2)):
        cell+=line
      elif((space >= math.floor((11-fmt_len)/2)) and (space<math.ceil((11-fmt_len)))):
        try:
          cell+=str(data[buffer])
          buffer+=1
        except: cell+=line
      else:
        cell+=line
  except Exception as e:
    print(e)
    
  return cell

def LuckyRod(rodBonus, amountOfRods):
  randomBurstOfLuck=random.randint(1,3);randomBurstOfLuckPhaseTwo=0;randomBurstOfLuckPhaseThree=0
  
  if randomBurstOfLuck==3:
      randomBurstOfLuckPhaseTwo=random.randint(1,20)
      if randomBurstOfLuckPhaseTwo==17:
          randomBurstOfLuckPhaseThree=random.randint(1,100)
          if randomBurstOfLuckPhaseThree==77:rodBonus=amountOfRods*777#Multiplies the amount of the user's current rod by the rod bonus
          else:rodBonus=amountOfRods*77#Multiplies the amount of the user's current rod by the rod bonus
      else:rodBonus=amountOfRods*7#Multiplies the amount of the user's current rod by the rod bonus
  else:rodBonus=amountOfRods*3#Multiplies the amount of the user's current rod by the rod bonus
  #fishingReward=fishingReward*rodBonus
  return rodBonus

  print(f"LUCK: 1: {randomBurstOfLuck}\t2: {randomBurstOfLuckPhaseTwo}\t3: {randomBurstOfLuckPhaseThree}")

def SortFishByRarity(FISH_OBJECTS: []):
  common=[]; uncommon=[]; rare=[]; epic=[]; legendary=[]; exotic=[]; daily=[]; event = []; sortedRarityArray=[]

  for item in FISH_OBJECTS:
    #print(f"rarity: {item['Rarity']}\t|\t{item['FISH_ID']}")
    if (item['Rarity']) == "Common": common.append(item)
    elif (item['Rarity']) == "Uncommon": uncommon.append(item)
    elif (item['Rarity']) == "Rare": rare.append(item)
    elif (item['Rarity']) == "Epic": epic.append(item)
    elif (item['Rarity']) == "Legendary": legendary.append(item)
    elif (item['Rarity']) == "Exotic": exotic.append(item)
    elif (item['Rarity']) == "Daily": daily.append(item)
    elif (item['Rarity']) == "Event": event.append(item)

  #sortedRarityArray.append([common, uncommon, rare, epic, legendary, exotic, daily, event])
  sortedRarityArray.append(common)
  sortedRarityArray.append(uncommon)
  sortedRarityArray.append(rare)
  sortedRarityArray.append(epic)
  sortedRarityArray.append(legendary)
  sortedRarityArray.append(exotic)
  sortedRarityArray.append(daily)
  sortedRarityArray.append(event)
  #print(f"\n{sortedRarityArray}")
  return sortedRarityArray

def GrabFishFromRarity(ctx, rarity: str, FISH_OBJECTS_SBRarity: []):
  grabbedFish = random.choice(FISH_OBJECTS_SBRarity)
  updateFishCount=D.GrabFromDB(ctx.author.id, 'USERS',f'Total_{str(rarity).capitalize()}')
  D.UpdateDB(ctx.author.id, f'USERS', f'Total_{str(rarity).capitalize()}', updateFishCount+1)
  
  #for item in FISH_OBJECTS_SBRarity:
  #  print(f"rarity: {item['Rarity']}\t|\t{rarity} == {item['FISH_ID']}")
  #  if (rarity) == (item['Rarity']):
  #      #do_something(item[fish])
  #      print("In")
  #      print("Found Fish "+str(item['Name']))
  #      fishEmbed = CreateFishEmbed(item)

  return grabbedFish  

def GenerateNewUserFish(fishDict: {}, isAncient: bool, ctx):
  ffd=fishDict
  #userKeyString = "U"+str(ctx.author.id); userKey=db[userKeyString]

  # Fish Variables
  rarityBonus = 0;fishingReward=1; weight = round(random.uniform(ffd['MIN_WEIGHT'],ffd['MAX_WEIGHT']),2); length=round(random.uniform(ffd['MIN_LENGTH'],ffd['MAX_LENGTH']),2); girth=round(random.uniform(ffd['MIN_WIDTH'],ffd['MAX_WIDTH']),2)

  # Calculated Variables
  percent_Weight = float(weight - fishDict['MIN_WEIGHT'])/(fishDict['MAX_WEIGHT']-fishDict['MIN_WEIGHT'])
  percent_Length = float(length - fishDict['MIN_LENGTH'])/(fishDict['MAX_LENGTH']-fishDict['MIN_LENGTH'])
  percent_Width  = float(girth - fishDict['MIN_WIDTH'])/(fishDict['MAX_WIDTH']-fishDict['MIN_WIDTH'])
  
  # The Percentage of the fish; How good the fish is statistically.
  percent = ( (percent_Weight * 45) + (percent_Length * 35) + (percent_Width * 20) )
  ffd.update({'Weight':weight, 'Length':length,'Width':girth, 'Percent':percent})

  ffd.update({'Percent_Weight':percent_Weight, 'Percent_Length':percent_Length,'Percent_Width':percent_Width})
  #print(f"\tUSERKEY:\t{userKey}")

  #print(f"Rod:\t\t\t{str(userKey['ITEMS']['Current_Rod'])} - {str(userKey['ITEMS']['RODS'][userKey['ITEMS']['Current_Rod']])}")
  #print(f"Rod:\t\t\t{str(userKey['ITEMS']['Current_Rod'])}")
  
  currentRod = f"Rod_{D.GrabFromDB(ctx.author.id, 'USER_ITEM_ROD','Current_Rod')}"
  #currentRod = D.GrabFromDB(ctx.author.id, 'USER_ITEM_ROD','Current_Rod')

  #amountOfRods=userKey['ITEMS']['RODS'][userKey['ITEMS']['Current_Rod']]['Amount']
  amountOfRods=D.GrabFromDB(ctx.author.id, 'USER_ITEM_ROD', currentRod)
  # Generates the rodBonus
  #rodBonus=(userKey['ITEMS']['RODS'][userKey['ITEMS']['Current_Rod']]['Rod_Base_Bonus'])*userKey['ITEMS']['RODS'][userKey['ITEMS']['Current_Rod']]['Amount']
  rodBonus=(IV.GetItemValues('RODS', currentRod)['Rod_Base_Bonus'])*amountOfRods
  if(currentRod=='Rod_Basic'): rodBonus=rodBonus+1
  if(currentRod=='Rod_Lucky'): rodBonus=LuckyRod(rodBonus, amountOfRods)

  userLevel=D.GrabFromDB(ctx.author.id, 'USERS', 'User_Level'); userExp=D.GrabFromDB(ctx.author.id, 'USERS', 'User_Exp'); prestigeCount=D.GrabFromDB(ctx.author.id, 'USERS', 'Prestige_Count')

  
  # The Rarity
  embedColour=discord.Color.green() # Default
  if(ffd['Rarity']=='Common'):      embedColour = discord.Color.greyple(); rarityBonus=1
  elif(ffd['Rarity']=='Uncommon'):  embedColour = discord.Color.green(); rarityBonus=1.5
  elif(ffd['Rarity']=='Rare'):      embedColour = discord.Color.blue(); rarityBonus=2.5
  elif(ffd['Rarity']=='Epic'):      embedColour = discord.Color.purple(); rarityBonus=4
  elif(ffd['Rarity']=='Legendary'): embedColour = discord.Color.gold(); rarityBonus=8
  elif(ffd['Rarity']=='Exotic'):    embedColour = discord.Color.red(); rarityBonus=20
  elif(ffd['Rarity']=='Daily'):     embedColour = discord.Color.teal(); rarityBonus=20
  elif(ffd['Rarity']=='Event'):     embedColour = discord.Color.magenta(); rarityBonus=20
  if(isAncient): embedColour = discord.Color.blurple(); rarityBonus=rarityBonus*2; print("Is Ancient {isAncient}")
  ffd.update({'RarityBonus':rarityBonus,'RodBonus':rodBonus, 'RarityColour':embedColour})

  # The Trophy Level
  trophyText = ""; trophyBonus=1
  if(False):
    if(percent>=ffd['Trophy_Sizes']['Diamond']):
      trophyText = "\t**Trophy Rank : Diamond** :gem:"; trophyBonus=4
    elif(percent>=ffd['Trophy_Sizes']['Ruby']):
      trophyText = "\t**Trophy Rank : Ruby** <a:rotatingruby:859191883338219530>"; trophyBonus=2.5
    elif(percent>=ffd['Trophy_Sizes']['Platinum']):
      trophyText = "\t**Trophy Rank : Platinum** <:Platinium_Valorant:796864109319684126>"; trophyBonus=2
    elif(percent>=ffd['Trophy_Sizes']['Gold']):
      trophyText = "\t**Trophy Rank : Gold** :first_place:"; trophyBonus=1.75
    elif(percent>=ffd['Trophy_Sizes']['Silver']):
      trophyText = "\t**Trophy Rank : Silver** :second_place:"; trophyBonus=1.5
    elif(percent>=ffd['Trophy_Sizes']['Bronze']):
      trophyText = "\t**Trophy Rank : Bronze** :third_place:"; trophyBonus=1.25
    ffd.update({'TrophyText':trophyText, 'TrophyBonus':trophyBonus})

  if(percent>=97.5):
    trophyText = "\t**Trophy Rank : Diamond** :gem:"; trophyBonus=4
  elif(percent>=95):
    trophyText = "\t**Trophy Rank : Ruby** <a:rotatingruby:859191883338219530>"; trophyBonus=2.5
  elif(percent>=90):
    trophyText = "\t**Trophy Rank : Platinum** <:Platinium_Valorant:796864109319684126>"; trophyBonus=2
  elif(percent>=82.5):
    trophyText = "\t**Trophy Rank : Gold** :first_place:"; trophyBonus=1.75
  elif(percent>=75):
    trophyText = "\t**Trophy Rank : Silver** :second_place:"; trophyBonus=1.5
  elif(percent>=60):
    trophyText = "\t**Trophy Rank : Bronze** :third_place:"; trophyBonus=1.25
  ffd.update({'TrophyText':trophyText, 'TrophyBonus':trophyBonus})

  # The Calculation
  fishingReward = ( ( ( weight * trophyBonus ) * rarityBonus ) * rodBonus ) * ( ( ( userLevel / 20 ) * (((prestigeCount/2)+2)/2) ) + 1 )
  #print(f'{fishingReward} = ( ( ( {weight * trophyBonus} ) * {rarityBonus} ) * {rodBonus} ) * ( ( ( {userLevel} / 20 ) * ((({prestigeCount}/2)+2)/2) ) + 1 )')

  #print(f"Reward: {fishingReward}")
  ffd.update({'FishingReward':fishingReward,'USER_FISH_ID':0})
  currBal = D.GrabFromDB(ctx.author.id, 'USERS', 'Current_Balance')
  D.UpdateDB(ctx.author.id, 'USERS', 'Current_Balance', currBal+fishingReward)
  #userKey['USER']['Current_Balance']+=fishingReward
  print(f"FISH COMPLETED: {ffd}")
  print(f"UPLOADING TO THE DATABASE...")
  # Find the lowest value number. If there are missing numbers in the DB, use the lowest missing number.
  userFishID = 0

  

  #try:userFishID = len(D.GrabFromDB_WHERE(ctx.author.id, 'USER_FISH', 'Fish_ID', f'Discord_ID={ctx.author.id}', 'a'))
  userFishID = len(D.GrabFromDB_WHERE(ctx.author.id, 'USER_FISH', 'FishNumber', f'Discord_ID={ctx.author.id}', 'a'))
  #print(f"Missing Any nums? {D.GrabFromDB_WHERE(ctx.author.id, 'USER_FISH', 'FishNumber', f'Discord_ID={ctx.author.id}', 'a')}")
  try: 
    checkEmptyRows=UM.AssignMissingNumber(D.GrabFromDB_WHERE(ctx.author.id, 'USER_FISH', 'FishNumber', f'Discord_ID={ctx.author.id}', 'a'))
    #print(f"EMPTY??? {checkEmptyRows}")
    if(checkEmptyRows==None): userFishID+=1
    else: userFishID=checkEmptyRows[0]
  except: userFishID+=1
  #print(f'userFishID={userFishID}')
  str_Regions = ""; itr_Reg=0
  for reg in ffd['Regions']: 
    str_Regions+=f"{reg}"
    itr_Reg+=1
    if(itr_Reg>=len(ffd['Regions'])): break
    str_Regions+="\, "
  #print(str_Regions)
  currentTime=datetime.datetime.now(); str_CurrentTime=currentTime.strftime("%a\, %B %d\, %Y | %H:%M:%S")
  #if(trophyText==""): trophyText=None
  selectedLure = D.GrabFromDB(ctx.author.id, 'USER_ITEM_LURE','Current_Lure');currentRod=D.GrabFromDB(ctx.author.id, 'USER_ITEM_ROD','Current_Rod')
  D.InsertIntoDB(ctx.author.id, tableName='USER_FISH', 
                 columnsToUpdate=f'''Discord_ID, FishNumber, Fish_Name, Fish_Type, Fish_Set, Fish_Rarity, Fish_Region, 
                 Fish_Weight, Fish_Length, Fish_Width, Fish_Percent, Date_Caught, Trophy_Size, Points_Received, Rod_Used, 
                 Lure_Used''', 
                 valuesToInsert= f'''{ctx.author.id}, {userFishID}, '{ffd['Name']}', '{ffd['Type']}', '{ffd['Set']}', '{ffd['Rarity']}', '{str_Regions}',
                 {ffd['Weight']}, {ffd['Length']}, {ffd['Width']}, {round(percent,2)}, '{str_CurrentTime}', '{trophyText}', {fishingReward}, '{currentRod}',
                 '{selectedLure}\'''')
  #percent = ffd['Percent']; weight = ffd['Weight']; length=ffd['Length']; girth=ffd['Width']; percent_Weight=ffd['Percent_Weight']; percent_Length=ffd['Percent_Length']; percent_Width=ffd['Percent_Width']
  #rarityBonus=ffd['RarityBonus']; rodBonus=ffd['RodBonus']; embedColour = ffd['RarityColour']; 
  #fishingReward=ffd['FishingReward']; trophyText=ffd['TrophyText']; trophyBonus=ffd['TrophyBonus']
  print(f"DONE")

  ffd['USER_FISH_ID'] = userFishID
  
  return ffd

#==============================================================================================
""" Embed Area """

def CreateFishEmbed(fishDict: {}, isAncient: bool, ctx):
  ffd=fishDict
  #userKeyString = "U"+str(ctx.author.id); userKey=db[userKeyString]

  # GET VALUES FIRST, THEN UPDATE AT THE END!!!

  # Dict Variables
  selectedLure = D.GrabFromDB(ctx.author.id, 'USER_ITEM_LURE','Current_Lure');currentRod=D.GrabFromDB(ctx.author.id, 'USER_ITEM_ROD','Current_Rod')
  remainingLures = D.GrabFromDB(ctx.author.id, 'USER_ITEM_LURE',f'Lure_{selectedLure}'); amountOfRods = D.GrabFromDB(ctx.author.id, 'USER_ITEM_ROD',f'Rod_{currentRod}')
  #selectedLure = userKey['ITEMS']['Current_Lure']; amountOfRods=userKey['ITEMS']['RODS'][userKey['ITEMS']['Current_Rod']]['Amount']
  percent = ffd['Percent']; weight = ffd['Weight']; length=ffd['Length']; girth=ffd['Width']; percent_Weight=ffd['Percent_Weight']; percent_Length=ffd['Percent_Length']; percent_Width=ffd['Percent_Width']
  rarityBonus=ffd['RarityBonus']; rodBonus=ffd['RodBonus']; embedColour = ffd['RarityColour']; 
  fishingReward=ffd['FishingReward']; trophyText=ffd['TrophyText']; trophyBonus=ffd['TrophyBonus']

  setString=""
  if(ffd['Set']):setString = ffd['Set']

  # For testing the levelling
  #userKey['USER']['Level']=1; userKey['USER']['User_Exp']=0

  #userLevel=userKey['USER']['Level']; userExp=userKey['USER']['User_Exp']; prestigeCount=userKey['USER']['Prestige_Count']
  userLevel=D.GrabFromDB(ctx.author.id, 'USERS', 'User_Level'); userExp=D.GrabFromDB(ctx.author.id, 'USERS', 'User_Exp'); prestigeCount=D.GrabFromDB(ctx.author.id, 'USERS', 'Prestige_Count')
  gainedExp=float(fishingReward)/10
  userExp+=gainedExp
  # userLevelUpMath=(userLevel*50)+50
  userLevelUpMath=(userLevel*50)+((userLevel*50)+(userLevel*50))+50
  
  #print(f'\n\tBase EXP: {userExp}/{userLevelUpMath} = {userExp/userLevelUpMath}')
  userExp=D.UpdateDB(ctx.author.id, 'USERS', 'User_Exp', userExp+gainedExp)
  #userKey['USER']['User_Exp']+=(gainedExp)
  currBal = D.GrabFromDB(ctx.author.id, 'USERS', 'Current_Balance')
  
  userFishID = len(D.GrabFromDB_WHERE(ctx.author.id, 'USER_FISH', 'FishNumber', f'Discord_ID={ctx.author.id}', 'a'))
  numOfFish = len(D.GrabFromDB_WHERE(ctx.author.id, 'USER_FISH', 'FishNumber', f'Discord_ID={ctx.author.id}', 'a'))

  levelUpText=""
  checkLevelup=0
  try: checkLevelup=userExp/userLevelUpMath
  except: checkLevelup=0
  if(math.floor(checkLevelup)>0):
    numTimesLvlUp=0
    for levelUpIteration in range(0,math.floor(checkLevelup)):
      if(checkLevelup < 1):break
      #userKey['USER']['User_Exp']-=userLevelUpMath
      userExp=D.UpdateDB(ctx.author.id, 'USERS', 'User_Exp', userExp-userLevelUpMath)
      #userExp=userKey['USER']['User_Exp']
      #userKey['USER']['Level']+=1
      userLevel = D.UpdateDB(ctx.author.id, 'USERS', 'User_Level', userLevel+1)
      #print("Level Up!")
      userLevelUpMath=(userLevel*50)+((userLevel*50)+(userLevel*50))
      numTimesLvlUp+=1
      levelUpText=f'(Leveled Up {numTimesLvlUp}x)'
      if(userExp/userLevelUpMath < 1):break
  calc_rodBonus=1
  try: calc_rodBonus = rodBonus/(amountOfRods)
  except: calc_rodBonus=calc_rodBonus
  # Finally generate the image (?)
  try:
    IMG.GenerateFishOutputImage(ffd, currentRod, calc_rodBonus, amountOfRods, userLevel, userExp, userLevelUpMath, levelUpText, prestigeCount, percent, gainedExp)
  except Exception as e:
    print("Could not generate Image: {e}")

  #print(len(f" **Congratulations, you caught {str(UM.Gen_A_An(ffd['Name']))} {str(ffd['Name'])} ({str(ffd['Rarity'])[0]})** "))
  headerTitle = str(f" **Congratulations, you caught {str(UM.Gen_A_An(ffd['Name']))} {str(ffd['Name'])} ({str(ffd['Rarity'])[0]})** ").center(60, '═')
  embed={'Header':
          #{'title':f"═══════ **Congratulations, you caught {str(UM.Gen_A_An(ffd['Name']))} {str(ffd['Name'])} ({str(ffd['Rarity'])[0]})** ═══════", 'description':f"You caught {str(UM.Gen_A_An(ffd['Rarity']))} **{str(ffd['Rarity'])} {str(ffd['Name'])} {str(setString)}**", 'color':embedColour
          {'title':f"{headerTitle}", 'description':str(f"You caught {str(UM.Gen_A_An(ffd['Rarity']))} **{str(ffd['Rarity'])} {str(ffd['Name'])} {str(setString)}**").center(60), 'color':embedColour
            }, 
          #'Thumbnail':f'{ctx.author.avatar_url}',
          'Fields':[
            {'name':"Weight", 'value':f"""```diff\n{weight} lbs /{ffd['MAX_WEIGHT']} lb\nPercent: {round(percent_Weight*100,2)}%```""", 'inline':True},
            {'name':"Rod Bonus", 'value':f"""```fix\n{currentRod} - {round(rodBonus,3)}\n{round(rodBonus,3)} = {amountOfRods} x {round(calc_rodBonus, 3)}```""", 'inline':True},
            {'name':"Rarity Bonus", 'value':f"""```diff\n{ffd['Rarity']}: {rarityBonus}```""", 'inline':True}, # Use Center FOrmatting
            {'name':"Size:", 'value':f"""```diff\nL: {UM.comma(length)} ({ffd['MIN_LENGTH']}:{ffd['MAX_LENGTH']})\t{round(percent_Length*100,2)}%\nG:~{girth} in ({ffd['MIN_WIDTH']}:{ffd['MAX_WIDTH']})\t{round(percent_Width*100,2)}%```""", 'inline':False},
            {'name':"Level Bonus", 'value':f"""```diff\nLvl {userLevel}: {((userLevel/20)+1)}x\t|\t{UM.comma(round(userExp,2))}/{UM.comma(userLevelUpMath)} {levelUpText}```""", 'inline':True},
            #{'name':"Item?", 'value':f"""```diff\nN/A```""", 'inline':True},
            {'name':"Calculation", 'value':f"""```fix\n{(UM.comma(float(round(fishingReward,2))))} = ((({(weight)} x {trophyBonus}) x {(rarityBonus)}) x {UM.comma(round(rodBonus,2))}) x {(round(((userLevel/20)+1)*(((prestigeCount/2)+2)/2),3))} (Rounded)\nAward = (((Weight * Trophy Bonus) * Rarity Bonus) * Rod Bonus) * (Level Multiplier * Prestige)```""", 'inline':False},
            {'name':"Total Award", 'value':f"""```diff\n{UM.comma(float(round(fishingReward,2)))} pts```""", 'inline':True},
            {'name':"Total", 'value':f"""```diff\n{round(percent,2)}% / 100%\nExp: {UM.comma(round(gainedExp,2))}```{trophyText}""", 'inline':True},
            {'name':"Current Fish", 'value':f"""```diff\nN/A (Fish#: {ffd['USER_FISH_ID']})```""", 'inline':True}
            ], 
          'Footer':{'text':f"Fish Shown: {ffd['USER_FISH_ID']}/{numOfFish}  |  Lures Left: {UM.comma(remainingLures)}  |  Current Balance: {UM.comma(round(currBal,2))}", 'icon_url':f'{ctx.author.avatar_url}'}}
  print("""__**Type{:^9}Min{:^9}Max**__\n""".format('|','|',))
  return UM.CreateDiscordEmbedFromDict(embed)

def CreateFishViewEmbed(fishDict: {}):
  
  formattedFishDict = {'FISH_ID':fishDict['FISH_ID'], 'Name':fishDict['Name'], 'Type':fishDict['Type'], 'Rarity':fishDict['Rarity'], 
                      'Set':fishDict['Set'], 'Regions':fishDict['Regions'], 'MIN_WEIGHT':fishDict['MIN_WEIGHT'], 'MAX_WEIGHT':fishDict['MAX_WEIGHT'],'MIN_LENGTH':fishDict['MIN_LENGTH'], 'MAX_LENGTH':fishDict['MAX_LENGTH'], 'MIN_WIDTH':fishDict['MIN_WIDTH'], 'MAX_WIDTH':fishDict['MAX_WIDTH'], 'Trophy_Sizes':fishDict['Trophy_Sizes']}
  ffd=formattedFishDict

  embedColour=discord.Color.green() # Default
  if(ffd['Rarity']=='Common'): embedColour = discord.Color.greyple()
  elif(ffd['Rarity']=='Uncommon'): embedColour = discord.Color.green()
  elif(ffd['Rarity']=='Rare'): embedColour = discord.Color.blue()
  elif(ffd['Rarity']=='Epic'): embedColour = discord.Color.purple()
  elif(ffd['Rarity']=='Legendary'): embedColour = discord.Color.gold()
  elif(ffd['Rarity']=='Exotic'): embedColour = discord.Color.red()
  elif(ffd['Rarity']=='Daily'): embedColour = discord.Color.teal()
  elif(ffd['Rarity']=='Event'): embedColour = discord.Color.magenta()
  #if(ffd['Rarity']==): embedColour = discord.Color.green()

  embed={'Header':
          {'title':f"═══════ **Viewing Fish: {ffd['Name']}** ═══════", 'description':"*\"Put Fish Description Here.\"*", 'color':embedColour
            }, 
          'Fields':[
            {'name':f"Name: `{ffd['Name']}` (id:{ffd['FISH_ID']})", 'value':f"""type:\t{ffd['Type']}\nSet:\t{ffd['Set']}\nRarity:\t{ffd['Rarity']}""", 'inline':True},
            {'name':"Can be found in:", 'value':f"""{ffd['Regions']}""", 'inline':True},
            #{'name':"Details", 'value':f"""__**Type\t\t|\t\tMin\t\t|\t\tMax**__\nWgt\t\t|\t\t{ffd['MIN_WEIGHT']}\nMax Weight:\t{ffd['MAX_WEIGHT']}\nMin Length:\t{ffd['MIN_LENGTH']}\nMax Length:\t{ffd['MAX_LENGTH']}\nMin Width:\t{ffd['MIN_WIDTH']}\nMax Width:\t{ffd['MAX_WIDTH']}""", 'inline':False}, # Use Center FOrmatting
            {'name':"Details", 'value':"""__**\_\_\_\_Type\_\_\_\_|\_\_\_\_Min\_\_\_\_|\_\_\_\_Max\_\_\_\_**__\n"""+
            f"""__\_\_\_Weight\_\_\_|{formatCell({ffd['MIN_WEIGHT']})}|{formatCell({ffd['MAX_WEIGHT']})}__\n__\_\_\_Length\_\_\_|{formatCell({ffd['MIN_LENGTH']})}|{formatCell({ffd['MAX_LENGTH']})}__\n__\_\_\_Width\_\_\_\_|{formatCell({ffd['MIN_WIDTH']})}|{formatCell({ffd['MAX_WIDTH']})}__""", 'inline':False}, # Use Center FOrmatting
            {'name':"Potential Points:", 'value':f"""```fix\nValues```""", 'inline':False},
            {'name':"Trophy Sizes:", 'value':f"""{fishDict['Trophy_Sizes']}""", 'inline':True}
            ], 
          'Footer':f"Fish Shown: {fishDict['FISH_ID']}/amt"}
  print("""__**Type{:^9}Min{:^9}Max**__\n""".format('|','|',))
  return UM.CreateDiscordEmbedFromDict(embed)
  
  #embed=discord.Embed(title="**Pepe**", description="{fishDescription}")
  #embed.add_field(name="Name: Pepe (id:4)", value="type:\t{fishType}\nSet:\t{set}\nRarity:\t{rarity}", inline=True)
  #embed.add_field(name="Details:", value="Weight, length, girth here", inline=True)
  #embed.add_field(name="Can be found in:", value="{forList}", inline=True)
  #embed.add_field(name="Potential Points:", value="undefined", inline=False)
  #embed.add_field(name="TrophySizes:", value="undefined", inline=True)
  #embed.set_footer(text="Fish x/array Length")