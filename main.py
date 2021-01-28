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
tkActive = False

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

pow_image = pygame.transform.scale(cargar_img("fuente_poder.png"),(200,110))
pow_image2 = pygame.transform.rotate(pygame.transform.scale(cargar_img("fuente_poder.png"),(200,110)),90) 
pow_imageB =pygame.transform.scale(cargar_img("fuente_poder.png"),(100,60))
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
    #TextButton("CREATE FILE", 400, 100, 120, 40, black, white, 30, 250, "new", True)
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
        self.id = 1
        self.image = pow_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.w = abs(self.rect.topright[0]-self.rect.topleft[0])
        self.h = abs(self.rect.topright[1]-self.rect.bottomright[1])

        self.id = "V"+str(len(power_S))
        self.Voltaje = 5

    def over(self, pos):
        if pos[0] > self.x - self.w//2 and pos[0] < self.x + self.w//2:
            if pos[1] > self.y- self.h//2 and pos[1] < self.y + self.h//2:
                return True
        return False  

    def rotate(self):
        print("Rotate")
        if self.image == pow_image:
            print("image1")
            self.image = pow_image2
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.w = abs(self.rect.topright[0]-self.rect.topleft[0])
            self.h = abs(self.rect.topright[1]-self.rect.bottomright[1])
            options.active = False
            time.sleep(0.3)

        else:
            print("image1")
            self.image = pow_image
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.w = abs(self.rect.topright[0]-self.rect.topleft[0])
            self.h = abs(self.rect.topright[1]-self.rect.bottomright[1])
            options.active = False
            time.sleep(0.3)

    def show_data(self):
        PrintText(self.x,self.y-30,20,self.id +":"+ str(self.Voltaje),blue,self.w,self.h)


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
        
        if pos[0] > self.x - self.w//2 and pos[0] < self.x + self.w//2:
            if pos[1] > self.y- self.h//2 and pos[1] < self.y + self.h//2:
                return True
        return False  

    def rotate(self):
        if self.image == res_image1:
            self.image = res_image2
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.w = abs(self.rect.topright[0]-self.rect.topleft[0])
            self.h = abs(self.rect.topright[1]-self.rect.bottomright[1])
            options.active = False
            time.sleep(0.3)

        else:
            self.image = res_image1
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.w = abs(self.rect.topright[0]-self.rect.topleft[0])
            self.h = abs(self.rect.topright[1]-self.rect.bottomright[1])
            options.active = False
            time.sleep(0.3)

        
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

    def show_data(self):
        PrintText(self.x,self.y-30,20,self.id +":"+ str(self.res),blue,self.w,self.h)

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

    def draw(self,screen,outline,image):

        if outline:
            pygame.draw.rect(screen,self.border,(self.x-2,self.y-2,self.w+4,self.h+4),0)
        
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.w,self.h),0)

        if image:
            screen.blit(self.image,(self.x +(self.w//2 - self.rectw//2), self.y + (self.h//2 - self.recth//2)))

    def line_B(self):
        pygame.draw.line(screen,black,(self.x+20, self.y+self.h//2), (self.x + self.w-20 , self.y+self.h//2),5)
        
            
    def over(self,pos):
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True
        return False

    def highlight(self,image):
        self.color = self.colorh
        

    def unhighlight(self,image):
        self.color = self.colorR
        
    def check(self,pos):
        if self.over(pos):
            self.highlight(True)
        else:
            self.unhighlight(True)

class ElementOptions():

    def __init__(self):
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        """
        self.buttons = [Element_Button(gray,600,530,110,40,black,res_image1),
                        Element_Button(gray,600,580,110,40,red,res_image1), 
                        Element_Button(gray,600,630,110,40,white,res_image1)]

        self.text = ["Rotate", "Rename", "Delete"]
        self.item = None
        self.active = False

    def draw(self,screen):

        i = 0
        for button in self.buttons:
            button.draw(screen,False,False)
            if button.color == button.colorh:
                PrintText(button.x,button.y,15,self.text[i],white,button.w,button.h)
            else:
                PrintText(button.x,button.y,15,self.text[i],black,button.w,button.h)
            i += 1

    def overclick(self,pos):
        
        for button in self.buttons:
            if button.over(pos):
                if button.border == black:
                    self.item.rotate()
                elif button.border == red:
                    pass
                elif button.border == white:
                    self.item.kill()
                    self.active = False
            else:
                self.active = False

    def over(self,pos):
        for button in self.buttons:
            if button.over(pos):
                button.highlight(False)
                self.draw(screen)
            else:
                button.unhighlight(False)
                self.draw(screen)


class Cable_line():

    def __init__(self,pos1,pos2):
        self.pos1 = pos1
        self.pos2 = pos2
    
    def draw(self):
        pygame.draw.line(screen,black, self.pos1 , self.pos2,5)

    def over(self,pos):

        if pos[0] > self.pos1[0] and pos[0] < self.pos2[0]:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True
        return False

#Cable list
class Cable_list():
    def __init__(self):
        self.list = []

    def get_list(self):
        return self.list

    def add_line(self,line):
        self.list.append(line)

def drawlines():

    position = 100
    for i in range(1,8):
        pygame.draw.line(screen,black,(0,position) , (s_width-220 ,position),1)
        
        position += 70

    position = 70
    for i in range(1,15):
        pygame.draw.line(screen,black,(position,100) , (position,s_height-110),1)
        position += 70

    pygame.draw.line(screen,black,(0,590), (s_width-220,590),1)
    pygame.draw.rect(screen,darkGray,(s_width-200,0,200,s_height),0)
    pygame.draw.rect(screen,darkGray,(0,s_height-105,s_width,105),0)
    
    for line in C_list.get_list():
        line.draw()
    

#element buttons
resi_B = Element_Button(gray,50,s_height-90,110,60,black,res_image1)
power_B = Element_Button(gray,230,s_height-90,110,60,black,pow_imageB)  
options = ElementOptions()
cable_B = Element_Button(gray,410,s_height-90,110,60,black,pow_imageB)  


C_list = Cable_list()
#Posible locations
Xposible = [70, 140, 210, 280, 350, 420, 490, 560, 630, 700, 770, 840, 910]
Yposible = [170, 240, 310, 380, 450, 520]

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
            resi_B.highlight(True)
            selecting = True
            typeE = 1
            drag_element = res_image1
            
            
        elif power_B.over(pos):
            power_B.highlight(True)
            selecting = True
            typeE = 2
            drag_element = pow_image
            
        elif cable_B.over(pos):
            cable_B.highlight(True)
            selecting = True
            typeE = 3
            
        active1 = False
        active2 = False
        pos1 = (0,0)
        pos2 = (0,0)

        while selecting:
            screen.fill(white)
            TextButton("MENU", 20, 20, 120, 40, black, white, 30, 20, "menu", True)

            drawlines()

            pos = pygame.mouse.get_pos()

            if drag_element != None:
                screen. blit(drag_element,(pos[0] - (drag_element.get_width()//2) ,pos[1] - (drag_element.get_height()//2)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pos[1] < s_height-100:
                        if typeE == 1:
                            poscal = calculateLocation(pos)
                            tmp = Resistance(len(resistance_S),poscal[0],poscal[1])
                            resistance_S.add(tmp)
                            all_sprites.add(tmp)
                            selecting = False
                            resi_B.unhighlight(True)
                            time.sleep(0.3)

                        elif typeE == 2:
                            poscal = calculateLocation(pos)
                            tmp = Power_Output(poscal[0],poscal[1])
                            power_S.add(tmp)
                            all_sprites.add(tmp)
                            selecting = False
                            power_B.unhighlight(True)

                        elif typeE == 3:
                            if active2:
                            #surface, color, x & y start, x & y end, width
                                if (abs(pos2[0]-pos[0]) > abs(pos2[1]-pos[1])):
                                    pos = (pos[0],pos2[1])
                                else:
                                    pos = (pos2[0],pos[1])
                                print(pos)
                                tmp1 = pygame.draw.line(screen,black,pos1 , pos2,4)
                                tmp2 = pygame.draw.line(screen,black,pos2 , pos,4)
                                C_list.add_line(Cable_line(pos1,pos2)) 
                                C_list.add_line(Cable_line(pos2,pos))
                                active2 = False
                                cable_B.unhighlight(False)
                                selecting = False

                            elif active1:
                                active1 = False
                                active2 = True
                                pos2 = pos

                                if (abs(pos1[0]-pos2[0]) > abs(pos1[1]-pos2[1])):
                                    pos2 = (pos2[0],pos1[1])
                                else:
                                    pos2 = (pos1[0],pos2[1])

                                print(pos2)
                            else:
                                active1 = True
                                pos1 = pos
                                print(pos1)
                                

                    elif resi_B.over(pos):
                        selecting = False
                        resi_B.unhighlight(True)
                        time.sleep(0.3)  
                        break
                        
                    elif power_B.over(pos):
                        selecting = False
                        power_B.unhighlight(True)
                        time.sleep(0.3)
                        break

                    elif cable_B.over(pos):
                        selecting = False
                        cable_B.unhighlight(False)
                        time.sleep(0.3)
                        break
                        
            resi_B.draw(screen,False,True)
            power_B.draw(screen,False, True)
            cable_B.draw(screen,False,False)
            cable_B.line_B()
            all_sprites.draw(screen)
            pygame.display.update()

###########################################################################################################################      
    
    #background
    screen.fill(white)
    
    drawlines()
    
    #variables
    mouse = pygame.mouse.get_pos()# gets mouse position
    click = pygame.mouse.get_pressed()#to know if the mouse was pressed
    
    TextButton("MENU", 20, 20, 120, 40, black, white, 30, 20, "menu", True)

    resi_B.draw(screen,False,True)
    power_B.draw(screen,False,True)
    cable_B.draw(screen,False,False)
    cable_B.line_B()

    if options.active:
        options.draw(screen)
        options.over(mouse)
        options.item.show_data()

    resi_B.check(mouse)
    power_B.check(mouse)
    cable_B.check(mouse)


    if click[0]:
        if options.active:
            options.overclick(mouse)

        for resistance in resistance_S:
            if resistance.over(mouse):
               options.active = True
               options.item = resistance
        
        for power in power_S:
            if power.over(mouse):
                options.active = True
                options.item = power

        #for cable in C_list.get_list():
            #if cable.over(mouse):
                #options.active = True
        
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
def Simulationmode():
    pass

def TkinterSaved():
    global tkActive, box
    
    box.config(width=100, height=100)
    box.title("Save Project")
    box.resizable(False, False)

    tkActive = True

    nameEntry = Entry(box, width = 25, bg = "#00000")
    nameEntry.place(x=10, y=80)

    info = Entry(box, width = 25, bg = "#00000")
    info.place(x=60, y=80)

    create = Button(box, text = "Ok", bg = "#21201E", command = lambda: WriteNewSaved(nameEntry.get(), info.get()))
    create.place(x = 10, y= 20)

    box.mainloop()
   
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
                
                Tk().wm_withdraw()
                if messagebox.askyesno("SAVED PROJECTS", "Do you want to Exit without saving "  + "?"):
                    all_sprites.empty()
                    resistance_S.empty()
                    power_S.empty()
                    ScreenNum = 0
                

            elif action == "import":
                Tk().wm_withdraw()
                if messagebox.askyesno("SAVED PROJECTS", "Do you want to load " + toLoad.split(".")[0] + "?"):
                    project = ReadProject(toLoad)
                    print(project)

            elif action == "new":
                TkinterSaved()
                
        
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
    global tkActive
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


