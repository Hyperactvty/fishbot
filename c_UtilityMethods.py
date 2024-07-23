import math, re
import locale#For the commas in numbers
locale.setlocale(locale.LC_ALL, 'en_US.utf8')
import sys, traceback
import discord, pyodbc
import datetime, calendar
from PIL import Image, ImageDraw, ImageFont
import c_PillowVariables as PILVar, c_ItemValues as IV, c_Database as D

class Str: 
  def Plural(word):
    if(type(word)==list):
      if(len(word)>1):
        return 's'
    return ''

  def Apostrophe(word):
    if(str(word)[-1]=='s'):
        return "'"
    return "'s"

  def ConvertListToItem(word):
    if(type(word)==list):
      return str(str(word).replace("[", "")).replace("]","")
    return word

  def ListWithAnd(word):
    print(f"WORD {word}")
    #wordAnd = ConvertListToItem(word)
    wordAnd = str(str(word).replace("[", "")).replace("]","")
    print(wordAnd)
    k = wordAnd.rfind(",")
    print(k)
    wordAnd = wordAnd[:k] + " and" + wordAnd[k+1:]
    print(wordAnd)
    return wordAnd

  def IsAre(word):
    print(type(word))
    if(type(word)==list):
      if(len(word)>1): return 'are'
    return 'is'

  def Rank(num):
    return f"""{str("%d%s" % (num,"tsnrhtdd"[(math.floor(num/10)%10!=1)*(num%10<4)*num%10::4]))}"""
    
#The Comma Method
def comma(dataToHaveCommas):
    try: 
      splitter=str(dataToHaveCommas).split(".")
      commatose=locale.format_string("%d", int(splitter[0]), grouping=True)
      finalProduct=str(commatose)+"."+(str(splitter[1]))
      return(finalProduct)
    except: 
      commatose=locale.format_string("%d", int(dataToHaveCommas), grouping=True)
      print(commatose)
      #finalProduct=str(commatose)+"."+(str(splitter[1]))
      return(commatose)

def ShopTimer():
  ct = datetime.datetime.now()
  currentTime = datetime.datetime(ct.year, ct.month, ct.day, hour=ct.hour, minute=ct.minute, second=ct.second)
  future = datetime.datetime(ct.year, ct.month, ct.day, 4, 0, 0)
  if(ct.hour<4): future = datetime.datetime(ct.year, ct.month, ct.day, 4, 0, 0)
  elif(ct.hour>=4 and ct.hour<16): future = datetime.datetime(ct.year, ct.month, ct.day, 16, 0, 0)
  elif(ct.hour>=16): future = datetime.datetime(ct.year, ct.month, ct.day, 4, 0, 0)
  difference = future - currentTime 
      
  checkRemainingHours=difference.seconds//3600; checkRemainingMins = (difference.seconds//60)%60; checkRemainingSecs=difference.seconds%60
  return checkRemainingHours,checkRemainingMins,checkRemainingSecs

def createErrorMessage(e):
    last_type, last_value, last_traceback = sys.exc_info()
    type, value, tb = sys.exc_info()
    sys.last_type = last_type
    sys.last_value = last_value
    sys.last_traceback = last_traceback

    tblist = traceback.extract_tb(tb)
    
    #del tblist[:1]
    list = traceback.format_list(tblist)
    #print("\n\tlist:\t"+str(list))
    if list:
        list.insert(0, "Traceback (most recent call last of thing [c_Cmds]):\n")
    list[len(list):] = traceback.format_exception_only(type, value)
    print("\n\tlist:\t"+str(list))

    errorText=""
    for err in range(0, len(list)):
        errorText += list[err]+"\n"

    print('\nA problem has occurred from the problematic code: ', e)
    errorMessageEmbed=discord.Embed(title="**An Error has Occurred**", description="Details:```py\n"+str(errorText)+"``````py\n"+str(e)+"```Send this error message to the support server here to receive a reward.", color=discord.Color.red())
    errorMessageEmbed.set_footer(text="ERRID: {errID} | If you have any questions or concerns, feel free to let Hyperactvty know.")#https://discord.gg/FrxSzXs
    return errorMessageEmbed

def Gen_A_An(word):
        a_an = re.search("[aeiouAEIOU]", word[0])
        if(a_an): return ("an")
        return ("a")

def GetDateName(*args):
  dayNames=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
  if(len(args)>0):
    return dayNames[args[0]]
  return dayNames[datetime.datetime.today().weekday()]

def GetDateMonthName(*args):
  
  now = datetime.datetime.now()-datetime.timedelta(days =datetime.datetime.today().weekday())
  endDate=now + datetime.timedelta(days = 6)
  #print(f"7 Day Period:\t{now}\t-\t{endDate}")
  fixedDate_Start = now.date().strftime("%c")
  fixedDate_End = endDate.date().strftime("%c")
  monthNames=["January","Febuary","March","April","May","June","July","August","September","October","November","December"]
  if(len(args)>0):
    #if(args[0]=='WeekStart'): return datetime.datetime.now()-datetime.timedelta(days =datetime.datetime.today().weekday())
    #if(args[0]=='WeekEnd'):    now = datetime.datetime.now()-datetime.timedelta(days =datetime.datetime.today().weekday()); return now + datetime.timedelta(days = 6)

    #if(args[0]=='WeekStart'): return f"{fixedDate_Start[:3]}, {fixedDate_Start[7:10]} {fixedDate_Start[4:6]}"
    #if(args[0]=='WeekEnd'):   return f"{fixedDate_End[:3]}, {fixedDate_End[7:10]} {fixedDate_End[4:6]}"

    if(args[0]=='WeekStart'): return f"{now.date().strftime('%a, %B %d')}"
    if(args[0]=='WeekEnd'):   return f"{endDate.date().strftime('%a, %B %d')}"
  mon=datetime.datetime.today()
  return mon.strftime("%b")

def CreateFieldFromDict(dictVal, fieldType, ctx):
  embedField=[]; numberButtons=["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣",]
  numButton=0
  if(fieldType=='ROD'):
    for item in dictVal:
      try:
        print(item)
        splitString = str(item).split("_")
        itemPrice=IV.GetItemValues(f'{str(fieldType).upper()}S',f'Rod_{str(splitString[1]).capitalize()}')['Price']
        embedField.append({'name':f"{numberButtons[numButton]} {str(splitString[1]).capitalize()}", 'value':f"""```bash\n${round(D.GrabFromDB(ctx.author.id, 'USER_ITEM_ROD',f'Rod_{str(splitString[1]).capitalize()}')*itemPrice,2)+itemPrice}/ rod```"""})
      except: pass
      numButton+=1
  elif(fieldType=='REGION'):
    for item in dictVal:
      splitString = str(item).split("_")
      grabRegionFromDB = D.GrabFromDB(ctx.author.id, 'USER_ITEM_REGION',f'{item}')
      itemPrice=IV.GetItemValues(f'{str(fieldType).upper()}S',f'Region_{str(splitString[1]).capitalize()}')['Price']
      regionOwned = f'-\tNot Owned - {itemPrice}'
      if(grabRegionFromDB>=1): regionOwned = '+\tOwned and Available'
      embedField.append({'name':f"{numberButtons[numButton]} {splitString[1]}", 'value':f"""```diff\n{regionOwned}```"""})
      numButton+=1
  elif(fieldType=='LURE'):
    for item in dictVal:
      splitString = str(item).split("_")
      grabLureFromDB = D.GrabFromDB(ctx.author.id, 'USER_ITEM_LURE',f'{item}')
      itemPrice=IV.GetItemValues(f'{str(fieldType).upper()}S',f'Lure_{str(splitString[1]).capitalize()}')['Price']
      
      embedField.append({'name':f"{numberButtons[numButton]} {splitString[1]}", 'value':f"""```bash\n${round(itemPrice,2)}/ lure```"""})
      numButton+=1
  embedField.append({'name':"❌", 'value':"""```fix\nCloses the menu```"""})
  return embedField

def RequestUserToUpdate(ctx):
    generatedEmbed=discord.Embed(title="empty value",description="empty value", color=discord.Color.red())
    try:

          generatedEmbed=discord.Embed(title=f"Update Required", description=f"Please update your user data by using `f-update`", color=discord.Color.red())
       
    except Exception as e:
        print("Hit EXCEPT in RequestUserToUpdate")
        
        generatedEmbed=createErrorMessage(e)
    return generatedEmbed

def UpdateUserData(ctx):
  with pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=FishbotDatabase') as conn:
    conn.autocommit = True; cursor = conn.cursor(); #cursor.fast_executemany=True
    TABLES_TO_CHECK = ['USER_ITEM_BAIT','USER_ITEM_LURE','USER_ITEM_REGION','USER_ITEM_ROD','USER_TROPHYWALL']
    #try:
    #    conn.autocommit = False
    #    params = [ ('A', 1), ('B', 2) ]
    #    cursor.executemany(f"insert into {table}(Discord_ID) values (?)", params)
    #    break
    #except pyodbc.DatabaseError as err:
    #    conn.rollback()
    #else:
    #    conn.commit()
    #finally:
    #    conn.autocommit = True

    try:
      for table in TABLES_TO_CHECK:
        try:
          inTable=D.GrabFromDB(ctx.author.id, f'{table}', 'Discord_ID')
        except Exception as e:
          cursor.execute(f"""INSERT INTO {table}(Discord_ID) VALUES(?)""",ctx.author.id)
    except: pass
    #cursor.executemany(f"""INSERT INTO {table}(Discord_ID) VALUES(?)""",params)
    print(cursor.rowcount, "record(s) inserted")
    cursor.close()

def AutoCheckDatabase():
  # Get all users
  ALL_USERS = D.GrabFromDB_ALL("*", 'USERS', 'Discord_ID', 'a')
  print(f"All Users:\t{ALL_USERS}")
  TABLES_TO_CHECK = ['USER_ITEM_BAIT','USER_ITEM_LURE','USER_ITEM_REGION','USER_ITEM_ROD','USER_TROPHYWALL']
  for table in TABLES_TO_CHECK:
    ALL_USERS_IN_TABLE = D.GrabFromDB_ALL('*', table, 'Discord_ID', 'a')
    MISSING_MEMBERS=list(set(ALL_USERS) - set(ALL_USERS_IN_TABLE))
    print(f"\tMissing Members in {table}:\t{MISSING_MEMBERS}")
    try:
      #D.GrabFromDB_ALL('*', table, 'Discord_ID', 'a')
      with pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=FishbotDatabase') as conn:
        conn.autocommit = True; cursor = conn.cursor(); #cursor.fast_executemany=True
        #try:
        #    conn.autocommit = False
        #    params = [ ('A', 1), ('B', 2) ]
        #    cursor.executemany(f"insert into {table}(Discord_ID) values (?)", params)
        #    break
        #except pyodbc.DatabaseError as err:
        #    conn.rollback()
        #else:
        #    conn.commit()
        #finally:
        #    conn.autocommit = True
        for USERID in MISSING_MEMBERS:
          cursor.execute(f"""INSERT INTO {table}(Discord_ID) VALUES(?)""",USERID)
        #cursor.executemany(f"""INSERT INTO {table}(Discord_ID) VALUES(?)""",params)
        print(cursor.rowcount, "record(s) inserted")
        cursor.close()
        #break
    except Exception as e: print(f'\n\tError in AutoCheckDatabase:\t{e}\n'); return createErrorMessage(e)
  return

def CheckForUpdate(ctx):
  try:
    #D.
    print("Fix This")
  except:
    # Insert into the database
    print("Insert discord ID here")
  return

def CreateDiscordEmbedFromDict(tutorialPageClass):
    generatedEmbed=discord.Embed(title="empty value",description="empty value", color=discord.Color.red())
    #print("In CreateDiscordEmbedFromDict")
    try:
        try:
          #print(tutorialPageClass['Header']['color'])
          ###print(tuple(int(str(tutorialPageClass['Header']['color'])[i:i+2], 16) for i in (0, 2, 4)))
          #print(str(tutorialPageClass['Header']['title'])+"\t\t"+str(tutorialPageClass['Header']['description'])+"\t\t"+tutorialPageClass['Header']['color'])
          generatedEmbed=discord.Embed(title=str(tutorialPageClass['Header']['title']),description=str(tutorialPageClass['Header']['description']), color=tutorialPageClass['Header']['color'])
        except:
          generatedEmbed=discord.Embed(title=str(tutorialPageClass['Header']['title']),description=str(tutorialPageClass['Header']['description']), color=discord.Color.blurple())
        try:
          generatedEmbed.set_thumbnail(url=tutorialPageClass['Thumbnail'])
          #generatedEmbed.set_author(url=tutorialPageClass['Thumbnail'])
        except: pass#print("No Thumbnail")
        try:
          for field in range(0, len(tutorialPageClass['Fields'])):
            try:
              generatedEmbed.add_field(name=str(tutorialPageClass['Fields'][field]['name']),value=str(tutorialPageClass['Fields'][field]['value']), inline=str(tutorialPageClass['Fields'][field]['inline']))
            except:
              generatedEmbed.add_field(name=str(tutorialPageClass['Fields'][field]['name']),value=str(tutorialPageClass['Fields'][field]['value']))
        except: pass
        try:
          generatedEmbed.set_footer(text=str(tutorialPageClass['Footer']['text']), icon_url=str(tutorialPageClass['Footer']['icon_url']))
        except:
          generatedEmbed.set_footer(text=str(tutorialPageClass['Footer']))
        try:
          generatedEmbed.set_image(url=str(tutorialPageClass['Image']))
        except:
          pass
    except Exception as e:
        print("Hit EXCEPT in CreateDiscordEmbedFromDict")
        
        generatedEmbed=createErrorMessage(e)
    return generatedEmbed

def AssignMissingNumber(lst):
  return sorted(set(range(1, lst[-1])) - set(lst))
  #return [i for x, y in zip(lst, lst[1:]) 
  #      for i in range(x + 1, y) if y - x > 1]

def GenerateProgressBar(value, endProgress, *args):
  progressPercent = value/endProgress
  print(progressPercent)
  width = 800; height= 50
  col_DISCORDEMBEDGRAY = (47,49,54, 255)
  col_BACKGROUND = (54,57,63, 255)
  #col_BACKGROUND = (54,57,163, 255)
  # Open template and get drawing context
  im = Image.new('RGBA', (width, height), col_DISCORDEMBEDGRAY)
  #im = Image.open('progress.png').convert('RGB')
  draw = ImageDraw.Draw(im)

  # The Background Bar
  draw.ellipse([50,5,50+40,5+40], fill=col_BACKGROUND)
  draw.ellipse([700,5,700+40,5+40], fill=col_BACKGROUND)
  #draw.rectangle(xy=[50,5,700,45], value=col_BACKGROUND, thresh=40)
  #ImageDraw.floodfill(im, ([50,5],[700,45]), value=col_BACKGROUND, thresh=40)
  draw.rectangle((50+20,5,700+20,45), fill=col_BACKGROUND)

  # Cyan-ish fill colour
  color=(98,211,245)

  # Draw circle at right end of progress bar
  x, y, diam = 50, 5, 40
  draw.ellipse([x,y,x+diam,y+diam], fill=color)
  
  barLimit=700
  x, y, diam = (progressPercent*700), 5, 40
  draw.ellipse([x,y,x+diam,y+diam], fill=color)
  draw.rectangle((50+20,5,x+20,45), fill=color)

  try:
    if(args):
      # Text Time! 
      font=ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/AMATIC-REGULAR.ttf', 50)
      col_WHITE = (255,255,255,255)# PILVar.GetColour('col_WHITE')
      # The Current Level Text
      text_LEFT = f"{args[0]}"
      text_CENTER = f"{value}/{endProgress}"
      text_CENTER = f"{(comma(round(value,2)))}/{(comma(endProgress))}"
      text_RIGHT = f"{args[1]}"
      lenOfCenter=len(f"{text_CENTER}")
      text_width, text_height = draw.textsize(text_CENTER, font)
      centerPosition = ((width-text_width)/2,-8)
      draw.text((5, -8), text_LEFT, fill=col_WHITE, font=font,anchor=None,spacing=4,align='left',direction=None,features=None,language=None,stroke_width=1,stroke_fill=(255,255,255))
      draw.text(centerPosition, text_CENTER, fill=col_WHITE, font=font,anchor=None,spacing=4,align='center',direction=None,features=None,language=None,stroke_width=1,stroke_fill=(255,255,255))
      draw.text((755, -8), text_RIGHT, fill=col_WHITE, font=font,anchor=None,spacing=4,align='left',direction=None,features=None,language=None,stroke_width=1,stroke_fill=(255,255,255))
  except Exception as e: print(f"Error\t{e}")

  # Save result
  im.save('FishBot_py3.8/ImagesForTesting/progressbar.png')