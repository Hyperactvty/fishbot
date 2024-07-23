import datetime, time, calendar
#from datetime import timedelta, datetime
import random, math

# Have this change every 10 mins or so.
def WorldEnviroment():
  enviroment = {
      'WEATHER':{
        'CurrentWeather':'Clear',
        'Clear':{
          'Name':'Clear', 'WaterState':'Wavy', 'CurrentTemp':15
        },'Calm':{
          'Name':'Clear', 'WaterState':'Calm', 'CurrentTemp':15
        }, 'Rainy':{
          'Name':'Rainy', 'WaterState':'Wavy', 'CurrentTemp':15
        }, 'Stormy':{
          'Name':'Stormy', 'WaterState':'Very Wavy', 'CurrentTemp':15
        }, 'Foggy':{
          'Name':'Foggy', 'WaterState':'Wavy', 'CurrentTemp':15
        }, 'Cloudy':{
          'Name':'Cloudy', 'WaterState':'Wavy', 'CurrentTemp':15
        }
      }, 'TIME':{
        'CurrentTime':0, 'Times':['Dusk', 'Night', 'Dawn', 'Day']
      }, 'SEASON': {
        'CurrentSeason':1, 'SeasonDay':0, 'Seasons':['Spring', 'Summer', 'Autumn', 'Winter']
      }, 'NATURAL_EVENTS':{
        'Tsunami':{
          'MinTimeAfterPrev':4
        }, 'LunarEclipse':{
          'Requirments':{'Time':'Night'}
        }
      }, 'FORECAST': [[[],[],[],[],[]],[[],[],[],[],[]],[15,15,15,15,15]]
      
    }
  print(f"Enviroment: {enviroment}")
  GetForcast(enviroment)
  return enviroment

def ChangeWorldEnviroment(currentEnviroment):
  
  #print(currentEnviroment)
  #changedEnviroment=currentEnviroment#{'WEATHER':None, 'TIME':None, 'SEASON':None}
  #checkIfSeasonChange = datetime.time.minute() % 3
  currentMinuteCalculation = (
    ( (datetime.datetime.now().date().year - 2021) * 525600) +
    ( (datetime.datetime.now().date().month) * 43800) +
    ( (datetime.datetime.now().date().day) * 1440) +
    ( (datetime.datetime.now().time().hour) * 60 ) +
    ( (datetime.datetime.now().time().minute))
  )
  #totalMinutesInDay= (math.floor(datetime.datetime.now().time().hour) * 60 ) + (datetime.datetime.now().time().minute)
  print(currentMinuteCalculation)
  # The Season Changer
  if(currentMinuteCalculation % 100 == 0):
    prevSeasonInt=currentEnviroment['SEASON']['CurrentSeason']
    seasonInt=prevSeasonInt+1
    if(seasonInt>3): seasonInt=0
    prevSeason=currentEnviroment['SEASON']['Seasons'][prevSeasonInt]; newSeason=currentEnviroment['SEASON']['Seasons'][seasonInt]
    print(f'Season Changing: {prevSeason} -> {newSeason}')
    currentEnviroment['SEASON']['CurrentSeason'] = seasonInt

  # The Weather Changer
  #if(datetime.datetime.now().time().minute % 1==0): # % 5, 10, or 15 by steps of 5
  if(currentMinuteCalculation % 15==0): #(random.randrange(5,15,5))==0): # % 5, 10, or 15 by steps of 5
    weatherChoice=currentEnviroment['FORECAST'][1][0]
    GetForcast(currentEnviroment)
    print("CALLED NEW WEATHER NETWORK")
    print(f'Weather Changing: {weatherChoice}')
    currentEnviroment['WEATHER']['CurrentWeather'] = weatherChoice

  # The Time Changer
  #if(datetime.datetime.now().time().minute % 1==0): # 5
  if(currentMinuteCalculation % 5==0): # 5
    currentEnviroment['TIME']['CurrentTime']+=1
    timeInt=currentEnviroment['TIME']['CurrentTime']
    if(timeInt>3): timeInt=0; currentEnviroment['SEASON']['SeasonDay']+=1;currentEnviroment['TIME']['CurrentTime']=0
    
    
    # To Ease into the seasons
    if(currentEnviroment['SEASON']['SeasonDay']>=20): currentEnviroment['SEASON']['SeasonDay']=0

    newTime=currentEnviroment['TIME']['Times'][timeInt]
    print(f'Time Changing: {newTime}')
    currentEnviroment['SEASON']['CurrentTime'] = timeInt

  

  return currentEnviroment

def GetWeather(currentEnviroment, iterr):
    weatherChoice='Clear' # Clear is default
    # Determine the weather based off of the current season
    """SPRING"""
    if(int(currentEnviroment['SEASON']['CurrentSeason'])==0): 
        availableWeather=['Calm','Rainy','Stormy','Foggy', 'Cloudy'];weatherPercentages=[[10,15],[15,35],[35,45],[45,65],[65,80]]
        randomPercent = random.random() * 100; iteration=0; currentEnviroment['WEATHER']['CurrentWeather']=0
        for iter in weatherPercentages:
          #print(f'Weather : {iter[0]} - {iter[1]}\t{randomPercent}')
          if(randomPercent>=iter[0] and randomPercent<iter[1]): 
            #print(f'Found New Weather: {availableWeather[iteration]}'); 
            weatherChoice = availableWeather[iteration]
          iteration+=1
    """SUMMER"""
    if(int(currentEnviroment['SEASON']['CurrentSeason'])==1): 
        availableWeather=['Calm','Rainy','Stormy','Foggy', 'Cloudy'];weatherPercentages=[[10,30],[30,45],[45,50],[50,60],[60,75]]
        randomPercent = random.random() * 100; iteration=0; currentEnviroment['WEATHER']['CurrentWeather']=0
        for iter in weatherPercentages:
          #print(f'Weather : {iter[0]} - {iter[1]}\t{randomPercent}')
          if(randomPercent>=iter[0] and randomPercent<iter[1]): 
            #print(f'Found New Weather: {availableWeather[iteration]}'); 
            weatherChoice = availableWeather[iteration]
          iteration+=1
    """Autumn"""
    if(int(currentEnviroment['SEASON']['CurrentSeason'])==2): 
        availableWeather=['Calm','Rainy','Stormy','Foggy', 'Cloudy'];weatherPercentages=[[10,30],[30,45],[45,50],[50,60],[60,75]]
        randomPercent = random.random() * 100; iteration=0; currentEnviroment['WEATHER']['CurrentWeather']=0
        for iter in weatherPercentages:
          #print(f'Weather : {iter[0]} - {iter[1]}\t{randomPercent}')
          if(randomPercent>=iter[0] and randomPercent<iter[1]): 
            #print(f'Found New Weather: {availableWeather[iteration]}'); 
            weatherChoice = availableWeather[iteration]
          iteration+=1
    """WINTER"""
    if(currentEnviroment['SEASON']['CurrentSeason']==3): 
        availableWeather=['Calm','Rainy','Stormy','Foggy', 'Cloudy'];weatherPercentages=[[10,30],[30,45],[45,50],[50,60],[60,75]]
        randomPercent = random.random() * 100; iteration=0; currentEnviroment['WEATHER']['CurrentWeather']=0
        for iter in weatherPercentages:
          #print(f'Weather : {iter[0]} - {iter[1]}\t{randomPercent}')
          if(randomPercent>=iter[0] and randomPercent<iter[1]): 
            #print(f'Found New Weather: {availableWeather[iteration]}'); 
            weatherChoice = availableWeather[iteration]
          iteration+=1
        #if(random.randint() * 7==2 and weatherChoice == 'Rainy'):
        #  print("Freezing Rain/ Hail")
    print(f'Weather {iterr} : {weatherChoice}')
    return weatherChoice
    
    
      
    

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


def GetForcast(currentEnviroment):
  forcastString="```fix\n"
  cE=currentEnviroment; currentTime=datetime.datetime.now()

  dt = datetime.time(hour=currentTime.time().hour, minute=currentTime.time().minute,microsecond=1)
  #dt = datetime.time(hour=currentTime.time().hour, minute=30,microsecond=1)
  print(dt)
  #print(math.ceil(dt.minute//15*15))
  print(math.ceil((math.ceil(dt.minute/15)) )*15)# *(currentTime.time().second/100)

  itr=0; w_hour=currentTime.time().hour; w_minute=currentTime.time().minute
  w_minute = (math.ceil((math.ceil(dt.minute/15))  )*15)
  print(f'E: {w_minute}')
  for column in range(0,5):
    #w_minute = math.ceil(( dt.microsecond/10)+(math.ceil(w_minute/15))  )*15
    
#    if(nextInterval>=60): nextInterval=nextInterval%60
    if(w_minute>=60): w_minute=w_minute%60; w_hour+=1
    if(w_hour>=24): w_hour=w_hour%24
    print(f'{w_hour:02}:{w_minute:02}')
    currentEnviroment['FORECAST'][0][itr] = f'{w_hour:02}:{w_minute:02}'
    currentEnviroment['FORECAST'][1][itr] = GetWeather(currentEnviroment,column)
    w_minute+=15
    itr+=1
  
  for column in range(0, 5):
    forcastString+=f"{currentEnviroment['FORECAST'][0][column]}\t"
  forcastString+='\n'
  for column in range(0, 5):
    forcastString+=f"{currentEnviroment['FORECAST'][1][column]}\t"
  forcastString+='\n'
  for column in range(0, 5):
    forcastString+=f"{currentEnviroment['FORECAST'][2][column]}°c\t"
  #dt = datetime.time(hour=currentTime.time().hour, minute=w_minute)
  
  #mod_time = datetime.datetime.time(dt.hour, dt.minute//15*15)
  print(f'{currentTime} -> {dt}')
  
  print(currentEnviroment['FORECAST'])
  # The footer of the text
  forcastString+="```Note: Weather isn't 100% accurate. Weather may change at any given point."
  return forcastString

def GenerateForecastEmbed(currentEnviroment):
  forcastString="```fix\n"

  for column in range(0, 5):
    forcastString+=f"{str(currentEnviroment['FORECAST'][0][column]).ljust(8)}"
    if(column==4):break
    forcastString+='|\t'
  forcastString+='\n'
  for column in range(0, 5):
    forcastString+=f"{str(currentEnviroment['FORECAST'][1][column]).ljust(8)}"
    if(column==4):break
    forcastString+='|\t'
  forcastString+='\n'
  for column in range(0, 5):
    forcastString+=(f"{currentEnviroment['FORECAST'][2][column]}°c").ljust(8)
    if(column==4):break
    forcastString+='|\t'

  forcastString+="```Note: Weather isn't 100% accurate. Weather may change at any given point."
  return forcastString