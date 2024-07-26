from slime_type import *
class Item:
    all_items = set()
    item_profile = dict()
    item_type = dict()
    location = '/Users/jasmineshi/Desktop/'

    def __init__(self, name, type):
        self.name = name
        self.type = type
        reference = {'slimes':'PNG','sound':'mp3','other':'png'}
        ref = reference[type] if type in ['slimes','sound'] else reference['other']
        self.image = f"{Item.location}112 TP codes/Images/{type}/{name}.{ref}"
        Item.all_items.add(self)
        Item.item_profile[self.name] = self.image
        Item.item_type[self.name] = self.type
    
    def __eq__(self,other):
        if isinstance(other, Item):
            return ((self.name == other.name) and (self.type == other.type))
        else:
            return False
    def __repr__(self):
        return f"{self.name}"
    
    def __hash__(self):
        return hash(str(self))

def itemSetDefault():
    for slimes in Slime.all_in:
        Item(f'{slimes}_crystal','slimes')
    for item in ['hoe','slime net']:
        Item(item,'tools')
    textures = ['barn','grass', 'path','ranch','shop','right_entry',
               'left_entry','up_entry','down_entry','rocket']
    for texture in textures:
        Item(texture,'texture')
    for sound in ['main_theme','pickup']:
        Item(sound,'sound')
    for help in ['startPage','help','endPage']:
        Item(help,'help pages')

itemSetDefault()

