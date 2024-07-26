from slime_type import *
import random

class Shop:
    slimePrice = dict()
    toolPrice = dict()
    rocketPrice = {'rocket':15112}

    def __init__(self,name):
        self.name = name
        self.slimeCategory = Slime.all_names
        
    
    def refreshPrice(self):
        refreshSlimePrice()


def refreshSlimePrice():
    if Shop.slimePrice == dict():
        for name in Slime.all_in:
           Shop.slimePrice[name] = [name.price,None]
    else:
        for name in Slime.all_in:
            newPrice = random.randint(name.minPrice, name.maxPrice)
            if newPrice > Shop.slimePrice[name][0]:
               Shop.slimePrice[name][1] = '+'
            elif newPrice < Shop.slimePrice[name][0]:
               Shop.slimePrice[name][1] = '-'
            else:
                Shop.slimePrice[name][1] = None
            Shop.slimePrice[name][0] = newPrice
        for name in ['hoe','slime net']:
            Shop.toolPrice[name] = 2000 if name == 'hoe' else 300

refreshSlimePrice()