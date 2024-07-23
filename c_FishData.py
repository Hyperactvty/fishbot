class CreateFish():
  def __init__( self, name: str, fish_type: str, rarity: str, fish_set: str, regions: [], 
                MIN_WEIGHT: float, MAX_WEIGHT: float, MIN_LENGTH: float, MAX_LENGTH: float, MIN_WIDTH: float, MAX_WIDTH: float,
                trophy_Sizes: {}):
    self.name = name; self.fish_type = fish_type; self.rarity = rarity; self.fish_set = fish_set; self.regions = regions
    self.MIN_WEIGHT = type; MIN_WEIGHT.MAX_WEIGHT = MAX_WEIGHT; self.MIN_WIDTH = MIN_WIDTH; self.MAX_LENGTH = MAX_LENGTH; self.MIN_WIDTH = MIN_WIDTH
    self.MAX_WIDTH = MAX_WIDTH; self.trophy_Sizes = trophy_Sizes

    
      
  def FishDataTemplate():
    fishDataTemplate = {'FISH_ID':0, 'Name':None, 'Type':'Fish', 'Rarity':'Common', 'Set':None, 'Regions':['Lake'], 
                        'MIN_WEIGHT':0, 'MAX_WEIGHT':0,'MIN_LENGTH':0, 'MAX_LENGTH':0, 'MIN_WIDTH':0, 'MAX_WIDTH':0,
                        'Trophy_Sizes':{'Bronze':60, 'Silver':75, 'Gold':85, 'Platinum':90, 'Ruby':95, 'Diamond':97.5}
                       }
    return fishDataTemplate