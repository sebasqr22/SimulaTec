import pygame
import sys
from pygame import mixer
import random
import math
import winsound

sys.setrecursionlimit(10**9)
pygame.init()
mixer.init()

# global variables
x_carro = 1035
y_carro = 550

width = 1190
height = 700
y = 0

xpos = random.randrange(707, 1040)
ypos = -100

x_truck = random.randrange(710, 1030)
y_truck = -800

x_tesla = 1040
y_tesla = -1000

orangex = random.randrange(703, 1040)
orangey = -1300

hondax = 750
honday = 900

lives = 3
score = 0
gas = 100
finish_time = 300
velocity = 100
score_time = 0
seleccion = 0
ReWriteName = 0
quantityWRITE = 0
user = ""#user name
user_rect = pygame.Rect(15, 600, 140, 32)#rectangle to write name

FPS = pygame.time.Clock()

# ============

# Colors
redc = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
lightblue = (135, 206, 235)
colornot = pygame.Color("gray15")
color = colornot
active = False
# ====================

game = pygame.display.set_mode((width, height))
pygame.display.set_caption("HONDA CIVIC BOMBOCLAT")

font = pygame.font.SysFont("comicsans", 50)
font2 = pygame.font.SysFont("comicsans", 90)
font3 = pygame.font.SysFont("comicsans", 25)

# Images
hondaT = pygame.image.load("Pics/hondaT.png")
civicT = pygame.image.load("Pics/civic.png")
bomboT = pygame.image.load("Pics/bomboT.png")
clatT = pygame.image.load("Pics/clatT (2).png")
honda_logo = pygame.image.load("Pics/logoH.png")
bag = pygame.image.load("Pics/city.png")
level1 = pygame.image.load("Pics/level1B.png")
level2 = pygame.image.load("Pics/level2B.png")
level3 = pygame.image.load("Pics/level3B.png")
beach = pygame.image.load("Pics/background.jpg")
heart = pygame.image.load("Pics/heart.png")
bam = pygame.image.load("Pics/bamP.png")
speed = pygame.image.load("Pics/speed.png")
mainmenu = pygame.image.load("Pics/mainmenuB.png")
retry = pygame.image.load("Pics/retry.png")
instructions = pygame.image.load("Pics/instructionsB.png")
tec = pygame.image.load("Pics/logo-tec.png")
programmer = pygame.image.load("Pics/programmerB.png")
top = pygame.image.load("Pics/scores.png")

# cars
honda = pygame.image.load("Pics/carro.png")
red = pygame.image.load("Pics/redCAR.png")
truck = pygame.image.load("Pics/truckP.png")
tesla = pygame.image.load("Pics/teslaP.png")
orange = pygame.image.load("Pics/skrtP.png")
truckCO = pygame.image.load("Pics/truckCO.png")
# ================================================
mixer.music.load("intro.mp3")#contains the music
mixer.music.play(-1)#plays the music

def userDATA(name, score1):
    if isinstance(name, str) and isinstance(score1, float):#Verifies if user data can be added
        return AddUser(name, score1)
    else:
        return "YOUR DATA CAN'T BE ADD"

def ReadData():
    route = "User_Info.txt"
    registry = open(route)
    content = registry.readlines() #gets info from the .txt
    registry.close()
    return content

def WriteData(info): #writes the user info in the .txt
    route = "User_Info.txt"
    registry = open(route, "a")
    registry.write(info+ "\n")
    registry.close()

def AddUser(name, score1):#creates the correct format to write the info
    data = name+ "," +str(score1)
    WriteData(data)

def HighScore(data, scoreUSER, counter, length, highscore):#checks who has the highest score
    print(data[counter].split(",")[1][1])
    if counter == (length-1):
        return highscore

    elif float(data[counter].split(",")[1]) > float(highscore):
            return HighScore(data, scoreUSER, counter + 1, length, float(data[counter].split(",")[1]))

    else:
            return HighScore(data, scoreUSER, counter + 1, length, highscore)

highscore1 = HighScore(ReadData(), score, 0, len(ReadData()), 0.0)# calls the function that verifies who has the highest score

def WorstScore(data, worst):#function to find who was the worst score
    if data == []:
        return worst

    elif float(data[0].split(",")[1]) < worst:
        return WorstScore(data[1:], float(data[0].split(",")[1]))

    else:
        return WorstScore(data[1:], worst)

worst_score = WorstScore(ReadData(), 1000)

def ScoresOrder(data, highscore, pos2, pos3, pos4, pos5, pos6, pos7, trash, order, length, counter, repeatTIMES):
    if repeatTIMES == length:
        order = [highscore, pos2, pos3, pos4, pos5, pos6, pos7, trash]
        return order

    else:
        if counter == length:
            return ScoresOrder(data, highscore, pos2, pos3, pos4, pos5, pos6, pos7, trash, order, length, 0, repeatTIMES+1)

        else:
            if float(data[counter].split(",")[1]) >= pos2 and float(data[counter].split(",")[1]) < highscore:
                return ScoresOrder(data, highscore, float(data[counter].split(",")[1]), pos3, pos4, pos5, pos6, pos7, trash, order, length, counter+1, repeatTIMES)

            elif float(data[counter].split(",")[1]) >= pos3 and float(data[counter].split(",")[1]) < pos2:
                return ScoresOrder(data, highscore, pos2, float(data[counter].split(",")[1]), pos4, pos5, pos6, pos7, trash, order, length, counter+1, repeatTIMES)

            elif float(data[counter].split(",")[1]) >= pos4 and float(data[counter].split(",")[1]) <= pos3:
                return ScoresOrder(data, highscore, pos2, pos3, float(data[counter].split(",")[1]), pos5, pos6, pos7, trash, order, length, counter+1, repeatTIMES)

            elif float(data[counter].split(",")[1]) >= pos5 and float(data[counter].split(",")[1]) <= pos4:
                return ScoresOrder(data, highscore, pos2, pos3, pos4, float(data[counter].split(",")[1]), pos6, pos7, trash, order, length, counter+1, repeatTIMES)

            elif float(data[counter].split(",")[1]) >= pos6 and float(data[counter].split(",")[1]) < pos5:
                return ScoresOrder(data, highscore, pos2, pos3, pos4, pos5, float(data[counter].split(",")[1]), pos7, trash, order, length, counter+1, repeatTIMES)

            elif float(data[counter].split(",")[1]) >= pos7 and float(data[counter].split(",")[1]) < pos6:
                return ScoresOrder(data, highscore, pos2, pos3, pos4, pos5, pos6, float(data[counter].split(",")[1]), trash, order, length, counter+1, repeatTIMES)

            else:
                return ScoresOrder(data, highscore, pos2, pos3, pos4, pos5, pos6, pos7, float(data[counter].split(",")[1]), order, length, counter+1, repeatTIMES)

ScoreOrder = ScoresOrder(ReadData(), highscore1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, [], len(ReadData()), 0, 0)
pos2 = ScoreOrder[1]
pos3 = ScoreOrder[2]
pos4 = ScoreOrder[3]
pos5 = ScoreOrder[4]
pos6 = ScoreOrder[5]
pos7 = ScoreOrder[6]



def ScoreScreen():
    game.fill(black)

    best = font2.render("BEST SCORES SO FAR!!!!!", 1, white)
    l1TEXT1 = font2.render("1 PLACE:" +str(highscore1), 1, white)
    l1TEXT2 = font2.render("2 PLACE:" + str(pos2), 1, white)
    l1TEXT3 = font2.render("3 PLACE:" + str(pos3), 1, white)
    l1TEXT4 = font2.render("4 PLACE:" + str(pos4), 1, white)
    l1TEXT5 = font2.render("5 PLACE:" + str(pos5), 1, white)
    l1TEXT6 = font2.render("6 PLACE:" + str(pos6), 1, white)
    l1TEXT7 = font2.render("7 PLACE:" + str(pos7), 1, white)
    game.blit(best, (250, 0))
    game.blit(l1TEXT1, (100, 100))
    game.blit( l1TEXT2,(100, 150))
    game.blit(l1TEXT3, (100, 200))
    game.blit(l1TEXT4, (100, 250))
    game.blit(l1TEXT5, (100, 300))
    game.blit(l1TEXT6, (100, 350))
    game.blit(l1TEXT7, (100, 400))
    button(400, 600, 300, 45, mainmenu, white, "menu", "no")#calls button function
def intructions():#all the instructions needded to play the game
    game.fill(black)
    ins1 = font3.render("YOU ARE CONTROLLING A MODIFY HONDA CIVIC THAT IS LOOSING TO MUCH GAS VERY FAST", 1, white)
    ins2 = font3.render("THE ARE 4 TYPES OF CARS THAT ARE CONSIDERED AS ENEMIES", 1, white)
    ins2_1 = font3.render("YOU CAN MOVE THE HONDA WITH LETTERS (W, S, A, D) OR KEYBOARD ARROWS", 1, white)
    ins3 = font3.render("IF COLLIDE LOSES 1 LIVE", 1, white)
    ins4 = font3.render("IF COLLIDE, LOSES 2 LIVES", 1, white)
    ins5 = font3.render("CHANGES LANE, IF COLLIDE LOSES 1 LIVE", 1, white)
    ins6 = font3.render("IF COLLIDE, WINS 500PTS AND ELLON MUSK WOULD BE PROUD!", 1, white)
    game.blit(ins1, (10, 50))
    game.blit(ins2_1, (10, 70))
    game.blit(ins2, (10, 90))
    game.blit(red, (60, 310))
    game.blit(ins3, (10, 480))
    game.blit(truckCO, (300, 200))
    game.blit(ins4, (230, 170))
    game.blit(orange, (610, 200))
    game.blit(ins5, (560, 170))
    game.blit(tesla, (900, 310))
    game.blit(ins6, (600, 480))
    game.blit(honda_logo, (1000, 0))

    button(400, 600, 300, 45, mainmenu, white, "menu", "no")#calls button function

def programmer_screen():#screen in which there is info of who create the game and in which country and university
    game.fill(black)
    game.blit(tec, (905, 3))

    pro1 = font.render("INSTITUTO TECNOLÓGICO DE COSTA RICA", 1, white)
    pro2 = font.render("COMPUTER ENGINEERING", 1, white)
    pro3 = font.render("COURSE --> TALLER DE PROGRAMACIÓN", 1, white)
    pro4 = font.render("PROFRESOR: JAISON LEITÓN JIMENEZ",1, white)
    pro5 = font.render("VERSION 1.0", 1, white)
    pro6 = font.render("PROGRAMMER --> SEBASTIÁN QUESADA ROJAS", 1, white)
    pro7 = font.render("COSTA RICA -- 2020", 1, white)

    game.blit(pro1,(250, 70))
    game.blit(pro2, (370, 130))
    game.blit(pro3, (270, 190))
    game.blit(pro4, (280, 250))
    game.blit(pro5, (400, 310))
    game.blit(pro6, (220, 370))
    game.blit(pro7, (350, 430))

    button(400, 600, 300, 45, mainmenu, white, "menu", "no")

def crash(x_position, y_position):#function to display image in case of collision
    #crash_boom = pygame.mixer.Sound("collision.wav")
    #crash_boom.play()
    bam = pygame.image.load("Pics/bamP.png")
    game.blit(bam, (x_position - 200, y_position - 200))

def lose_screem3():#screen in case you lose level3
    global seleccion, user, score, highscore1, quantityWRITE
    final_score = font2.render("YOUR FINAL SCORE IS: " + str(score) + "pts", 1, redc)
    text_lose = font2.render("IT LOOKS LIKE YOU LOSE SON...", 1, redc)
    gas_text = font2.render("YOU HAVE NO GAS UH?", 1, redc)
    high1 = font.render("YOU ARE THE HIGHEST SCORE SO FAR", 1, redc)
    if quantityWRITE == 0:
        quantityWRITE += 1
        userDATA(user, score)

    game.blit(beach, (0, 0))
    game.blit(text_lose, (150, 250))
    game.blit(final_score, (150, 400))
    button(100, 600, 300, 72, mainmenu,white,  "menu")
    button(500, 600, 300, 72, retry,white,  "go3", "retry")
    if gas < 5:
        game.blit(gas_text, (150, 500))

    if score > highscore1:
        game.blit(high1, (150, 50))


def lose_screen2():#screen in case you lose level2
    global seleccion, user, score, highscore1, quantityWRITE
    final_score = font2.render("YOUR FINAL SCORE IS: " + str(score) + "pts", 1, redc)
    text_lose = font2.render("IT LOOKS LIKE YOU LOSE SON...", 1, redc)
    gas_text = font2.render("YOU HAVE NO GAS UH?", 1, redc)

    if quantityWRITE == 0:
        quantityWRITE += 1
        userDATA(user, score)
        HighScore(ReadData(), score, 0, len(ReadData()), highscore1)

    game.blit(beach, (0, 0))
    game.blit(text_lose, (150, 250))
    game.blit(final_score, (150, 400))
    button(100, 600, 300, 72, mainmenu,white,  "menu")
    button(500, 600, 300, 72, retry, white, "go2", "retry")
    if gas < 5:
        game.blit(gas_text, (150, 500))


def lose_screen():#screen in case you lose level1
    global seleccion, user, score, highscore1, quantityWRITE
    final_score = font2.render("YOUR FINAL SCORE IS: " + str(score) + "pts", 1, redc)
    text_lose = font2.render("IT LOOKS LIKE YOU LOSE SON...", 1, redc)
    gas_text = font2.render("YOU HAVE NO GAS UH?", 1, redc)
    high1 = font.render("YOU ARE THE HIGHEST SCORE SO FAR", 1, redc)
    if quantityWRITE == 0:
        quantityWRITE += 1
        userDATA(user, score)


    game.blit(beach, (0, 0))
    game.blit(text_lose, (150, 250))
    game.blit(final_score, (150, 400))
    button(100, 600, 300, 72, mainmenu,white,  "menu")
    button(500, 600, 300, 72, retry, white, "go1", "retry")
    if gas < 5:
        game.blit(gas_text, (150, 500))

    if score > highscore1:
        game.blit(high1, (150, 50))



def win_screen3():#screen in case you win level3
    global seleccion, user, score, highscore1, quantityWRITE
    final_score = font2.render("YOUR FINAL SCORE IS: " + str(score) + "pts", 1, redc)
    text_win = font2.render("YOU WIN BRO!!!!!!!", 1, redc)
    honda2 = pygame.image.load("Pics/hondacar2.png")
    high1 = font.render("YOU ARE THE HIGHEST SCORE SO FAR", 1, redc)

    if quantityWRITE == 0:
        quantityWRITE += 1
        userDATA(user, score)


    game.blit(beach, (0, 0))
    game.blit(text_win, (150, 300))
    game.blit(honda2, (hondax, honday))
    game.blit(final_score, (150, 400))
    # seleccion = 0
    button(100, 600, 300, 72, mainmenu,white, "menu")
    button(500, 600, 300, 72, retry, white, "go3", "retry")
    if score > highscore1:
        game.blit(high1, (150, 50))



def win_screen2():#screen in case you win level2
    global seleccion, user, score, highscore1, quantityWRITE
    final_score = font2.render("YOUR FINAL SCORE IS: " + str(score) + "pts", 1, redc)
    text_win = font2.render("YOU WIN BRO!!!!!!!", 1, redc)
    honda2 = pygame.image.load("Pics/hondacar2.png")
    high1 = font.render("YOU ARE THE HIGHEST SCORE SO FAR", 1, redc)

    if quantityWRITE == 0:
        quantityWRITE += 1
        userDATA(user, score)

    game.blit(beach, (0, 0))
    game.blit(text_win, (150, 300))
    game.blit(honda2, (hondax, honday))
    game.blit(final_score, (150, 400))
    # seleccion = 0
    button(100, 600, 300, 72, mainmenu,white, "menu")
    button(500, 600, 300, 72, retry,white, "go2", "retry")

    if score > highscore1:
        game.blit(high1, (150, 50))


def win_screen():#screen in case you win level1
    global seleccion, user, score, highscore1, quantityWRITE
    final_score = font2.render("YOUR FINAL SCORE IS: " + str(score) + "pts", 1, redc)
    text_win = font2.render("YOU WIN BRO!!!!!!!", 1, redc)
    honda2 = pygame.image.load("Pics/hondacar2.png")
    high1 = font.render("YOU ARE THE HIGHEST SCORE SO FAR", 1, redc)

    if quantityWRITE == 0:
        quantityWRITE += 1
        userDATA(user, score)

    game.blit(beach, (0, 0))
    game.blit(text_win, (150, 300))
    game.blit(honda2, (hondax, honday))
    game.blit(final_score, (150, 400))
    button(100, 600, 300, 72, mainmenu, white, "menu", "no")
    button(500, 600, 300, 72, retry,white, "go1", "retry")

    if score > highscore1:
        game.blit(high1, (150, 50))


#======================================================================================================================
#Function where all the game development is display
def highway_game1(vel, velRed, velTRUCK, velTESLA, orangevel, velROAD):
    global x_carro, y_carro, xpos, ypos, x_truck, y_truck, x_tesla, y_tesla, orangex, orangey, score, finish_time, lives, y, velocity, gas, user, ReWriteName, collide
    if lives > 0 and lives < 4 and finish_time != 0 and gas != 0:
        ReWriteName += 1
        game.fill(black)
        var_y = y % beach.get_rect().width
        game.blit(beach, (0, var_y - beach.get_rect().width))

        pygame.time.delay(20)
        #if var_y < width:
        game.blit(beach, (0, var_y))
        game.blit(honda, (x_carro, y_carro))
        game.blit(red, (xpos, ypos))
        game.blit(truck, (x_truck, y_truck))
        game.blit(tesla, (x_tesla, y_tesla))
        game.blit(orange, (orangex, orangey))
        game.blit(speed, (0, 436))

        pygame.draw.rect(game, black, [350, 635, 310, 60])
        pygame.draw.rect(game, redc, [355, 640, 300, 50])
        pygame.draw.rect(game, green, [355, 640, gas * 3, 50])

        text = font.render("SCORE: " + str(score), 1, black)
        game.blit(text, (10, 10))  # https://www.youtube.com/watch?v=JLUqOmE9veI

        livesTEXT = font.render("LIVES :", 1, black)
        game.blit(livesTEXT, (10, 70))

        timeP = font.render("TIME:" + str(finish_time / 10) + "seconds", 1, black)
        game.blit(timeP, (10, 190))

        velTEXT = font.render(str(velocity), 1, black)
        game.blit(velTEXT, (85, 552))

        gasTEXT = font.render("GAS", 1, black)
        game.blit(gasTEXT, (450, 600))

        player = font.render("PLAYER :"+user, 1, black)
        game.blit(player, (10, 400))

        y += velROAD

        if lives == 3:
            game.blit(heart, (0, 110))
            game.blit(heart, (35, 110))
            game.blit(heart, (70, 110))

        elif lives == 2:
            game.blit(heart, (0, 110))
            game.blit(heart, (35, 110))

        else:
            game.blit(heart, (0, 110))

        if math.sqrt((x_carro - xpos) ** 2 + (
                y_carro - ypos) ** 2) < 50:  # checks for collison between mobile car and the red car
            winsound.PlaySound("collision.wav", winsound.SND_ASYNC)#play sound if car crashes
            crash(x_carro, y_carro)
            lives -= 1
            ypos = -200
            xpos = random.randrange(707, 1040)

        if math.sqrt((x_carro - x_truck) ** 2 + (y_carro - (y_truck + 439)) ** 2) < 10 or math.sqrt(
                (x_carro - x_truck) ** 2 + (y_carro - y_truck + 50) ** 2) < 50 or math.sqrt((x_carro - x_truck) ** 2 + (
                y_carro - (y_truck + 219)) ** 2) < 50:  # checks for collison between mobile car and the truck
            winsound.PlaySound("collision.wav", winsound.SND_ASYNC)  # play sound if car crashes
            x_truck = random.randrange(710, 1030)
            y_truck = -800
            lives -= 2
            crash(x_carro, y_carro)

        if math.sqrt((x_carro - x_tesla) ** 2 + (y_carro - y_tesla) ** 2) < 50:  # checks for collison between mobile car and the yellow car
            winsound.PlaySound("collision.wav", winsound.SND_ASYNC)  # play sound if car crashes
            crash(x_carro, y_carro)
            score += 500
            y_tesla = -1000
            x_tesla = random.randrange(700, 990)
            if gas + 40 > 90:
                gas = 100

            else:
                gas += 40

        if math.sqrt((x_carro - orangex) ** 2 + (
                y_carro - orangey) ** 2) < 50:  # checks for collison between mobile car and orange car
            winsound.PlaySound("collision.wav", winsound.SND_ASYNC)  # play sound if car crashes
            crash(x_carro, y_carro)
            lives -= 1
            orangex = random.randrange(703, 1040)
            orangey = -1300

        if math.sqrt(
                (xpos - x_truck) ** 2 + (ypos - y_truck) ** 2) < 50:  # checks for collison between red car and truck
            winsound.PlaySound("collision.wav", winsound.SND_ASYNC)  # play sound if car crashes
            crash(xpos, ypos)
            x_truck = random.randrange(710, 1030)
            y_truck = -800
            ypos = -200
            xpos = random.randrange(707, 1040)

        if math.sqrt(
                (xpos - x_tesla) ** 2 + (
                        ypos - y_tesla) ** 2) < 50:  # checks for collison between red car and yellow car
            winsound.PlaySound("collision.wav", winsound.SND_ASYNC)  # play sound if car crashes
            crash(xpos, ypos)
            ypos = -200
            xpos = random.randrange(707, 1040)
            y_tesla = -1000
            x_tesla = random.randrange(700, 990)

        if math.sqrt(
                (xpos - orangex) ** 2 + (ypos - orangey) ** 2) < 100:  # checks for collison between red and orange car
            winsound.PlaySound("collision.wav", winsound.SND_ASYNC)  # play sound if car crashes
            crash(xpos, ypos)
            ypos = -200
            xpos = random.randrange(707, 1040)
            orangex = random.randrange(703, 1040)
            orangey = -1300

        if math.sqrt((x_tesla - x_truck) ** 2 + (
                y_tesla - y_truck) ** 2) < 50:  # checks for collison between yellow car and truck
            winsound.PlaySound("collision.wav", winsound.SND_ASYNC)  # play sound if car crashes
            crash(x_tesla, y_tesla)
            y_tesla = -1000
            x_tesla = random.randrange(700, 990)
            x_truck = random.randrange(710, 1030)
            y_truck = -800

        if math.sqrt((x_tesla - orangex) ** 2 + (
                y_tesla - orangey) ** 2) < 50:  # checks for collison between yellor and orange car
            winsound.PlaySound("collision.wav", winsound.SND_ASYNC)  # play sound if car crashes
            crash(x_tesla, y_tesla)
            y_tesla = -1000
            x_tesla = random.randrange(700, 990)
            orangex = random.randrange(703, 1040)
            orangey = -1300

        if math.sqrt((x_truck - orangex) ** 2 + (
                y_truck - orangey) ** 2) < 50:  # checks for collison between truck and orange car
            winsound.PlaySound("collision.wav", winsound.SND_ASYNC)  # play sound if car crashes
            if y_truck < 300:
                crash(x_truck, 350)

            else:
                crash(x_truck, y_truck)
            orangex = random.randrange(703, 1040)
            orangey = -1300
            x_truck = random.randrange(710, 1030)
            y_truck = -800

        if orangey > 250:  # checks orange car's position to change its x direction
            if orangex > 872:
                orangex = 1030

            else:
                orangex = 730

        keys = pygame.key.get_pressed()

        # moves orange car
        if orangey < 700:
            orangey += orangevel
        else:
            FPS.tick(60)
            orangex = random.randrange(703, 1040)
            orangey = -1300

        # redcar
        if ypos < 700:
            ypos += velRed
        else:
            FPS.tick(60)
            ypos = -100
            xpos = random.randrange(707, 1040)

        # truck
        if y_truck < 1200:
            y_truck += velTRUCK
        else:
            FPS.tick(600)
            x_truck = random.randrange(710, 1030)
            y_truck = -800

        # Tesla
        if y_tesla < 800:
            y_tesla += velTESLA
        else:
            FPS.tick(120)
            y_tesla = -1000
            x_tesla = random.randrange(700, 990)

        # mobile car
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and x_carro > 715:# moves car in left direction
            x_carro -= vel

        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and x_carro < 1030:# moves car in right direction
            x_carro += vel

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and y_carro > 30:# moves car in north direction
            y_carro -= vel
            gas -= 0.5
            if velocity < 300:
                velocity += 10

            else:
                velocity = 300

        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and y_carro < 600:# moves car in south direction
            y_carro += vel
            if velocity > 100:
                velocity -= 10

            else:
                velocity = 100

        finish_time -= 0.5#substract 0.5 from the game´s time
        pygame.display.update()#update the screen

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def button(x, ys, wid, hei, image,fill, action = None, action2 = None):#function to create a button
    global seleccion, gas, score, finish_time, lives, active, ReWriteName, quantityWRITE
    mouse = pygame.mouse.get_pos()# gets mouse position
    click = pygame.mouse.get_pressed()#to know if the mouse was pressed

    if x + wid > mouse[0] > x and ys + hei > mouse[1] > ys:
        pygame.draw.rect(game, fill, [x, ys, wid, hei])#if the mouse if above the image and creates a rectangle
        if click[0] == 1 and action != None:
            active = False
            if action == "go1":# action == level1
                if action2 == "retry":#checks if level 1 is restarted
                    score = 0
                    gas = 100
                    finish_time = 300
                    lives = 3
                    seleccion = 1
                else:
                    seleccion = 1

            elif action == "go2":# action == level2
                quantityWRITE = 0
                if action2 == "retry":#checks if level2 is restarted
                    score = 0
                    gas = 100
                    finish_time = 300
                    lives = 3
                    seleccion = 2
                else:
                    seleccion = 2

            elif action == "go3":# action == level3
                quantityWRITE = 0
                if action2 == "retry":#checks if level3 is restarted
                    score = 0
                    gas = 100
                    finish_time = 300
                    lives = 3
                    seleccion = 3
                else:
                    seleccion = 3

            elif action == "menu":#checks if user wants to go back to the main menu
                ReWriteName = 0
                seleccion = 0
                score = 0

            elif action == "ins":#checks if user wants to go to the instructions´ screen
                seleccion = 4
                pygame.display.update()

            elif action == "pro":#checks if user wants to go to the credits´ screen
                seleccion = 5

            elif action == "top": #checks if user wants to go to the scores´ screen
                seleccion = 6

            elif acion == "exit":#checks if user wants to exit the program
                pygame.quit()
                sys.exit()
    game.blit(image, (x, ys))



def main_menu():# main menu screen
    global user, user_rect, color

    user_text = font3.render(user, 1, white)
    writeNAME = font3.render("PLEASE WRITE YOU NAME, SELECT THE BOX AND CLICK MOUSE TO WRITE", 1, white)

    user_rect.w = max(100, user_text.get_width() + 10)
    button(200, 700, 300, 41, top, redc, "top", "no")
    game.blit(bag, (0, 0))
    game.blit( hondaT,(200, 25))
    game.blit(civicT, (710, 35))
    game.blit(bomboT, (350, 145))
    game.blit(clatT, (600, 155))
    game.blit(honda_logo, (500, 25))
    game.blit(writeNAME, (10, 570))
    button(10, 400, 300, 70, level1,white, "go1", "no")
    button(400, 400, 300, 61, level2,white, "go2", "no")
    button(890, 400, 300, 59, level3, white, "go3", "no")
    button(50, 500, 400, 45, instructions, white, "ins", "no")
    button(880, 600, 300, 41, top, redc, "top", "no")
    button(700, 500, 300, 55, programmer, redc, "pro", "no")

    if active:
        color = white

    else:
        color = colornot


    game.blit(user_text, (user_rect.x + 5, user_rect.y + 5))
    pygame.draw.rect(game, color,user_rect, 2 )#https://www.youtube.com/watch?v=Rvcyf4HsWiw
    user_rect.w = user_text.get_width() + 10

def error_screen():#screen in case the game crashed
    game.fill(lightblue)
    errorTEXT = font2.render("LOOKS LIKE WE ARE HAVING SOME PROBLEMS CONNECTING TO THE GAME :/",1, black)
    error2TEXT = font2.render("TRY RESTARTING TE GAME",1, black)

    game.blit(errorTEXT,(100, 100))
    game.blit(error2TEXT, (100, 200))

run = True
while run:#main loop
    mouse = pygame.mouse.get_pos()#gets mouse´s position

    for event in pygame.event.get():
        if event.type == pygame.QUIT:#checks if user wants to exit the program
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:#checks if a button of the mouse was pressed
            if math.sqrt((mouse[0] - 15) ** 2 + (mouse[1] - 600) ** 2) < 100:#checks for collison between mouse and the rectangle in lower part of main menu
                active = True

        if event.type == pygame.KEYDOWN:#checks if keys of the keyboard are pressed
            if active == True:
                if event.key == pygame.K_BACKSPACE:#if user uses backspace, it would delete a character
                    user = user[:-1]

                elif event.key == pygame.K_RETURN:#if user press enter, it would stop writting
                    active = False

                else:
                    user += event.unicode# any other keys would be added while writting

    if seleccion == 0:#checks seleccion value
        main_menu()

    elif seleccion == 1:#checks seleccion value
        if lives > 0 and lives < 4 and finish_time != 0:
            if gas > 1:
                highway_game1(20, 15, 5, 15, 15, 12)
                if score_time % 5 == 0:
                    score += 0.5
                    gas -= 0.3
                pygame.display.update()

            else:
                lose_screen()


        elif finish_time == 0:
            win_screen()

        else:
            lose_screen()

    elif seleccion == 2:#checks seleccion value
        if lives > 0 and lives < 4 and finish_time != 0:
            if gas > 1:
                highway_game1(30, 20, 10, 20, 20, 15)
                if score_time % 5 == 0:
                    score += 0.5
                    gas -= 0.3
                pygame.display.update()

            else:
                lose_screen2()

        elif finish_time == 0:
            win_screen2()

        else:
            lose_screen2()

    elif seleccion == 3:#checks seleccion value
        if lives > 0 and lives < 4 and finish_time != 0:
            if gas > 1:
                highway_game1(40, 30, 20, 30, 30, 20)
                if score_time % 5 == 0:
                    score += 0.5
                    gas -= 0.3
                pygame.display.update()

            else:
                lose_screem3()

        elif finish_time == 0:
            win_screen3()

        else:
            lose_screem3()

    elif seleccion == 4:#checks seleccion value
        intructions()

    elif seleccion == 5:#checks seleccion value
        programmer_screen()

    elif seleccion == 6:
        ScoreScreen()

    elif seleccion > 6:#checks seleccion value
        error_screen()
    pygame.display.update()