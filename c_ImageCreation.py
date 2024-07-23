from PIL import Image, ImageDraw, ImageFont
import math
import re
import c_UtilityMethods as UM


img_SpinnerGraph0 = Image.open("FishBot_py3.8/images/wheelSpin0.png")
img_SpinnerGraph1 = Image.open("FishBot_py3.8/images/wheelSpin1.png")
img_SpinnerGraph2 = Image.open("FishBot_py3.8/images/wheelSpin2.png")
img_LabeledSpinner0 = Image.open("FishBot_py3.8/images/labeledWheelspin0.png")
img_Ticker = Image.open("FishBot_py3.8/images/ticker.png")
hyperFont = ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/AMATIC-REGULAR.ttf', 80)

col_WHITETEXT = (255,255,255)
col_DISCORDEMBEDGRAY = (47,49,54, 255)
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

def GenerateWheelspine(chance):
  
  # For resetting the size
  discordFont = ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/WHITNEY-BOOK.OTF', 30)
  
  placeToLand = (chance*18)+11.5 # For the middle of the pie piece
  print(f"chance*18: {chance*18}")
  print(f"land: {placeToLand}")

  imgcopy_spin0= img_SpinnerGraph0.copy()
  imgcopy_ticker= img_Ticker.copy()
  ftw,fth = imgcopy_spin0.size
  print(f"SIZES: {ftw}  {fth}")
  # Open template and get drawing context
  im = Image.new('RGBA', (ftw,fth), col_DISCORDEMBEDGRAY)
  draw = ImageDraw.Draw(im)
  
  # This Works ===================
  imgcopy_spin0 = imgcopy_spin0.rotate(placeToLand)

  # paste image giving dimensions
  im.paste(imgcopy_spin0,(0,0))
  im.paste(img_Ticker,(0,0),imgcopy_ticker)
  
  # ===================
  

  try:
    images=[]
    rotations=0
    for i in range(0, 360*3, 18):
      if(i%360==0): rotations+=1
      print(i, rotations)
      imgcopy_spin0 = imgcopy_spin0.rotate(i)

      # paste image giving dimensions
      im.paste(imgcopy_spin0,(0,0))
      im.paste(img_Ticker,(0,0),imgcopy_ticker)
      
      draw.ellipse((0 - i, 0 - i,
                        0 + i, 0 + i),
                        fill = col_DISCORDEMBEDGRAY)

      images.append(im)
  
            
    # Save result
    #im.save('FishBot_py3.8/images/wheelSpinTestOutput.gif')

    images[0].save('FishBot_py3.8/images/wheelSpinTestOutput.gif',
                    save_all = True, append_images = images[1:], 
                    optimize = False, duration = 5)
  except Exception as e: print(f'GenerateWheelspin ERROR:\t{e}')


def GenerateWheelspinEnd():
  return
  
  for RNGesus in range(360,0,-18):
    colour=""
    #RNGesus = 60
    images=[]
    if   (RNGesus >= 342): colour=("Rose") # Lucky
    elif (RNGesus >= 324): colour=("Hot Pink")
    elif (RNGesus >= 306): colour=("Pink")
    elif (RNGesus >= 288): colour=("Flamingo")
    elif (RNGesus >= 270): colour=("Purble")
    elif (RNGesus >= 252): colour=("Grape")
    elif (RNGesus >= 234): colour=("Blue")
    elif (RNGesus >= 216): colour=("Denim Blue")
    elif (RNGesus >= 198): colour=("Sky Blue")
    elif (RNGesus >= 180): colour=("Cyan")
    elif (RNGesus >= 162): colour=("Aquamarine")
    elif (RNGesus >= 144): colour=("Mint Green")
    elif (RNGesus >= 126): colour=("Very Green")
    elif (RNGesus >= 108): colour=("Lime Green")
    elif (RNGesus >= 90 ): colour=("Green")
    elif (RNGesus >= 72 ): colour=("Yellow-Green")
    elif (RNGesus >= 54 ): colour=("Yellow")
    elif (RNGesus >= 36 ): colour=("Mango")
    elif (RNGesus >= 18 ): colour=("Orange")
    else: colour=("Red") # Lucky

    chance=0
    try:
      chance = int(RNGesus/18) # 0 might be broken
    except: chance= 1;
    print(f"Chance: {chance}")
  
    width,height = img_SpinnerGraph0.size
    imgcopy_spin0= img_SpinnerGraph2.copy()
    imgcopy_lSpin0= img_LabeledSpinner0.copy()
    placeToLand = (chance*18)+11.5 # For the middle of the pie piece
    rotation=0

    for i in range(0, 360*3, 36):                
        #im = Image.new('RGBA', (width, height), col_DISCORDEMBEDGRAY)
                
               
        #draw = ImageDraw.Draw(im)

        #im.paste(imgcopy_spin0,(0,0))
        #im.paste(img_Ticker,(0,0),img_Ticker)
        imgcopy_spin0 = imgcopy_spin0.rotate(-18*3, fillcolor=col_DISCORDEMBEDGRAY)
        rotation-=18*3
        #print(f"placeToLand: {placeToLand}\trotation: {rotation%360}")
        #imgcopy_spin0 = imgcopy_spin0.rotate(-18*3)
               

        #images.append(im)
    rots=0
    if(True):
      # 510
      # 180 + 510 = 690
      step=18; slow=False;  tempPrev=0
      #if(math.ceil((rotation%360)/18)!=chance):
      while True:
        if(step==0): break

        # If Not Red...
        #if(math.ceil(((rotation-30)%360)/18)==chance): print("Slowing..."); slow=True

        # If For Red...
        if(math.ceil(((rotation+30)%360)/18)==chance): print("Slowing..."); slow=True



        if(((rotation-30)%360)>tempPrev): rots+=1#; print(f"Rot = {rots}")
        tempPrev = (rotation-30)%360
        if(slow): step-=1#; print(f"\tStep Change: {step}")
        #im = Image.new('RGBA', (width, height), col_DISCORDEMBEDGRAY)               
        #draw = ImageDraw.Draw(im)

        #im.paste(imgcopy_spin0,(0,0))
        #im.paste(img_Ticker,(0,0),img_Ticker)
        imgcopy_spin0 = imgcopy_spin0.rotate(-step*3, fillcolor=col_DISCORDEMBEDGRAY)
        rotation-=step*3

    # The Final Frames
    if(True):
      for frame in range(0,5):
        imgcopy_spin0 = imgcopy_spin0.rotate(-0.1, fillcolor=col_DISCORDEMBEDGRAY)

    im = Image.new('RGBA', (width, height), col_DISCORDEMBEDGRAY)
    draw = ImageDraw.Draw(im)
    imgcopy_lSpin0 = imgcopy_lSpin0.rotate(rotation, fillcolor=col_DISCORDEMBEDGRAY)# (rotation-30)%360
    im.paste(imgcopy_lSpin0,(0,0))
    im.paste(img_Ticker,(0,0),img_Ticker)         
    draw = ImageDraw.Draw(im)
    images.append(im)
    #images[0].save(f'FishBot_py3.8/images/Wheelspin_Labeled/EndImages/ws_Red.gif',
    images[0].save(f'FishBot_py3.8/images/Wheelspin_Labeled/EndImages/ws_{colour}.gif',
                    save_all = True, append_images = images[1:], 
                    optimize = False, duration = 1)
    #return

def GenerateWheelspin(chance):
    return
    try:
      #for RNGesus in range(360,0,-18):
            #print(RNGesus)
            images = []
            RNGesus = 60
            colour=""
            if   (RNGesus >= 342): colour=("Rose") # Lucky
            elif (RNGesus >= 324): colour=("Hot Pink")
            elif (RNGesus >= 306): colour=("Pink")
            elif (RNGesus >= 288): colour=("Flamingo")
            elif (RNGesus >= 270): colour=("Purble")
            elif (RNGesus >= 252): colour=("Grape")
            elif (RNGesus >= 234): colour=("Blue")
            elif (RNGesus >= 216): colour=("Denim Blue")
            elif (RNGesus >= 198): colour=("Sky Blue")
            elif (RNGesus >= 180): colour=("Cyan")
            elif (RNGesus >= 162): colour=("Aquamarine")
            elif (RNGesus >= 144): colour=("Mint Green")
            elif (RNGesus >= 126): colour=("Very Green")
            elif (RNGesus >= 108): colour=("Lime Green")
            elif (RNGesus >= 90 ): colour=("Green")
            elif (RNGesus >= 72 ): colour=("Yellow-Green")
            elif (RNGesus >= 54 ): colour=("Yellow")
            elif (RNGesus >= 36 ): colour=("Mango")
            elif (RNGesus >= 18 ): colour=("Orange")
            else: colour=("Red") # Lucky

            chance=0
            try:
              chance = int(RNGesus/18) # 0 might be broken
            except: chance= 1;
            print(f"Chance: {chance}")
  
            width,height = img_SpinnerGraph0.size
            

            #imgcopy_spin0= img_SpinnerGraph0.copy()
            imgcopy_spin0= img_SpinnerGraph2.copy()
            imgcopy_lSpin0= img_LabeledSpinner0.copy()

            placeToLand = (chance*18)+11.5 # For the middle of the pie piece
            rotation=0
            #for i in range(0, 360*3, 12):
            for i in range(0, 360*3, 36):                
                im = Image.new('RGBA', (width, height), col_DISCORDEMBEDGRAY)
                
               
                draw = ImageDraw.Draw(im)

                im.paste(imgcopy_spin0,(0,0))
                im.paste(img_Ticker,(0,0),img_Ticker)
                imgcopy_spin0 = imgcopy_spin0.rotate(-18*3, fillcolor=col_DISCORDEMBEDGRAY)
                rotation-=18*3
                print(f"placeToLand: {placeToLand}\trotation: {rotation%360}")
                #imgcopy_spin0 = imgcopy_spin0.rotate(-18*3)
               

                images.append(im)
            rots=0
            if(True):
              # 510
              # 180 + 510 = 690
              step=18; slow=False;  tempPrev=0
              #if(math.ceil((rotation%360)/18)!=chance):
              while True:
                if(step==0): break
                print(f"{math.ceil(((rotation-30)%360)/18)}\t|\t{math.ceil(((rotation-30)%360))}")

                # If Not Red...
                if(math.ceil(((rotation-30)%360)/18)==chance): print("Slowing..."); slow=True
                print((rotation-30)%360)

                # If For Red...
                #if(math.ceil(((rotation+30)%360)/18)==chance): print("Slowing..."); slow=True
                #print((rotation+30)%360)


                if(((rotation-30)%360)>tempPrev): rots+=1; print(f"Rot = {rots}")
                tempPrev = (rotation-30)%360
                if(slow): step-=1; print(f"\tStep Change: {step}")
                im = Image.new('RGBA', (width, height), col_DISCORDEMBEDGRAY)               
                draw = ImageDraw.Draw(im)

                im.paste(imgcopy_spin0,(0,0))
                im.paste(img_Ticker,(0,0),img_Ticker)
                imgcopy_spin0 = imgcopy_spin0.rotate(-step*3, fillcolor=col_DISCORDEMBEDGRAY)
                rotation-=step*3

                images.append(im)

            if(False):
              # 510
              # 180 + 510 = 690
              step=18; slow=False
              if(math.ceil((rotation%360)/18)!=chance):
                while True:
                  print(math.ceil(((rotation+255+145)%360)/18)) # FIND WAY TO NOT HAVE THING GO BE BACK BY 4
                  print(math.ceil(((rotation+255+145)%360))) 
                  if(math.ceil(((rotation+255+145)%360)/18)==chance): print("Done"); break
                  im = Image.new('RGBA', (width, height), col_DISCORDEMBEDGRAY)               
                  draw = ImageDraw.Draw(im)

                  im.paste(imgcopy_spin0,(0,0))
                  im.paste(img_Ticker,(0,0),img_Ticker)
                  imgcopy_spin0 = imgcopy_spin0.rotate(-1*3)
                  rotation-=1*3

                  images.append(im)

            if(False):
              step=19 # Maybe reduce this as it passes i%12
            
              for i in range(0, 360, step):
                  if(i%step<=9): step-=1; print(f"\tStep Change: {step}")
                  print(f"I: {i}\tStep: {step}")
                  #if(i>placeToLand): break
                
                  # (147, 49, 54) is an awesome red
                
                  im = Image.new('RGBA', (width, height), col_DISCORDEMBEDGRAY)
                
               
                  draw = ImageDraw.Draw(im)


                  im.paste(imgcopy_spin0,(0,0))
                  im.paste(img_Ticker,(0,0),img_Ticker)
                  imgcopy_spin0 = imgcopy_spin0.rotate(-step*3)
                  rotation-=step*3
                  print(f"placeToLand: {placeToLand}\trotation: {rotation%360}")
                  print(f"\trotationNum: {(rotation%360)/18}")


                
                

                  images.append(im)
              itr=18; addToNum=0
              for x in range(18,0,-1):
                print(f"{itr}*3 = {itr*3}\tnum = {addToNum}")
                addToNum += itr*3
                itr-=1
              # (chance*18)+11.5
              # If the image is still not roated properly, spin it slowly until it gets there
              if(math.ceil((rotation%360)/18)!=chance):
                while True:
                  print(math.ceil(((rotation+255+145)%360)/18)) # FIND WAY TO NOT HAVE THING GO BE BACK BY 4
                  if(math.ceil(((rotation+255+145)%360)/18)==chance): print("Done"); break
                  im = Image.new('RGBA', (width, height), col_DISCORDEMBEDGRAY)               
                  draw = ImageDraw.Draw(im)

                  im.paste(imgcopy_spin0,(0,0))
                  im.paste(img_Ticker,(0,0),img_Ticker)
                  imgcopy_spin0 = imgcopy_spin0.rotate(-1*3)
                  rotation-=1*3

                  images.append(im)
                
            # The Final Frames
            if(True):
              for frame in range(0,5):
                print(f"{math.ceil(((rotation-30)%360)/18)}\t|\t{math.ceil(((rotation-30)%360))}\t|\t{math.ceil(((rotation-30)))}")
                im = Image.new('RGBA', (width, height), col_DISCORDEMBEDGRAY)               
                draw = ImageDraw.Draw(im)

                im.paste(imgcopy_spin0,(0,0))
                im.paste(img_Ticker,(0,0),img_Ticker)
                imgcopy_spin0 = imgcopy_spin0.rotate(-0.1, fillcolor=col_DISCORDEMBEDGRAY)
                #rotation-=step*3

                images.append(im)

            imgcopy_lSpin0 = imgcopy_lSpin0.rotate(rotation, fillcolor=col_DISCORDEMBEDGRAY)# (rotation-30)%360
            im.paste(imgcopy_lSpin0,(0,0))
            im.paste(img_Ticker,(0,0),img_Ticker)         
            draw = ImageDraw.Draw(im)
            images.append(im)
            #images[0].save(f'FishBot_py3.8/images/Wheelspin_Labeled/ws_Red.gif',
            images[0].save(f'FishBot_py3.8/images/Wheelspin_Labeled/ws_{colour}.gif',
                           save_all = True, append_images = images[1:], 
                           optimize = False, duration = 8)
            return rots
    except Exception as e:
      print(e)




