class Inventory:
    def __init__(self, name):
        self.bag = [None,None,None,None,None,None,None]
        self.number = dict()
    
    def add(self,other,number):
        if other in self.bag:
            self.number[other] += number
        elif (None in self.bag):
            self.number[other] = number
            self.bag[self.bag.index(None)] = other

    def take(self,other,amount):
        if self.number[other] >= amount:
            self.number[other] -= amount
        if self.number[other] == 0:
            self.number.pop(other)
            self.bag.remove(other)
            self.bag.append(None)