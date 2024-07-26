def loadElementData(filename):
    result = dict()
    fileString = getFileContents(filename)
    for i in fileString.splitlines():
        if i != 'Name,Icon':
            comma = i.find(',')
            name = i[:comma]
            text = i[comma+1:]
            result[name] = text
    return result

def loadReactionData(filename):
    result = dict()
    fileString = getFileContents(filename)
    for i in fileString.splitlines():
        if i != 'Element1,Element2,Element3':
            firstComma = i.find(',')
            secondComma = len(i) - i[::-1].find(',')-1
            ele1 = i[:firstComma]
            ele2 = i[firstComma+1:secondComma]
            ele3 = i[secondComma+1:]
            if ele1 in result:
                result[ele1].append((ele2,ele3))
            else:
                result[ele1] = [(ele2,ele3)]
    return result

def tryReaction(elem1, elem2, reactionsDict):
    if reactionsDict.get((elem1,elem2)) != None:
        return reactionsDict.get((elem1,elem2))
    elif reactionsDict.get((elem2,elem1)) != None:
        return reactionsDict.get((elem2,elem1))
    else:
        return None

def isTerminalElement(elem, reactionsDict):
    for i in reactionsDict:
        if elem in i:
            return False
    return True

def getFileContents(filename):
    fileContents = {'slime_reactions.csv':"""\
Element1,Element2,Element3
mud,normal,water_crystal
mud,veggie,fire_crystal
gold,fire,diamond_crystal
honey,water,veggie_crystal
rock,mud,fire_crystal
villan,fluffy,fire_crystal
crystal,rock,glass_crystal
villan,gold,diamond_crystal
thunder,lumine,gold_crystal
quantum,lumine,thunder_crystal
diamond,crystal,lumine_crystal
ghost,villan,water_crystal
fluffy,diamond,honey_crystal
radiation,thunder,quantum_crystal
glass,rock,fire_crystal
"""}
    if filename in fileContents:
        return fileContents[filename]
    else:
        print(f'Filename "{filename}" not found in file contents dictionary.')
        print('Available filenames are:')
        for name in fileContents:
            print(f'\t{name}')
        return None

class Slime:
    all_names = set()
    all_in = []
    crystalToName = dict()
    nameToAll = dict()
    reactionDict = loadReactionData('slime_reactions.csv')
    location = '/Users/jasmineshi/Desktop/'

    def __init__(self, name, default, max, min, habitat, ranchtype, wildspawn, sleep = False):
        self.name = name
        self.habitat = habitat
        self.ranchtype = ranchtype
        self.sleep = sleep
        self.aggressive = False
        self.wildspawn = wildspawn
        self.image = f"{Slime.location}112 TP codes/Images/slimes/{self.name}.png"
        self.crystalImage = f"{Slime.location}112 TP codes/Images/slimes/{self.name}_crystal.png"
        self.nightimage = f"{Slime.location}112 TP codes/Images/slimes/{self.name}2.png"
        self.price = default
        self.maxPrice = max
        self.minPrice = min    
        Slime.all_names.add(self.name)
        Slime.all_in.append(self)
        Slime.crystalToName[f'{self.name}_crystal'] = self
        Slime.nameToAll[f'{self.name}'] = self
    
    def setPrice(self,default,max,min):
        self.price = default
        self.maxPrice = max
        self.minPrice = min
        return(f'{self.price}:max={self.maxPrice},min={self.minPrice}')

    def __repr__(self):
        return f"{self.name}"
    
    def __eq__(self,other):
        if isinstance(other,Slime):
            return self.name == other.name
    
    def __hash__(self):
        return hash(str(self))
    
    def setup(self):
        slimeSetDefault()

def slimeSetDefault():
    normal = Slime('normal', 2, 5, 1, 'land', 'ranch', True, True)
    veggie = Slime('veggie', 5, 8, 2, 'land', 'ranch', True, True)
    fire = Slime('fire', 8, 15, 2, 'land', 'ranch', True, True)
    water = Slime('water', 7, 15, 1, 'aqua', 'pond', True, True)
    mud = Slime('mud', 10, 14, 7, 'aqua', 'pond', True, True)
    honey = Slime('honey', 15, 20, 12, 'aqua', 'pond', False, True)
    glass = Slime('glass', 20, 27, 15, 'aqua', 'pond', False, True)
    fluffy = Slime('fluffy', 65, 80, 50, 'land', 'ranch', False, True)
    rock = Slime('rock', 18, 25, 12, 'land', 'ranch', True, True)
    gold = Slime('gold', 70, 110, 55, 'land', 'ranch', False, True)
    lumine = Slime('lumine', 25, 40, 18, 'cave', 'tent', True)
    crystal = Slime('crystal', 30, 60, 8, 'cave', 'tent', True, True)
    villan = Slime('villan', 75, 100, 60, 'cave', 'tent', False, True)
    diamond = Slime('diamond', 50, 150, 35, 'cave', 'tent', False, True)
    thunder = Slime('thunder', 90, 100, 80, 'deep_cave', 'experimental_dish', False, True)
    quantum = Slime('quantum', 105, 145, 90, 'deep_cave', 'experimental_dish', False)
    radiation = Slime('radiation', 120, 180, 65, 'deep_cave', 'experimental_dish', False, True)
    ghost = Slime('ghost', 150, 225, 100, 'cave', 'tent', False)

slimeSetDefault()