import pygame
import random
#https://algotree.org/algorithms/single_source_shortest_path/dijkstras_shortest_path_python/
#Combinando este con https://www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php
#podemos crear el graph con dijsktra





#######################################################################################################
class Vertex:

    def __init__(self, idv):
        self.id = idv
        self.adjacent = {}
        self.previous = None

    def add_Neighbor(self, name, cost = 0):
        self.adjacent[name] = cost

    def get_Connections(self):
        return self.adjacent.keys()
    
    def get_Id(self):
        return self.id
    
    def set_Previous(self, prev):
        self.previous = prev
    
    def get_Previous(self):
        return self.previous

    def get_Weight(self, neighbor):
        return self.adjacent[neighbor]

   
       
#######################################################################################################





    
class Graph:

    def __init__(self):
        self.v = {}
        self.size = 0

    def __iter__(self):
        return iter(self.v.values())

    def add_Vertex(self, name):
        new_vertex = Vertex(name)
        self.v[name] = new_vertex

        self.size += 1
    
    def add_Edge(self, frm, to, res):

        if frm not in self.v:
            self.add_Vertex(frm)
        if to not in self.v:
            self.add_Vertex(to)

        self.v[frm].add_Neighbor(self.v[to], res.get_Res())

    def Dijsktra_short_path(self,frm):
        pass
    
    def Dijsktra_long_path(self,frm):
        pass

#######################################################################################################

class Resistance(pygame.sprite.Sprite):

    def __init__(self, idr):
        self.res = random.randrange(10,100)
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

#######################################################################################################   

g = Graph()

g.add_Vertex('a')
g.add_Vertex('b')
g.add_Vertex('c')
g.add_Vertex('d')

R1 = Resistance(1)
R2 = Resistance(2)
R3 = Resistance(3)
R4 = Resistance(4)

g.add_Edge('a','b',R1)
g.add_Edge('a','c',R2)
g.add_Edge('b','c',R3)
g.add_Edge('c','d',R4)

print ('Graph data:')

for v in g:
    for w in v.get_Connections():
        vid = v.get_Id()
        wid = w.get_Id()
        print (( vid , wid, v.get_Weight(w)))
ps = 100
lista = []
for i in range(0,8):
    lista.append(ps)
    ps += 70

print(lista)