
def GetItemValues(itemType : str, item : str, *returnDict : bool):
  ITEMDICT={
    'RODS':{
        'Rod_Basic':{
            'Amount':1, 'Rod_Base_Bonus':0.01, 'Price':100, 'Description':'A cheap, basic wooden rod. Nothing special about it.'
        },'Rod_Bamboo':{
            'Amount':0, 'Rod_Base_Bonus':1.15, 'Price':2500,'Description':''
        },'Rod_Advanced':{
            'Amount':0, 'Rod_Base_Bonus':1.25, 'Price':7500,'Description':''
        },'Rod_Fiberglass':{
            'Amount':0, 'Rod_Base_Bonus':1.5, 'Price':15000, 'Description':''
        },'Rod_Triple':{
            'Amount':0, 'Rod_Base_Bonus':1.15, 'Price':33333,'Description':''
        },'Rod_Lucky':{
            'Amount':1, 'Rod_Base_Bonus':3, 'Price':77777,'Description':''
        },'Rod_Masterly':{
            'Amount':0, 'Rod_Base_Bonus':4.5, 'Price':1250000,'Description':''
        }
    }, 'LURES':{
        'Lure_Normal':{
            'Amount':10000, 'Rod_Base_Bonus':0.01, 'Price':10, 'Description':'A cheap, basic lure. Nothing appealing about it.'
        },'Lure_Special':{
            'Amount':0, 'Rod_Base_Bonus':1.15, 'Price':750,'Description':''
        },'Lure_Master':{
            'Amount':0, 'Rod_Base_Bonus':1.25, 'Price':2500,'Description':'Pretty good for finding rare fish'
        },'Lure_Nightly':{
            'Amount':0, 'Rod_Base_Bonus':2.5, 'Price':15000, 'Description':''
        }
    }, 'REGIONS':{
        'Region_Pond':{
            'Amount':0, 'Price':1500, 'Description':'A pond populated with fish and frogs. Small fish live here.'
        }, 'Region_Lake':{
            'Amount':1, 'Price':0, 'Description':'A standard lake. Expect to find many fish here.'
        }, 'Region_Tropical':{
            'Amount':0, 'Price':12500, 'Description':'A tropical escape. Beware of sharks and dolphins. Colourful fish live here.' # Have fish colours maybe vibrant when in this region?
        },'Region_Piratecove':{
            'Amount':0, 'Price':1725000, 'Description':'A very dangerous region. Please keep all limbs inside the boat at all times. A small chance Tick-Tock Croc will appear.'
        },'Region_Ocean':{
            'Amount':0, 'Price':250000, 'Description':'An ocean filled with various types of sea life. It smells like salt.'
        },'Region_Deepocean':{
            'Amount':0, 'Price':15000000, 'Description':'A deep ocean. Expect to find large fish and cephalopods. The Kraken lurks sometimes during the night...'
        }, 'Region_Mystical':{
            'Amount':0, 'Price':17500000, 'Description':'A very magical region. Fairies may lend you a bonus from time to time. Magical fish live here.'
        },
    }, 'BAITS':{
        'Bait_Normal':{
            'Amount':30, 'Price':15, 'Description':'Some hotdog bits. Fish like it.'
        }, 'Bait_Worm':{
            'Amount':0, 'Price':75, 'Description':'This is a rip-off. Go dig some up.'
        }, 'Bait_Grub':{
            'Amount':0, 'Price':250, 'Description':'Slimy.'
        },'Bait_Bluegill':{
            'Amount':0, 'Price':750, 'Description':'Small fish to attract bigger fish.'
        },'Bait_Minnow':{
            'Amount':0, 'Price':1500, 'Description':'Smaller fish to attract bigger fish.'
        },'Bait_Glowing':{
            'Amount':0, 'Price':2250, 'Description':'It glows.'
        }
    },
  }
  try: 
    if(True in returnDict): print('Returning Dict'); return ITEMDICT[f'{itemType}']
  except: pass
  itemToReturn=ITEMDICT[f'{itemType}'][f'{item}']
  return itemToReturn