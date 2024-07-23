import c_UtilityMethods as UM, c_Database as D
import random
import discord
import json, datetime

# Called first to create the quests
#ALLQUESTS = QuestTemplates()


def CheckQuestDeadline():
  """
  Call this at the start of every hour"""

  return

def GenerateQuestText(questItem):
  questText = ""
  try: questItem['Requirements']
  except: questItem = (json.loads(questItem))
  questReqs = questItem['Requirements']
  if(questItem['Type']=='Amount'):
    typeText=questReqs['Type']
    if(questReqs['Type']=='Any'): typeText=f"fish (any)"
    rarityText=questReqs['Rarity']
    if(questReqs['Rarity']=='Any'): rarityText=""
    regionText=questReqs['Rarity']
    if(questReqs['Region']=='Any'): regionText="any"
    questText = f"Fish `{questReqs['Amount']} {rarityText} {typeText}` from {regionText} region"
  return questText

def GenerateNewQuest(ctx):
  newQuest=""
  grabbedQuestsFromDB = D.GrabFromDB_WHERE(ctx.author.id, 'USER_QUESTS', '*', f'Discord_ID = {ctx.author.id}', 'a')
  if(len(grabbedQuestsFromDB)<15):
  #if(True):
    grabbedQuest = GenerateRandomQuest()
    questReqs = grabbedQuest['Requirements']
    if(grabbedQuest['Type']=='Amount'):
      typeText=questReqs['Type']
      if(questReqs['Type']=='Any'): typeText=f"fish (any)"
      rarityText=questReqs['Rarity']
      if(questReqs['Rarity']=='Any'): rarityText=""
      regionText=questReqs['Rarity']
      if(questReqs['Region']=='Any'): regionText="any"
      questText = f"Fish `{questReqs['Amount']} {rarityText} {typeText}` from {regionText} region"
      print(f"Quest Text: {questText}")
  
      str_GrabbedQuest = str(grabbedQuest).replace("'",'"')
      D.InsertIntoDB(ctx.author.id, tableName='USER_QUESTS', 
                   columnsToUpdate=f'''Discord_ID, Difficulty, Quest_Type, Quest_Reqs''', 
                   valuesToInsert= f'''{ctx.author.id}, '{grabbedQuest['Difficulty']}', '{grabbedQuest['Type']}', '{str_GrabbedQuest}\'''')
  
  usersName=ctx.author
  try: usersName=ctx.author.nick
  except: pass
  questEmbed = discord.Embed(title=f"{usersName}'s Quests",description=f"Here are your ongoing quests:", color=discord.Color.blurple())
  for quest in grabbedQuestsFromDB:
    if(type(quest)==str):
      if(quest[0]=='{'):
        quest = (json.loads(quest))
        print(quest)
        questReqs = quest['Requirements']
        #print(f"Quest reqs: {questReqs}")
        #print(json.loads(quest)['Type'])
        if(quest['Type']=='Amount'):
          typeText=questReqs['Type']
          if(questReqs['Type']=='Any'): typeText=f"fish (any)"
          rarityText=f" {questReqs['Rarity']}"
          if(questReqs['Rarity']=='Any'): rarityText=""
          regionText=questReqs['Rarity']
          if(questReqs['Region']=='Any'): regionText="any"
          questText = f"Fish **{questReqs['Amount']}{rarityText} {typeText}** from {regionText} region"
          print(f"Quest Text: {questText}")
          currentTime = datetime.datetime.now()
          checkRemainingHours = 12-currentTime.hour%12; checkRemainingMins = 60-currentTime.minute%60; checkRemainingSecs = 60-currentTime.second%60
          questEmbed.add_field(name=str(f"{quest['Type']} ({quest['Difficulty'][0]})"), value=f"```{questText}```**{checkRemainingHours}h {checkRemainingMins}m {checkRemainingSecs}s left**", inline=False)
  #await ctx.channel.send(embed=questEmbed)
  #print(f"Data : {grabbedQuestsFromDB[4]}")
  return questEmbed

def CheckQuestReqs_FISH(ctx, fishObject):
  grabbedQuestFromDB = D.GrabFromDB_WHERE(ctx.author.id, 'USER_QUESTS', 'Quest_Reqs', f'Discord_ID = {ctx.author.id}', 'a')
  grabbedQuestIDFromDB = D.GrabFromDB_WHERE(ctx.author.id, 'USER_QUESTS', 'QUEST_ID', f'Discord_ID = {ctx.author.id}', 'a')
  it = 0; completeQuestArray=[]
  for questItem in grabbedQuestFromDB:
    try: questItem['Requirements']
    except: questItem = (json.loads(questItem))
    print(f"Quest Item: {questItem}")
    questReqs = questItem['Requirements']
    if(questItem['Type']=='Amount'):
      if(questReqs['Type']=='Any' or questReqs['Type']==fishObject['Type']): 
        if(questReqs['Rarity']=='Any' or questReqs['Rarity']==fishObject['Rarity']): 
          if(questReqs['Region']=='Any' or questReqs['Region'] in fishObject['Regions']): 
            #print("Matches Criteria")
            #print(f'B4\t{questReqs}')
            questReqs['Amount'] -= 1
            if(questReqs['Amount']<0): questReqs['Amount'] = 0
            #print(f'AFTER: \t{questReqs}')
            questItem['Requirements'] = questReqs
            questItem = str(questItem).replace("'",'"')
            D.UpdateDB_WHERE(ctx.author.id, 'USER_QUESTS', 'Quest_Reqs', f"'{questItem}'", f'QUEST_ID = {grabbedQuestIDFromDB[it]}')
    
    # Check if quest is now complete
    if (questReqs['Amount'] <= 0):
      completeQuestArray.append(it+1)
      #return it+1
    # Adds one to the iterator
    it+=1
  else: print('\n\t\tNOPE')
  if(len(completeQuestArray)!=0): return completeQuestArray
  return None

def CheckQuestClaim(ctx):
  grabbedQuestFromDB = D.GrabFromDB_WHERE(ctx.author.id, 'USER_QUESTS', 'Quest_Reqs', f'Discord_ID = {ctx.author.id}', 'a')
  grabbedQuestIDFromDB = D.GrabFromDB_WHERE(ctx.author.id, 'USER_QUESTS', 'QUEST_ID', f'Discord_ID = {ctx.author.id}', 'a')
  it = 0
  completeQuestArray=[]
  print(f'\n\n\tGRA: {grabbedQuestFromDB}\n\n')
  for questItem in grabbedQuestFromDB:
    try: questItem['Requirements']
    except: questItem = (json.loads(questItem))
    print(f"\tChecking UQest Item: {questItem}")
    questReqs = questItem['Requirements']
    # Check if quest is now complete
    if (questReqs['Amount'] <= 0):
      print("ADded")
      completeQuestArray.append(it+1)
    # Adds one to the iterator
    it+=1
  if(len(completeQuestArray)!=0): return True, completeQuestArray
  return None

def GenerateQuestBoard(ctx):
  """Note:
    Wipe database every 12 hours for refresh
  """
  questBoardArray=[]; questTextArray=[]
  questEmbed=discord.Embed(title=f"Quests Available",description=f"Quests are available", color=discord.Color.blurple())
  hasUserRefreshedQuest = D.GrabFromDB(ctx.author.id, f'USERS',f'Has_Refreshed_Quest')
  if(hasUserRefreshedQuest==0):
    print(f"Refreshing Questboard for {ctx.author}")
    for itr in range(0,7):
      grabbedQuest = GenerateRandomQuest()
      str_GrabbedQuest = str(grabbedQuest).replace("'",'"')
      questBoardArray.append(str_GrabbedQuest)
      quest = grabbedQuest# (json.loads(itr))
      #print(quest)
      questReqs = quest['Requirements']
      #print(f"Quest reqs: {questReqs}")
      #print(json.loads(quest)['Type'])
      if(quest['Type']=='Amount'):
        typeText=questReqs['Type']
        if(questReqs['Type']=='Any'): typeText=f"fish (any)"
        rarityText=f" {questReqs['Rarity']}"
        if(questReqs['Rarity']=='Any'): rarityText=""
        regionText=questReqs['Rarity']
        if(questReqs['Region']=='Any'): regionText="any"
        questText = f"Fish **{questReqs['Amount']}{rarityText} {typeText}** from {regionText} region"
      
        #print(f"Quest Text: {questText}")
        currentTime = datetime.datetime.now()
        checkRemainingHours = 12-currentTime.hour%12; checkRemainingMins = 60-currentTime.minute%60; checkRemainingSecs = 60-currentTime.second%60
      questTextArray.append(questText)
      D.UpdateDB(ctx.author.id, tableName=f'USERS', thingToSelect=f'Has_Refreshed_Quest', valuesToUpdate=1)
    
  else: 
      grabbedQuest =  D.GrabFromDB_WHERE(ctx.author.id, 'USER_QUESTBOARD', 'Q1, Q2, Q3, Q4, Q5, Q6, Q7', f'Discord_ID = {ctx.author.id}', 'o')
      for questItem in grabbedQuest:
        
        questBoardArray.append(questItem)
        quest = (json.loads(questItem))
        #print(quest)
        questReqs = quest['Requirements']
        #print(f"Quest reqs: {questReqs}")
        #print(json.loads(quest)['Type'])
        if('Amount' in quest['Type']):
          typeText=questReqs['Type']
          if(questReqs['Type']=='Any'): typeText=f"fish (any)"
          rarityText=f" {questReqs['Rarity']}"
          if(questReqs['Rarity']=='Any'): rarityText=""
          regionText=questReqs['Rarity']
          if(questReqs['Region']=='Any'): regionText="any"
          questText = f"Fish **{questReqs['Amount']}{rarityText} {typeText}** from {regionText} region"
      
          #print(f"Quest Text: {questText}")
          currentTime = datetime.datetime.now()
          checkRemainingHours = 12-currentTime.hour%12; checkRemainingMins = 60-currentTime.minute%60; checkRemainingSecs = 60-currentTime.second%60
        questTextArray.append(questText)
  
  qba = questBoardArray

  #print(f"qba  =  {qba}")
  if(hasUserRefreshedQuest==0):
    D.InsertIntoDB(ctx.author.id, tableName='USER_QUESTBOARD', 
                   columnsToUpdate=f'''Discord_ID, Q1, Q2, Q3, Q4, Q5, Q6, Q7''', 
                   valuesToInsert= f'''{ctx.author.id}, '{qba[0]}', '{qba[1]}', '{qba[2]}', '{qba[3]}', '{qba[4]}', '{qba[5]}', '{qba[6]}\'''')
  
  for itr in range(0,9):
    if(itr)==6: questEmbed.add_field(name=str(f"Special Points"), value=f"```fix\n<special points amount>```", inline=True)
    elif(itr)==8: questEmbed.add_field(name=str(f"Close"), value=f"```fix\nCloses the Questboard```", inline=True)
    else:
      num=itr
      if(itr)==7: num=6
      #print(json.loads(qba[num])['Type'])
      pinned='📌'
      if('Accepted' in json.loads(qba[num])['Type']): pinned = '✅'
      questEmbed.add_field(name=str(f"{pinned}{json.loads(qba[num])['Type']} ({json.loads(qba[num])['Difficulty'][0:2]})"), value=f"{questTextArray[num]}", inline=True)
  #questEmbed.add_field(name=str(f"📌{json.loads(qba[0])['Type']} ({json.loads(qba[0])['Difficulty'][0:2]})"), value=f"{questTextArray[0]}", inline=True)
  #questEmbed.add_field(name=str(f"📌{json.loads(qba[1])['Type']} ({json.loads(qba[1])['Difficulty'][0:2]})"), value=f"{questTextArray[1]}", inline=True)
  #questEmbed.add_field(name=str(f"📌{json.loads(qba[2])['Type']} ({json.loads(qba[2])['Difficulty'][0:2]})"), value=f"{questTextArray[2]}", inline=True)
  #questEmbed.add_field(name=str(f"📌{json.loads(qba[3])['Type']} ({json.loads(qba[3])['Difficulty'][0:2]})"), value=f"{questTextArray[3]}", inline=True)
  #questEmbed.add_field(name=str(f"📌{json.loads(qba[4])['Type']} ({json.loads(qba[4])['Difficulty'][0:2]})"), value=f"{questTextArray[4]}", inline=True)
  #questEmbed.add_field(name=str(f"📌{json.loads(qba[5])['Type']} ({json.loads(qba[5])['Difficulty'][0:2]})"), value=f"{questTextArray[5]}", inline=True)
  #questEmbed.add_field(name=str(f"Special Points"), value=f"```fix\n<special points amount>```", inline=True)
  #questEmbed.add_field(name=str(f"📌{json.loads(qba[6])['Type']} ({json.loads(qba[6])['Difficulty'][0:2]})"), value=f"{questTextArray[6]}", inline=True)
  #questEmbed.add_field(name=str(f"Close"), value=f"```fix\nCloses the Questboard```", inline=True)
  #for quest in questBoardArray:
  #  print(quest)
  return questEmbed

def GenerateRandomQuest():
  """
  Have only 3 (5 if premium) per person.
  """
  QUESTS={}; percentRarity=random.uniform(1,100)
  if(percentRarity>=0 and percentRarity<=50):
    QUESTS = random.choice(AVAILABLEQUESTS[0])
  elif(percentRarity>50 and percentRarity<=75):
    QUESTS = random.choice(AVAILABLEQUESTS[1])
  elif(percentRarity>75 and percentRarity<=90):
    QUESTS = random.choice(AVAILABLEQUESTS[2])
  elif(percentRarity>90 and percentRarity<=97.5):
    QUESTS = random.choice(AVAILABLEQUESTS[3])
  elif(percentRarity>97.5 and percentRarity<=99):
    QUESTS = random.choice(AVAILABLEQUESTS[4])
  elif(percentRarity>99 and percentRarity<=110):
    QUESTS = random.choice(AVAILABLEQUESTS[5])
  else:
    QUESTS = random.choice(AVAILABLEQUESTS[2])
  chosenQuest = random.choice(QUESTS)
  print(f"CHOSEN QUEST: {chosenQuest}")
  return chosenQuest


def QuestTemplates():
  """

  Example Quest:
  **Common Quest**
  |  Fish as many fish as you can within the time alloted
  |  More fish means more XP.
  |  
  |  Time Remaining: `0d 1h 19m`
  |  

  Arguments:
    Type: The type of the quest
    Experience: The expereince for the quest  (Quest XP * Rarity (1,2,3,4,6,8))
    Timer: The timer or deadline (in hours) of when the quest will end
  Types:
    Amount : Fish an amount of fish to complete the quest

  Timer:
    Example: 0d 5h 49m remaining

  """
  TEMPLATES = {
        #'Difficulty':{
          'Common':[
            {'Difficulty':'Common', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,30), 'Region':'Any', 'Type':'Any', 'Rarity':'Any'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(1,3)*1000},
            {'Difficulty':'Common', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,15), 'Region':'Any', 'Type':'Any', 'Rarity':'Uncommon'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(2,4)*1000},
            {'Difficulty':'Common', 'Type':'Amount', 'Requirements':{'Amount':random.randint(5,10), 'Region':'Any', 'Type':'Any', 'Rarity':'Rare'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(3,6)*1000},
          ], 'Uncommon':[
            {'Difficulty':'Uncommon', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,30), 'Region':'Any', 'Type':'Any', 'Rarity':'Any'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(1,3)*1000},
            {'Difficulty':'Uncommon', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,15), 'Region':'Any', 'Type':'Any', 'Rarity':'Uncommon'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(2,4)*1000},
            {'Difficulty':'Uncommon', 'Type':'Amount', 'Requirements':{'Amount':random.randint(5,10), 'Region':'Any', 'Type':'Any', 'Rarity':'Rare'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(3,6)*1000},
          ], 'Rare':[
            {'Difficulty':'Rare', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,30), 'Region':'Any', 'Type':'Any', 'Rarity':'Any'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(1,3)*1000},
            {'Difficulty':'Rare', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,15), 'Region':'Any', 'Type':'Any', 'Rarity':'Uncommon'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(2,4)*1000},
            {'Difficulty':'Rare', 'Type':'Amount', 'Requirements':{'Amount':random.randint(5,10), 'Region':'Any', 'Type':'Any', 'Rarity':'Rare'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(3,6)*1000},
          ], 'Epic':[
            {'Difficulty':'Epic', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,30), 'Region':'Any', 'Type':'Any', 'Rarity':'Any'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(1,3)*1000},
            {'Difficulty':'Epic', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,15), 'Region':'Any', 'Type':'Any', 'Rarity':'Uncommon'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(2,4)*1000},
            {'Difficulty':'Epic', 'Type':'Amount', 'Requirements':{'Amount':random.randint(5,10), 'Region':'Any', 'Type':'Any', 'Rarity':'Rare'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(3,6)*1000},
          ], 'Legendary':[
            #{'Type':'Amount', 'Requirements':{'Amount':random.randint(10,30), 'Region':CheckUserRegions(), 'Type':'Any', 'Rarity':'Any'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(1,3)*1000},
            {'Difficulty':'Legendary', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,30), 'Region':'Any', 'Type':'Any', 'Rarity':'Any'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(1,3)*1000},
            {'Difficulty':'Legendary', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,15), 'Region':'Any', 'Type':'Any', 'Rarity':'Uncommon'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(2,4)*1000},
            {'Difficulty':'Legendary', 'Type':'Amount', 'Requirements':{'Amount':random.randint(5,10), 'Region':'Any', 'Type':'Any', 'Rarity':'Rare'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(3,6)*1000},
          ], 'Exotic':[
            {'Difficulty':'Exotic', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,30), 'Region':'Any', 'Type':'Any', 'Rarity':'Any'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(1,3)*1000},
            {'Difficulty':'Exotic', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,15), 'Region':'Any', 'Type':'Any', 'Rarity':'Uncommon'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(2,4)*1000},
            {'Difficulty':'Exotic', 'Type':'Amount', 'Requirements':{'Amount':random.randint(5,10), 'Region':'Any', 'Type':'Any', 'Rarity':'Rare'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(3,6)*1000},
          ]
          #}
        }
  return TEMPLATES
ALLQUESTS = QuestTemplates()

def CheckUserRegions(ctx):
  return

def SortQuests():
  """ Call this method at the start of a certain time amount (Maybe 6 hours or so)
  """
  QUESTS=QuestTemplates()
  common=[]; uncommon=[]; rare=[]; epic=[]; legendary=[]; exotic=[]; daily=[]; event = []; sortedRarityArray=[]
  # for item in QUESTS:#['Difficulty']:
  #   print(f"Item: {item}\t|\tThings: {QUESTS[item]}")
  for item in QUESTS:#['Difficulty']:
    if   (item) == 'Common': 
      #print(f"Item: {item}")
      common.append(QUESTS[item])
    elif (item) == "Uncommon": uncommon.append(QUESTS[item])
    elif (item) == "Rare": rare.append(QUESTS[item])
    elif (item) == "Epic": epic.append(QUESTS[item])
    elif (item) == "Legendary": legendary.append(QUESTS[item])
    elif (item) == "Exotic": exotic.append(QUESTS[item])
    elif (item) == "Daily": daily.append(QUESTS[item])
    elif (item) == "Event": event.append(QUESTS[item])

  #sortedRarityArray.append([common, uncommon, rare, epic, legendary, exotic, daily, event])
  sortedRarityArray.append(common)
  sortedRarityArray.append(uncommon)
  sortedRarityArray.append(rare)
  sortedRarityArray.append(epic)
  sortedRarityArray.append(legendary)
  sortedRarityArray.append(exotic)
  sortedRarityArray.append(daily)
  sortedRarityArray.append(event)
  return sortedRarityArray
# Temporary
AVAILABLEQUESTS = SortQuests()

def DailyEvent():
  TEMPLATES = {
        #'Difficulty':{
          'Common':[
            {'Difficulty':'Common', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,30), 'Region':'Any', 'Type':'Any', 'Rarity':'Any'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(1,3)*1000},
            {'Difficulty':'Common', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,15), 'Region':'Any', 'Type':'Any', 'Rarity':'Uncommon'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(2,4)*1000},
            {'Difficulty':'Common', 'Type':'Amount', 'Requirements':{'Amount':random.randint(5,10), 'Region':'Any', 'Type':'Any', 'Rarity':'Rare'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(3,6)*1000},
          ], 'Uncommon':[
            {'Difficulty':'Uncommon', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,30), 'Region':'Any', 'Type':'Any', 'Rarity':'Any'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(1,3)*1000},
            {'Difficulty':'Uncommon', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,15), 'Region':'Any', 'Type':'Any', 'Rarity':'Uncommon'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(2,4)*1000},
            {'Difficulty':'Uncommon', 'Type':'Amount', 'Requirements':{'Amount':random.randint(5,10), 'Region':'Any', 'Type':'Any', 'Rarity':'Rare'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(3,6)*1000},
          ], 'Rare':[
            {'Difficulty':'Rare', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,30), 'Region':'Any', 'Type':'Any', 'Rarity':'Any'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(1,3)*1000},
            {'Difficulty':'Rare', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,15), 'Region':'Any', 'Type':'Any', 'Rarity':'Uncommon'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(2,4)*1000},
            {'Difficulty':'Rare', 'Type':'Amount', 'Requirements':{'Amount':random.randint(5,10), 'Region':'Any', 'Type':'Any', 'Rarity':'Rare'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(3,6)*1000},
          ], 'Epic':[
            {'Difficulty':'Epic', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,30), 'Region':'Any', 'Type':'Any', 'Rarity':'Any'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(1,3)*1000},
            {'Difficulty':'Epic', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,15), 'Region':'Any', 'Type':'Any', 'Rarity':'Uncommon'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(2,4)*1000},
            {'Difficulty':'Epic', 'Type':'Amount', 'Requirements':{'Amount':random.randint(5,10), 'Region':'Any', 'Type':'Any', 'Rarity':'Rare'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(3,6)*1000},
          ], 'Legendary':[
            #{'Type':'Amount', 'Requirements':{'Amount':random.randint(10,30), 'Region':CheckUserRegions(), 'Type':'Any', 'Rarity':'Any'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(1,3)*1000},
            {'Difficulty':'Legendary', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,30), 'Region':'Any', 'Type':'Any', 'Rarity':'Any'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(1,3)*1000},
            {'Difficulty':'Legendary', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,15), 'Region':'Any', 'Type':'Any', 'Rarity':'Uncommon'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(2,4)*1000},
            {'Difficulty':'Legendary', 'Type':'Amount', 'Requirements':{'Amount':random.randint(5,10), 'Region':'Any', 'Type':'Any', 'Rarity':'Rare'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(3,6)*1000},
          ], 'Exotic':[
            {'Difficulty':'Exotic', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,30), 'Region':'Any', 'Type':'Any', 'Rarity':'Any'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(1,3)*1000},
            {'Difficulty':'Exotic', 'Type':'Amount', 'Requirements':{'Amount':random.randint(10,15), 'Region':'Any', 'Type':'Any', 'Rarity':'Uncommon'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(2,4)*1000},
            {'Difficulty':'Exotic', 'Type':'Amount', 'Requirements':{'Amount':random.randint(5,10), 'Region':'Any', 'Type':'Any', 'Rarity':'Rare'}, 'Experience':500, 'Timer':random.randint(3,6), 'Award':random.randint(3,6)*1000},
          ]
          #}
        }
  return


