import pygame
import sys
import time
import random
import threading
from tkinter import *
import math
from tkinter import messagebox

# RECURSION EXTENSION
sys.setrecursionlimit(7100)

pygame.init()

# SCREEN GEOMETRY
screenWidth = 1200
screenHeight = 700

# COLOR CONSTANTS
red = (255, 0, 0)
darkRed = (170, 0, 0)
green = (0, 255, 0)
darkGreen = (0, 150, 0)
blue = (0, 0, 255)
darkBlue = (0,0,170)
white = (255, 255, 255)
gray = (170, 170, 170)
darkGray = (120, 120, 120)
ultraDarkGray = (25,25,25)
black = (0, 0, 0)
sandColor = (245, 194, 109)
ultraDarkGreen = (2, 48, 0)
strangeBlue = (0, 130, 139)
colornot = pygame.Color("gray15")
color = colornot

# GAME SCREENS INIT
menuScreen = False
gameScreen = False
pauseScreen = False
defeatScreen = False
winScreen = False
gameWonScreen = False
hallOfFameScreen = False
creditsScreen = False
instructionsScreen = False

# MATRIX INIT
gameMatrixGrid = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]

# TIME COUNTER INIT
elapsedTime = 0
timeCounting = False

# LEVEL INIT
level = 1

#MOUSE & CLICK
mouse = []
click = []

# MISCELLANEOUS
scoreYPos = 300
gameWonCounter = 0.0
scoreLines = []
creditsPos = 700
refreshRate = 20
close = False

# SOUNDS
rookDestroySound = pygame.mixer.Sound("sounds/rooks/destroyRook.wav")
avatarKillSound = pygame.mixer.Sound("sounds/avatars/avatarKill.wav")
arrowShootSound = pygame.mixer.Sound("sounds/avatars/arrow_thrown.wav")
arrowHitSound = pygame.mixer.Sound("sounds/avatars/arrow_hit.wav")
swordShootSound = pygame.mixer.Sound("sounds/avatars/sword_thrown.wav")
swordHitSound = pygame.mixer.Sound("sounds/avatars/sword_hit.wav")
meleeSound = pygame.mixer.Sound("sounds/avatars/meleeSound.wav")
clubHitSound = pygame.mixer.Sound("sounds/avatars/club_hit.wav")
axeHitSound = pygame.mixer.Sound("sounds/avatars/axe_hit.wav")
waterSound = pygame.mixer.Sound("sounds/rooks/WaterRook.wav")
sandSound = pygame.mixer.Sound("sounds/rooks/SandRook.wav")
rockSound = pygame.mixer.Sound("sounds/rooks/RockRook.wav")
fireSound = pygame.mixer.Sound("sounds/rooks/FireRook.wav")
musicPlaying = "None"

# ROOKS IMAGES
waterA = pygame.image.load("images/rooks/aya.png")
water = pygame.image.load("images/rooks/water.png")
fire = pygame.image.load("images/rooks/fire.png")
fireA = pygame.image.load("images/rooks/fattack.png")
rock = pygame.image.load("images/rooks/rock.png")
rockA = pygame.image.load("images/rooks/rattack.png")
sand = pygame.image.load("images/rooks/sand.png")
sandA = pygame.image.load("images/rooks/sattack.png")
col25 = pygame.image.load("images/rooks/25.png")
col50 = pygame.image.load("images/rooks/50.png")
col100 = pygame.image.load("images/rooks/100.png")
CoinDrawing = pygame.image.load("images/coin.png")
check = pygame.image.load("images/rooks/check.png")
equis = pygame.image.load("images/rooks/equis.png")
price = pygame.image.load("images/rooks/coin.png")
ForBg = pygame.image.load("images/rooks/bg.png")
woodRooks = pygame.image.load("images/rooks/wood.png")

# BACKGROUND
background = pygame.image.load("images/background1.png")
transparent_black = pygame.image.load("images/transparent_black.png")
transparent_white = pygame.image.load("images/transparent_white.png")
wood = pygame.image.load('images/wood.png')
creditsImg = pygame.image.load('images/gameWon/credits.png')
instructionsImg = pygame.image.load("images/instructions.png")

# CREDITS
creditsImg = pygame.image.load('images/credits/credits.png')
sebas = pygame.image.load('images/credits/sebas.png')
luis = pygame.image.load('images/credits/luis.png')

# AVATARS IMAGES
archerAvatar = pygame.image.load("images/avatars/archer_avatar.png")
knightAvatar = pygame.image.load("images/avatars/knight_avatar.png")
lumberjackAvatar = pygame.image.load("images/avatars/lumberjack_avatar.png")
cannibalAvatar = pygame.image.load("images/avatars/cannibal_avatar.png")

# AVATARS ANIMATIONS
archerAvatarAnimation = [pygame.image.load("images/avatars/archer_animations/archer_attack_1.png"),pygame.image.load("images/avatars/archer_animations/archer_attack_2.png"),pygame.image.load("images/avatars/archer_animations/archer_attack_3.png"),pygame.image.load("images/avatars/archer_animations/archer_attack_4.png"),pygame.image.load("images/avatars/archer_animations/archer_attack_5.png")]
cannibalAvatarAnimation = [pygame.image.load("images/avatars/cannibal_animations/cannibal_attack_1.png"),pygame.image.load("images/avatars/cannibal_animations/cannibal_attack_2.png"),pygame.image.load("images/avatars/cannibal_animations/cannibal_attack_3.png"),pygame.image.load("images/avatars/cannibal_animations/cannibal_attack_4.png"),pygame.image.load("images/avatars/cannibal_animations/cannibal_attack_5.png")]
knightAvatarAnimation = [pygame.image.load("images/avatars/knight_animations/knight_attack_1.png"),pygame.image.load("images/avatars/knight_animations/knight_attack_2.png"),pygame.image.load("images/avatars/knight_animations/knight_attack_3.png"),pygame.image.load("images/avatars/knight_animations/knight_attack_4.png"),pygame.image.load("images/avatars/knight_animations/knight_attack_5.png")]
lumberjackAvatarAnimation = [pygame.image.load("images/avatars/lumberjack_animations/lumberjack_attack_1.png"),pygame.image.load("images/avatars/lumberjack_animations/lumberjack_attack_2.png"),pygame.image.load("images/avatars/lumberjack_animations/lumberjack_attack_3.png"),pygame.image.load("images/avatars/lumberjack_animations/lumberjack_attack_4.png"),pygame.image.load("images/avatars/lumberjack_animations/lumberjack_attack_5.png")]

# AVATARS PROJECTILES
arrow = pygame.image.load("images/avatars/archer_animations/arrow.png")
sword = pygame.image.load("images/avatars/knight_animations/sword.png")
placeholder = pygame.image.load("images/avatars/placeholder.png")

# AVATARS INITIALIZATION
archerAvatarInit =     [2, 5, 12, 10]
knightAvatarInit =     [3, 10, 10, 15]
lumberjackAvatarInit = [9, 20, 13, 5]
cannibalAvatarInit =   [12, 25, 14, 3]
avatarsInit =          [cannibalAvatarInit, lumberjackAvatarInit, knightAvatarInit, archerAvatarInit]
avatars = []
allAvatars = []
avatarsKilled = 0
avatarsCreated = 0

# ROOKS VARIABLES xpos, ypos, damage, shootingTime, image, animation, health):
WaterRook = [8, 100, 1, 1, 16, 1]
SandRook = [2, 100, 2, 2, 10, 2]
RockRook = [4, 100, 3, 3, 14, 3]
FireRook = [8, 100, 4, 4, 16, 4]
rooksInit = [WaterRook, SandRook, RockRook, FireRook]
rooks = []
rookAttackVel = 0
vel = ""
velWrite = False
attackVelRect = pygame.Rect(1050, 485, 140, 32)
allRooks = []

#COINS xpos, ypos, value, image)
Co25 = [25, col25]
Co50 = [50, col50]
Co100 = [100, col100]
CoinList = [Co25, Co50, Co100]
coin = []

# GLOBAL VARIABLES
mouse = pygame.mouse.get_pos()
TimesPressed = 0
WaterCol = False
SandCol = False
RockCol = False
FireCol = False
selected = "NONE"
coins = 100
delete = False
user = ""
font = "consolas.ttf"
save = False
selection = False

# fonts
font3 = pygame.font.SysFont("comicsans", 25)
font4 = pygame.font.SysFont("comicsans", 20)

pygame.display.set_caption("AVATARS VS. ROOKS")
FPS = pygame.time.Clock()

def PauseButton():
    """PLACES PAUSE BUTTON"""

    pauseRect = PrintScreen("PAUSE", 30, 20, 20, white)

    if pauseRect.right + 10 > mouse[0] > 0 and pauseRect.bottom > mouse[1] > 0:
        pygame.draw.rect(game, white, (0,0,pauseRect.right + 10, pauseRect.bottom + 10))
        PrintScreen("PAUSE", 30, 20, 20, black)
        if click[0] == 1:
            ChangeScreens(pause=True)
            return
        
def MatrixButton(xpos, ypos, width, height, fill, corj, cori, num=None):
    global selected, gameMatrixGrid, coins, delete, selection
    click = pygame.mouse.get_pressed()
    if xpos + width > mouse[0] > xpos and ypos + height > mouse[1] > ypos:
        pygame.draw.rect(game, fill, [xpos - 5, ypos - 5, width + 10,
                                      height + 10])  # if the mouse if above the image and creates a rectangle

        if click[0] == 1:
            selection = False
            if selected != "" and gameMatrixGrid[corj][cori] == 0:
                if selected == 'WATER':
                    if coins >= 150:
                        RookGenerator(cori, corj, 1)
                        gameMatrixGrid[corj][cori] = 1
                        selected = 'NONE'
                        coins -= 150
                    else:
                        selected = 'NONE'

                elif selected == "SAND":
                    if coins >= 50:
                        RookGenerator(cori, corj, 2)
                        gameMatrixGrid[corj][cori] = 2
                        selected = 'NONE'
                        coins -= 50
                    else:
                        selected = 'NONE'

                elif selected == "ROCK":
                    if coins >= 100:
                        RookGenerator(cori, corj, 3)
                        gameMatrixGrid[corj][cori] = 3
                        selected = 'NONE'
                        coins -= 100
                    else:
                        selected = 'NONE'

                elif selected == "FIRE":
                    if coins >= 150:
                        RookGenerator(cori, corj, 4)
                        gameMatrixGrid[corj][cori] = 4
                        selected = 'NONE'
                        coins -= 150
                    else:
                        selected = 'NONE'
    else:
        if click[0] == 1:
            selected == "NONE"

def RookButton(xpos, ypos, width, height, image, action, value):
    global mouse, selected, coins, selection

    click = pygame.mouse.get_pressed()

    if coins >= value:
        game.blit(check, (xpos, ypos+90))
        fill = darkGreen

    else:
        game.blit(equis, (xpos, ypos+90))
        fill = red

    if xpos + width > mouse[0] > xpos and ypos + height > mouse[1] > ypos:
        pygame.draw.rect(game, fill, [xpos - 10, ypos - 5, 69 + 10,
                                      92 + 5])  # if the mouse if above the image and creates a rectangle

        if click[0] == 1 and action != None and coins >= value:
            if action == "water":
                selected = "WATER"

            elif action == "sand":
                selected = "SAND"

            elif action == "rock":
                selected = "ROCK"

            elif action == "fire":
                selected = "FIRE"

            selection = True

    game.blit(ForBg, (xpos-5, ypos-5))
    game.blit(image, (xpos, ypos+5))
    game.blit(price, (xpos+17, ypos+62))

    if action != "sand":
        PrintScreen(str(value), xpos+20, ypos+74, 10, white, True)
    
    else:
        PrintScreen(str(value), xpos+23, ypos+74, 10, white, True)

def RookImageMouse():
    if selection:
        if selected == "WATER":
            image = water

        elif selected == "ROCK":
            image = rock

        elif selected == "FIRE":
            image = fire

        elif selected == "SAND":
            image = sand

        game.blit(image, (mouse[0]-10, mouse[1]-10))
    return

def PrintScreen(text, x, y, fontsize, color, justified=False):
    """PRINTS TEXT ON PYGAME SCREEN"""

    font = pygame.font.Font("consolas.ttf", fontsize)
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect()
    if justified:
        textRect.midleft = (x, y)
    else:
        textRect.center = (x, y)
    game.blit(textSurface, textRect)
    return textRect

def Grid(column, row):
    """PRINTS THE GRID"""

    if column == 9:
        return Grid(0, row + 1)

    if row == 5:
        pygame.draw.rect(game, darkRed, [60 + 10 * 80, 50, 80, 5*90-10])
        pygame.draw.rect(game, darkGray, [0, 50, 20, 5*90-10])
        RookButton(50, 510, 76, 59, water, "water", 150)
        RookButton(50+90*1, 510, 74, 87, rock, "rock", 100)
        RookButton(50+90*2, 510, 76, 91, sand, "sand", 50)
        RookButton(50+90*3, 510, 50, 91, fire, "fire", 150)
        PrintScreen("Spawned: " + str(avatarsCreated), 900, 520, 30, white)
        PrintScreen("Killed: " + str(avatarsKilled) , 900, 550, 30, white)
        PrintScreen("Need to kill: " + str(15*level) , 900, 580, 30, white)
        PrintScreen("Game time: "+ str(int(elapsedTime)), 600, 520, 30, white)
        return

    pygame.draw.rect(game, ultraDarkGreen, [50 + column * 90, 50 + row * 90, 80, 80])
    MatrixButton(50 + column * 90, 50 + row * 90, 80, 80, sandColor, row, column)
    return Grid(column + 1, row)

def Time():
    """COUNTS TIME"""
    global elapsedTime
    time.sleep(0.05)
    if timeCounting:
        elapsedTime = round(elapsedTime + 0.05, 2)
    elif close:
        return
    return Time()

def AvatarGenerator():
    """GENERATES AVATARS RANDOMLY"""
    global avatarsCreated

    if avatarsCreated > 15*level - 1:
        return

    if random.randint(0, 500 - level * 150) == random.randint(0, 500 - level * 150):
        global gameMatrixGrid, avatars
        y = random.randint(0, 4)
        if gameMatrixGrid[y][8] != 0:
            return
        ranAvat = random.randint(-4, -1)
        gameMatrixGrid[y][8] = ranAvat
        avatars += [Avatars(8, y, ranAvat, avatarsInit[ranAvat + 4][0], avatarsInit[ranAvat + 4][1],avatarsInit[ranAvat + 4][2], avatarsInit[ranAvat + 4][3])]
        avatarsCreated += 1
        return

def CoinGenerator():
    global coin, CoinList
    if random.randint(0, 1500) == random.randint(0, 1500):
        ranCoin = random.randint(0, 2)
        coin += [Coin(1000, random.randrange(145, 550), CoinList[ranCoin][0], CoinList[ranCoin][1])]
        return

def RookGenerator(xpos, ypos, var):
    global rooks
    rooks += [
        Rooks(xpos, ypos, rooksInit[var - 1][0], rooksInit[var - 1][1], rooksInit[var - 1][2], rooksInit[var - 1][3],
              rooksInit[var - 1][4], rooksInit[var - 1][5])]

def AvatarsInteractions(i, stop):
    """MANAGES ALL AVATAR INTERACTIONS AND PRINTINGS"""
    if i > stop-1:
        return
    avatars[i].MoveAvatar()
    avatars[i].PlaceAvatar()
    avatars[i].Attack()
    avatars[i].AnimateAttack()
    avatars[i].Health()
    avatars[i].Collision()
    avatars[i].AnimateRangeAttack()

    if avatars[i].Death():
        global avatarsKilled, coins
        
        del avatars[i]
        avatarsKilled += 1
        if coins < 1000:
            coins += 75
        
        if avatarsKilled == 15*level:
            if level == 3:
                ChangeScreens(gameWon=True)
                return
            ChangeScreens(win=True)
            pygame.mixer.music.stop()
            return
        return AvatarsInteractions(i, stop - 1)
    return AvatarsInteractions(i + 1, stop)

def PlaceCoin(i, stop):
    if i > stop-1:
        return
    if coins < 1000:
        coin[i].draw()
    if coin[i].Erase():
        del coin[i]
        return PlaceCoin(i + 1, stop - 1)
    return PlaceCoin(i + 1, stop)

def PlaceRooks(i, stop):
    global delete
    if i > stop-1:
        return
    rooks[i].PlaceRook()
    rooks[i].Vel()
    if rooks[i].CheckFront():
        rooks[i].attack()
    rooks[i].Health()
    rooks[i].collision()
    if rooks[i].Death() or rooks[i].Delete() or delete == True:
        pygame.mixer.Sound.play(rookDestroySound)
        del rooks[i]
        delete = False
        return PlaceRooks(i + 1, stop-1)
    return PlaceRooks(i + 1 , stop)

def Version():
    file = open("./txt/version.txt")
    version = file.read()
    file.close()
    versionWords = version.split(" ")
    versionNums = versionWords[1].split(".")
    finalVersion = versionWords[0] + " " + versionNums[0] + "." + versionNums[1] + "." + str(
        int(versionNums[2]) + 1) + " " + versionWords[2]
    file = open("version.txt", "w")
    file.write(finalVersion)
    file.close()

def LoadLevel(newLevel):
    global gameMatrixGrid, timeCounting, avatars, avatarsKilled, avatarsCreated, rooks, music, background, level, selected, musicPlaying

    # LEVEL INIT
    level=newLevel

    if level > 4:
        level = 3

    # MATRIX INIT
    gameMatrixGrid = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]

    # TIME COUNTER INIT
    timeCounting = True

    # AVATARS INIT
    for avatar in avatars:
        del avatar
    avatars = []
    avatarsKilled = 0
    avatarsCreated = 0

    # ROOKS INIT
    for rook in rooks:
        del rook
    rooks = []
    selected = "NONE"

    # MUSIC
    pygame.mixer.music.load("sounds/music/level"+ str(level) +".wav")
    background = pygame.image.load("images/background"+ str(level) +".png")
    musicPlaying = "level"+str(level)
    pygame.mixer.music.play(-1)

def WriteSaveGame(data):
        route = "SaveGame.txt"
        change = open(route, "w")
        change.write(data)
        change.close()

def ReadSaveGame():
        route = "SaveGame.txt"
        change = open(route)
        content = change.readlines()
        change.close()
        return content

def WriteObject(data, route):
    change = open(route, "w")
    change.write(data)
    change.close()

def ReadObject(route):
    change = open(route)
    content = change.readlines()
    change.close()
    return content

def GameDataSave():
    matrix = ""
    for row in gameMatrixGrid:
        for column in row:
            matrix += str(column)+","
        matrix += "&"
    print("matrix = ", matrix)
    data = str(user)+ "$" +str(coins)+ "$" +matrix+ "$" +str(level)+ "$" + str(round(elapsedTime, 2))
    WriteSaveGame(data)

def SetRookAttackVel():
    global rookAttackVel, vel
    try:
        if abs(int(vel)) > 5 and abs(int(vel)) < 10:
            rookAttackVel = abs(int(vel))

        else:
            rookAttackVel = random.randint(5, 10)
            vel = ""

    except:
        rookAttackVel = random.randint(5, 10)
        vel = ""

def SaveRooks():
    kisawea = ""
    for rook in rooks:
        kisawea += "$"+str(rook.Save())[1:-1]
    print(kisawea)

    WriteObject(kisawea, "SaveRooks.txt")

def LoadRooks(data):
    global rooks
    if data == []:
        return
    kisawea = []
    listamiedo= data[0].split("$")[1:]
    print(listamiedo)
    rooksAUX = []
    for rook in listamiedo:
        rooksAUX = rook.split(",")
        for element in rooksAUX:
            kisawea += [int(element)]
            print(kisawea)
        rooks += [Rooks(int(kisawea[0]),int(kisawea[1]),int(kisawea[2]),int(kisawea[3]),int(kisawea[4]),int(kisawea[5]),int(kisawea[6]), int(kisawea[7]))]
    print(rooks)

def SaveAvatars():
    #for avatar in avatars:
        #avatar.Save()
    #print(allAvatars)
    #WriteObject(allAvatars, "SaveAvatars.txt")
    kisawea = ""
    for avatar in avatars:
        kisawea += "$"+str(avatar.Save())[1:-1]
    #print(kisawea)
    WriteObject(kisawea, "SaveAvatars.txt")

def LoadAvatars(data):
    global avatars
    if data == []:
        return
    kisawea = []
    print("data = ",data)
    print('data[0].split("$")[1:] = ', [data[0].split("$")[1:]])
    listamiedo= data[0].split("$")[1:]
    print("lista miedo ", listamiedo)
    print("len listamiedo ",len(listamiedo))
    prueba = []
    for avatar in listamiedo:
        prueba = avatar.split(",")
        for element in prueba:
            kisawea += [round(int(element))]
            print("kisawea = ", kisawea)
        avatars += [Avatars(int(kisawea[0]),int(kisawea[1]),int(kisawea[2]),int(kisawea[3]),int(kisawea[4]),int(kisawea[5]),int(kisawea[6]))]
        print(avatars)
        print("len avatars = ", len(avatars))


    #avatars += [Avatars(int(avatar[0]), int(avatar[1]), int(avatar[2]), int(avatar[3]), int(avatar[4], int(avatar[5]), int(avatar[6])))]
    #avatars += [Avatars()]

def AddDataToGame(data): #FORMAT(user, rooks, avatars, coins, gameMatrixGrid, level)
        global rooks, avatars, coins, gameMatrixGrid, level, menuScreen, gameScreen, elapsedTime
        if data == []:
            return
        if str(data[0].split("$")[0]) == user:
            coins = int(data[0].split("$")[1])
            temporalMatrix = data[0].split("$")[2]
            rows = temporalMatrix.split("&")
            print("\n\nrows = ", rows)
            columns = []
            rows2 = []
            for row in rows:
                if row == "":
                    break
                for column in row.split(","):
                    if column == "":
                        break
                    columns += [int(column)]
                rows2 = [columns]
            print("rows2 = ", rows2)
            level = int(data[0].split("$")[3])
            LoadLevel(level)
            elapsedTime = float(data[0].split("$")[4])
            LoadAvatars(ReadObject("SaveAvatars.txt"))
            LoadRooks(ReadObject("SaveRooks.txt"))
            ChangeScreens(game=True)
            
        else:
            Tk().wm_withdraw()
            messagebox.showerror("ERROR", "YOU ARE TRYING TO LOAD ANOTHER PERSON'S GAME")

def TextButton(text, xpos, ypos, width, height, ActiveColor, InactiveColor,text_size, action = None, OptionalRect = None):
    global menuScreen, gameScreen, hallOfFameScreen
    click = pygame.mouse.get_pressed()

    if OptionalRect:
        pygame.draw.rect(game, strangeBlue, [xpos-60, ypos+40, width+120, height-5])
    color = InactiveColor
    if xpos + width > mouse[0] > xpos and (ypos+40) + height > mouse[1] > (ypos+40):
        #pygame.draw.rect(game, fill, [xpos - 5, ypos - 5, width + 10,height + 10])  # if the mouse if above the image and creates a rectangle
        #PrintScreen(text, xpos + 60, ypos + 60, text_size, ActiveColor)
        color = ActiveColor
        if click[0] == 1:
            if action == "play":
                level = 1
                ChangeScreens(game=True)
                LoadLevel(1)

            elif action == "level2":
                ChangeScreens(game=True)
                LoadLevel(2)

            elif action == "level3":
                level = 3
                ChangeScreens(game=True)
                LoadLevel(3)

            elif action == "top":
                ChangeScreens(hallOfFame=True) #BEST SCORES

            elif action == "about":
                # INFO OF PROGRAMMERS
                ChangeScreens(creditS=True)

            elif action == "info":
                # INSTRUCTIONS OF GAME
                ChangeScreens(instructions=True)

            elif action == "load":
                AddDataToGame(ReadSaveGame())

            elif action == "exit":
                Tk().wm_withdraw()  # to not show tkinter window
                if messagebox.askokcancel("EXIT", "Are you sure that you want to exit the game? Progress would not be saved", icon = "warning"):
                    Quit()

    PrintScreen(text, xpos+60, ypos+60, text_size, color)

def LoadScore():
    """LOADS SCORE FROM FILE"""
    global scoreLines

    scoreFile = open("./txt/score.txt", "r")
    lines = scoreFile.readlines()
    scoreFile.close()

    scoreLines = []
    for line in lines:
        scoreLines += [line.split("!")[:-1]]
    
def SaveScore():
    scoreFile = open("./txt/score.txt", "a")
    scoreFile.write(str(elapsedTime) + "!" + user + "!\n")
    scoreFile.close()

    scoreFile = open("./txt/score.txt", "r")
    lines = scoreFile.readlines()
    scoreFile.close()

    scores = []
    scoreStr = []
    sortedScores = []

    for line in lines:
        scoreStr += [line.split("!")[0]]
    
    for score in scoreStr:
        scores += [round(float(score), 2)]

    for score in sorted(scores):
        for line in lines:
            if round(float(line.split("!")[0]), 2) == score:
                sortedScores += [str(round(float(line.split("!")[0]),2)) + "!" + line.split("!")[1] + "!\n"]
                break
    
    scoreFile = open("./txt/score.txt", "w")
    scoreFile.writelines(sortedScores)
    scoreFile.close()

def Quit():
    """CLOSES THE ENTIRE GAME"""
    global close
    close = True
    Version()
    pygame.quit()
    sys.exit()

# ====================================== Screens ======================================================================================================================

def Login():
    """LOGIN SCREEN"""
    def register(name):
            data = str(name)
            WriteUser(data)

    def WriteUser(data):
        route = "Users.txt"
        registry = open(route, "a")
        registry.write(data + "\n")
        registry.close()

    def ReadUsers():
        route = "Users.txt"
        registry = open(route)
        content = registry.readlines()
        registry.close()
        return content

    def VerifyUser(data):
        global menuScreen
        if (user+"\n") in data:
            if messagebox.askokcancel("USER", "You're already register in databse, want to play with user: |" +user+ "|"):
                window.destroy()
                ChangeScreens(menu=True)

        else:
            if messagebox.askokcancel("USER", "You aren't in database, want to register?", icon = "warning"):
                register(user)
                window.destroy()
                ChangeScreens(menu=True)

    def VerifyAddUser(data):
        global  menuScreen
        if (user+"\n") in data:
            messagebox.showerror("USER", "This name is already register, please try login or changing username")

        else:
            if messagebox.askokcancel("USER", "You want to add |" +user+ "| to database?"):
                register(user)
                window.destroy()
                ChangeScreens(menu=True)   
 
    def LoginName(name):
        global user
        user = name
        if user == "":
            messagebox.showwarning("ERROR", "PLEASE INSERT A VALID NAME")
        else:
            VerifyUser(ReadUsers())

    def RegisterName(name):
        global user
        user = name
        if user == "":
            messagebox.showwarning("ERROR", "PLEASE INSERT A VALID NAME")
        else:
            VerifyAddUser(ReadUsers())

    def Keydown(e):
        print ("picha")


    window = Tk()
    window.title("AVATARS VS ROOKS LOGIN")
    window.minsize(300, 50)
    window.resizable(False, False)
    window.config(bg = "darkgrey")

    text1 = Label(window, text = "NAME", font = (font, 13), bg = "darkgrey", fg = "black")
    text1.place(x=15, y=27)

    name = Entry(window, width = 30, bg = "white")
    name.place(x=70, y=30)

    login = Button(window, text = "LOGIN", font = (font, 10), bg = "darkgrey", fg = "black", command= lambda :LoginName(name.get()) )
    login.place(x=15, y=70)

    window.bind("<Return>", lambda event:LoginName(name.get()))

    register1 = Button(window, text = "REGISTER", font = (font, 10), bg = "darkgrey", fg = "black", command= lambda : RegisterName(name.get()))
    register1.place(x=100, y=70)

    window.protocol("WM_DELETE_WINDOW", exit)

    window.mainloop()

def Menu():
    """MENU SCREEN"""
    global rookAttackVel, attackVelRect
    game.fill(black)
    vel_text = font3.render(vel, 1, white)

    PrintScreen("MAIN MENU", screenWidth // 2, 100, 70, white)
    PrintScreen("PLEASE SELECT THE BOX AND WRITE A VALUE BETWEEN 5-10", 650, 500, 20, white)
    PrintScreen("TO SET ROOKS'S TIME TO SHOOT, ELSE IT WOULD BE ADD RANDOMLY", 690, 520, 20, white)
    PrintScreen("PLAYER: "+user, 30, 20, 30, gray, True)

    TextButton("PLAY", 120, 200, 120, 40, white, gray, 30, "play", True)

    TextButton("INSTRUCTIONS", 120, 440, 150, 40, white, gray, 30, "info", True)
    TextButton("HALL OF FAME", 120, 520, 150, 40, white, gray, 30, "top", True)
    TextButton("CREDITS", (screenWidth//2)-30, 520, 135, 40, white, gray, 30, "about", True)

    TextButton("LOAD GAME", 1000, 520, 130, 40, white, gray, 30, "load", True)
    TextButton("EXIT", 50, 570, 120, 40, white, gray, 30, "exit", False)
    if velWrite:
        color = white

    else:
        color = colornot

    game.blit(vel_text, (attackVelRect.x + 5, attackVelRect.y + 5))
    pygame.draw.rect(game, color, attackVelRect, 2 )
    attackVelRect.w = vel_text.get_width() + 10

def Game():
    global velWrite
    """GAME SCREEN"""
    game.fill(black)
    velWrite = False
    SetRookAttackVel()
    game.blit(background, (0,0))
    game.blit(wood, (1000, 10))

    game.blit(CoinDrawing, (955, 65))
    PrintScreen(str(coins), 1080, 105, 40, white)
    Grid(0, 0)
    AvatarGenerator()
    AvatarsInteractions(0, len(avatars))
    PlaceRooks(0, len(rooks))
    PlaceCoin(0, len(coin))
    CoinGenerator()
    RookImageMouse()
    PauseButton()

def Pause():
    """PAUSED"""
    global pauseScreen, menuScreen, gameScreen

    game.blit(transparent_black, (0,0))
    PrintScreen("PAUSED", screenWidth // 2, 100, 45, white)

    if screenWidth // 2 + 70 > mouse[0] > screenWidth // 2 - 70 and 310 > mouse[1] > 280:
        PrintScreen("Continue", screenWidth // 2, 300, 30, white)

        if click[0] == 1:
            ChangeScreens(game=True)
    else:
        PrintScreen("Continue", screenWidth // 2, 300, 30, gray)

    if screenWidth // 2 + 160 > mouse[0] > screenWidth // 2 - 160 and 360 > mouse[1] > 340:
        PrintScreen("Return to menu", screenWidth // 2, 350, 30, white)

        if click[0] == 1:
            
            ChangeScreens(menu=True)

    else:
        PrintScreen("Return to menu", screenWidth // 2, 350, 30, gray)

    if screenWidth // 2 + 75 > mouse[0] > screenWidth // 2 - 75 and 465 > mouse[1] > 435:
        PrintScreen("Quit & save", screenWidth // 2, 450, 30, white)
        if click[0] == 1:
            Tk().wm_withdraw()  # not to show tkinter window
            if messagebox.askquestion('Exit Game?', "Want to save progress?",icon='warning') == 'yes':
                GameDataSave()
                SaveRooks()
                SaveAvatars()
                Quit()
            else:
                Quit()
    else:
        PrintScreen("Quit & save", screenWidth // 2, 450, 30, gray)

def Credits():
    """SHOWS INFO ABOUT THE GAME"""
    global creditsPos

    game.fill(black)

    game.blit(luis, (0,100))
    game.blit(sebas, (screenWidth-162,100))
    game.blit(creditsImg, (0, creditsPos))
    creditsPos -= 2

    if creditsPos < - 1300:
        creditsPos = 700
        ChangeScreens(menu=True)

    if PrintScreen("Quit", screenWidth - 35, screenHeight - 20, 25, gray).collidepoint(mouse):
        PrintScreen("Quit", screenWidth - 35, screenHeight - 20, 25, darkGreen)
        if click[0] == 1:
            Tk().wm_withdraw()  # to not show tkinter window
            if messagebox.askquestion('Exit Game?', "Exit game?",icon='warning') == 'yes':
                Quit()

    if PrintScreen("Return to menu", 100, screenHeight - 20, 25, gray).collidepoint(mouse):
        PrintScreen("Return to menu", 100, screenHeight - 20, 25, darkGreen)
        if click[0] == 1:
            ChangeScreens(menu=True)
            creditsPos = 700

def Defeat():
    """DEFEAT SCREEN"""
    game.blit(transparent_black, (0,0))
    PrintScreen("YOU LOOSE", screenWidth//2, screenHeight//2.5, 150, darkRed)

    if PrintScreen("Quit", screenWidth - 35, screenHeight - 20, 25, darkRed).collidepoint(mouse):
        PrintScreen("Quit", screenWidth - 35, screenHeight - 20, 25, red)
        if click[0] == 1:
            Tk().wm_withdraw()  # to not show tkinter window
            if messagebox.askquestion('Exit Game?', "Exit game?",icon='warning') == 'yes':
                Quit()
    if PrintScreen("Return to menu", 100, screenHeight - 20, 25, darkRed).collidepoint(mouse):
        PrintScreen("Return to menu", 100, screenHeight - 20, 25, red)
        if click[0] == 1:
            ChangeScreens(menu=True)

def Win():
    """WIN"""
    #game.fill(white)
    game.blit(transparent_black, (0,0))
    PrintScreen("LEVEL COMPLETED", screenWidth//2, screenHeight//4, 100, sandColor)
    nextLevelRect = PrintScreen("Next level", screenWidth//2, screenHeight//5*2,25, sandColor)

    if nextLevelRect.right + 20 > mouse[0] > nextLevelRect.left - 20 and nextLevelRect.bottom + 10 > mouse[1] > nextLevelRect.top - 10:

        pygame.draw.rect(game, sandColor,[0, nextLevelRect.top - 10, screenWidth, 50])
        PrintScreen("Next level", screenWidth//2, screenHeight//5*2,25, black)
        if click[0] == 1:
            if level == 1:
                LoadLevel(2)
            elif level == 2:
                LoadLevel(3)
            ChangeScreens(game=True)

    quitRect = PrintScreen("Quit & save", screenWidth // 2, 450, 25, sandColor)
    if quitRect.right + 20 > mouse[0] > quitRect.left - 20 and 465 > mouse[1] > 435:
        pygame.draw.rect(game, sandColor,[0, quitRect.top - 10, screenWidth, 50])
        PrintScreen("Quit & save", screenWidth // 2, 450, 25, black)
        if click[0] == 1:
            Tk().wm_withdraw()  # not to show tkinter window
            if messagebox.askquestion('Exit Game?', "Want to save progress?",icon='warning') == 'yes':
                GameDataSave()
                Quit()
            else:
                Quit()

def GameWon():
    """PRINTS THE FINAL SCREEN WHEN GAME IS COMPLETED"""
    global gameWonCounter, coins, creditsPos
    

    if gameWonCounter < 1.3: # SHOWS BUTTONS AFTER SCREEN ANIMATION
        PrintScreen("CONGRATULATONS", screenWidth//2, screenHeight//6, 120, green)
        PrintScreen("YOU COMPLETED", screenWidth//2, screenHeight//3, 80, green)
        PrintScreen("AVATARS VS ROOKS", screenWidth//2, screenHeight//2, 80, green)
        game.blit(transparent_white, (0,0))
        gameWonCounter += 0.034
        return

    game.fill(white)

    game.blit(creditsImg, (0, creditsPos))
    creditsPos -= 2

    pygame.draw.rect(game, white, (0, 0, screenWidth, 400))
    pygame.draw.rect(game, white, (0, screenHeight-45, screenWidth,45))

    PrintScreen("CONGRATULATONS", screenWidth//2, screenHeight//6, 120, green)
    PrintScreen("YOU COMPLETED", screenWidth//2, screenHeight//3, 80, green)
    PrintScreen("AVATARS VS ROOKS", screenWidth//2, screenHeight//2, 80, green)

    if PrintScreen("Hall of fame", screenWidth//2, screenHeight - 20, 30, gray).collidepoint(mouse):
        PrintScreen("Hall of fame", screenWidth//2, screenHeight - 20, 30, darkGreen)
        if click[0] == 1:
            SaveScore()
            ChangeScreens(hallOfFame=True)
            gameWonCounter = 0
            coins = 0
            creditsPos = 700
            
    if PrintScreen("Quit", screenWidth - 35, screenHeight - 20, 25, gray).collidepoint(mouse):
        PrintScreen("Quit", screenWidth - 35, screenHeight - 20, 25, darkGreen)
        if click[0] == 1:
            Tk().wm_withdraw()  # not to show tkinter window
            if messagebox.askquestion('Exit Game?', "Exit game?",icon='warning') == 'yes':
                SaveScore()
                Quit()

    if PrintScreen("Return to menu", 100, screenHeight - 20, 25, gray).collidepoint(mouse):
        PrintScreen("Return to menu", 100, screenHeight - 20, 25, darkGreen)
        if click[0] == 1:
            SaveScore()
            ChangeScreens(menu=True)
            gameWonCounter = 0
            coins = 0
            creditsPos = 700
            
def HallOfFame():
    """HALL OF FAME SCREEN"""
    global scoreYPos
    
    game.fill(black)
    lastScoreYPos = 700
    for i in range(0,len(scoreLines)):
        lastScoreYPos = scoreYPos + i*60
        pygame.draw.rect(game, ultraDarkGray, (0, scoreYPos + i*60 - 15, screenWidth, 30))
        PrintScreen(str(i+1) + ". " + scoreLines[i][0] + "s, : " + scoreLines[i][1], 200, scoreYPos + i*60, 30, white, True)
        
    pygame.draw.rect(game, black, (0,0,screenWidth,200))
    pygame.draw.rect(game, black, (0,screenHeight-45,screenWidth,45))
    PrintScreen("Hall of fame", screenWidth//2, 100, 100, sandColor)

    if PrintScreen("Quit", screenWidth - 35, screenHeight - 20, 25, darkGray).collidepoint(mouse):
        PrintScreen("Quit", screenWidth - 35, screenHeight - 20, 25, white)
        if click[0] == 1:
            Tk().wm_withdraw()  # not to show tkinter window
            if messagebox.askquestion('Exit Game?', "Exit game?",icon='warning') == 'yes':
                Quit()
    if PrintScreen("Return to menu", 100, screenHeight - 20, 25, darkGray).collidepoint(mouse):
        PrintScreen("Return to menu", 100, screenHeight - 20, 25, white)
        if click[0] == 1:
            ChangeScreens(menu=True)
            scoreYPos = 300

    if scoreYPos < 300:
        if PrintScreen("UP", screenWidth//3, screenHeight-20, 25, darkGreen).collidepoint(mouse):
            PrintScreen("UP", screenWidth//3, screenHeight-20, 25, green)
            if click[0] == 1:
                scoreYPos += 10
    if scoreYPos < 300:
        if PrintScreen("TOP", screenWidth//2, screenHeight-20, 25, darkGreen).collidepoint(mouse):
            PrintScreen("TOP", screenWidth//2, screenHeight-20, 25, green)
            if click[0] == 1:
                scoreYPos = 300
    
    if lastScoreYPos > screenHeight-100:
        if PrintScreen("DOWN", screenWidth/3*2, screenHeight-20, 25, darkGreen).collidepoint(mouse):
            PrintScreen("DOWN", screenWidth/3*2, screenHeight-20, 25, green)
            if click[0] == 1:
                scoreYPos -= 10

def Instructions():
    """SHOWS INSTRUCTIONS"""
    game.blit(instructionsImg, (0,0))
    if PrintScreen("Quit", screenWidth - 35, screenHeight - 20, 25, gray).collidepoint(mouse):
        PrintScreen("Quit", screenWidth - 35, screenHeight - 20, 25, white)
        if click[0] == 1:
            Tk().wm_withdraw()  # to not show tkinter window
            if messagebox.askquestion('Exit Game?', "Exit game?",icon='warning') == 'yes':
                Quit()

    if PrintScreen("Return to menu", 100, screenHeight - 20, 25, gray).collidepoint(mouse):
        PrintScreen("Return to menu", 100, screenHeight - 20, 25, white)
        if click[0] == 1:
            ChangeScreens(menu=True)


#=====================================================================================================================================================================================================

#===================================================      Avatars Class      =========================================================================================================================

#=====================================================================================================================================================================================================

class Avatars:
    def __init__(self, x, y, avatarType, avatarAttackDamage, health, movingTime, shootingTime):
        """INITIALIZATION OF AVATAR"""
        self.x = x
        self.y = y
        self.avatarType = avatarType
        self.avatarAttackDamage = avatarAttackDamage
        self.health = health
        self.actualHealth = health
        self.movingTime = movingTime
        self.shootingTime = shootingTime
        self.lastMovedTime = elapsedTime
        self.nextAttack = elapsedTime #+ shootingTime

        # AVATAR IMAGES
        if avatarType == -1:
            self.avatarImg = archerAvatar
            self.avatarAnimationImgs = archerAvatarAnimation
            self.projectileImg = arrow
        elif avatarType == -2:
            self.avatarImg = knightAvatar
            self.avatarAnimationImgs = knightAvatarAnimation
            self.projectileImg = sword
        elif avatarType == -3:
            self.avatarImg = lumberjackAvatar
            self.avatarAnimationImgs = lumberjackAvatarAnimation
            self.projectileImg = None
        else:
            self.avatarImg = cannibalAvatar
            self.avatarAnimationImgs = cannibalAvatarAnimation
            self.projectileImg = None


        # ANIMATION VARIABLES
        self.proX = 0
        self.attacking = False
        self.animateAttack = False
        self.animationNum = 0

    def Save(self):
        global allAvatars
        return [self.x, self.y, self.avatarType, self.avatarAttackDamage, self.health, self.movingTime, self.shootingTime]

    def MoveAvatar(self): 
        """PLACES AVATAR IN NEXT SQUARE WHEN MOVING TIME HAS PASSED AND IS NOT ANY OBSTACLE IN FRONT"""
        global gameMatrixGrid
        if elapsedTime - self.lastMovedTime >= self.movingTime-(level-1)*2:
            self.lastMovedTime = elapsedTime
            if self.x == 0:
                ChangeScreens(defeat=True)
                return
            else:
                if gameMatrixGrid[self.y][self.x-1] == 0:
                    gameMatrixGrid[self.y][self.x] = 0
                    self.x -= 1
                    gameMatrixGrid[self.y][self.x] = self.avatarType
        else: 
            return

    def AnimateAttack(self):
        """ANIMATES AVATAR BEFORE ATTACKING"""

        if not self.animateAttack:
            return

        if self.animationNum > 40:
            
            self.animationNum = 0
            self.attacking = True

            if self.avatarType == -1:
                pygame.mixer.Sound.play(arrowShootSound)
                self.avatarImg = archerAvatar

            elif self.avatarType == -2:
                pygame.mixer.Sound.play(swordShootSound)
                self.avatarImg = knightAvatar

            else:
                if self.avatarType == -4:
                    self.avatarImg = cannibalAvatar
                else:
                    self.avatarImg = lumberjackAvatar

                pygame.mixer.Sound.play(meleeSound)
                if self.avatarType == -3:
                    pygame.mixer.Sound.play(axeHitSound)
                else:
                    pygame.mixer.Sound.play(clubHitSound)

                for rook in rooks:
                    if rook.GetPos()[0] == self.x - 1 and rook.GetPos()[1] == self.y:
                        rook.DamageRecieved(self.avatarAttackDamage)
                        continue
                

            self.animateAttack = False
            return
        self.avatarImg = self.avatarAnimationImgs[self.animationNum//10]
        self.animationNum += 1

    def GetPos(self):
        """GIVES MATRIX POSITION"""
        return [self.x, self.y]

    def HitRecieved(self, damage):
        """REDUCES LIFE WHEN HIT"""
        if damage > 0:
            self.health -= damage

    def Health(self):
        """PRINTS LIFE BAR"""
        pygame.draw.rect(game, darkRed, [self.x*90 + 55 + 10, self.y*90 + 50 + 82, 50, 5])
        pygame.draw.rect(game, darkGreen, [self.x*90 + 55 + 10, self.y*90 + 50 + 82, int(self.actualHealth*50/self.health), 5])

    def Death(self):
        """CHECKS IS AVATAR IS DEAD"""
        global gameMatrixGrid
        if self.actualHealth < 1:
            gameMatrixGrid[self.y][self.x] = 0
            pygame.mixer.Sound.play(avatarKillSound)
            return True
        else:
            return False

    def PlaceAvatar(self):
        """PRINTS THE AVATAR IN ITS POSITION"""
        game.blit(self.avatarImg, (60 + self.x * 90, 60 + self.y * 90))

    def Attack(self):
        """ATTACKS ROOKS"""

        if self.avatarType > -3:
            #RANGER AVATARS 
            if self.RangerAttack() and self.nextAttack <= elapsedTime:
                
                self.nextAttack = elapsedTime + self.shootingTime-(level-1)*2

                if self.avatarType == -1:
                    #ARCHER
                    self.animateAttack = True

                elif self.avatarType == -2:
                    #KIGHT
                    self.animateAttack = True

        elif self.MeleeAttack() and self.nextAttack <= elapsedTime:
            self.animateAttack = True
            self.nextAttack = elapsedTime + self.shootingTime

    def AnimateRangeAttack(self):
        """MOVES THE RANGED OBJECT"""
        if not self.attacking:
            return
        if self.attacking and self.avatarType > -3:
            #IF ITS ATTACKING

            if self.x*90+40+self.proX > 0:
                #IF PROYECTILE IS STILL ON SCREEN
                self.proX -=8

            else:
                #RESET PROJECTILE POSITION AND DON'T SHOW IT ANYMORE
                self.proX = 0
                self.attacking = False
        
            game.blit(self.projectileImg, [40+self.x*90+self.proX, 60+self.y*90])

    def MeleeAttack(self):
        """CHECKES IF THERE IS AN ENEMY IN THE NEXT MATRIX GRID"""
        if self.x == 0:
            return False
        else:
            return gameMatrixGrid[self.y][self.x - 1] > 0

    def RangerAttack(self):
        """CHECKS IF THERE ARE FRONT ENEMIES"""
        if self.x == 0:
            return False

        for i in range(0, self.x):
            if gameMatrixGrid[self.y][i] > 0:
                return True
        else:
            return False

    def GetDamage(self):
        """GIVES THE AVATAR DAMAGE"""
        return self.avatarAttackDamage

    def GetAttackPos(self):
        """GIVES THE POSITION OF THE PROJECTILE"""
        return (self.x*90+40+self.proX, 60+self.y*90)

    def ResetProjectile(self):
        """RESETS THE POSITION OF PROJECTILE AND HIDES IT"""
        self.proX = 0
        self.attacking = False
        if self.avatarType == -1:
            pygame.mixer.Sound.play(arrowHitSound)
        elif self.avatarType == -2:
            pygame.mixer.Sound.play(swordHitSound)
        return

    def Collision(self):
        """DETECTS COLLISION WITH ENEMY PROJECTILES"""
        for rook in rooks:
            if 60 + self.x * 90 < rook.GetAttackPos()[0] and 60 + self.y * 90 == rook.GetAttackPos()[1]:
            #if math.sqrt(((60 + self.x * 90 - rook.GetAttackPos()[0])**2 + (60+self.y*90 - rook.GetAttackPos()[1])**2)) < 20:
                self.actualHealth -= rook.GetDamage()
                rook.ResetProjectile()


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Rooks:
    def __init__(self, xpos, ypos, damage, shootingTime, image, animation, health, type):
        self.xpos = xpos
        self.ypos = ypos
        self.damage = damage
        self.health = health
        self.shootingTime = rookAttackVel
        self.time = shootingTime
        self.AttackCollision = False
        self.Verify = True
        self.xani = xpos
        self.yani = ypos
        self.actualhealth = health
        self.xanim = 0
        self.type = type
        self.ImageCopy = image
        self.AniCopy = animation
        if image == 1:
            self.image = water

        elif image == 2:
            self.image = sand

        elif image == 3:
            self.image = rock

        else:
            self.image = fire

        if animation == 1:
            self.animation = waterA

        elif animation == 2:
            self.animation = sandA

        elif animation == 3:
            self.animation = rockA

        else:
            self.animation = fireA

    def Vel(self):
        if self.Verify == False:
            if self.shootingTime < 1:
                self.Verify = True
                self.shootingTime = rookAttackVel
            else:
                self.shootingTime -= 0.05

    def CheckFront(self):   
        #gamematrix[][self.xpos] 
        i = 0
        verify = False
        while i < 9:
            if gameMatrixGrid[self.ypos][i] >= 0:
                verify = False
            
            else:
                verify = True
                break

            i += 1
        return verify

    def attack(self):
        global rookAttackVel
        if self.Verify:
                if self.xani * 90 + 60 + self.xanim < 900:
                    if self.xanim !=0:
                        pass
                    elif self.type == 1:
                        pygame.mixer.Sound.play(waterSound)

                    elif self.type == 2:
                        pygame.mixer.Sound.play(sandSound)

                    elif self.type == 3:
                        pygame.mixer.Sound.play(rockSound)

                    elif self.type == 4:
                        pygame.mixer.Sound.play(fireSound)
                    self.xanim += 16

                else:
                    self.Verify = False
                    self.xanim = 0

                game.blit(self.animation, (40 + self.xani * 90 + self.xanim, 60 + self.yani * 90))

    def ResetProjectile(self):
        self.Verify = False
        self.xanim = 0

    def draw(self):
        game.blit(self.image, (self.xpos, self.ypos))

    def Death(self):
        global gameMatrixGrid
        if self.actualhealth < 1:
            gameMatrixGrid[self.ypos][self.xpos] = 0
            return True
        else:
            return False

    def GetAttackPos(self):
        return (60 + self.xani * 90 + self.xanim, 60 + self.yani * 90)

    def PlaceRook(self):
        game.blit(self.image, (60 + self.xpos * 90, 60 + self.ypos * 90))

    def Health(self):
        pygame.draw.rect(game, darkRed, [self.xpos * 90 + 55 + 10, self.ypos * 90 + 50 + 82, 50, 5])
        pygame.draw.rect(game, darkGreen,[self.xpos * 90 + 55 + 10, self.ypos * 90 + 50 + 82, int(self.actualhealth*50/self.health), 5])

    def DamageRecieved(self, damage):
        self.actualhealth -= damage

    def Delete(self):
        click = pygame.mouse.get_pressed()
        if math.sqrt((60 + self.xpos * 90 - mouse[0])**2 + (60 + self.ypos * 90 - mouse[1])**2) < 60:
            if click[2] == 1:
                gameMatrixGrid[self.ypos][self.xpos] = 0
                return True

            else:
                return False

    def collision(self):
        for avatar in avatars:
            if math.sqrt((60 + self.xpos * 90 - avatar.GetAttackPos()[0])**2 + (60 + self.ypos * 90 - avatar.GetAttackPos()[1])**2) < 10:
                self.actualhealth -= avatar.GetDamage()

                avatar.ResetProjectile()

    def GetDamage(self):
        return self.damage
      
    def GetPos(self):
        return [self.xpos, self.ypos]

    def Type(self):
        return self.image

    def Save(self):
        global allRooks
        return [self.xpos, self.ypos, self.damage,round(self.shootingTime), self.ImageCopy, self.AniCopy, self.health, self.type]


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Coin:
    def __init__(self, xpos, ypos, value, image):
        self.xpos = xpos
        self.ypos = ypos
        self.value = value
        self.image = image
        self.death = False

    def draw(self):
        global mouse, coins
        click = pygame.mouse.get_pressed()
        if self.xpos + 100 > mouse[0] > self.xpos and self.ypos + 103 > mouse[1] > self.ypos:
            if click[0] == 1 and coins < 10000:
                coins += self.value
                self.death = True

        game.blit(self.image, (self.xpos, self.ypos))

    def Erase(self):
        if self.death:
            return True

        else:
            return False


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def ChangeScreens(menu=False, game=False, pause=False, defeat=False, hallOfFame=False, win=False, gameWon=False, creditS=False, instructions=False):

    global musicPlaying, menuScreen, gameScreen, pauseScreen, defeatScreen, hallOfFameScreen, winScreen, gameWonScreen, refreshRate, timeCounting, creditsScreen, instructionsScreen, elapsedTime

    menuScreen = menu
    gameScreen = game
    pauseScreen = pause
    defeatScreen = defeat
    hallOfFameScreen = hallOfFame
    winScreen = win
    gameWonScreen = gameWon
    creditsScreen = creditS
    instructionsScreen = instructions

    # COUNTS TIME ONLY IF GAME IS RUNNING
    timeCounting = game
    
    if game:
        refreshRate = 60
    elif gameWon:
        refreshRate = 30
    else:
        refreshRate = 20
    
    if hallOfFame:
        LoadScore()
    elif menu:
        if musicPlaying != "Menu":
            pygame.mixer.music.load("sounds/music/menuTheme.wav")
            pygame.mixer.music.play(-1)
            musicPlaying = "Menu"
        elapsedTime = 0
    elif defeat:
        pygame.mixer.music.load("sounds/music/defeatTheme.wav")
        pygame.mixer.music.play()
        musicPlaying = "Defeat"

def MouseVariables():
    """DECLARES MOUSE POSITION AND CLICK"""
    global mouse, click
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

def ScorePos(increment):
    global scoreYPos
    scoreYPos += increment

def CoinsHack():
    global coins
    coins += 1000

# RUNS LOGIN BEFORE PYGAME SCREEN
Login()

# RUNS PYGAME AFTER LOGIN
game = pygame.display.set_mode((screenWidth, screenHeight))

# RUNS THE TIME THREAD
timeThread = threading.Thread(target=Time)
timeThread.daemon = True
timeThread.start()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # checks if user wants to exit the program
            Quit()

        # DETECTS KEYS WHEN GAME IS RUNNING
        elif gameScreen:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ChangeScreens(pause=True)
                    pygame.mixer.music.pause()
                elif event.key == pygame.K_RCTRL:
                    ChangeScreens(creditS=True)
                elif event.key == pygame.K_h:
                    ChangeScreens(hallOfFame=True)

                # PROGRAMING SHORTCUTS
                elif event.key == pygame.K_END:
                    ChangeScreens(gameWon=True)
                elif event.key == pygame.K_HOME:
                    ChangeScreens(win=True)
                elif event.key == pygame.K_PAUSE:
                    CoinsHack()
                elif event.key == pygame.K_RALT:
                    ChangeScreens(defeat=True)
                    
        # DETECT KEYS WHEN GAME IS PAUSED
        elif pauseScreen:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ChangeScreens(game=True)
                    pygame.mixer.music.unpause()

    
        if event.type == pygame.MOUSEBUTTONDOWN:#checks if a button of the mouse was pressed
            if math.sqrt((mouse[0] - 1050) ** 2 + (mouse[1] - 485) ** 2) < 100:#checks for collison between mouse and the rectangle in lower part of main menu
                velWrite = True

        if event.type == pygame.KEYDOWN:#checks if keys of the keyboard are pressed
            if velWrite:
                if event.key == pygame.K_BACKSPACE:#if user uses backspace, it would delete a character
                    vel = vel[:-1]

                elif event.key == pygame.K_RETURN:#if user press enter, it would stop writing
                    velWrite = False

                else:
                    vel += event.unicode# any other keys would be added while writing

    MouseVariables() # UPDATES MOUSE POSITION AND CLICK VALUES

    if menuScreen: Menu()   #SHOWS MENU
    elif gameScreen: Game()   #SHOWS GAME
    elif pauseScreen: Pause() #SHOWS PAUSE SCREEN
    elif defeatScreen: Defeat() #SHOWS DEFEAT SCREEN
    elif winScreen: Win()     #SHOWS WIN SCREEN
    elif hallOfFameScreen: HallOfFame() #SHOWS HALL OF FAME
    elif gameWonScreen: GameWon()
    elif creditsScreen: Credits()
    elif instructionsScreen: Instructions()
    else: ChangeScreens(menu=True)

    pygame.display.update()

    FPS.tick(refreshRate)