from PIL import Image, ImageDraw, ImageFont
import math
import re
import c_UtilityMethods as UM

def Oeuf():
        return ("eggw")

img_Ribbon = Image.open("ImagesForTesting/Ribbon.png")
#img_Ribbon = Image.open("FishBotItems/ImagesForTesting/Ribbon.png")
myFont = ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/AMATIC-REGULAR.ttf', 80)

#img_Sunset0 = Image.open("FishBot_py3.8/ImagesForTesting/african-sunset-clipart-2.jpg")
#img_Sunset1 = Image.open("FishBot_py3.8/ImagesForTesting/duskmaybe.jfif")
#img_FishTemplate = Image.open("FishBot_py3.8/ImagesForTesting/fishbotNewLayout.png")

img_Sunset0 = Image.open("ImagesForTesting/african-sunset-clipart-2.jpg")
img_Sunset1 = Image.open("ImagesForTesting/duskmaybe.jfif")
img_FishTemplate = Image.open("ImagesForTesting/fishbotNewLayout.png")

class c_GenerateFishImage(object):
    print("EGG")
    #myFont = ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/AMATIC-REGULAR.ttf', 80)
    print("Font Loaded")

    def GenerateFishAnimation():
        print("This")

    def Gen_A_An(word):
        a_an = re.search("[aeiouAEIOU]", word[0])
        if(a_an): return ("an")
        return ("a")

    def GenerateFishAnimation(fishName):

            images = []
            # Have animation of struggling in water, then pull up as a sillohette, cue to white flash, then finally show the fish
            #water_l1 = Image.open("FishBotItems/ImagesForTesting/ws_2.gif")
            #img_Ribbon = Image.open("FishBotItems/ImagesForTesting/Ribbon.png")
  
            myFont = ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/AMATIC-REGULAR.ttf', 80)
            width = 800
            height= 600
            centerx = width // 2
            centery = height // 2

            color_1 = (255,255, 0)
            color_2 = (255, 0, 0)
            
            colVar_FADECOLOUR = 1 # The number for the fade colour
            col_WHITE = (47,49,54, 0)
            col_DISCORDEMBEDGRAY = (47,49,54, 255)
            #col_WHITE = (54,57,63, colVar_FADECOLOUR)

            max_radius = int(centerx * 1.5)
            step = 16

            if(len(fishName)>32):
                myFont = ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/AMATIC-REGULAR.ttf', int((width-50)/len(fishName)))
            
  
            for i in range(max_radius, 0, -step):

                if(i<10): i=0
                # (147, 49, 54) is an awesome red
                col_WHITE = (147,49,54, int((i/max_radius)*255))
                im = Image.new('RGBA', (width, height), col_DISCORDEMBEDGRAY)
                
                #myFont = ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/AMATIC-REGULAR.ttf', 40)
                #im.text((0, 0), "Dis a Fish", font=myFont, fill =(255, 0, 0))
                #im.show()
                #im.save("images/image_text.jpg")

                draw = ImageDraw.Draw(im)
                
                
                

                #draw.bitmap([0,0],img_Ribbon,color_2)


                imr = img_Ribbon.convert('RGBA')

                # Split into 4 channels
                r, g, b, a = imr.split()

                # Increase Reds
                r = r.point(lambda i: i * 1)

                # Decrease Greens
                g = g.point(lambda i: i * 1)

                #a = a.point(lambda i: 0)

                # Recombine back to RGB image
                result = Image.merge('RGBA', (r, g, b, a))
                draw.bitmap([0,0],result,col_WHITE)
                #draw.rectangle([0,0,width,height], col_WHITE)
                draw = ImageDraw.Draw(im)

                #im_rgba = img_Ribbon.copy()
                #im_rgba.putalpha(128)
                #draw = ImageDraw.Draw(im_rgba)
                

                # The Upper Text
                text = "You caught "+(c_GenerateFishImage.Gen_A_An(fishName))
                text_width, text_height = draw.textsize(text, myFont)
                position = ((width-text_width)/2,((height-text_height)/2)-200)
                draw.text(position, text, fill =(0, 0, 0), font=myFont,anchor=None,spacing=4,align='left',direction=None,features=None,language=None,stroke_width=8,stroke_fill=(255,255,255))

                # The Fish Text
                text = fishName
                text_width, text_height = draw.textsize(text, myFont)
                position = ((width-text_width)/2,((height-text_height)/2)+200)
                draw.text(position, text, fill =(255, 255, 255), font=myFont)

                draw.ellipse((centerx - i, centery - i,
                              centerx + i, centery + i),
                             fill = col_DISCORDEMBEDGRAY)
                             #fill = (47,149,54, int(255*0.25)))
                
                #draw.bitmap([0,centery+math.sin(math.radians(30))],water_l1); draw.bitmap([800,centery+math.sin(math.radians(30))],water_l1)
                #print(i)
                

                images.append(im)
  
            images[0].save('FishBot_py3.8/ImagesForTesting/pillow_imagedrawe.gif',
                           save_all = True, append_images = images[1:], 
                           optimize = False, duration = 5)
        
            if False:
                images = []
                # Have animation of struggling in water, then pull up as a sillohette, cue to white flash, then finally show the fish
                #water_l1 = Image.open("FishBotItems/ImagesForTesting/ws_2.gif")
                water_l1 = Image.open("FishBotItems/ImagesForTesting/Water_l1.png")
                water_l2 = Image.open("FishBotItems/ImagesForTesting/Water_l2.png")
  
                width = 800
                height= 600
                centerx = width // 2
                centery = height // 2

                color_1 = (0,255, 0)
                color_2 = (255, 0, 0)
                max_radius = int(centery * 1.5)
                step = 8
  
                for i in range(0, max_radius, step):
                    print("SINE: "+str(math.sin(math.radians(30))))
                    im = Image.new('RGB', (width, height), color_2)
                    draw = ImageDraw.Draw(im)
                    draw.ellipse((centerx - i, centery - i,
                                  centerx + i, centery + i),
                                 fill = color_1)
                    draw.bitmap([0+i,centery*math.sin(math.radians(i))],water_l1); draw.bitmap([-800+i,centery+(math.sin(math.radians(i))/3)],water_l1)
                    #draw.bitmap([0,centery+math.sin(math.radians(30))],water_l1); draw.bitmap([800,centery+math.sin(math.radians(30))],water_l1)

                    images.append(im)
  
                images[0].save('FishBot_py3.8/ImagesForTesting/pillow_imagedrawe.gif',
                               save_all = True, append_images = images[1:], 
                               optimize = False, duration = 5)
        
        #==========================================
        

            return ()

    def GeneratePhoneBannerAnimation():
      if('Sunset'=='Sunset'):
            img_Sunset0 = Image.open("FishBot_py3.8/ImagesForTesting/african-sunset-0.png")
            images = []
            # Have animation of struggling in water, then pull up as a sillohette, cue to white flash, then finally show the fish
            
            # On Calm, have clouds casually moving right to left on screes, or whatever.
            #img_Ribbon = Image.open("FishBotItems/ImagesForTesting/Ribbon.png")

            dayColour= tuple(int('ADCFE9'[i:i+2], 16) for i in (0, 2, 4))
            duskColour = tuple(int('ECC1B2'[i:i+2], 16) for i in (0, 2, 4))
            nightColour = tuple(int('08113B'[i:i+2], 16) for i in (0, 2, 4))
            dawnColour = tuple(int('E49759'[i:i+2], 16) for i in (0, 2, 4))
            niceBlack = tuple(int('272727'[i:i+2], 16) for i in (0, 2, 4))
  
            
            width = 800
            height= 100
            #height= 800
            centerx = width // 2
            centery = height // 2

            
            step = 16


            
            img_Sunset0copy = img_Sunset0.copy()
            ss0w,ss0h = img_Sunset0copy.size
            print(f"SIZES: {(math.floor(ss0w/10))}  {math.floor(ss0h/10)}")
            ssRS=img_Sunset0copy.resize((math.floor(ss0w/1.75),math.floor(ss0h/1.75)))
            for i in range( -150, 100, step):
                print(i)
                if(i<-150): i=-150
                bkgrnd = Image.new('RGBA', (width, height), dawnColour)
                
                # paste image giving dimensions
                bkgrnd.paste(ssRS, (-50, -200+i))
                

                images.append(bkgrnd)
            
            images[0].save('D:\The Discord Bot\FishBot_py3.8\ImagesForTesting\phoneBanner.gif',
                               save_all = True, append_images = images[1:], 
                               optimize = False, duration = 2)

            #im = Image.new('RGBA', (width, height), dawnColour)
                
            if False:
              bkgrnd = Image.new('RGBA', (width, height), dawnColour)
              img_Sunset2copy=img_Sunset2.copy()
              img_Sunset0copy = img_Sunset0.copy()
              ss0w,ss0h = img_Sunset0copy.size
              print(f"SIZES: {(math.floor(ss0w/10))}  {math.floor(ss0h/10)}")
              ssRS=img_Sunset0copy.resize((math.floor(ss0w/1.75),math.floor(ss0h/1.75)))
  
              # paste image giving dimensions
              bkgrnd.paste(ssRS, (-50, -200))

              bkgrnd.save('D:\The Discord Bot\FishBot_py3.8\ImagesForTesting\phoneBanner.png')
        
            if False:
                images = []
                # Have animation of struggling in water, then pull up as a sillohette, cue to white flash, then finally show the fish
                #water_l1 = Image.open("FishBotItems/ImagesForTesting/ws_2.gif")
                water_l1 = Image.open("FishBotItems/ImagesForTesting/Water_l1.png")
                water_l2 = Image.open("FishBotItems/ImagesForTesting/Water_l2.png")
  
                width = 800
                height= 600
                centerx = width // 2
                centery = height // 2

                color_1 = (0,255, 0)
                color_2 = (255, 0, 0)
                max_radius = int(centery * 1.5)
                step = 8
  
                for i in range(0, max_radius, step):
                    print("SINE: "+str(math.sin(math.radians(30))))
                    im = Image.new('RGB', (width, height), color_2)
                    draw = ImageDraw.Draw(im)
                    draw.ellipse((centerx - i, centery - i,
                                  centerx + i, centery + i),
                                 fill = color_1)
                    draw.bitmap([0+i,centery*math.sin(math.radians(i))],water_l1); draw.bitmap([-800+i,centery+(math.sin(math.radians(i))/3)],water_l1)
                    #draw.bitmap([0,centery+math.sin(math.radians(30))],water_l1); draw.bitmap([800,centery+math.sin(math.radians(30))],water_l1)

                    images.append(im)
  
                images[0].save('D:\The Discord Bot\FishBotItems\ImagesForTesting\pillow_imagedrawe.gif',
                               save_all = True, append_images = images[1:], 
                               optimize = False, duration = 5)
        
        #==========================================
        

            return ()
    
    def Oeuf():
        return ("egg")

col_WHITETEXT = (255,255,255)
#discordFont = ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/AMATIC-REGULAR.ttf', 30)
discordFont = ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/WHITNEY-BOOK.OTF', 30)

def FontShortener(text, isName):
  lengOfLvlStr=len(text)
  amtOfChars=32
  if(isName): amtOfChars=36
  print(f"""Length of Level text : {lengOfLvlStr}""")
  discordFont = ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/WHITNEY-BOOK.OTF', 30)
  if(lengOfLvlStr>amtOfChars): discordFont = ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/WHITNEY-BOOK.OTF', int(30*(30/lengOfLvlStr)))
  return discordFont

def GenerateFishOutputImage(fishData, currentRod, calc_rodBonus, amountOfRods, userLevel, userExp, userLevelUpMath, levelUpText,prestigeCount, percent, gainedExp):
  print(f'FishData:\n\t{fishData}')
  # For resetting the size
  discordFont = ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/WHITNEY-BOOK.OTF', 30)

  imgcopy_FishTemplate= img_FishTemplate.copy()
  ftw,fth = imgcopy_FishTemplate.size
  print(f"SIZES: {ftw}  {fth}")
  # Open template and get drawing context
  im = Image.new('RGBA', (800, 640), col_WHITETEXT)
  draw = ImageDraw.Draw(im)
  
  # paste image giving dimensions
  im.paste(imgcopy_FishTemplate,(0,0))
      
  
  #im = Image.open('progress.png').convert('RGB')
  

  try:
      # Text Time! 
      fishSet = "";
      if(fishData['Set']!=None): fishSet=fishData['Set']
      
      draw.text((40, 50), f"{fishData['Name']} {fishSet}", fill=col_WHITETEXT, font=FontShortener(f"{fishData['Name']} {fishSet}", False),spacing=4,align='left',stroke_width=0,stroke_fill=(255,255,255))
      draw.text((560, 50), f"{fishData['Rarity']} : {fishData['RarityBonus']}x", fill=fishData['RarityColour'].to_rgb(), font=discordFont,spacing=4,align='left',stroke_width=0,stroke_fill=(255,255,255))
      draw.text((40, 140), f"{fishData['Type']}", fill=col_WHITETEXT, font=discordFont,spacing=4,align='left',stroke_width=0,stroke_fill=(255,255,255))
      # Limit Level Field to 32 Chars
      #t_width, t_height = draw.textsize(text_CENTER, font)
      #pos_Level= ((550-t_width)/2,-8)
      lengOfLvlStr=len(f"Lvl {userLevel}: {((userLevel/20)+1)}x\t|\t{UM.comma(round(userExp,2))}/{UM.comma(userLevelUpMath)} {levelUpText}")
      print(f"""Length of Level text : {lengOfLvlStr}""")
      if(lengOfLvlStr>32): discordFont = ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/WHITNEY-BOOK.OTF', int(30*(30/lengOfLvlStr)))
      #if(lengOfLvlStr>32): discordFont = ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/WHITNEY-BOOK.OTF', int(550/(lengOfLvlStr)))
      draw.text((370, 140), f"Lvl {userLevel}: {((userLevel/20)+1)}x\t|\t{UM.comma(round(userExp,2))}/{UM.comma(userLevelUpMath)} {levelUpText}", fill=col_WHITETEXT, font=discordFont,spacing=4,align='left',stroke_width=0,stroke_fill=(255,255,255))
      draw.text((370, 200), f"{fishData['TrophyText']}", fill=col_WHITETEXT, font=discordFont,spacing=4,align='left',stroke_width=0,stroke_fill=(255,255,255))
      # For resetting the size
      discordFont = ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/WHITNEY-BOOK.OTF', 30)
      draw.text((40, 230), f"{currentRod} - {round(fishData['RodBonus'],3)} ({amountOfRods} x {calc_rodBonus})", fill=col_WHITETEXT, font=discordFont,spacing=4,align='left',stroke_width=0,stroke_fill=(255,255,255))
      draw.text((40, 320), f"{fishData['Regions']}", fill=col_WHITETEXT, font=discordFont,spacing=4,align='left',stroke_width=0,stroke_fill=(255,255,255))
      #discordFont = ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/WHITNEY-BOOK.OTF', 12)
      discordFont = ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/WHITNEY-BOOK.OTF', 30)
      draw.text((40, 410), f"{UM.comma(float(round(fishData['FishingReward'],2)))} pts", fill=col_WHITETEXT, font=discordFont,spacing=4,align='left',stroke_width=0,stroke_fill=(255,255,255))
      discordFont = ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/WHITNEY-BOOK.OTF', 20)
      draw.text((40, 500), f"{round(percent,2)}% / 100%\t|\tExp: {UM.comma(round(gainedExp,2))}", fill=col_WHITETEXT, font=discordFont,spacing=4,align='left',stroke_width=0,stroke_fill=(255,255,255))
      
      #draw.text((5, -8), text_LEFT, fill=col_WHITETEXT, font=discordFont,anchor=None,spacing=4,align='left',direction=None,features=None,language=None,stroke_width=1,stroke_fill=(255,255,255))
      #draw.text(centerPosition, text_CENTER, fill=col_WHITETEXT, font=discordFont,anchor=None,spacing=4,align='center',direction=None,features=None,language=None,stroke_width=1,stroke_fill=(255,255,255))
      #draw.text((755, -8), text_RIGHT, fill=col_WHITETEXT, font=discordFont,anchor=None,spacing=4,align='left',direction=None,features=None,language=None,stroke_width=1,stroke_fill=(255,255,255))
      
      # Save result
      im.save('FishBot_py3.8/ImagesForTesting/generatedFishStatsImage.png')
  except Exception as e: print(f'GENERATEFISHOUTPUTIMAGE ERROR:\t{e}')

  




