import pygame
import pygame.freetype
import sys
import time
import random
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import os

#Init pygame engine
pygame.init()

#Global variables
s_width = 1200
s_height = 700
screen = pygame.display.set_mode((s_width,s_height))
click = pygame.mouse.get_pressed()
ScreenNum = 0
tkActive = False
justSaved = False
counterSave = 0
namePro = ""
arrayToPrint = []
FPS = pygame.time.Clock()
saved = []


#Image route
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

#Imagenes de resistencias
res_image1 = pygame.transform.scale(cargar_img("resistencia.png"),(100,30))
res_image2 = pygame.transform.rotate(pygame.transform.scale(cargar_img("resistencia.png"),(100,30)),90)  


#Imagenes de fuente de poder
pow_image = pygame.transform.scale(cargar_img("fuente_poder.png"),(200,110))
pow_image2 = pygame.transform.rotate(pygame.transform.scale(cargar_img("fuente_poder.png"),(200,110)),90) 
pow_imageB = pygame.transform.scale(cargar_img("fuente_poder.png"),(100,60))

#imagen del nodo
node_image = pygame.transform.scale(cargar_img("node.png"),(45,45))

#Imagen de botones
arrow_up = cargar_img("flechaArriba.png")
arrow_upRed = cargar_img("flechaArribaRed.png")
arrow_down = cargar_img("flechaAbajo.png")
arrow_downRed = cargar_img("flechaAbajoRed.png")
logo = cargar_img("simulatec.png")
check = cargar_img("check.png")
xRed = cargar_img("xRed.png")

#SpriteGroups
all_sprites = pygame.sprite.Group()
resistance_S = pygame.sprite.Group()
power_S = pygame.sprite.Group()
node_S = pygame.sprite.Group()


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
greenPichudo = (54, 115, 84)


#SCREENS

def Menu(): #Menu screen
    #El la funcion que se encarga de dibujar y la logica del menu
    global saved
    screen.fill((129, 138, 125))

    #boton para crear nuevo file
    TextButton("CREATE NEW", 65, 150, 120, 40, black, white, 30, 950, "design", True, None, ((58,76,83)))
    
    #
    projects =  ReadProject("savedProjects.txt")
    saved = SeparateContent(projects)
    xpos = 50
    ypos = 250
    length = len(saved)
    counter = 0
    quantityCounter = 0

    screen.blit(logo, (375, 10))

    Text(50, 260, 30, "IMPORTS:", white)

    #genera los butones de los files para poder cargar 
    if saved != []:
        while counter < length:
            if counter == (length-1):
                break
            
            if quantityCounter == 8:
                ypos = 250
                xpos += 50
                quantityCounter = 0
            ypos += 50

            #boton del file
            TextButton(saved[counter].split(".")[0], xpos, ypos, 120, 40, black, white, 30, 50, "import", True, saved[counter], (58,76,83))

            counter += 1
            quantityCounter += 1
    else:
        Text(50, 290, 30, "No saved projects :/", white)

    

class Graph: #Class to create the graph
    def __init__(self):#constructor
        self.v = {}
        self.size = 0
        self.i = 1

    def __iter__(self):
        return iter(self.v.values())

    def add_Vertex(self, name):#method to add a vertex
        self.v[name] = {}
        self.size += 1
    
    def add_Edge(self, frm, to, res):#method to add a edge
        if to in self.v[frm]:#Determinar si el nodo ya existe en el grafo
            #to = str(to) + str(self.i)
            #self.i += 1
            if self.v[frm][to] >= res.get_Res():
                resFinal = res.get_Res()
                self.v[frm].update({to: resFinal})

        else:
            self.v[frm].update({to: res.get_Res()})

            
            #self.add_Vertex(to)
        
    
    def empty(self):#method to clear all the graph
        self.v.clear()



class Node(pygame.sprite.Sprite):#Class to create nodes with pygame sprites

    def __init__(self,x,y, idn):# main constructor
        pygame.sprite.Sprite.__init__(self)#super constructor
        self.id = idn 
        self.x = x 
        self.y = y
        self.image = node_image
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.w = abs(self.rect.topright[0]-self.rect.topleft[0])
        self.h = abs(self.rect.topright[1]-self.rect.bottomright[1])
        self.type = "node"
        self.rotation = None
        self.Volataje = random.randint(0,10)#generacion de los valores random
        self.C = random.randint(0,1000)

    def over(self, pos):#method to check if mouse is over
        if pos[0] > self.x - self.w//2 and pos[0] < self.x + self.w//2:
            if pos[1] > self.y- self.h//2 and pos[1] < self.y + self.h//2:
                return True
        return False     

    def check(self,pos):##method to check if a rectangle has to change its color
        if self.over(pos):
            self.highlight(True)
        else:
            self.unhighlight(True)

    def show_data(self):#method to print data from node
        PrintText(self.x+10,self.y-50,40,self.id ,blue,self.w,self.h)

    def show_sim(self):#method to show information in simulation mode
        PrintText(self.x+30,self.y-50,40,self.id ,blue,self.w,self.h)
        PrintText(self.x+30,self.y-20,40,str(self.Volataje)+" V" ,blue,self.w,self.h)
        PrintText(self.x+30,self.y +10,40,str(self.C)+" mA" ,blue,self.w,self.h)

class NodeNamer():#Class to create name to a node

    def __init__(self):#main constructor

        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 
                        'g', 'h', 'i', 'j', 'k', 'l', 
                        'm', 'n', 'o', 'p', 'q', 'r', 
                        's', 't', 'u', 'v', 'w', 'x', 
                        'y', 'z']
        self.i = 0

    def get_name(self):##method to get name 
        if len(node_S) == 0:
            self.i = 0

        for node in node_S:
            if node.id == self.letters[self.i]:
                self.i += 1
                

        tmp = self.letters[self.i]
        self.i += 1
        return tmp



class Power_Output(pygame.sprite.Sprite):#Class that create power outputs

    def __init__(self,  x, y):#Constructor
        pygame.sprite.Sprite.__init__(self)#super constructor
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
        self.type = "power"

    def over(self, pos):#Method that determines if the mouse over the object
        if pos[0] > self.x - self.w//2 and pos[0] < self.x + self.w//2:
            if pos[1] > self.y- self.h//2 and pos[1] < self.y + self.h//2:
                return True
        return False  

    def rotate(self):#Method that rotates the object
        print("Rotate")
        if self.image == pow_image:#Check what image the object has
            #Redefinir los valores de la imagen
            self.image = pow_image2
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.w = abs(self.rect.topright[0]-self.rect.topleft[0])
            self.h = abs(self.rect.topright[1]-self.rect.bottomright[1])
            options.active = False
            time.sleep(0.3)
            justSaved = False

        else:
            #Redefinir los valores de la imagen
            self.image = pow_image
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.w = abs(self.rect.topright[0]-self.rect.topleft[0])
            self.h = abs(self.rect.topright[1]-self.rect.bottomright[1])
            options.active = False
            time.sleep(0.3)
            justSaved = False

    def show_data(self):#Method that shows the data of the object
    
        if self.image == pow_image2:#detemrines where to place it depending on the rotation
            PrintText(self.rect.topleft[0],self.rect.topleft[1]-50,30,self.id +" : "+ str(self.Voltaje) + " V",blue,self.w,self.h)
        else:
            PrintText(self.rect.center[0]-20,self.y-70,30,self.id +" : "+ str(self.Voltaje) + " V",blue,self.w,self.h)

    def get_rotation(self):#Method that return a boolean value of rotation
        if self.image == pow_image:
            return 0
        else:
            return 1

    def get_Voltaje(self):#Method that return the voltaje of the object
        return self.Voltaje
             
class Resistance(pygame.sprite.Sprite): #Class to create a resistance with pygame sprites
    
    def __init__(self, idr, x, y):#main constructor
        pygame.sprite.Sprite.__init__(self)#Super constructor
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
        self.type = "res"
        
    def over(self, pos):#method to check if mouse is over
        
        if pos[0] > self.x - self.w//2 and pos[0] < self.x + self.w//2:
            if pos[1] > self.y- self.h//2 and pos[1] < self.y + self.h//2:
                return True
        return False  

    def rotate(self):#method to rotate a resistance
        if self.image == res_image1:
            self.image = res_image2
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.w = abs(self.rect.topright[0]-self.rect.topleft[0])
            self.h = abs(self.rect.topright[1]-self.rect.bottomright[1])
            options.active = False
            time.sleep(0.3)
            justSaved = False

        else:
            self.image = res_image1
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.w = abs(self.rect.topright[0]-self.rect.topleft[0])
            self.h = abs(self.rect.topright[1]-self.rect.bottomright[1])
            options.active = False
            time.sleep(0.3)
            justSaved = False

    def get_rotation(self): #method to get rotation of the resistance
        if self.image == res_image1:
            return 0
        else:
            return 1
            
    def get_Res(self):#method to get to resistance´s value
        return self.res
    
    def set_Res(self, res):#method to set a resistance´s value
        self.res = res
    
    def get_Id(self):#method to get resistance´s id
        return self.id
    
    def set_Id(self, idr):# method to set resistance´s id
        self.id = id
    
    def get_Connectedto(self):#method to get where is the resistance connected to
        return self.connectedto
    
    def set_Connectedto(self, node):#method to set where is going to be the resistance connected to
        self.connectedto = node

    def show_data(self):#method to show important data
        if self.image == res_image1:
            PrintText(self.rect.topleft[0],self.rect.topleft[1]-30,30,self.id +" : "+ str(self.res)+ " Ω",blue,self.w,self.h)
        else:
            PrintText(self.rect.center[0]+self.w//2 + 40,self.y-50,30,self.id +" : "+ str(self.res)+ " Ω",blue,self.w,self.h)

class Element_Button():#Class that creates the buttons for circuit elements

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

    def draw(self,screen,outline,image):# draws all the buttons

        if outline:#If the button has outline
            pygame.draw.rect(screen,self.border,(self.x-2,self.y-2,self.w+4,self.h+4),0)
        
        #Button rect
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.w,self.h),0)

        if image:#if the button has an image 
            screen.blit(self.image,(self.x +(self.w//2 - self.rectw//2), self.y + (self.h//2 - self.recth//2)))

    def line_B(self):#draw cable line
        pygame.draw.line(screen,black,(self.x+20, self.y+self.h//2), (self.x + self.w-20 , self.y+self.h//2),5)
        
            
    def over(self,pos):#method to check if mouse is over
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True
        return False

    def highlight(self,image):#method that highlights the button
        self.color = self.colorh
        

    def unhighlight(self,image):#method that unhighlights the button
        self.color = self.colorR
        
    def check(self,pos):#Methos that determines if the mouse is over the button and changes color
        if self.over(pos):
            self.highlight(True)
        else:
            self.unhighlight(True)

class ElementOptions():#Class that generates the buttons of elements

    def __init__(self):
        #list of all the buttons
        self.buttons = [Element_Button(gray,50,s_height-90,110,60,black,res_image1),#Rotate
                        Element_Button(gray,600,s_height-90,110,60,red,res_image1), #Rename
                        Element_Button(gray,600,s_height-90,110,60,white,res_image1)]#Delete
        
        self.respow_B = Element_Button(gray,600,s_height-90,110,60,gray,res_image1)#Revalue
        self.nodeC_B = Element_Button(gray,600,s_height-90,110,60,green,res_image1)#Connect
        self.item = None
        self.active = False
        self.text = ["Rotate","Rename","Delete"]

    def draw(self,screen):#draws the buttons
        
        xpos = 50
        i = 0
        for button in self.buttons:#Draws each button in the list 
            
            button.x = xpos #Determines xpos
            button.draw(screen,False,False)

            if button.color == button.colorh:#Highlights the text in the button
               
                PrintText(button.x,button.y,30,self.text[i],white,button.w,button.h)
            else:
            
                PrintText(button.x,button.y,30,self.text[i],black,button.w,button.h)
                
            i += 1
            xpos += 150 #add to the xpos

        if isinstance(self.item,Resistance) or isinstance(self.item,Power_Output):#Checks if the item is a resistance or powerout
            self.respow_B.x = xpos
            self.respow_B.draw(screen,False,False)

            if self.respow_B.color == self.respow_B.colorh:#highlights the text
                   
                PrintText(self.respow_B.x,self.respow_B.y,30,"Value",white,self.respow_B.w,self.respow_B.h)
            else:
            
                PrintText(self.respow_B.x,self.respow_B.y,30,"Value",black,self.respow_B.w,self.respow_B.h)
                
            xpos += 150


        if isinstance(self.item, Node):#Checks if the item is a node
            self.nodeC_B.x = xpos
            self.nodeC_B.draw(screen,False,False)

            if self.nodeC_B.color == self.nodeC_B.colorh:#highlights the text
                   
                PrintText(self.nodeC_B.x,self.nodeC_B.y,30,"Connect",white,self.nodeC_B.w,self.nodeC_B.h)
            else:
            
                PrintText(self.nodeC_B.x,self.nodeC_B.y,30,"Connect",black,self.nodeC_B.w,self.nodeC_B.h)
            
            xpos += 150
            


    def overclick(self,pos):#Determines if the button is clicked and does the action
        global justSaved
        fbuttons =[]

        for ele in self.buttons:
            fbuttons += [ele]

        if isinstance(self.item,Node):#determines if its a node
            fbuttons += [self.nodeC_B]

        if isinstance(self.item,Resistance) or isinstance(self.item,Power_Output):#determines if its a node or a powerout
            fbuttons += [self.respow_B]

        for button in fbuttons:#draws all buttons present
            if button.over(pos):
                
                if button.border == black:#Rotates the item
                    if  not isinstance(self.item, Node):
                        self.item.rotate()
                    
                elif button.border == red:#Renames the item
                    Tk().wm_withdraw()
                    
                    newname = simpledialog.askstring("Rename","Please enter new name")
                    if newname != None:
                        if len(newname) <= 10:
                            try:
                                newname = int(newname)
                                Tk().wm_withdraw()
                                messagebox.showerror("ERROR", "New name can't be an integer number")
                            
                            except:
                                print("Nuevo nombre: " + newname)
                                self.item.id = newname
                        else:
                            Tk().wm_withdraw()
                            messagebox.showerror("ERROR", "New name can only have a maximum length of 10 characters")
                        
                elif button.border == white:#Deletes the item
                    if isinstance(self.item, Node):#Cheks if its a node
                        graph.empty()
                        
                    self.item.kill()
                    self.active = False
                    justSaved = False

                elif button.border == gray:#Revalues the item
                    Tk().wm_withdraw()
                    
                    newvalue = simpledialog.askinteger("ReValue","Please enter new Value")
                    if newvalue != None:
                        print("Nuevo Valor: " + str(newvalue))
                        if isinstance(self.item, Resistance):
                            self.item.res = newvalue
                        else:
                            self.item.Voltaje = newvalue

                elif button.border == green:
                    print("Connecting nodes 1")
                    connect_nodes(self.item)
                    
            else:
                self.active = False

    def over(self,pos):#Checks if the button is selected
        for button in self.buttons:#Checks every button
            if button.over(pos):
                button.highlight(False)
                self.draw(screen)
            else:
                button.unhighlight(False)
                self.draw(screen)

        if isinstance(self.item,Resistance) or isinstance(self.item,Power_Output):#Determines if its a resitance or power
            if self.respow_B.over(pos):#highlights
                self.respow_B.highlight(False)
                self.draw(screen)
            else:
                self.respow_B.unhighlight(False)
                self.draw(screen)

        if isinstance(self.item,Node):#checks if its node 
            if self.nodeC_B.over(pos):
                self.nodeC_B.highlight(False)
                self.draw(screen)
            else:
                self.nodeC_B.unhighlight(False)
                self.draw(screen)

class Cable_line(): #Class to draw cable

    def __init__(self,pos1,pos2):#main constructor
        self.pos1 = pos1
        self.pos2 = pos2
        self.type = "cable"
        self.id = None
        self.rotation = None
        
    
    def draw(self):#method to draw the cable
        pygame.draw.line(screen,black, self.pos1 , self.pos2,5)
        
    

#Cable list
class Cable_list(): #Class to create a list of cables
    def __init__(self): #Main constructor
        self.list = []

    def get_list(self): #Method to get the list of cables
        return self.list

    def add_line(self,line): #Method to add a new cable
        self.list.append(line)
        
    def empty(self): #Method to delete all existing cables
        self.list = []

class dataHolder(): #Class to hold the necessary Dijkstra info
    
    def __init__(self): #Main constructor
        self.path = ""
        self.weight = "0"


    def set_path(self,path): #Sets a path
        self.path = path

    def set_weight(self,weight): #Sets weight
        self.weight = weight



def drawlines(sim): #Function that draws lines

    if sim:#determines if its sim mode or designmode
        position = 100
        for i in range(1,8):#horizontal lines
            pygame.draw.line(screen,black,(0,position) , (s_width-220 ,position),1)
            
            position += 70

        position = 70
        for i in range(1,15):#Vertical lines
            pygame.draw.line(screen,black,(position,100) , (position,s_height-110),1)
            position += 70

        pygame.draw.line(screen,black,(0,590), (s_width-220,590),1)

    pygame.draw.rect(screen,darkGray,(0,s_height-105,s_width,105),0)
    pygame.draw.rect(screen,(52, 54, 48),(s_width-200,0,200,s_height),0)
    
    for line in C_list.get_list():#draws cables
        line.draw()



#element buttons
resi_B = Element_Button(gray,s_width-155,100,110,60,black,res_image1)
power_B = Element_Button(gray,s_width-155,190,110,60,black,pow_imageB)  
options = ElementOptions()
cable_B = Element_Button(gray,s_width-155,280,110,60,black,pow_imageB)  
Node_B = Element_Button(gray,s_width-155,370,110,60,black,node_image)

#constants
C_list = Cable_list()
node_namer = NodeNamer()
graph = Graph()
dataH = dataHolder()


#Posible locations
Xposible = [70, 140, 210, 280, 350, 420, 490, 560, 630, 700, 770, 840, 910]
Yposible = [170, 240, 310, 380, 450, 520]

def draw_designmode():# fuction to create the design mode screen
    drawlines(True)#Calls lines
    #buttons
    resi_B.draw(screen,False,True)
    power_B.draw(screen,False, True)
    cable_B.draw(screen,False,False)
    cable_B.line_B()
    Node_B.draw(screen,False,True)
    all_sprites.draw(screen)

    #buttons
    TextButton("MENU", 20, 20, 120, 40, black, white, 30, 20, "menu", True)#Menu
    TextButton("Simulate", s_width-170, 20, 120, 40, black, white, 30, 20, "simulations", True)#Simulate
    TextButton("Reset Graph", s_width-170, 470, 120, 40, black, white, 30, 20, "resetG", True)#Reset graph
    TextButton("Reset Cables", s_width-170, 540, 120, 40, black, white, 30, 20, "resetC", True)#Reset cables
    TextButton("SAVE", s_width-170, 610, 120, 40, black, white, 30, 20, "save", True)#Save

    if justSaved:#Checks if the document is saved
        screen.blit(check, (940, 10))
    
    else:
        screen.blit(xRed, (940, 10))

    if namePro != "":
        Text(s_width//2 - 170, 20, 60, namePro.split(".")[0], black)
   
def connect_nodes(node1):#Fuction to connect the nodes
    selecting = True
    resactive = False
    resSelected = None
    
    while selecting: #If its selecting the while continues
        pos = pygame.mouse.get_pos()#gets mouse pos

        for event in pygame.event.get():#checks events in pygame
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  

            if event.type == pygame.MOUSEBUTTONDOWN:#checks if a click

                if not resactive:#If a resistance is not selected
                   
                    for resistance in resistance_S:#checks if you click a resistance
                        if resistance.over(pos):
                            resSelected = resistance
                            resactive = True
            
                else:#when a resistance is selected
                    for node in node_S:#for each node it checks
                        if node.over(pos):                            
                            if not(node1.id in graph.v):#if the node exists
                                graph.add_Vertex(node1.id)  
                            if not(node.id in graph.v):#if the node exists
                                graph.add_Vertex(node.id)       
                            graph.add_Edge(node1.id,node.id,resSelected)
                            selecting = False
                            break

            

def calculateLocation(pos):#Function to calculate location for objects
    posx = pos[0]
    posy = pos[1]
    minx = []
    miny = []
    finalx = 0
    finaly = 0

    for distancex in Xposible:#determines the a list of the values of posx-pos1
        minx.append(abs(pos[0]-distancex))
    
    finalx = Xposible[minx.index(min(minx))] #determines closest posible x in the grid

    for distancey in Yposible:#determines the a list of the values of posy-pos1
        miny.append(abs(pos[1]-distancey))

    finaly = Yposible[miny.index(min(miny))]#determines closest posible y in the grid

    return (finalx,finaly)


def DesignMode(): # Screen where someone can design a model
    
    def select_element(pos):#places the element that client selected
        global justSaved
        selecting = False
        typeE = 0

        drag_element = None

        if resi_B.over(pos):#item selected is resitance
            print("Click in resistance")
            resi_B.highlight(True)
            selecting = True
            typeE = 1
            drag_element = res_image1
            
            
        elif power_B.over(pos):#item selected is power output
            power_B.highlight(True)
            selecting = True
            typeE = 2
            drag_element = pow_image
            
        elif cable_B.over(pos):#item selected is cable
            cable_B.highlight(True)
            selecting = True
            typeE = 3

        elif Node_B.over(pos):#item selected is node
            Node_B.highlight(False)
            selecting = True
            typeE = 4
            
        active1 = False
        pos1 = (0,0)

############################################################################################################################
        while selecting: #while the item hasnt been placed
            screen.fill(white)

            pos = pygame.mouse.get_pos()#gets mouse position

            if drag_element != None:
                screen. blit(drag_element,(pos[0] - (drag_element.get_width()//2) ,pos[1] - (drag_element.get_height()//2)))

            for event in pygame.event.get():#checks every event in pygame
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  

                if event.type == pygame.MOUSEBUTTONDOWN:#i the mouse is clicked
                    if pos[1] < s_height-100 and pos[0] < s_width-200:#If the click happened the the placeable zone
                        if typeE == 1:#if item is resistance
                            poscal = calculateLocation(pos)
                            tmp = Resistance(len(resistance_S),poscal[0],poscal[1])
                            resistance_S.add(tmp)
                            all_sprites.add(tmp)
                            selecting = False
                            resi_B.unhighlight(True)
                            time.sleep(0.3)
                            justSaved = False

                        elif typeE == 2:#if item is power output
                            poscal = calculateLocation(pos)
                            tmp = Power_Output(poscal[0],poscal[1])
                            power_S.add(tmp)
                            all_sprites.add(tmp)
                            selecting = False
                            power_B.unhighlight(True)
                            justSaved = False

                        elif typeE == 3:#if item is cable
                            if active1:
                            
                                if (abs(pos1[0]-pos[0]) > abs(pos1[1]-pos[1])):#determines the axis where the cable is 
                                    newpos = calculateLocation(pos)
                                    pos = (pos[0],newpos[1])
                                    pos1 = (pos1[0],newpos[1])
                                else:
                                    newpos = calculateLocation(pos)
                                    pos = (newpos[0],pos[1])
                                    pos1 = (newpos[0],pos1[1])
                                
                                C_list.add_line(Cable_line(pos1,pos)) #adds cables to c list
                                
                                #Deselects the button
                                cable_B.unhighlight(False)
                                selecting = False
                                active1 = False
                                justSaved = False

                            
                            else:
                                active1 = True
                                pos1 = (pos[0],pos[1])
                                print(pos1)
                                justSaved = False

                        elif typeE == 4:#Item selected is node
                            poscal = calculateLocation(pos)
                            tmp = Node(poscal[0],poscal[1],node_namer.get_name())#creates node
                            node_S.add(tmp)
                            all_sprites.add(tmp)
                            selecting = False
                            Node_B.unhighlight(True)
                            justSaved = False

                    #resets the button /Deselects the button
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

                    elif Node_B.over(pos):
                        print("NodeB")
                        selecting = False
                        Node_B.unhighlight(False)
                        time.sleep(0.3)
                        break
                        
            draw_designmode()
            pygame.display.update()

###########################################################################################################################      
    
    #background
    screen.fill(white)
    
    #variables
    mouse = pygame.mouse.get_pos() #gets mouse position
    click = pygame.mouse.get_pressed() #to know if the mouse was pressed

    draw_designmode()#draws desing mode

    if options.active:#checks if the option button is active
        options.draw(screen)
        options.over(mouse)
        options.item.show_data()

    #checks if the button is highlited
    resi_B.check(mouse)
    power_B.check(mouse)
    cable_B.check(mouse)
    Node_B.check(mouse)

    #Depening of where it clicks
    if click[0]:
        if options.active:
            options.overclick(mouse)

        for resistance in resistance_S:#Checks if what was clicked was a resistance
            if resistance.over(mouse):
               options.active = True
               options.item = resistance
        
        for power in power_S:#Checks if what was clicked was a power
            if power.over(mouse):
                options.active = True
                options.item = power

        for node in node_S:#Checks if what was clicked was a node
            if node.over(mouse):
                options.active = True
                options.item = node

        select_element(mouse) # checks normal placing button



def Draw_simulation(): #Function to create the simulation screen
    global arrayTo, shortest_path
    drawlines(False)#Draws the lines 
    all_sprites.draw(screen)
    #creats all buttons
    pygame.draw.rect(screen, greenPichudo,(s_width-200,0,200,s_height),0)
    TextButton("MENU", 20, 20, 120, 40, black, white, 30, 20, "menu", True, None, (58,76,83))#menu
    TextButton("Design mode", s_width-173, 20, 120, 40, black, white, 30, 38, "design",True, None, (58,76,83))#design mode
    TextButton("Dijkstra", 20, s_height-80, 120, 40, black, white, 30, 38, "dijkstra",True, None, (58,76,83))#Dijkstra
    Button(1130, 535, 30, 55, arrow_down, (159, 171, 166), arrow_downRed, "descendingOrder")#descending
    Button(1050, 535, 30, 55, arrow_up, (159, 171, 166), arrow_upRed, "ascendingOrder")#ascending
    #
    pygame.draw.rect(screen,(159, 171, 166),(300,s_height-90,600,80),0)#-----------
    pygame.draw.rect(screen, (159, 171, 166),(s_width-175,100,160,400),0)#----------------
    TextButton("SAVE", s_width-170, 610, 120, 40, black, white, 30, 20, "save", True, None,(58,76,83) )#---------

    Printdijkstra(320,s_height-80,30,"Shortest Path: " + dataH.path, black)#----------
    Printdijkstra(320,s_height-50,30,"Minimum Weight: " + str(dataH.weight),black)#----------

    #checks the array 
    if arrayToPrint != []:
        PrintOrder(arrayToPrint)
    
    if justSaved:
        screen.blit(check, (940, 10))
    
    else:
        screen.blit(xRed, (940, 10))

    if namePro != "":
        Text(s_width//2 - 170, 20, 60, namePro.split(".")[0], black)
   

def Simulationmode(): #Function that initiates simulation mode
    
    screen.fill(white)
    Draw_simulation()
    mouse = pygame.mouse.get_pos()#Gets mouse position

    for node in node_S:#Checks mouse over node
        if node.over(mouse):
            node.show_sim()

    for resistance in resistance_S:#Checks mouse over resistance
        if resistance.over(mouse):
            resistance.show_data()

    for power in power_S:#checks mouse over power output
        if power.over(mouse):
            power.show_data()

def dijkstra_nodes(): #Function that uses two selected nodes to apply the Dijkstra algorithm between them
    
    node1 = None
    node2 = None
    selecting = True   
    
    while selecting:#
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  

            if event.type == pygame.MOUSEBUTTONDOWN:
                if node1 == None:
                    for node in node_S:
                        if node.over(pos):
                            node1 = node.id
                            print(node.id)
                else:
                    for node in node_S:
                        if node.over(pos):
                            node2 = node.id
                            selecting = False
                            print(node.id)
    
    dijkstra = Dijkstra(graph,node1,node2)
    shortest_path = " "
    i_path = 0
    while i_path < len(dijkstra[1]) - 1:
        shortest_path += dijkstra[1][i_path]  + "-> "
        i_path += 1
    shortest_path += dijkstra[1][i_path]

    dataH.set_path(shortest_path)
        
    dataH.set_weight(str(dijkstra[0]))
    
def Dijkstra(graph,start,goal): #Function that calculates the shortest route from one node to another and its total weight
    shortest_distance = {}
    predecessor = {}
    unseenNodes = list(graph.v.keys())
    infinity = 999999
    path = []
    for node in unseenNodes:
        shortest_distance[node] = infinity
    shortest_distance[start] = 0
    
    while unseenNodes:
        minNode = None
        for node in unseenNodes:
            if minNode is None:
                minNode = node
            elif shortest_distance[node] < shortest_distance[minNode]:
                minNode = node
        for childNode, weight in graph.v[minNode].items():
            if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                shortest_distance[childNode] = weight + shortest_distance[minNode]
                predecessor[childNode] = minNode
        unseenNodes.remove(minNode)
    
    currentNode = goal
    while currentNode != start:
        try:
            path.insert(0,currentNode)
            currentNode = predecessor[currentNode]
        except KeyError:
            print('Path not reachable')
            shortest_distance[goal] = "Path not reachable"
            break
    path.insert(0,start)
    if shortest_distance[goal] != infinity:
        print('Shortest distance is ' + str(shortest_distance[goal]))
        print('And the path is ' + str(path))

    return (shortest_distance[goal],path)
    
# Objects 
def Button(x, ys, wid, hei, image,fill,image2,  action = None): #function to create a button
    global seleccion, gas, score, finish_time, lives, active, ReWriteName, quantityWRITE, arrayToPrint
    mouse = pygame.mouse.get_pos() #gets mouse position
    click = pygame.mouse.get_pressed() #to know if the mouse was pressed

    pygame.draw.rect(screen, fill, [x, ys, wid, hei]) #if the mouse if above the image and creates a rectangle

    if x + wid > mouse[0] > x and ys + hei > mouse[1] > ys:
        if click[0] == 1 and action != None:
            active = False  
            listaRes = []

            for resistance in resistance_S:
                listaRes += [resistance.id]

            if action == "ascendingOrder":
                time.sleep(0.3)
                if listaRes !=[]:
                    arrayToPrint = InsertionSort(listaRes)
                    print(InsertionSort(listaRes))

            elif action == "descendingOrder":
                time.sleep(0.3)
                if listaRes != []:
                    arrayToPrint = QuickSort(listaRes)
                    print(QuickSort(listaRes))
                
        screen.blit(image2, (x, ys))
    else:
        screen.blit(image, (x, ys))

def TextButton(text, xpos, ypos, width, height, ActiveColor, InactiveColor,text_size, extraSize, action = None, OptionalRect = None, toLoad = None, rectColor = None): #Function that creates a textbutton
    global ScreenNum, saved, justSaved, counterSave, namePro
    color = ActiveColor
    mouse = pygame.mouse.get_pos() #gets mouse position
    click = pygame.mouse.get_pressed() #to know if the mouse was pressed

    width += extraSize

    if rectColor == None:
        rectColor = oliveGreen

    if OptionalRect:
        pygame.draw.rect(screen, rectColor, [xpos, ypos, width, height])

    color = InactiveColor
    if xpos + width > mouse[0] > xpos and ypos + height > mouse[1] > ypos:
        #pygame.draw.rect(game, fill, [xpos - 5, ypos - 5, width + 10,height + 10])  # if the mouse if above the image and creates a rectangle
        #PrintScreen(text, xpos + 60, ypos + 60, text_size, ActiveColor)
        color = ActiveColor
        if click[0] == 1:
            if action == "design":
                ScreenNum = 1
                time.sleep(0.3)
                arrayToPrint = []

            elif action == "menu":#menu 
                if not justSaved:
                    Tk().wm_withdraw()
                    if messagebox.askyesno("SAVED PROJECTS", "Do you want to Exit without saving "  + "?", icon = "warning"):
                        all_sprites.empty()
                        resistance_S.empty()
                        power_S.empty()
                        graph.empty()
                        node_S.empty()
                        C_list.empty()
                        justSaved = False
                        counterSave = 0
                        namePro = ""
                        arrayToPrint = []
                        ScreenNum = 0

                else:
                    ScreenNum = 0
                    all_sprites.empty()
                    resistance_S.empty()
                    power_S.empty()
                    graph.empty()
                    C_list.empty()
                    node_S.empty()
                    justSaved = False
                    counterSave = 0
                    namePro = ""
                    arrayToPrint = []
                

            elif action == "import":#import
                Tk().wm_withdraw()
                if messagebox.askyesno("SAVED PROJECTS", "Do you want to load " + toLoad.split(".")[0] + "?"):
                    project = LoadProject(toLoad)
                    namePro = toLoad
                    counterSave = 1
                    ScreenNum = 1
                    justSaved = True

            elif action == "new":#
                TkinterSaved()
                
            elif action == "save":
                Tk().wm_withdraw()
                if messagebox.askyesno("SAVE", "Do you want to save?"):
                    SaveProject()

            elif action == "simulations":
                ScreenNum = 2
                time.sleep(0.3)
                arrayToPrint = []

            elif action == "resetG":
                Tk().wm_withdraw()
                if messagebox.askyesno("RESET GRAPH", "Do you want to reset the Graph?"):
                    graph.empty()


            elif action == "resetC":
                Tk().wm_withdraw()
                if messagebox.askyesno("RESET CABLES", "Do you want to reset the Cables?", icon = "warning"):
                    C_list.empty()
                
            elif action == "dijkstra":
                dijkstra_nodes()

            elif action == "Ohm":
                CalculateCiurcuitType()


        elif click[2] == 1:
            if action == "import":
                Tk().wm_withdraw()
                if messagebox.askyesno("SAVED PROJECTS", "Do you want to detele " + toLoad.split(".")[0] + "?", icon = "warning"):
                    DeleteFile(toLoad)
   
    PrintText( xpos, ypos, text_size, text, color, width, height)
        

def PrintText(x, y, size, text, color, width = None, height = None): #Function that puts text on the screen
    font = pygame.font.SysFont("Teko", size)
    text = font.render(text, True, color)
    
    screen.blit(text, (x +(width//2 - text.get_width()//2), y + (height//2 - text.get_height()//2)))


def Printdijkstra(x,y,size,text,color): #Function that puts relevant Dijkstra values on the screen
    font = pygame.font.SysFont("Teko", size)
    text = font.render(text, True, color)
    screen.blit(text, (x , y))

def Text(x, y, size, text, color): #Function that puts text on the screen
    font = pygame.font.SysFont("Teko", size)
    text = font.render(text, True, color)
    screen.blit(text, (x,y))

def WriteNewSaved(name): #writes info to then load a project
    route = "./savedProjects/savedProjects.txt"
    registry = open(route, "a")
    registry.write(name + "{")
    registry.close()

def WriteProject(data, name): #Function that saves a circuit
    global tkActive
    route = "./savedProjects/" + name
    registry = open(route, "w")
    registry.write(data)
    registry.close()

def ReadProject(project): #Function that read lines of an specific project
    route = "./savedProjects/" + project
    read = open(route)
    content = read.readlines()
    read.close()
    

    return content

def LoadProject(project): #function to load lines from a project and draw everthing in design mode
    route = "./savedProjects/" + project
    read = open(route)
    content = read.readlines()
    print(content)
    
    for line in content:
        line = line.split("|")
        line[-1] = line[-1].split("\n")[0]
        print(line)
        if line != None:
            if line[0] == "res":
                create_Res(line)
            elif line[0] == "power":
                create_Pow(line)
            elif line[0] == "cable":
                create_Cable(line)
            elif line[0] == "node":
                create_Node(line)  
            elif line[0] == "graph":
                create_graph(line)
           
    read.close()
    
def create_graph(content):#function to create a graph from a saved project

    dictionary = eval(content[1])
    graph.v = dictionary
    
def create_Res(content):#function to create all resistances from a saved project
    
    tmp = Resistance(content[1],int(content[2]),int(content[3]))
    resistance_S.add(tmp)
    all_sprites.add(tmp)
    tmp.set_Res(int(content[5]))
    tmp.id = content[1]
    if content[4] == "1": 
        tmp.rotate()


def create_Pow(content):#function to create the batery from a saved project
    
    tmp = Power_Output(int(content[2]),int(content[3]))
    power_S.add(tmp)
    all_sprites.add(tmp)
    tmp.id = content[1]
    tmp.Voltaje = int(content[5])

    if content[4] == "1":
        tmp.rotate()

def create_Cable(content): #function to create the cables from a saved project
    
    C_list.add_line(Cable_line((int(content[2]),int(content[3])),(int(content[4]),int(content[5])))) 

def create_Node(content): #function to create nodes from a saved projects

    tmp = Node(int(content[2]),int(content[3]),content[1])
    node_S.add(tmp)
    all_sprites.add(tmp)
    
def SeparateContent(data): #function to separete content
    try:
        data = data[0].split("{")
        return data
    except:
        return []

def DeleteFile(name): #function to delete a file from computer
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

def SaveAll():#function to save everthing
    with open("./savedProjects/" + namePro, 'w') as savefile:
        tmp = ""
        for res in resistance_S:
            tmp = str(res.type)+'|'+str(res.id)+'|'+str(res.rect.centerx)+'|'+str(res.rect.centery)+"|"+str(res.get_rotation()) + "|"+ str(res.get_Res())
            savefile.writelines(tmp+"\n")
        
        for powe in power_S:
            tmp = str(powe.type)+'|'+str(powe.id)+ '|' + str(powe.rect.centerx)+'|'+str(powe.rect.centery)+"|"+str(powe.get_rotation()) +"|"+ str(powe.get_Voltaje())
            savefile.writelines(tmp+"\n")

        for node in node_S:
            tmp = str(node.type)+'|'+str(node.id)+'|'+str(node.rect.centerx)+'|'+str(node.rect.centery)+"|"+str(node.rotation)
            savefile.writelines(tmp+"\n")

        for cable in C_list.get_list():
            tmp = str(cable.type)+'|'+str(cable.id)+ '|'+str(cable.pos1[0])+'|'+str(cable.pos1[1])+'|'+str(cable.pos2[0])+"|"+str(cable.pos2[1])
            savefile.writelines(tmp+"\n")

        savefile.writelines("graph"+"|"+str(graph.v))

def SaveProject():#fucntion to save a project
    global justSaved, counterSave, namePro
    justSaved = True
    if counterSave == 0:
        Tk().wm_withdraw()        
        newname = simpledialog.askstring("ReValue","Please enter new Name for your savefile")
        if newname != None and len(newname) <= 15:
            if CheckName(newname) == False:
                namePro = newname + ".txt"
                SaveAll()
                counterSave += 1
                WriteNewSaved(namePro)
            else:
                Tk().wm_withdraw() 
                messagebox.showerror("ERROR", "The file's name is already used")
                justSaved = False
        else:
           Tk().wm_withdraw() 
           messagebox.showerror("ERROR", "The file's name can have a maximum length of 15 characters")
           newname = ""
           justSaved = False
    else:
        SaveAll()

def CheckName(name):#function to check if a name already exists
    name += ".txt"
    route = "./savedProjects"
    files = os.listdir(route)
    if name in files:
        return True
    else:
        return False

######## ORDERING ALGORITHMS ########
def QuickSort(array): #Sorts in Descending order
        minor = []
        equal = []
        major = []

        if len(array) > 1:
            pivote = array[0]

            for i in array:
                if i > pivote:
                    major.append(i)
                if i == pivote:
                    equal.append(i)
                if i < pivote:
                    minor.append(i)

            return QuickSort(major) + equal + QuickSort(minor)
        
        else:
            return array

def InsertionSort(array): #Sorts in Ascending order 
        length = len(array)

        for i in range(1, length):
            value = array[i]
            pos = i

            while pos > 0 and array[pos-1] > value:
                array[pos] = array[pos-1]
                pos -= 1

            array[pos] = value

        return array

def PrintOrder(array): #Prints the list in the selected order, Ascending or Descending on the screen
    global FPS
    #print("Entrando a imprimir")
    xpos = 1030
    ypos = 80
    length = len(array)
    counter = 0
    while counter < length:
        ypos += 25
        Text(xpos, ypos, 20, array[counter], (58,76,83))
        counter += 1

def CalculateCiurcuitType():
    #for res in resistance_S:
#tmp = str(res.type)+'|'+str(res.id)+'|'+str(res.rect.centerx)+'|'+str(res.rect.centery)+"|"+str(res.get_rotation()) + "|"+ str(res.get_Res())
    paralelo = []
    serie = []
    resList = []
    length = len(resistance_S)

    for res in resistance_S:
        resList+= [res]
    pivotex = resList[0].x
    pivotey = resList[0].y
    pivoteRot = resList[0].get_rotation()
    counter = 1


    while counter < length:
        analize = resList[counter]
        if analize.get_rotation() == 0 and pivoteRot == 0:
            if analize.x == pivotex or analize.x in range(pivotex-400, pivotex + 400):
                if analize.y != pivotey:
                    paralelo += [analize]
            elif analize.y == pivotey or analize.y in range(pivotey-400, pivotey+400):
                serie += [analize]

        elif analize.get_rotation() == 1 and pivoteRot == 1:
            if analize.x == pivotex or analize.x in range(pivotex-400, pivotex + 400):
                if analize.y != pivotey:
                    serie += [analize]
            elif analize.y == pivotey or analize.y in range(pivotey-400, pivotey+400):
                paralelo += [analize]

        counter += 1

    pivoteRot = resList[length-1].get_rotation()
    pivotex = resList[length-1].x
    pivotey = resList[length-1].y

    analize = resList[0]

    if analize.get_rotation() == 0 and pivoteRot == 0:
            if analize.x == pivotex or analize.x in range(pivotex-400, pivotex + 400):
                if analize.y != pivotey:
                    paralelo += [analize]
            elif analize.y == pivotey or analize.y in range(pivotey-400, pivotey+400):
                serie += [analize]

    elif analize.get_rotation() == 1 and pivoteRot == 1:
        if analize.x == pivotex or analize.x in range(pivotex-400, pivotex + 400):
                if analize.y != pivotey:
                    serie += [analize]

        elif analize.y == pivotey or analize.y in range(pivotey-400, pivotey+400):
            paralelo += [analize]
    #return [[paralelo], [serie]]
    print([[paralelo], [serie]])

def CircuitTypeAux(analize, pivoteRot, pivotey, pivotex):
    pass

                

######## MAIN LOOP ############                
while True: 
    #print(random.randint(1,100))   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if not justSaved and ScreenNum != 0:
                Tk().wm_withdraw()
                if messagebox.askokcancel("EXIT", "Do you want to exit without saving?", icon="warning"):
                    pygame.quit()
                    sys.exit()
            else:
                pygame.quit()
                sys.exit()

    if ScreenNum == 0:
        Menu()

    elif ScreenNum == 1:
        
        DesignMode()

    elif ScreenNum == 2:
        Simulationmode()
    
    pygame.display.update()