import random, copy, math, os, pathlib
from PIL import Image, ImageDraw
from cmu_graphics import *
from slime_type import *
from terrain_generator import *
from player_all import *
from ranch import *
from shop import *
from time_system import *
from PIL import Image
from barn import *
from pickable_items import *
from map import *

def onAppStart(app):
    newgame(app)

def newgame(app):
    app.FileLocation = '/Users/jasmineshi/Desktop/'
    app.END = False
    app.BEGIN = True
    app.PAUSE = False
    app.RANCH = False
    app.SHOP = False
    app.BARN = False
    app.WILD = False
    app.HELP = False
    app.width = 1000
    app.height = 750
    app.player1 = Player('Default Player')
    app.scrollX = 0
    app.scrollY = 0
    app.scrollMarginX = 500
    app.scrollMarginY = 350
    app.playerX = app.width//2 
    app.playerY = app.height//2 
    app.ranch1 = Ranch('firstRanch')
    app.playerWidth = app.playerHeight = 50
    app.board = [ [None]*25 for row in range(20) ]
    app.time = Timer('time')
    app.stepsPerSecond = 25
    app.counter = 0
    app.time.hour = 6
    app.ranchSelection = None
    app.takingFromRanch = False
    app.takingFromRanchRowCol = None
    app.dragingItemLocation = None
    app.dragingItemProperty = dict()
    app.crystalRate = 1
    app.player1.inventory.add('diamond_crystal',8)
    app.ranch1.block[5][40] = 'thunder'
    app.ranch1.block[8][40] = 'fire'
    app.ranch1.block[8][42] = 'ghost'
    wildDefaultSetup(app)
    barnDefaultSetup(app)
    shopDefaultSetup(app)
    inventoryDefaultSetup(app)
    beginDefaultSetup(app)

def beginDefaultSetup(app):
    app.beginBoardRows = 2
    app.beginBoardLeftTop = (300,200)
    app.beginBoardWidthHeight = (200,300)
    app.menuSelection = None

def wildDefaultSetup(app):
    app.wildMapId = 4
    app.wildBiome = 'land'
    app.wildBoardLeftTop = (200,25)
    app.wildBoardRowsCols = (15,15)
    app.wildBoardWidthHeight = (40,40)
    app.wildBoardElements = {0:[],1:[],2:[],3:[],4:[],5:[]}
    assignMaps()

def inventoryDefaultSetup(app):
    app.inventorySelection = None
    app.inventoryBoardLeftTop = (255,655)
    app.inventoryBoardWidthHeight = (90,90)
    app.takingFromInventory = False

def shopDefaultSetup(app):
    app.shopMessage = None
    app.shopSelection = None
    app.shopSlimeBoardLeftTop = (50,75)
    app.shopSlimeBoardRowsCols = (5,4)
    app.shopSlimeBoardWidthHeight = (100,100)
    app.shopSlimeBoard = [ [None]*4 for row in range(5) ]
    for i in range(18):
        row = i//4
        col = i%4
        app.shopSlimeBoard[row][col] = Slime.all_in[i]
    app.shopToolBoardLeftTop = (525,50)
    app.shopToolBoardRowsCols = 2

def barnDefaultSetup(app):
    app.barnSelection = None    
    app.barnBoardLeftTop = (50,75)
    app.barnBoardRowsCols = (5,7)
    app.barnBoardWidthHeight = (100,100)
    app.barn1 = Barn('Barn1')

def onStep(app):
    if not (app.BEGIN == True or app.PAUSE == True):
        if not(app.SHOP == True or app.BARN == True):
            app.counter += 1
            if app.counter == 25:
                if (app.time.hour == 6 and app.time.minute == 0):
                    refreshSlimePrice() 
                    app.wildBoardElements = {0:[],1:[],2:[],3:[],4:[],5:[]}
                    for i in range(6):  
                        app.wildMapId = i
                        updateWildBasic(app)
                    updateWildElement(app)
                    app.wildMapId = 4 
                if app.player1.san <= 0:
                    app.player1.san = 0
                    app.player1.health -= 1
                app.time.minute += 1
                app.counter = 0
                crystalProduction(app)
                checkCarrying(app)
            timeUpdate(app)
        if app.RANCH == True and (1 <= app.player1.position[0] <= 2) and (40 <= app.player1.position[1] <= 41):
            app.RANCH = False
            app.WILD = True
            app.player1.wPosition = [13,7]
            app.player1.position = [3,41]
            app.wildMapId = 4
    app.wildBiome = 'cave' if 0 <= app.wildMapId <= 2 else 'land'
    if app.player1.health <= 0:
        app.player1.position = [55,39]
        app.player1.health = 100
        app.player1.san = 100
        app.player1.inventory.bag = [None,None,None,None,None,None,None]
        app.player1.inventory.number = dict()

def makePlayerVisible(app):
    if (app.playerX < app.scrollX + app.scrollMarginX):
        app.scrollX = app.playerX - app.scrollMarginX
    if (app.playerX > app.scrollX + app.width - app.scrollMarginX):
        app.scrollX = app.playerX - app.width + app.scrollMarginX
    if (app.playerY < app.scrollY + app.scrollMarginY):
        app.scrollY = app.playerY - app.scrollMarginY
    if (app.playerY > app.scrollY + app.height - app.scrollMarginY):
        app.scrollY = app.playerY - app.height + app.scrollMarginY

def redrawAll(app):
    if app.BEGIN == True:
        drawStartPage(app)
    else:
        if app.RANCH == True:
            drawRanch(app)
            drawBoard(app)
            drawPlayer(app)
        elif app.SHOP == True:
            drawShop(app)
        elif app.BARN == True:
            drawBarn(app)
        elif app.WILD == True:
            drawWild(app)
            drawWildBoard(app)
            drawWildElements(app)
        if app.PAUSE == True:
            drawMenu(app)
        drawUI(app)
        drawInventory(app)
        drawTimeOnScreen(app)
    if app.HELP == True:
        drawHelp(app)
    if app.END == True:
        drawEnd(app)

def drawRanch(app):
    color = rgb(134,191,48)
    drawRect(0,0,1000,750, fill = color)
    [playerY, playerX] = app.player1.position
    content = app.ranch1.map
    dx = -50*(playerX-10)
    dy = -50*(playerY-8)
    drawImage(content,dx-5,dy-10, width = 4000,height = 3000)
    

def timeUpdate(app):
    if app.time.minute == 60:
        app.time.hour += 1
        app.time.minute = 00
        playerRecover(app,'small')
    if app.time.hour == 24:
        app.time.day += 1
        app.time.hour = 00
        playerRecover(app,'large')

def drawUI(app):
    [playerY, playerX] = app.player1.position
    drawRect(800,0,200,100,fill = 'paleGoldenrod',border = 'darkKhaki',borderWidth=5)
    drawLabel(app.time, 900,45,size = 20,bold=True,align = 'center',fill='darkOliveGreen')
    drawLabel(app.player1.position, 900,20,size = 20,bold=True,align = 'center',fill='seaGreen')
    drawLabel(f'money: {app.player1.money}$', 900,70,size = 20,bold=True,align = 'center')
    drawRect(0,650,1000,100,fill = 'darkKhaki')
    image = f'{app.FileLocation}112 TP codes/Images/characters/standing_character.PNG'
    drawImage(image,-50,600,width =200,height=200)
    drawLabel(app.player1.name,175,675, font='montserrat', size= 18, bold=True,fill = 'saddleBrown')
    drawLabel(f'health: {app.player1.health}/100',175,700, font='montserrat', size= 18, bold=True,fill = 'saddleBrown')
    drawLabel(f'sanity: {app.player1.san}/100',175,725, font='montserrat', size= 18, bold=True,fill = 'saddleBrown')

def drawBoard(app):
    if app.ranchSelection != None:
        (cx, cy) = app.ranchSelection
        drawRect(cx*50, cy*50, 50, 50, fill=None, border = 'darkRed', borderWidth = 3)
    [playerY, playerX] = app.player1.position
    updateBoard(app)
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            if app.board[row][col] != None:
                name = app.board[row][col]
                if name in Slime.all_names:
                    if 7 <= app.time.hour <= 18:
                        content = Slime.nameToAll[name].image
                    else:
                        content = Slime.nameToAll[name].nightimage
                elif name in Slime.crystalToName:
                    content = Slime.nameToAll[f'{Slime.crystalToName[name]}'].crystalImage
                else:
                    content = f'{app.FileLocation}112 TP codes/Images/texture/{name}.png'
                scrollingY = 0
                if app.player1.position[0] <= 7:
                    scrollingY = 50*(7-app.player1.position[0])
                drawImage(content, 50*col, 50*row + scrollingY, width = 50, height = 50)

def updateBoard(app):
    [playerY, playerX] = app.player1.position
    newX = -1
    newY = -1
    for row in range(len(app.ranch1.block)):
        if row < ((playerY) - 7):
            continue
        elif row > ((playerY) + 8):
            break
        else:
            newX = -1
            newY += 1
            for col in range(len(app.ranch1.block[0])):
                if col < ((playerX) - 10): 
                    continue
                elif col <= (playerX + 10) and row < ((playerY) + 10):
                    newX += 1
                    app.board[newY][newX] = app.ranch1.block[row][col]
                    
def drawInventory(app):
    for i in range(7):
        x0 = 300 + i*100
        y0 = 700
        drawRect(x0,y0,90,90,fill = 'lemonChiffon',align = 'center') 
        if app.player1.inventory.bag[i] != None:
            icon = Item.item_profile[app.player1.inventory.bag[i]]
            drawImage(icon,x0,y0,width = 50,height = 50,align = 'center')
            counts = app.player1.inventory.number[app.player1.inventory.bag[i]]
            drawLabel(counts,x0+30,y0+30,size = 16, bold = True, fill = 'saddleBrown')
    if app.inventorySelection != None:
        index = app.inventorySelection
        drawRect(300 + index*100 ,y0,90,90,fill = None ,align = 'center',border = 'saddleBrown',borderWidth = 3) 
    if (app.dragingItemLocation != None and app.dragingItemProperty != dict()):
        [cy,cx] = app.dragingItemLocation
        stuff = None
        for key in app.dragingItemProperty:
            stuff = key
        drawImage(Item.item_profile[stuff], cx,cy,width = 50,height = 50)

def drawTimeOnScreen(app):
    opacity = 0
    if 21 <= app.time.hour <=24 or 0 <= app.time.hour <= 4:
        opacity = 30
    elif 19 <= app.time.hour < 21 or 5 <= app.time.hour < 6:
        opacity = 20
    elif app.time.hour == 18 or app.time.hour == 6:
        opacity = 10
    drawRect(0, 0, app.width, app.height, fill='black', opacity= opacity)

def drawPlayer(app):
    cx, cy = app.playerX, app.playerY
    cx -= (25 * app.scrollX)
    cy -= (25 * app.scrollY)
    if app.player1.profile == 'standing_character.PNG':      
        image = f"{app.FileLocation}112 TP codes/Images/characters/{app.player1.profile}"
        drawImage(image, cx, cy, align='center',width=100, height=100)
    else:
        sprite = app.player1.profile[(app.counter)%4]
        image = f"{app.FileLocation}112 TP codes/Images/characters/{sprite}"
        drawImage(image, cx, cy, align='center',width=100, height=100)
    if app.player1.carry == None:
        if app.inventorySelection != None:
            icon = app.inventorySelection
            if app.player1.inventory.bag[icon] != None:
                holding = Item.item_profile[app.player1.inventory.bag[icon]]
                drawImage(holding, cx, cy + 20, align='center',width=50, height=50)
    else:
        if 7 <= app.time.hour <= 18:
            image = Slime.nameToAll[app.player1.carry].image
        else:
            image = Slime.nameToAll[app.player1.carry].nightimage
        drawImage(image, cx, cy + 20, align='center',width=50, height=50)

def onKeyPress(app, key):
    if not (app.BEGIN == True):
        if key == 'p':
            app.PAUSE = not app.PAUSE
    if app.HELP == True and key == 'escape':
        app.HELP = False
    if app.END == True and key == 'r':
        newgame(app)
    if (app.RANCH == True or app.WILD == True):
        if (key == '1' or key == '2' or key == '3' or key == '4' or key == '5' or key == '6' or key == '7'):
            app.inventorySelection = int(key)-1
        if not(app.SHOP == True or app.BARN == True):
            if key == 'left':
                if ((0 < app.player1.position[1]) and (0 < app.player1.wPosition[1])):
                    app.player1.leftrun()
                    app.player1.direction = [-1,0]
                    movePlayer(app, 0, -1)
                    wildSwitchScreen(app,key)
            elif key == 'right':
                if ((app.player1.position[1] < 80) and (app.player1.wPosition[1] < 15)): 
                    app.player1.rightrun()
                    app.player1.direction = [1,0]
                    movePlayer(app, 0, +1)
                    wildSwitchScreen(app,key)
            elif key == 'up':
                if ((0 < app.player1.position[0]) and (0 < app.player1.wPosition[0])):
                    app.player1.leftrun()
                    app.player1.direction = [0,-1]
                    movePlayer(app ,-1, 0)
                    wildSwitchScreen(app,key)
            elif key == 'down':
                if ((app.player1.position[0] < 60) and (app.player1.wPosition[0] < 15)):
                    app.player1.rightrun()
                    app.player1.direction = [0,1]
                    movePlayer(app, +1, 0)
                    wildSwitchScreen(app,key)
            elif key == 'space':
                pickitup(app)
            elif key == 't':
                app.time.hour += 1
                timeUpdate(app)
            elif key == 'm':
                app.player1.money += 1000

def onKeyHold(app, keys):
    if app.RANCH == True:
        if 'left' in keys and 0 < app.player1.position[1]: 
            app.player1.leftrun()
            movePlayer(app, 0, -1)
        elif 'right' in keys and app.player1.position[1] < 80:
            app.player1.rightrun() 
            movePlayer(app, 0, +1)
        elif 'up' in keys and 0 < app.player1.position[0]:
            app.player1.leftrun()
            movePlayer(app ,-1, 0)
        elif 'down' in keys and app.player1.position[0] < 60 :
            movePlayer(app, +1, 0)
            app.player1.rightrun()

def onKeyRelease(app, key):
    if ((key == 'left') or (key == 'right') 
        or (key == 'up') or (key == 'down')):
        app.player1.stop()

def movePlayer(app, dy, dx):
    if app.RANCH == True:
        app.player1.position[1] += dx
        app.player1.position[0] += dy
        if not((0 <= app.player1.position[0] < 60) and (0 <= app.player1.position[1] < 80)):
            app.player1.position[1] -= dx
            app.player1.position[0] -= dy  
        makePlayerVisible(app)
    elif app.WILD == True:
        app.player1.wPosition[1] += dx
        app.player1.wPosition[0] += dy
        if not((0 <= app.player1.wPosition[0] < 15) and (0 <= app.player1.wPosition[1] < 15)):
            app.player1.wPosition[1] -= dx
            app.player1.wPosition[0] -= dy      

def onMousePress(app, mouseX, mouseY):
    if (app.BEGIN == True or app.PAUSE == True):
        selectedCell = getCell(app, mouseX, mouseY)
        if selectedCell != None:
            app.Test = selectedCell
            app.menuSelection = selectedCell
            callFunction(app)
            app.menuSelection = None
    else:
        if 250 <= mouseX <= 950 and 650 <= mouseY <= 750:
            invselectedCell = getCell(app, mouseX, mouseY)
            app.takingFromInventory = True
            if invselectedCell != None:
                app.inventorySelection = invselectedCell
        elif app.RANCH == True:
            selectedCell = getCell(app, mouseX, mouseY)
            if selectedCell != None:
                if selectedCell == app.ranchSelection:
                    callFunction(app)
                    app.ranchSelection = None
                else:
                    app.ranchSelection = selectedCell
        elif app.SHOP == True:
            if 525 <= mouseX <= 725 and 200 <= mouseY <= 400:
                if app.player1.money >= 15112:
                    app.SHOP = False
                    app.END = True
                else:
                    app.shopMessage = """You don't have enough money!"""
            selectedCell = getCell(app, mouseX, mouseY)
            if selectedCell != None:
                if selectedCell == app.shopSelection:
                    callFunction(app)
                else:
                    app.shopSelection = selectedCell
            elif 925 <= mouseX <= 975 and 100 <= mouseY <= 120:
                app.SHOP = False
                app.RANCH = True
        elif app.BARN == True:
            selectedCell = getCell(app, mouseX, mouseY)
            if selectedCell != None:
                if selectedCell == app.barnSelection:
                    callFunction(app)
                else:
                    app.barnSelection = selectedCell
            if 925 <= mouseX <= 975 and 100 <= mouseY <= 120:
                app.BARN = False
                app.RANCH = True 

def getCell(app, x, y):
    if app.BEGIN or app.PAUSE:
        (pauboardLeft,pauboardTop)= app.beginBoardLeftTop
        dx = x - pauboardLeft
        cellWidth, cellHeight = 400,90
        col = math.floor(dx / cellWidth)
        if col == 0:
            if 200 <= y <= 290:
                return 0
            elif 325 <= y <= 415:
                return 1
        else:
            return None
    else:
        if 250 <= x <= 950 and 650 <= y <= 750:
            (invboardLeft,invboardTop)= app.inventoryBoardLeftTop
            (invcellWidth, invcellHeight) = (100,100)
            dx = x - invboardLeft
            dy = y - invboardTop
            row = math.floor(dy / invcellHeight)
            col = math.floor(dx / invcellWidth)
            if (0 <= col < 7):
                return col
            else:
                return None
        elif app.RANCH == True:
            dx = x - 0
            dy = y - 0
            cellWidth, cellHeight = 50,50
            row = math.floor(dy / cellHeight)
            col = math.floor(dx / cellWidth)
            if (0 <= row < 15) and (0 <= col < 20):
                return (col, row)
            else:
                return None
        elif app.SHOP == True:
            if 0 <= x <= 500:
                (boardLeft,boardTop)= app.shopSlimeBoardLeftTop
                dx = x - boardLeft
                dy = y - boardTop
                (cellWidth, cellHeight) = app.shopSlimeBoardWidthHeight
                row = math.floor(dy / cellHeight)
                col = math.floor(dx / cellWidth)
                if ((0 <= row < 5) and (0 <= col < 4) 
                    and not(row == 4 and 2 <= col <= 3)):
                    return (row, col,'slime')
                else:
                    return None
            elif 525 <= x <= 725: 
                if 50 <= y <= 150: 
                    (boardLeft,boardTop)= app.shopToolBoardLeftTop
                    col = math.floor((x-boardLeft)/ 90)
                    if 0 <= col <= 1:
                        return (0,col,'tools')
                    else:
                        return None
        elif app.BARN == True:
            if 50 <= x <= 750: 
                (boardLeft,boardTop)= app.barnBoardLeftTop
                dx = x - boardLeft
                dy = y - boardTop
                (cellWidth, cellHeight) = app.barnBoardWidthHeight = (100,100)
                row = math.floor(dy / cellHeight)
                col = math.floor(dx / cellWidth)
                if ((0 <= row < 5) and (0 <= col < 7)):
                    return (row, col)
            pass

def callFunction(app):
    if (app.BEGIN == True or app.PAUSE == True):
        if app.menuSelection == 0:
            if app.BEGIN == True:
                app.BEGIN = False
                app.RANCH = True
                pass
            elif app.PAUSE == True:
                app.PAUSE = not app.PAUSE
        elif app.menuSelection == 1:
            app.HELP = True
    else:
        if (app.RANCH == True):
            if app.ranchSelection != None:
                (col, row) = app.ranchSelection
                selection = app.board[row][col]
                if selection == 'shop':
                    app.RANCH = False
                    app.SHOP = True
                    app.shopMessage = 'Welcome to Slime Valley Shop!'
                elif selection == 'barn':
                    app.RANCH = False
                    app.BARN = True
                elif selection in Slime.crystalToName:
                    if ((selection in app.player1.inventory.bag) or (None in app.player1.inventory.bag)):
                        app.player1.inventory.add(selection,1)
                        [playerY, playerX] = app.player1.position
                        app.ranch1.block[playerY + row - 7][playerX + col - 10] = None
                        updateBoard(app)
                        
        elif (app.SHOP == True and app.shopSelection != None):
            (row, col, type) = app.shopSelection
            if type == 'slime':
                for name in Slime.all_in:
                    if app.shopSlimeBoard[row][col] == name:
                        if (f'{name}_crystal' in app.player1.inventory.bag):
                            app.player1.inventory.take(f'{name}_crystal',1)
                            app.player1.money += Shop.slimePrice[name][0]
                            app.shopMessage = 'successfully sold!'
                        else:
                            app.shopMessage = f'not enough {name} crystals'
            elif type == 'tools':
                price = [2000,300]
                if app.player1.money >= price[col]:
                    if ((['hoe','slime net'][col] in app.player1.inventory.bag) or ['hoe','slime net'][col] in app.barn1.board):
                        tool = ['hoe','slime net'][col]
                        app.shopMessage = f'you already have a {tool} in your bag or barn!'
                    elif (None in app.player1.inventory.bag):
                        app.player1.money -= price[col]
                        tool = ['hoe','slime net'][col]
                        app.player1.inventory.add(tool,1)
                        app.shopMessage = 'successfully purchased!'
                    else:
                        app.shopMessage = 'not enough space in your bag'
                else:
                    app.shopMessage = 'not enough money'
            app.shopSelection = None
        elif (app.BARN == True and app.barnSelection != None):
            (row, col) = app.barnSelection
            index = row*7 + col
            if app.barn1.board[index] != None:
                if (None in app.player1.inventory.bag):
                    barnitem = app.barn1.board[index]
                    barnamount = app.barn1.number[barnitem]
                    app.player1.inventory.add(barnitem,barnamount)
                    app.barn1.remove(barnitem)
            app.barnSelection = None
            pass


def drawShop(app):
    drawRect(0,0,app.width,app.height, fill ='khaki',border = 'darkKhaki', borderWidth = 20)
    drawLabel('Slime Valley Shop',180,35, size=35, bold=True, fill = 'darkKhaki')
    drawRect(50,75,400,500,fill='darkKhaki')
    (slimerow, slimecol) = app.shopSlimeBoardRowsCols
    (slimeLeft, slimeTop) = app.shopSlimeBoardLeftTop
    for row in range(slimerow):
        for col in range(slimecol):
            drawRect(slimeLeft + 100*col + 5, slimeTop+ 100*row + 5, 90, 90, fill='wheat')
            slimeRecord = row*4 + col
            if slimeRecord < 18:
                icon = Slime.all_in[slimeRecord].crystalImage
                drawImage(icon,slimeLeft + 100*col+50, slimeTop+ 100*row + 55,width =50,height = 50,align = 'center')
                name = Slime.all_in[slimeRecord]
                drawLabel(name, slimeLeft + 100*col+50, slimeTop+ 100*row + 20,size = 15, align = 'center', fill='saddleBrown', bold=True)
                price = Shop.slimePrice[name]
                if price[1] != None:
                    drawLabel(f'price:{price[0]}({price[1]})', slimeLeft + 100*col+50, slimeTop+ 100*row +80, fill='saddleBrown', bold=True)
                else:
                    drawLabel(f'price:{price[0]}', slimeLeft + 100*col+50, slimeTop+ 100*row + 80, fill='saddleBrown', bold=True)
    drawRect(525,50,250,100,fill='darkKhaki')
    (toolLeft, toolTop) = app.shopToolBoardLeftTop
    for col in range(app.shopToolBoardRowsCols):
        drawRect(toolLeft + 100*col + 5, toolTop + 5, 90, 90, fill='wheat')
        name = ['hoe','slime net'][col]
        drawLabel(name, toolLeft + 100*col+50, toolTop + 20,size = 15, align = 'center', fill='saddleBrown', bold=True)
        icon = Item.item_profile[name]
        drawImage(icon,toolLeft + 100*col+50, toolTop+ 55,width =50,height = 50,align = 'center')
        price = Shop.toolPrice[name]
        drawLabel(f'price:{price}', toolLeft + 100*col+50, toolTop+ 85, fill='saddleBrown', bold=True)
    drawLabel(app.shopMessage, 500, 600, fill='saddleBrown')
    if app.shopSelection != None:
        (cx, cy,type) = app.shopSelection
        if type == 'slime':
            (slimeLeft, slimeTop) =app.shopSlimeBoardLeftTop
            drawRect(slimeLeft + 100*cy + 5, slimeTop+ 100*cx + 5, 90, 90, fill = None, border = 'darkRed', borderWidth = 3)
        elif type == 'tools':
            (toolLeft, toolTop) = app.shopToolBoardLeftTop
            drawRect(toolLeft + 100*cy + 5, toolTop + 5, 90, 90, fill=None, border = 'darkRed', borderWidth = 3)
    drawRect(525,200,150,150,fill='wheat')
    drawLabel('rocket ticket',600,210,size = 20, fill='saddleBrown', bold=True)
    drawImage(Item.item_profile['rocket'],600,275,width = 100,height = 100,align = 'center')
    drawLabel('price: 15112',600,335,size = 20, fill='saddleBrown', bold=True)
    drawRect(925,100,50,20, fill = 'darkKhaki', border ='saddleBrown',borderWidth = 2)
    drawLabel('Exit', 950,110,size = 15, bold = True, fill = 'saddleBrown')

def onMouseDrag(app, mouseX, mouseY):
    if app.RANCH == True:
        if app.takingFromInventory == True:
            app.dragingItemLocation = [mouseY,mouseX] 
            if app.dragingItemProperty == dict():
                takenName = app.player1.inventory.bag[app.inventorySelection]
                takenAmount = 1
                app.dragingItemProperty[takenName] = takenAmount
                app.player1.inventory.take(takenName,takenAmount)
        elif app.takingFromRanch == True:
            app.dragingItemLocation = [mouseY,mouseX] 
            if app.dragingItemProperty == dict():
                (col,row)= getCell(app, mouseX, mouseY)
                [playerY, playerX] = app.player1.position
                takenName = app.board[row][col]
                takenAmount = 1
                app.dragingItemProperty[takenName] = takenAmount
                app.ranch1.block[playerY+row-7][playerX +col-9] = None
                app.takingFromRanchRowCol = [(playerY+row-7),(playerX +col-9)]
        pass
    elif app.BARN == True:
        if app.takingFromInventory == True:
            app.dragingItemLocation = [mouseY,mouseX] 
            if app.dragingItemProperty == dict():
                takenName = app.player1.inventory.bag[app.inventorySelection]
                
                takenAmount = app.player1.inventory.number[takenName]
                app.dragingItemProperty[takenName] = takenAmount
                app.player1.inventory.take(takenName,takenAmount)
    elif app.SHOP == True:
        if app.takingFromInventory == True:
            app.dragingItemLocation = [mouseY,mouseX] 
            if app.dragingItemProperty == dict():
                takenName = app.player1.inventory.bag[app.inventorySelection]
                takenAmount = app.player1.inventory.number[takenName]
                app.dragingItemProperty[takenName] = takenAmount
                app.player1.inventory.take(takenName,takenAmount)

def onMouseRelease(app, mouseX, mouseY):
    if app.RANCH == True:
        if app.takingFromInventory == True:
            if 0 <= mouseY <= 650: 
                for name in app.dragingItemProperty:
                    (col, row) = getCell(app, mouseX, mouseY)
                    [playerY, playerX] = app.player1.position
                    boardItem = app.ranch1.block[playerY + row - 7][playerX + col - 9]
                    if f'{boardItem}' in Slime.nameToAll and (f'{name}' in Slime.crystalToName):
                        if ((f'{name}' in Slime.crystalToName) and (canReaction(f'{boardItem}',f'{name}') != False)): 
                            app.ranch1.block[playerY + row - 7][playerX + col - 9] = canReaction(f'{boardItem}',f'{name}')
                            updateBoard(app)
                        else: 
                            returnInventory(app)
                    elif Item.item_type[name] == 'tools': 
                        toolFunction(app,name)
                    else:
                        returnInventory(app)
            else:
                returnInventory(app)
    elif app.BARN == True:
        (barnLeft, barnTop) =app.barnBoardLeftTop
        if (barnLeft <= mouseX <= barnLeft + 710 and barnTop <= mouseY <= barnTop + 505) and app.dragingItemProperty != None:
            for takenName in app.dragingItemProperty:
                takenAmount = app.dragingItemProperty[takenName]
                if app.barn1.add(takenName,takenAmount) == False:
                    app.player1.inventory.add(takenName,takenAmount)
        else:
            for takenName in app.dragingItemProperty:
                takenAmount = app.dragingItemProperty[takenName]
                app.player1.inventory.add(takenName,takenAmount)
    elif app.SHOP == True:
        (slimeLeft, slimeTop) = app.shopSlimeBoardLeftTop
        if (slimeLeft <= mouseX <= slimeLeft + 400 and slimeTop <= mouseY <= slimeTop + 500) and app.dragingItemProperty != dict():
            for takenName in app.dragingItemProperty:
                takenAmount = app.dragingItemProperty[takenName]
                if Item.item_type[takenName] == 'slimes':
                    referral = Slime.crystalToName[takenName]
                    app.player1.money += (Shop.slimePrice[referral][0])*takenAmount
                elif Item.item_type[takenName] == 'tools':
                    app.shopMessage = 'you cannot sell a tool!'
                    for takenName in app.dragingItemProperty:
                        takenAmount = app.dragingItemProperty[takenName]
                        app.player1.inventory.add(takenName,takenAmount)
        else:
            for takenName in app.dragingItemProperty:
                takenAmount = app.dragingItemProperty[takenName]
                app.player1.inventory.add(takenName,takenAmount)
    app.dragingItemProperty = dict()
    app.takingFromInventory = False
    app.takingFromRanch = False
    app.takingFromRanchRowCol = None 
    pass  

def drawBarn(app):
    drawRect(0,0,app.width,app.height, fill ='moccasin',border = 'darkKhaki', borderWidth = 20)
    drawLabel('The Barn',100,35, size=35, bold=True, fill = 'darkKhaki')
    drawRect(45,70,710,505,fill='darkKhaki')
    (barnrow, barncol) = app.barnBoardRowsCols
    (barnLeft, barnTop) =app.barnBoardLeftTop
    for row in range(barnrow):
        for col in range(barncol):
            drawRect(barnLeft + 100*col + 5, barnTop+ 100*row + 5, 90, 90, fill='wheat')
            barnRecord = row*7 + col 
            if barnRecord < len(app.barn1.board): 
                key = app.barn1.board[barnRecord]
            if key != None:
                icon = Item.item_profile[key]
                drawImage(icon,barnLeft + 100*col+50, barnTop+ 100*row + 55,width =50,height = 50,align = 'center')
                name = app.barn1.board[barnRecord]
                amount = app.barn1.number[name]
                drawLabel(amount, barnLeft + 100*col+50 + 30, barnTop+ 100*row + 80,size = 15, align = 'center', fill='saddleBrown')
    if app.barnSelection != None:
        (cx, cy) = app.barnSelection
        (barnLeft, barnTop) = app.barnBoardLeftTop
        drawRect(barnLeft + 100*cy + 5, barnTop+ 100*cx + 5, 90, 90, fill=None, border = 'saddleBrown', borderWidth = 3)
    drawRect(925,100,50,20, fill = 'darkKhaki', border ='saddleBrown',borderWidth = 2)
    drawLabel('Exit', 950,110,size = 15, bold = True, fill = 'saddleBrown')

def drawWild(app):
    bgColor = 'lightCyan' if app.wildBiome == 'land' else 'cadetBlue'
    boardColor = 'seaGreen' if app.wildBiome == 'land' else 'slateGray'
    wbLeft, wbTop = app.wildBoardLeftTop
    drawRect(0,0,app.width,app.height,fill = bgColor)
    drawRect(wbLeft,wbTop,600,600,fill = boardColor)
    pass

def drawWildBoard(app):
    rows,cols = app.wildBoardRowsCols
    extreme = not((app.wildMapId == 1) or (app.wildMapId == 4))
    for row in range(rows):
        for col in range(cols):
            drawCell(app, row, col, extreme)
    pass

def drawCell(app, row, col, extreme):
    if app.WILD == True:
        cellLeft, cellTop = app.wildBoardLeftTop
        cellWidth, cellHeight = app.wildBoardWidthHeight
        dx = cellLeft + col * cellWidth
        dy = cellTop + row * cellHeight
        index = Map.all_maps[app.wildMapId][row][col]
        [wMax, wMin, wRange] = Map.land_range[app.wildMapId]
        referral = None
        opacity = 100
        if index == wMax:
            referral = 'wMax'
        elif extreme == True:
            if index == 0:
                referral = 'extreme'
            elif index == 1:
                referral = 'wThin'
            else:
                referral = 'wBlend'
                opacity = 100*(index - 1)//(wMax - 2)
        elif extreme == False:
            if index == wMin:
                referral = 'wThin'
            else:
                referral = 'wBlend'
                opacity = 100*(index - wMin)//(wMax-wMin - 1)
        color = Map.texture[app.wildBiome][referral]
        drawRect(dx, dy, cellWidth, cellHeight,fill=color, opacity = opacity)

def drawWildElements(app):
    cellLeft, cellTop = app.wildBoardLeftTop
    cellWidth, cellHeight = app.wildBoardWidthHeight
    for elem in app.wildBoardElements[app.wildMapId]:
        [row,col,name,category] = elem
        dx = cellLeft + col * cellWidth
        dy = cellTop + row * cellHeight
        if category == 'slime':
            if 7 <= app.time.hour <= 18:
                image = Slime.nameToAll[name].image
            else:
                image = Slime.nameToAll[name].nightimage
            drawImage(image,dx,dy,width = cellWidth, height = cellHeight)
    for i in range(6):  
        if app.wildMapId == i:
            signs = []
            [right,left,down,up] = Map.connections[i]
            if right == True:
              texture = Item.item_profile['right_entry']
              [row,col] = [7,14]
              signs.append((texture, cellLeft + col * cellWidth,cellTop + row * cellHeight))
            if left == True:
                texture = Item.item_profile['left_entry']
                [row,col] = [7,0]
                signs.append((texture, cellLeft + col * cellWidth,cellTop + row * cellHeight))
            if up == True:
                texture = Item.item_profile['up_entry']
                [row,col] = [0,7]
                signs.append((texture, cellLeft + col * cellWidth,cellTop + row * cellHeight))
            if down == True:
                texture = Item.item_profile['down_entry']
                [row,col] = [14,7]
                signs.append((texture, cellLeft + col * cellWidth,cellTop + row * cellHeight))
            for (texture,cx,cy) in signs:
                drawImage(texture,cx,cy,width = cellWidth, height = cellHeight)
    [wrow, wcol] = app.player1.wPosition
    cx = cellLeft + wcol * cellWidth
    cy = cellTop + wrow * cellHeight
    image = f"{app.FileLocation}112 TP codes/Images/characters/wild_profile.PNG"
    drawImage(image,cx,cy,width = cellWidth, height = cellHeight)
    if app.player1.carry != None:
        if 7 <= app.time.hour <= 18:
            carrying = Slime.nameToAll[app.player1.carry].image
        else:
            carrying = Slime.nameToAll[app.player1.carry].nightimage
        drawImage(carrying,cx,cy,width = cellWidth, height = cellHeight)

def pickitup(app):
    if app.RANCH == True:
        [playerX, playerY] = app.player1.position
        if app.player1.carry == None:
            if app.ranch1.block[playerX][playerY] in Slime.all_names:
                app.player1.carry = f'{app.ranch1.block[playerX][playerY]}'
                app.ranch1.block[playerX][playerY] = None
        else:
            if app.ranch1.block[playerX][playerY] == None:
                app.ranch1.block[playerX][playerY] = app.player1.carry
                app.player1.carry = None
    elif app.WILD == True:
        if app.player1.carry == None:
            for elem in app.wildBoardElements[app.wildMapId]:
                [row,col,name,category] = elem
                if [row,col] == app.player1.wPosition:
                    app.player1.carry = name
                    app.wildBoardElements[app.wildMapId].remove(elem)
                    break
        else:
            [wRow,wCol] = app.player1.wPosition
            app.wildBoardElements[app.wildMapId].append([wRow,wCol,app.player1.carry,'slime'])
            app.player1.carry = None

def updateWildElement(app):
    for i in range(6):
        biome = Map.biome[i]
        [common,rare,royal] = Map.possibleSlimes[biome]
        for j in range(3):
            chance = random.randint(0,100)
            if chance <= 75:
                place = [random.randint(0,14),random.randint(0,14),common,'slime']
                app.wildBoardElements[i].append(place)
        for j in range(2):
            chance = random.randint(0,100)
            if chance <= 50:
                place = [random.randint(0,14),random.randint(0,14),rare,'slime']
                app.wildBoardElements[i].append(place)
        for j in range(1):
            chance = random.randint(0,100)
            if chance <= 25:
                place = [random.randint(0,14),random.randint(0,14),royal,'slime']
                app.wildBoardElements[i].append(place)

def updateWildBasic(app):
    [right,left,down,up] = Map.connections[app.wildMapId]
    if right == True:
        app.wildBoardElements[app.wildMapId].append([7,14,'right_entry','unlock'])
    if left == True:
        app.wildBoardElements[app.wildMapId].append([7,0,'left_entry','unlock'])
    if down == True:
        app.wildBoardElements[app.wildMapId].append([14,7,'down_entry','unlock'])
    if up == True:
        app.wildBoardElements[app.wildMapId].append([0,7,'up_entry','unlock'])

def playerRecover(app,scale):
    if scale == 'small':
        if app.player1.san >= 60:
            app.player1.health += 5
        if app.player1.health >= 75:
            app.player1.san += 5
    elif scale == 'large':
        app.player1.health += 10
        app.player1.san += 5
    if app.player1.health > 100:
        app.player1.health = 100
    if app.player1.san > 100:
        app.player1.san = 100

def checkCarrying(app):
    harmHealth = {'fire','radiation','quantum','thunder','villan'}
    harmSanity = {'villan','ghost','radiation'}
    if app.player1.carry in harmHealth:
        app.player1.health -= 1
    if app.player1.carry in harmSanity:
        app.player1.san -= 1

def toolFunction(app,tool):
    if tool == 'hoe' and app.crystalRate > 2:
        app.crystalRate -= 1
    elif tool == 'slime net':
        app.player1.safeHour += 1

def canReaction(boardItem,name):
    for slimes in Slime.reactionDict:
        for item in Slime.reactionDict[slimes]:
            if item ==  (f'{boardItem}',f'{name}'):
                return f'{slimes}'
    return False

def returnInventory(app):
    for takenName in app.dragingItemProperty:
        takenAmount = app.dragingItemProperty[takenName]
        app.player1.inventory.add(takenName,takenAmount)

def wildSwitchScreen(app,key):
    if app.WILD == True:
        for i in range(6):  
            if app.wildMapId == i:
                [right,left,down,up] = Map.connections[i]
                if((down == True and i == 4) and 
                   (app.player1.wPosition == [14,7] and key == 'down')):
                    app.RANCH = True
                    app.WILD = False
                elif ((right == True and key == 'right') 
                    and (app.player1.wPosition == [7,14])):
                    app.wildMapId += 1
                    app.player1.wPosition = [7,0]
                elif ((left == True and key == 'left') and (app.player1.wPosition == [7,0])):
                    app.wildMapId -= 1
                    app.player1.wPosition = [7,14]
                elif ((up == True and key == 'up') and (app.player1.wPosition == [0,7])):
                    app.wildMapId -= 3
                    app.player1.wPosition = [14,7]
                elif ((down == True and key == 'down') and (app.player1.wPosition == [14,7])):
                    app.wildMapId += 3
                    app.player1.wPosition = [0,7]

def crystalProduction(app):
    update = math.ceil(60/app.crystalRate)
    if app.time.minute % update == 0:
        spawnCrystal(app)
        updateBoard(app)

def spawnCrystal(app):
    for row in range(len(app.ranch1.block)):
        for col in range(len(app.ranch1.block[0])):
            if app.ranch1.block[row][col] != None:
                name = app.ranch1.block[row][col]
                if name in Slime.all_names:
                    orientation = [(1,0),(-1,0),(0,1),(0,-1),
                                   (1,1),(1,-1),(-1,1),(-1,-1)]
                    for (dx,dy) in orientation:
                        cy = row + dy
                        cx = col + dx
                        if ((0 <= cy <= 59 and 0 <= cx <= 79) and app.ranch1.block[cy][cx] == None):
                            app.ranch1.block[cy][cx] = f'{name}_crystal'
                            break

def drawStartPage(app):
    drawRect(0,0,app.width,app.height,fill = 'powderBlue')
    drawImage(Item.item_profile['startPage'],125,0,width = 750,height = 750)
    drawLabel('The Slime Valley',app.width//2 + 10,85,size = 80,bold=True, fill = 'lightSlateGray',opacity = 25)
    drawLabel('The Slime Valley',app.width//2,75,size = 80,bold=True, fill = 'darkSlateGray')
    (boardLeft,boardTop) = app.beginBoardLeftTop
    (boardWidth,boardHeight) = (400,90)
    for i in range(app.beginBoardRows):
        cellLeft = boardLeft
        cellTop = boardTop + 125* i
        drawRect(cellLeft,cellTop,boardWidth,boardHeight,fill = 'wheat',border = 'tan',borderWidth = 10)
        label = ['New Game','Help']
        drawLabel(label[i],cellLeft + boardWidth//2,cellTop + boardHeight//2,size = 30,fill = 'tan',bold = True)
    pass

def drawMenu(app):
    drawRect(0,0,app.width,app.height, opacity = 35)
    (boardLeft,boardTop) = app.beginBoardLeftTop
    (boardWidth,boardHeight) = (400,90)
    for i in range(app.beginBoardRows):
        cellLeft = boardLeft
        cellTop = boardTop + 125* i
        drawRect(cellLeft,cellTop,boardWidth,boardHeight,fill = 'wheat',border = 'tan',borderWidth = 10)
        label = ['Resume','Help']
        drawLabel(label[i],cellLeft + boardWidth//2,cellTop + boardHeight//2,size = 30,fill = 'tan',bold = True)
    pass

def drawHelp(app):
    image = Item.item_profile['help']
    drawImage(image,0,100,width = 1000,height=550)

def drawEnd(app):
    drawRect(0,0,app.width,app.height,fill = 'powderBlue')
    drawImage(Item.item_profile['endPage'],125,0,width = 750,height = 750)
    drawLabel('Thank you for playing',app.width//2,app.height//2,size = 60,bold=True, fill = 'darkSlateGray')
    drawLabel("""Press 'r' to restart the game""",app.width//2 + 10,app.height//2 + 50,size = 35,bold=True, fill = 'lightSlateGray')

def main():
    runApp()

main()