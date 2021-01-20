import pygame
import pygame.freetype
import sys
import time
import random
from tkinter import *
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

saved = []

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
res_image = cargar_img("resistencia.png")
#SpriteGroups

all_sprites = pygame.sprite.Group()
resistance_S = pygame.sprite.Group()
power_S = pygame.sprite.Group()
cable_S = pygame.sprite.Group()


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


#SCREENS

def Menu(): #Menu screen
    global saved
    screen.fill(black)

    Text(300, 10, 40, "What kind of circuit do you want to open?", white)

    TextButton("CREATE NEW", 400, 60, 120, 40, black, white, 30, 250, "design", True)
    projects =  ReadProject("savedProjects.txt")
    saved = SeparateContent(projects)
    xpos = 50
    ypos = 250
    length = len(saved)
    counter = 0
    quantityCounter = 0

    Text(50, 260, 30, "IMPORTS:", white)
    if saved != []:
        while counter < length:
            if counter == (length-1):
                break
            
            if quantityCounter == 8:
                ypos = 250
                xpos += 50
                quantityCounter = 0
            ypos += 50

            TextButton(saved[counter].split(".")[0], xpos, ypos, 120, 40, black, white, 30, 20, "import", True, saved[counter])

            counter += 1
            quantityCounter += 1

    #TextButton("IMPORT", 750, 200, 120, 40, black, white, 30, 250, "import", True)

class Element(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.w = self.image.get_height()
        self.h = self.image.get_width()
        

    
    def over(self, pos):
            if pos[0] > self.x and pos[0] < self.x + self.w:
                if pos[1] > self.y and pos[1] < self.y + self.h:
                    return True
            return False   


    
class Resistance(Element):

    def ___init__(self, idr, x , y):
        Element.__init__(self, res_image, x, y)
        self.res = 100
        self.id = "R" + str(idr)
        self.connectedto = None
        

    def get_Res(self):
        return self.res
    
    def set_Res(self, res):
        self.res = res
    
    def get_Id(self):
        return self.id
    
    def set_Id(self, idr):
        self.id = id
    
    def get_Connectedto(self):
        return self.connectedto
    
    def set_Connectedto(self, node):
        self.connectedto = node



def DesignMode(): # Screen where someone can design a model
    screen.fill(gray)
    
    Text(123, 123, 40, "Esta es pantalla de diseno", white)

    TextButton("MENU", 120, 200, 120, 40, black, white, 30, 20, "menu", True)

    
    
    all_sprites.draw(screen)
   
# Objects 
def Button(x, ys, wid, hei, image,fill, action = None):#function to create a button
    global seleccion, gas, score, finish_time, lives, active, ReWriteName, quantityWRITE
    mouse = pygame.mouse.get_pos()# gets mouse position
    click = pygame.mouse.get_pressed()#to know if the mouse was pressed

    if x + wid > mousePos[0] > x and ys + hei > mousePos[1] > ys:
        pygame.draw.rect(game, fill, [x, ys, wid, hei])#if the mouse if above the image and creates a rectangle
        if click[0] == 1 and action != None:
            active = False

        if action == "simulador":
            pass
                 
    screenblit(image, (x, ys))

def TextButton(text, xpos, ypos, width, height, ActiveColor, InactiveColor,text_size, extraSize, action = None, OptionalRect = None, toLoad = None):
    global ScreenNum, saved
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

            elif action == "import":
                Tk().wm_withdraw()
                if messagebox.askyesno("SAVED PROJECTS", "Do you want to load " + toLoad.split(".")[0] + "?"):
                    project = ReadProject(toLoad)
                    print(project)
        
        elif click[2] == 1:
            if action == "import":
                Tk().wm_withdraw()
                if messagebox.askyesno("SAVED PROJECTS", "Do you want to detele " + toLoad.split(".")[0] + "?"):
                    DeleteFile(toLoad)
   
    PrintText( xpos, ypos, text_size, text, color, width, height)
        

def PrintText(x, y, size, text, color, width = None, height = None):
    font = pygame.font.SysFont("Teko", size)
    text = font.render(text, True, color)
    screen.blit(text, (x +(width//2 - text.get_width()//2), y + (height//2 - text.get_height()//2)))

def Text(x, y, size, text, color):
    font = pygame.font.SysFont("Teko", size)
    text = font.render(text, True, color)
    screen.blit(text, (x,y))

def WriteNewSaved(name, data): #writes info to then load a project
    route = "./savedProjects/savedProjects.txt"
    registry = open(route, "a")
    registry.write(name + "{")
    registry.close()
    WriteProject(data, name)

def WriteProject(data, name):
    route = "./savedProjects/" + name
    registry = open(route, "w")
    registry.write(data)
    registry.close()

def ReadProject(project):
    route = "./savedProjects/" + project
    read = open(route)
    content = read.readlines()
    read.close()
    return content

def SeparateContent(data):
    data = data[0].split("{")
    return data

def DeleteFile(name):
    route = "./savedProjects"
    files = os.listdir(route)

    if name in files:
        os.remove(route + "/" + name)

    files = os.listdir(route)
    print("Los files son: ")
    print(files)
    
    route = "./savedProjects/savedProjects.txt"
    newlist = []

    for save in files:
        print(save)
        if save != name and save != 'savedProjects.txt':
            newlist += [save]

    with open(route,"w") as file:
        temp = ""

        for elem in newlist:
            temp += elem + "{"
        print(temp)
        file.write(temp)

######## MAIN LOOP ############                
while True:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  

    if ScreenNum == 0:
        Menu()

    elif ScreenNum == 1:
        DesignMode()

    elif ScreenNum == 2:
        ImportScreen()
    
    pygame.display.update()