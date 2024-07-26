from inventory import *

class Player:    
    def __init__(self, name="player"):
        self.name = name
        self.money = 200
        self.health = 100
        self.position = [55,39]
        self.wPosition = [14,7]
        self.profile = 'standing_character.PNG'
        self.direction = [0,0] 
        self.carry = None 
        self.inventory = Inventory(self)
        self.san = 100
        self.safeHour = 0
    
    def repr(self):
        return f"{self.name}"
    
    def __eq__(self, other):
        if isinstance(other, Player):
            return (self.name==other.name)
        else:
            return False
    
    def leftrun(self):
        self.profile = ['0left.PNG','1left.PNG','2left.PNG','1left.PNG']
       
    def rightrun(self):
        self.profile = ['0right.PNG','1right.PNG','2right.PNG','1right.PNG']

    def stop(self):
        self.profile = 'standing_character.PNG'
