class Barn:
    def __init__(self,name):
        self.name = name
        self.board = []
        for i in range(35):
            self.board.append(None)
        self.number = dict()
    
    def __repr__(self):
        return f"{self.name}"
    
    def __eq__(self,other):
        if isinstance(other,Barn):
            return (self.board == other.board and self.number == other.number)
    
    def __hash__(self):
        return hash(str(self))
    
    def add(self,item,number):
        if item in self.board:
            self.number[item] += number
            isAdded = True
            return True
        else:
            if not (None in self.board):
                return False
            else:
                space = self.board.index(None)
                self.board[space] = item
                self.number[item] = number
                return True
    
    def remove(self,item):
        if item in self.board:
            self.board.remove(item)
            self.number.pop(item)


