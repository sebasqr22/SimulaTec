import pygame
import sys
import time
import random
from tkinter import messagebox
import os

pygame.init()

#Global variables

mousePos = pygame.mouse.get_pos()

s_width = 1200
s_height = 700
screen = pygame.display.set_mode((s_width,s_height))
click = pygame.mouse.get_pressed()
ScreenNum = 0

img_dir = os.path.join(os.path.dirname(__file__),'imgs')

def cargar_img(nombre):
    #cargar_img: utiliza os para poder importar imagenes de algun folder pygame
    #e: nombre de la imagen
    #s: imagen formato pygame
    #R: ---
    ruta = os.path.join(img_dir,nombre)
    imagen = pygame.image.load(ruta)
    return imagen



#Images
background = cargar_img("wallpaper.jpg")

#SpriteGroups

all_sprites = pygame.sprite.Group()
#Colors
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
oliveGreen = (161, 169, 106)




def Menu(): #Menu screen
    screen.fill(black)

    ##screen.blit(background, (0,0))

    TextButton("DESIGN", 50, 200, 120, 40, black, white, 30, 250, "design", True)

    TextButton("IMPORT", 750, 200, 120, 40, black, white, 30, 250, "import", True)


def DesignMode(): # Screen where someone can design a model
    screen.fill(gray)

    Text(123, 123, 40, "Esta es pantalla de diseno", white)

    TextButton("MENU", 120, 200, 120, 40, black, white, 30, 20, "menu", True)

    
# Objects 
def Button(x, ys, wid, hei, image,fill, action = None):#function to create a button
    global seleccion, gas, score, finish_time, lives, active, ReWriteName, quantityWRITE
    mouse = pygame.mouse.get_pos()# gets mouse position
    click = pygame.mouse.get_pressed()#to know if the mouse was pressed

    if x + wid > mousePos[0] > x and ys + hei > mousePos[1] > ys:
        print("fuck me")
        pygame.draw.rect(game, fill, [x, ys, wid, hei])#if the mouse if above the image and creates a rectangle
        if click[0] == 1 and action != None:
            active = False

        if action == "simulador":
            pass
                 
    screenblit(image, (x, ys))

def TextButton(text, xpos, ypos, width, height, ActiveColor, InactiveColor,text_size, extraSize, action = None, OptionalRect = None):
    global ScreenNum
    color = ActiveColor
    mouse = pygame.mouse.get_pos()# gets mouse position
    click = pygame.mouse.get_pressed()#to know if the mouse was pressed

    width += extraSize

    if OptionalRect:
        pygame.draw.rect(screen, oliveGreen, [xpos, ypos, width, height])

    color = InactiveColor
    if xpos + width > mouse[0] > xpos and ypos + height > mouse[1] > ypos:
        #pygame.draw.rect(game, fill, [xpos - 5, ypos - 5, width + 10,height + 10])  # if the mouse if above the image and creates a rectangle
        #PrintScreen(text, xpos + 60, ypos + 60, text_size, ActiveColor)
        color = ActiveColor
        if click[0] == 1:
            if action == "design":
                ScreenNum = 1

            elif action == "menu":
                ScreenNum = 0

            elif action == "import"
   
    PrintText( xpos, ypos, text_size, text, color, width, height)
        

def PrintText(x, y, size, text, color, width = None, height = None):
    font = pygame.font.SysFont("powergreen", size)
    text = font.render(text, True, color)
    screen.blit(text, (x +(width//2 - text.get_width()//2), y + (height//2 - text.get_height()//2)))

def Text(x, y, size, text, color):
    font = pygame.font.SysFont("powergreen", size)
    text = font.render(text, True, color)
    screen.blit(text, (x,y))

                   
while True:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  

    if ScreenNum == 0:
        Menu()

    elif ScreenNum == 1:
        DesignMode()
    
    pygame.display.update()