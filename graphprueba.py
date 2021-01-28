import pygame
import random
#https://algotree.org/algorithms/single_source_shortest_path/dijkstras_shortest_path_python/
#Combinando este con https://www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php
#podemos crear el graph con dijsktra

#######################################################################################################
class Graph:
    def __init__(self):
        self.v = {}
        self.size = 0
        self.i = 1

    def __iter__(self):
        return iter(self.v.values())

    def add_Vertex(self, name):
        self.v[name] = {}
        self.size += 1
    
    def add_Edge(self, frm, to, res):
        if to in self.v[frm]:
            to = str(to) + str(self.i)
            self.i += 1
        self.v[frm].update({to: res.get_Res()})


#######################################################################################################

class Resistance(pygame.sprite.Sprite):

    def __init__(self, idr, res):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = None
        #self.rect = self.sprite.get_rect()
        self.x = 0
        self.y = 0

        self.res = res
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

R1 = Resistance(1,100)
R2 = Resistance(2,200)
R3 = Resistance(3,300)
R4 = Resistance(4,400)

g.add_Edge('a','b',R1)
g.add_Edge('a','c',R2)
g.add_Edge('b','c',R3)
g.add_Edge('c','d',R4)

print(g.v)
#print ('Graph data:')

'''for v in g:
    for w in v.get_Connections():
        vid = v.get_Id()
        wid = w.get_Id()
        print (( vid , wid, v.get_Weight(w)))
'''

#graph = {'a':{'b':10,'c':3},'b':{'c':1,'d':2},'c':{'b':4,'d':8,'e':2},'d':{'e':7},'e':{'d':9}}
#graph = {'a':{'b':8,'f':13,'c':3},'b':{'c':2,'d':1},'c':{'b':3,'d':9,'e':2},'d':{'e':4,'h':2,'g':6},'e':{'a':5,'d':6,'f':5,'i':4},
#'f':{'i':7,'g':1},'g':{'h':4,'e':3},'h':{'i':1},'i':{'g':5}}
#print(graph.items())

def dijkstra(graph,start,goal):
    shortest_distance = {}
    predecessor = {}
    unseenNodes = graph.v
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
        unseenNodes.pop(minNode)
    
    currentNode = goal
    while currentNode != start:
        try:
            path.insert(0,currentNode)
            currentNode = predecessor[currentNode]
        except KeyError:
            print('Path not reachable')
            break
    path.insert(0,start)
    if shortest_distance[goal] != infinity:
        print('Shortest distance is ' + str(shortest_distance[goal]))
        print('And the path is ' + str(path))

dijkstra(g, 'a', 'd')

