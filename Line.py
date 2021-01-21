import pygame
import sys
import os


pygame.init()
s_width = 1200
s_height = 700
screen = pygame.display.set_mode((s_width,s_height))

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

all_sprites = pygame.sprite.Group()


img_dir = os.path.join(os.path.dirname(__file__),'imgs')

def cargar_img(nombre):
    #cargar_img: utiliza os para poder importar imagenes de algun folder pygame
    #e: nombre de la imagen
    #s: imagen formato pygame
    #R: ---
    ruta = os.path.join(img_dir,nombre)
    imagen = pygame.image.load(ruta)
    return imagen


res_image = cargar_img("resistencia.png")
res_image = pygame.transform.scale(res_image,(100,50))

class Element(pygame.sprite.Sprite):

    def __init__(self, x, y):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = res_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        
    
    def over(self, pos):
            if pos[0] > self.x and pos[0] < self.x + self.w:
                if pos[1] > self.y and pos[1] < self.y + self.h:
                    return True
            return False   
    

    


def linemaker():

    pass
tmp1 = Element(10,10)
tmp2 = Element(40,10)

all_sprites.add(tmp1)
all_sprites.add(tmp2)

print(len(all_sprites))
def main():
    
    active1 = False
    active2 = False
    pos1 = (0,0)
    pos2 = (0,0)
    screen.fill(white)
    
    while(True):
        
        res = Element(100,100)
        all_sprites.add(res)
        for event in pygame.event.get():

            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 

            if event.type == pygame.MOUSEBUTTONDOWN:
                #funcion de boton
                   
                if active2:
                    #surface, color, x & y start, x & y end, width
                    if (abs(pos2[0]-pos[0]) > abs(pos2[1]-pos[1])):
                        pos = (pos[0],pos2[1])
                    else:
                        pos = (pos2[0],pos[1])
                    print(pos)
                    pygame.draw.line(screen,black,pos1 , pos2,4)
                    pygame.draw.line(screen,black,pos2 , pos,4)

                    active2 = False

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
        
        pygame.display.update()


while True:    
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  
    
    main()
    
    pygame.display.update()
