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
res_image1 = pygame.transform.scale(cargar_img("resistencia.png"),(100,30))
res_image2 = pygame.transform.rotate(pygame.transform.scale(cargar_img("resistencia.png"),(100,30)),90)  

pow_image = pygame.transform.scale(cargar_img("fuente_poder.png"),(100,90))
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

class Power_Output(pygame.sprite.Sprite):

    def __init__(self,  x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pow_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.w = abs(self.rect.topright[0]-self.rect.topleft[0])
        self.h = abs(self.rect.topright[1]-self.rect.bottomright[1])

    def over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True
        return False  



class Resistance(pygame.sprite.Sprite):
    
    def __init__(self, idr, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = res_image1
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.w = abs(self.rect.topright[0]-self.rect.topleft[0])
        self.h = abs(self.rect.topright[1]-self.rect.bottomright[1])
        
        self.res = 100
        self.id = "R" + str(idr)
        self.connectedto = None
        
    def over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True
        return False  

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


class Element_Button():

    def __init__(self,color,x,y,w,h,border, image):
        self.color = color
        self.colorh = darkBlue
        self.colorR = color
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topright = (x,y)
        self.x = x
        self.rectw = abs(self.rect.topright[0]-self.rect.topleft[0])
        self.recth = abs(self.rect.topright[1]-self.rect.bottomright[1]) 
        self.y = y
        self.w = w
        self.h = h
        self.border = border

    def draw(self,screen,outline):

        if outline:
            pygame.draw.rect(screen,self.border,(self.x-2,self.y-2,self.w+4,self.h+4),0)

        pygame.draw.rect(screen,self.color,(self.x,self.y,self.w,self.h),0)
        screen.blit(self.image,(self.x +(self.w//2 - self.rectw//2), self.y + (self.h//2 - self.recth//2)))

        
            
    def over(self,pos):
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True
        return False

    def highlight(self):
        self.color = self.colorh
        self.draw(screen,False)

    def unhighlight(self):
        self.color = self.colorR
        self.draw(screen,False)

#element buttons
resi_B = Element_Button(gray,100,s_height-70,110,60,black,res_image1)
power_B = Element_Button(gray,300,s_height-100,110,60,black,pow_image)  
Xposible = [70, 140, 210, 280, 350, 420, 490, 560, 630, 700, 770, 840, 910, 980, 1050]
Yposible = [100, 170, 240, 310, 380, 450, 520, 590]

def calculateLocation(pos):
    posx = pos[0]
    posy = pos[1]
    minx = []
    miny = []
    finalx = 0
    finaly = 0

    for distancex in Xposible:
        minx.append(abs(pos[0]-distancex))

    finalx = Xposible[minx.index(min(minx))]

    for distancey in Yposible:
        miny.append(abs(pos[1]-distancey))

    finaly = Yposible[miny.index(min(miny))]

    return (finalx,finaly)

def DesignMode(): # Screen where someone can design a model

    def select_element(pos):
        selecting = False
        typeE = 0

        drag_element = None
        if resi_B.over(pos):
            print("Click in resistance")
            resi_B.highlight()
            selecting = True
            typeE = 1
            drag_element = res_image1
            
            
        elif power_B.over(pos):
            power_B.highlight()
            selecting = True
            typeE = 2
            drag_element = pow_image
            
        
        while selecting:
            screen.fill(white)

            position = 100
            for i in range(1,8):
                pygame.draw.line(screen,black,(0,position) , (s_width ,position),1)
                
                position += 70
            position = 70
            for i in range(1,15):
                pygame.draw.line(screen,black,(position,100) , (position,s_height),1)
                position += 70

            pos = pygame.mouse.get_pos()
            screen. blit(drag_element,(pos[0] - (drag_element.get_width()//2) ,pos[1] - (drag_element.get_height()//2)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pos[1] < s_height-100:
                        if typeE == 0:
                            pass
                        if typeE == 1:
                            poscal = calculateLocation(pos)
                            tmp = Resistance(len(resistance_S),poscal[0],poscal[1])
                            resistance_S.add(tmp)
                            all_sprites.add(tmp)
                            selecting = False
                            resi_B.unhighlight()

                        elif typeE == 2:
                            poscal = calculateLocation(pos)
                            tmp = Power_Output(poscal[0],poscal[1])
                            power_S.add(tmp)
                            all_sprites.add(tmp)
                            selecting = False
                            power_B.unhighlight()

                    elif resi_B.over(pos):
                        selecting = False
                        resi_B.unhighlight()
                        time.sleep(0.3)  
                        break
                        
                    elif power_B.over(pos):
                        selecting = False
                        power_B.unhighlight()
                        time.sleep(0.3)
                        break
            
            resi_B.draw(screen,False)
            power_B.draw(screen,False)
            all_sprites.draw(screen)
            pygame.display.update()
       
    #background
    screen.fill(white)
    #pygame.draw.rect(screen,darkGray,(s_width-200,0,200,s_height),0)
    #pygame.draw.rect(screen,darkGray,(0,s_height-100,s_width,100),0)

    
    position = 100
    for i in range(1,8):
        pygame.draw.line(screen,black,(0,position) , (s_width ,position),1)
        
        position += 70
    position = 70
    for i in range(1,15):
        pygame.draw.line(screen,black,(position,100) , (position,s_height),1)
        position += 70
    
    #variables
    mouse = pygame.mouse.get_pos()# gets mouse position
    click = pygame.mouse.get_pressed()#to know if the mouse was pressed
    
    

    Text(123, 123, 40, "Esta es pantalla de diseno", white)

    TextButton("MENU", 20, 20, 120, 40, black, white, 30, 20, "menu", True)

    resi_B.draw(screen,False)
    power_B.draw(screen,False)

    
 
    if click[0]:
        select_element(mouse)  
    #Draw all sprites
    all_sprites.draw(screen)


"""
with open(file, 'w') as savefile:
    tmp = ""
    for res in resistance_S:
        tmp = str(res.name)+'{'+str(res.id)+str(res.rect.centerx)+'{'+str(res.rect.centery)+"{"+str(res.rotation)
        savefile.writelines(tmp+"\n")
    
    for pow in power_S:
        tmp = str(res.name)+'{'+str(res.id)+str(res.rect.centerx)+'{'+str(res.rect.centery)+"{"+str(res.rotation)
        savefile.writelines(tmp+"\n")
"""



# Objects 
def Button(x, ys, wid, hei, image,fill, action = None):#function to create a button
    global seleccion, gas, score, finish_time, lives, active, ReWriteName, quantityWRITE
    mouse = pygame.mouse.get_pos()# gets mouse position
    click = pygame.mouse.get_pressed()#to know if the mouse was pressed

    if x + wid > mouse[0] > x and ys + hei > mouse[1] > ys:
        pygame.draw.rect(game, fill, [x, ys, wid, hei])#if the mouse if above the image and creates a rectangle
        if click[0] == 1 and action != None:
            active = False

        if action == "simulador":
            pass
    
    screen.blit(image, (x, ys))

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
    #print(random.randint(1,100))   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  

    if ScreenNum == 0:
        Menu()

    elif ScreenNum == 1:
        
        DesignMode()

    elif ScreenNum == 2:
        #ImportScreen()
        pass
    
    pygame.display.update()