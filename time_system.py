class Timer:
    def __init__(self,name):
        self.name = name
        self.minute = 00
        self.hour = 00
        self.day = 0
    
    def __repr__(self):
        return f'{self.name}: day{self.day},{self.hour}:{self.minute}'
    
    def __eq__(self,other):
        if isinstance(other,Timer):
            return ((self.day == other.day) and (self.hour == other.hour) 
                    and (self.minute == other.minute))
    
    def __hash__(self):
        return hash(str(self))