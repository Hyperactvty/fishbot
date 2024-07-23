import os.path
import Fish as F, c_UtilityMethods as UM
import pyodbc#For the MYSQL stuff

# Define a filename.
filename = "D:\The Discord Bot\FishBot_py3.8\Fish2.txt"

def ReadInputs():
  if not os.path.isfile(filename):
      print('File does not exist.')
  else:
  # Open the file as f.
  # The function readlines() reads the file.
    with open(filename) as f:
      content = f.read().splitlines()

  # Show the file contents line by line.
  # We added the comma to print single newlines and not double newlines.
  # This is because the lines contain the newline character '\n'.
    #for line in content:
    #  print(line)
    
    return content

#def SeperateValues(content):
#  processedValues=[]
#  for line in content:
#    tempFishString = line.split(',')
#    fv=FixFishValues(tempFishString)

#    # FISH_ID: int, name: str, fish_type: str, rarity: str, fish_set: str, regions: [], 
#    # MIN_WEIGHT: float, MAX_WEIGHT: float, MIN_LENGTH: float, MAX_LENGTH: float, MIN_WIDTH: float, MAX_WIDTH: float,
#    # trophy_Sizes: {}):
#    print(line)
    
#    processedValues.append(F.PutFishIntoDict(FISH_ID=fv[0], name=fv[3], fish_type=fv[2], rarity=fv[4], fish_set=fv[5], regions=fv[1], 
#                MIN_WEIGHT=fv[6], MAX_WEIGHT=fv[7], MIN_LENGTH=fv[8], MAX_LENGTH=fv[9], MIN_WIDTH=fv[10], MAX_WIDTH=fv[11],
#                trophy_Sizes=fv[12]))
    
  
#  return processedValues

"""
  Below was for the textfile to the database
"""
def SeperateValues(content):
  processedValues=[]
  with pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=FishbotDatabase') as conn:
    conn.autocommit = True; cursor = conn.cursor()
    for line in content:
      tempFishString = line.split(',')
      fv=FixFishValues(tempFishString)

      # FISH_ID: int, name: str, fish_type: str, rarity: str, fish_set: str, regions: [], 
      # MIN_WEIGHT: float, MAX_WEIGHT: float, MIN_LENGTH: float, MAX_LENGTH: float, MIN_WIDTH: float, MAX_WIDTH: float,
      # trophy_Sizes: {}):
      print(line)
      #FISH_ID]      
      #Regions]      
      #FishType]     
      #FishName]     
      #Rarity]       
      #SetName]      
      #MIN_WEIGHT]   
      #MAX_WEIGHT]   
      #MIN_LENGTH]   
      #MAX_LENGTH]   
      #MIN_WIDTH]    
      #MAX_WIDTH]    
      #AVG_DEPTH]    
      #Preferred_Bait
      #Nocturnal]    
      #Seasonal]     
      FISHLIST = [fv[0], UM.Str.ConvertListToItem(fv[1]).strip("'"), fv[2], fv[3], fv[4], str(fv[5]),
                  fv[6], fv[7], fv[8], fv[9], fv[10], fv[11]]
      FISHLIST = str(FISHLIST)[1:-1]
      #FISHLIST = str(FISHLIST).replace("'",'"')
      print(f'''INSERT INTO FISH(FISH_ID, Regions, FishType, FishName, Rarity, SetName,MIN_WEIGHT, MAX_WEIGHT, MIN_LENGTH, MAX_LENGTH, MIN_WIDTH, MAX_WIDTH) VALUES({FISHLIST})''')
      cursor.execute(f'''INSERT INTO FISH(FISH_ID, Regions, FishType, FishName, Rarity, SetName,
      MIN_WEIGHT, MAX_WEIGHT, MIN_LENGTH, MAX_LENGTH, MIN_WIDTH, MAX_WIDTH) VALUES({FISHLIST})''')
    
      processedValues.append(F.PutFishIntoDict(FISH_ID=fv[0], name=fv[3], fish_type=fv[2], rarity=fv[4], fish_set=fv[5], regions=fv[1], 
                  MIN_WEIGHT=fv[6], MAX_WEIGHT=fv[7], MIN_LENGTH=fv[8], MAX_LENGTH=fv[9], MIN_WIDTH=fv[10], MAX_WIDTH=fv[11],
                  trophy_Sizes=fv[12]))
    
  cursor.close()
  return processedValues

def TxtToDB(content):
  regionList=[]
  try:
    if(int(content[1])==1): content[1]='Pond'
    elif(int(content[1])==2): content[1]="Lake"
    elif(int(content[1])==3): content[1]="Tropical"
    elif(int(content[1])==4): content[1]="Pirate Cove"
    elif(int(content[1])==5): content[1]="Daily"
    elif(int(content[1])==6): content[1]="Ocean"
    elif(int(content[1])==7): content[1]="Mystical"
  except:
    pass

def FixFishValues(content):
  formattedLine=[]
  
  content[0]=int(content[0])
  if(content[1]==''): content[1]=["Lake"]
  else: 
    try:
      if(int(content[1])==1): content[1]='Pond'
      elif(int(content[1])==2): content[1]="Lake"
      elif(int(content[1])==3): content[1]="Tropical"
      elif(int(content[1])==4): content[1]="Pirate Cove"
      elif(int(content[1])==5): content[1]="Daily"
      elif(int(content[1])==6): content[1]="Ocean"
      elif(int(content[1])==7): content[1]="Mystical"
    except:
      pass
    content[1]=[content[1]]
  content[2]=content[2].strip('"')
  content[3]=content[3].strip('"')
  content[4]=content[4].strip('"')
  if(content[5]==''): content[5]=None
  else: content[5]=content[5].strip('"')

  for iter in range(6,12):
    content[iter] = float(content[iter])

  # For the Trophy Sizes
  # {'Bronze':60, 'Silver':75, 'Gold':85, 'Platinum':90, 'Ruby':95, 'Diamond':97.5}
  temp_content={'Bronze':60, 'Silver':75, 'Gold':85, 'Platinum':90, 'Ruby':95, 'Diamond':97.5}
  temp_content['Bronze']=(float(content[12])) # Bronze
  temp_content['Silver']=(float(content[13])) # Silver
  temp_content['Gold']=(float(content[14])) # Gold
  temp_content['Platinum']=(float(content[15])) # Platinum
  temp_content['Ruby']=(float(content[16])) # Ruby

  for popElems in range(12,17):
    content.pop(12)

  
  try:
    if (content[17]): 
      temp_content['Diamond']=(float(content[17])) # Diamond
      content.pop(17)
      formattedLine = content
      formattedLine.append(temp_content)
  except:
    temp_content['Diamond']=(97.5) # Diamond
    formattedLine = content
    formattedLine.append(temp_content)

  #print(formattedLine)


  return formattedLine