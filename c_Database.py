import os
import c_FishData as FD, Fish as F
#import mysql.connector
import pyodbc#For the access stuff

def StartupFishGrab():
    fishList=[]
    # The start-up fishing Database check
    with pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=FishbotDatabase') as conn:
        conn.autocommit = True; cursor = conn.cursor()
        
        grabFishFromDB=cursor.execute(f"SELECT * FROM FISH")
        fishListGrab=grabFishFromDB.fetchall()
        itr=0
        for fish in fishListGrab:
          #print(f"Fish #{itr}\t{fish}")
          itr+=1
          fishVars=[]
          for fishColumn in fish:
            #print (fishColumn)
            fishVars.append(fishColumn)
          
          fv = fishVars
          toDict=F.PutFishIntoDict(FISH_ID=fv[0], name=fv[3], fish_type=fv[2], rarity=fv[4], fish_set=fv[5], regions=fv[1], 
                  MIN_WEIGHT=fv[6], MAX_WEIGHT=fv[7], MIN_LENGTH=fv[8], MAX_LENGTH=fv[9], MIN_WIDTH=fv[10], MAX_WIDTH=fv[11],
                  trophy_Sizes=None, preferred_Bait=fv[13], nocturnal=fv[14], seasonal=fv[15])
          fishList.append(toDict)
        cursor.close()
        print("Fish database is ready from 'database.py'.\n======================")
    return fishList
  

def CreateNewUser(userID):
  with pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=FishbotDatabase') as conn:
    conn.autocommit = True; cursor = conn.cursor()
    cursor.execute(f'''INSERT INTO USERS(Discord_ID) VALUES({userID})''')
    cursor.execute(f'''INSERT INTO USER_ITEM_ROD(Discord_ID) VALUES({userID})''')
    cursor.execute(f'''INSERT INTO USER_ITEM_REGION(Discord_ID) VALUES({userID})''')
    cursor.execute(f'''INSERT INTO USER_ITEM_LURE(Discord_ID) VALUES({userID})''')
    cursor.execute(f'''INSERT INTO USER_ITEM_BAIT(Discord_ID) VALUES({userID})''')
    cursor.execute(f'''INSERT INTO USER_TROPHYWALL(Discord_ID) VALUES({userID})''')
    cursor.execute(f'''INSERT INTO USER_ITEM(Discord_ID) VALUES({userID})''')
    cursor.close()
    print(f'CREATED NEW USER: {userID}')


def CheckIfUserExists(userID):
  try:
    #with pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\The Discord Bot\FishBot_py3.8\Fishbot3_8.accdb;') as conn:#
    with pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=FishbotDatabase') as conn:
      conn.autocommit = True; cursor = conn.cursor()
      grabUsersFromDB=cursor.execute(f"""SELECT Discord_ID FROM USERS WHERE Discord_ID = {userID}"""); userListGrab=grabUsersFromDB.fetchall()
      cursor.close()
      #print(f"User: {userListGrab}")
      if(str(userID) in str(userListGrab)): return True
      return False
  except Exception as e:
    print(f"Error: {e}")
    #cursor.close()
  

def GrabFromDB(userID : int, tableName: str, thingToSelect: str): # , *where
  with pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=FishbotDatabase') as conn:
    conn.autocommit = True; cursor = conn.cursor()
    grabFromDB=cursor.execute(f"""SELECT {thingToSelect} FROM {tableName} WHERE Discord_ID = {userID}"""); listGrab=grabFromDB.fetchone()
    cursor.close()
    for item in listGrab: return item

def GrabFromDB_WHERE(userID : int, tableName: str, thingToSelect: str, where, *amount): # *args
  with pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=FishbotDatabase') as conn:
    conn.autocommit = True; cursor = conn.cursor()
    grabFromDB=cursor.execute(f"""SELECT {thingToSelect} FROM {tableName} WHERE {where}""")
    listGrab=[]
    try: 
      print(amount[0])
      if(amount[0]=='a'): 
        listGrab=grabFromDB.fetchall()#; print (listGrab)
        cursor.close()
        returnList=[]
        for item in listGrab: 
          for item2 in item: 
            returnList.append(item2)
        return returnList
      if(amount[0]=='all'): 
        listGrab=grabFromDB.fetchall()#; print (listGrab)
        cursor.close()
        returnList=[]
        for item in listGrab: 
          itemSublist=[]
          for item2 in item: 
            itemSublist.append(item2)
            #print(f"Item 2:\t{item2}")
          returnList.append(itemSublist)
          #print(f"\tItem 1:\t{item}")
        return returnList
      if(amount[0]=='o'): 
        listGrab=grabFromDB.fetchone();# print (listGrab)
        cursor.close()
        returnList=[]
        for item in listGrab: 
          returnList.append(item)
        return returnList
        #for item in listGrab: return item
    except: listGrab=grabFromDB.fetchone()
    cursor.close()
    for item in listGrab: return item

def GrabFromDB_ALL(userID : int, tableName: str, thingToSelect: str, *amount): # *args
  with pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=FishbotDatabase') as conn:
    conn.autocommit = True; cursor = conn.cursor()
    grabFromDB=cursor.execute(f"""SELECT {thingToSelect} FROM {tableName}""")
    listGrab=[]
    try: 
      print(amount[0])
      if(amount[0]=='a'): 
        listGrab=grabFromDB.fetchall()#; print (listGrab)
        cursor.close()
        returnList=[]
        for item in listGrab: 
          for item2 in item: 
            returnList.append(item2)
        return returnList
      if(amount[0]=='all'): 
        try: 
          if(args[1]=='order'):
            print('In order')
            grabFromDB=cursor.execute(f"""SELECT {thingToSelect} FROM {tableName} ORDER BY {args[2]}""")
        except: pass
        listGrab=grabFromDB.fetchall()#; print (listGrab)
        cursor.close()
        returnList=[]
        for item in listGrab: 
          itemSublist=[]
          for item2 in item: 
            itemSublist.append(item2)
            #print(f"Item 2:\t{item2}")
          returnList.append(itemSublist)
          #print(f"\tItem 1:\t{item}")
        return returnList
      if(amount[0]=='o'): 
        listGrab=grabFromDB.fetchone();# print (listGrab)
        cursor.close()
        returnList=[]
        for item in listGrab: 
          returnList.append(item)
        return returnList
        #for item in listGrab: return item
    except: listGrab=grabFromDB.fetchone()
    cursor.close()
    for item in listGrab: return item

def InsertIntoDB(userID : int, tableName, columnsToUpdate, valuesToInsert):
  with pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=FishbotDatabase') as conn:
    conn.autocommit = True; cursor = conn.cursor()
    if(type(columnsToUpdate)==list): 
      SQLList_Column=""
      for listItem in columnsToUpdate: SQLList_Column+=f"{listItem}, "
      #SQLList_Column+=""
      SQLList_Insert=""
      for listItem in valuesToInsert: SQLList_Insert+=f"{listItem}, "
      #SQLList_Insert+=")"
      cursor.execute(f"""INSERT INTO {tableName}({SQLList_Column}) VALUES({SQLList_Insert})""")
      cursor.close()
      return
    #print(f'''INSERT INTO {tableName}({columnsToUpdate}) VALUES({valuesToInsert})''')
    cursor.execute(f'''INSERT INTO {tableName}({columnsToUpdate}) VALUES({valuesToInsert})''')
    cursor.close()
    #print(f'INSERTED NEW : INSERT INTO {tableName}({columnsToUpdate}) VALUES({valuesToInsert})')
    return

def UpdateDB(userID : int, tableName, thingToSelect, valuesToUpdate): # *args
  with pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=FishbotDatabase') as conn:
    conn.autocommit = True; cursor = conn.cursor()
    print(f"UPDATE {tableName} SET {thingToSelect}={valuesToUpdate} WHERE Discord_ID = {userID}")
    if(type(valuesToUpdate)==list): 
      SQLList_Update="("
      for listItem in valuesToUpdate: SQLList_Update+=f"{listItem}, "
      SQLList_Update+=")"
      SQLList_Select="("
      for listItem in thingToSelect: SQLList_Select+=f"{listItem}, "
      SQLList_Select+=")"
      cursor.execute(f"""UPDATE {tableName} SET {SQLList_Select}={SQLList_Update} WHERE Discord_ID = {userID}""")
      cursor.close()
      return
    cursor.execute(f"""UPDATE {tableName} SET {thingToSelect}={valuesToUpdate} WHERE Discord_ID = {userID}""")
    cursor.close()
    return valuesToUpdate

def UpdateDB_WHERE(userID : int, tableName, thingToSelect, valuesToUpdate, where, *args):
  with pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=FishbotDatabase') as conn:
    conn.autocommit = True; cursor = conn.cursor()
    print(f"UPDATE {tableName} SET {thingToSelect}={valuesToUpdate} WHERE {where}")
    try:
      if(args):
        #print("In Try 2")
        cursor.execute(f"""UPDATE {tableName} SET {thingToSelect}={valuesToUpdate} WHERE {where}""")
        print(cursor.rowcount, "record(s) updated")
        cursor.close()
      else:
        print(args[2]) # To force a break

    except:
      #print("In Except 0")
      if(type(valuesToUpdate)==list): 
        SQLList_Update="("
        for listItem in valuesToUpdate: SQLList_Update+=f"{listItem}, "
        SQLList_Update+=")"
        SQLList_Select="("
        for listItem in thingToSelect: SQLList_Select+=f"{listItem}, "
        SQLList_Select+=")"
        cursor.execute(f"""UPDATE {tableName} SET {SQLList_Select}={SQLList_Update} WHERE {where}""")
        print(cursor.rowcount, "record(s) updated")
        cursor.close()
        return
      #print("In Except 1")
      cursor.execute(f"""UPDATE {tableName} SET {thingToSelect}={valuesToUpdate} WHERE {where}""")
      print(cursor.rowcount, "record(s) updated")
      cursor.close()
      return valuesToUpdate

def DeleteFromDB(userID : int, tableName, *args): # *args
  with pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=FishbotDatabase') as conn:
    conn.autocommit = True; cursor = conn.cursor()
    try:
      if(args):
        if(args[0]=='*' and userID == None):
          cursor.execute(f"""DELETE FROM {tableName}""")
          print(cursor.rowcount, "record(s) deleted")
        if(args[0]=='*' and userID != None):
          cursor.execute(f"""DELETE FROM {tableName} WHERE Discord_ID = {userID}""")
          print(cursor.rowcount, "record(s) deleted")
      cursor.close()
      return
    except: 
      cursor.execute(f"""DELETE FROM {tableName} WHERE Discord_ID = {userID}""")
      print(cursor.rowcount, "record(s) deleted")
      cursor.close()
      return

def DeleteFromDB_WHERE(userID : int, tableName, where): # *args
  with pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=FishbotDatabase') as conn:
    conn.autocommit = True; cursor = conn.cursor()
    print(f"""DELETE FROM {tableName} WHERE {where}""")
    cursor.execute(f"""DELETE FROM {tableName} WHERE {where}""")
    print(cursor.rowcount, "record(s) deleted")
    cursor.close()
    return