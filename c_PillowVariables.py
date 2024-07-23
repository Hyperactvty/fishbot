from PIL import Image, ImageDraw, ImageFont

class PillowVariables():
  def __init__(self):
    self.font_AMATIC = ImageFont.truetype('C:/Users/wert3/AppData/Local/Microsoft/Windows/Fonts/AMATIC-REGULAR.ttf', 80)
    self.value2 = 2
  
  def GetFont(fontType):
    if(fontType=='font_AMATIC'): return self.font_AMATIC

  def GetColour(colour):
    if(colour=='col_WHITE'): return (255,255,255,255)
    
    
  pass




