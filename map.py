import copy
from terrain_generator import *

class Map:
    all_names = []
    all_maps = dict() 
    texture = {'cave':{'wMax':'lightGray','extreme':'black','wThin':'dimGray','wBlend':'dimGray'},
               'land':{'wMax':'darkOliveGreen','extreme':'cadetBlue','wThin':'darkGoldenrod','wBlend':'olive'}}
    connections = [[True, False, False, False],
                    [True, True, True, False],
                    [False, True, False, False],
                    [True, False, False, False],
                    [True, True, True, True],
                    [False, True, False, False]]
    unlock = {4:{'right_entry':['veggie_crystal',80,0],'left_entry':['fire_crystal',80,0],'up_entry':['normal_crystal',120,0]},
              1:{'right_entry':['diamond_crystal',50,0],'left_entry':['glass_crystal',120,0]}}

    possibleSlimes = {'cave':['rock','crystal','lumine'],'deep_cave':['crystal','lumine','thunder'],
                      'land':['normal','veggie','fire'],'aqua':['water','mud','rock']}

    biome = ['deep_cave','cave','deep_cave',
             'aqua','land','aqua']
    
    land_range = [None,None,None,None,None,None]

    all_elements = dict()

    def __init__(self,name,content):
        self.name = name
        self.content = content
        Map.all_names.append(self)
        Map.all_maps[self.name] = copy.deepcopy(self.content)
    
    def __eq__(self,other):
        if isinstance(other,Map):
            return (self.id == other.id)
        else:
            return False
    
    def __repr__(self):
        return f'{self.id}'
    
    def __hash__(self):
        return hash(str(self))

def assignMaps():
    default = 0
    return helperAssignMaps(default)

def helperAssignMaps(number):
    temptsolution = optimizedTerrainGenerator()
    if number == 6:
        return True
    elif (isLegalMap(temptsolution,number) == True):
        Map(number,copy.deepcopy(temptsolution))        
        return helperAssignMaps(number + 1)
    else:
        return helperAssignMaps(number)

def isLegalMap(map,id):
    if (id != 1 and id != 4):
        if mapEvaluation(map,True) != False:
            result = copy.copy(mapEvaluation(map,True))
            Map.land_range[id] = copy.copy(result)
            return True
        else:
             return False
    else:
        if mapEvaluation(map,False) != False:
            result = copy.copy(mapEvaluation(map,False))
            Map.land_range[id] = copy.copy(result)
            return True
        else:
            return False

def mapEvaluation(map,extreme):
    most,least = -100,100
    numExtreme = 0
    for i in map:
        most = max(i) if max(i) > most else most
        least = min(i) if min(i) < least else least
        for j in i:
            if j == 0:
                numExtreme += 1
    if ((most-least) > 8):
        return False
    elif ((most-least) < 3):
        return False
    elif (extreme == True and numExtreme < 5):
        return False
    elif (extreme == False and least == 0):
        mapfix(map,1)
        return [most+1,least+1,(most-least + 2)]
    elif (extreme == True and least != 0):
        mapfix(map,-least)
        return [most-least,0,(most- 2*least + 1)]
    else:
        return [most,least,(most-least + 1)]

def mapfix(map,fix):
    for i in range(len(map)):
        for j in range(len(map[0])):
            map[i][j] += fix
    most,least = -100,100
    for i in map:
        most = max(i) if max(i) > most else most
        least = min(i) if min(i) < least else least

