class Ranch:
    location = '/Users/jasmineshi/Desktop/'
    farmLand = {0:[[8,8,26,16],'slimeRanch'],1:[[8,32,26,40],'slimeRanch'],2:[[8,54,26,62],'slimeRanch'],
                3:[[18,8,36,16],'slimeRanch'],4:[[18,32,36,40],'slimeRanch'],5:[[18,54,36,62],'slimeRanch'],
                6:[[32,8,50,16],'slimeRanch'],7:[[32,32,50,40],'slimeRanch'],8:[[32,54,50,62],'slimeRanch']}

    def __init__(self,name):
        self.name = name
        self.block =  [ [None]*80 for row in range(60) ]

        self.farmLand = [[None] for row in range(9)]
        self.fruitLand = [[None],[None]]
        self.map = f'{Ranch.location}112 TP codes/Images/texture/ranch.png'
        for i in range(53,55):
            for j in range(52,54):
                self.block[i][j] = 'shop'
        for i in range(53,55):
            for j in range(20,22):
                self.block[i][j] = 'barn'
        for i in range(1,3):
            for j in range(40,42):
                self.block[i][j] = 'path'
    
    def setUpDefault(self):
        setUpRanchDefault(self)
    
    def crop(self,L):
        [cx,cy] = L
        result = [[None]*15 for row in range(20)]
        for row in range(len(self.block)):
            if 0 <= row - cy  < 15:
                for col in range(len(self.block[0])):
                   if 0 <= col - cx < 20:
                       print([col - cx])
                       print([row - cy])
                       print(self.block[row])
                       result[row - cy][col - cx] = self.block[row][col]
        return result
                       

def setUpRanchDefault(ranch):

    for row in range(60):
        for col in range(80):
            ranch.block[row][col] = 'grass'
            if ((2 <= row <= 3 or 32 <= row <= 33 or 
                 56 <= row <= 57) and (4 <= col <= 76)):
                ranch.block[row][col] = 'path'
            if ((2 <= col <= 3 or 28 <= col <= 29 or 
                 75 <= col <= 76) and (2 <= row <= 56)):
                 ranch.block[row][col] = 'path'
    for row in [4,26,30]:
        for col in [14,40,62]:
            for i in range(2):
                for j in range(2):
                    ranch.block[row+i][col+j] = 'path'
    for row in [6,18,32]:
        for col in [6,32,54]:
            for width in range(18):
                for height in range(8):
                    ranch.block[row+height][col+width] = 'farmland'
    for row in range(48,54):
        for col in range(36,44):
            ranch.block[row][col] = 'home'