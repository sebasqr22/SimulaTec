"""
Tarea de Ordenamiento
Sebastián Quesada 
Audi Solis 
"""
import random
import time

def HaceLista5000():
     lista = []
     contador = 0
     while contador <= 5000 :
          lista += [random.randrange(0, 10000)]
          contador += 1

     return lista

#RadixSort
def RadixSort(lista):
     tiempo_de_inicio = time.time()
     if isinstance(lista, list):
          elementoMaximo = max(lista)
          pos = 1

          while elementoMaximo // pos > 0:
               RadixAux(lista, pos)
               pos *= 10
          print("Randix :", lista)
          print("--------------Tiempo--Transcurrido:-",(time.time()-tiempo_de_inicio), "---------segundos") 

     else:
          return "F"

def RadixAux(lista, posicion):
     tamaño = len(lista)
     salida = [0] * tamaño
     contador = [0] * 10

     for i in range(0, tamaño):
          elementos = lista[i] // posicion
          contador[elementos % 10] += 1

     for i in range(1, 10):
          contador[i] += contador[i-1]

     pos = tamaño-1
     while pos >= 0:
          index = lista[pos] // posicion
          salida[contador[index % 10]-1] = lista[pos]
          contador[index%10] -= 1
          pos -= 1

     for i in range(0, tamaño):
          lista[i] = salida[i]
#===================================================================================
#SelectionSort
def SelectionSort(lista):
     tiempo_de_inicio = time.time()
     for i in range(len(lista)-1):
          minimo = i

          for j in range(i+1, len(lista)-1):
               if lista[j] < lista[minimo]:
                    minimo = j

          lista[i], lista[minimo] = lista[minimo], lista[i]
     print("Selection : ", lista)
     print("--------------Tiempo--Transcurrido:-",(time.time()-tiempo_de_inicio), "---------segundos") 

#===================================================================================
#QuickSort
def QuickSort(lista):
    if isinstance(lista,list):
        # se definen tres listas
        menor = []
        igual = []
        mayor = []

        # Se define la función del caso en que la lista es mayor a 1
        if len(lista) > 1:
            # Se "settea" un valor, no es necesario que sea el primer elemento de la lista.
            # El pivote es el elemento en la posición asignada, en este caso, en la posición cero.
            pivote = lista[0]

            #Se pasa por cada elemento de la lista por medio de recursividad y se ordena.
            for i in lista:
                if i < pivote:
                    menor.append(i)
                if i == pivote:
                    igual.append(i)
                if i > pivote:
                    mayor.append(i)

            #Se retorna y se llama de forma recursiva a la función para que ordene la lista de menor a mayor
            return QuickSort(menor)+igual+QuickSort(mayor)
        else:
            return lista
    else:
        return "Ingrese una lista válida"
#===================================================================================
# Hecha en clase!
def BubbleSort(lista):
     if isinstance(lista, list) and lista != []:
          largo = len(lista)
          for i in range(0, largo):
               for j in range(0, largo):
                    if lista[j] > lista[j+1]:
                         aux = lista[j]
                         lista[j] = lista[j+1]
                         lista[j+1] = aux

          return lista

     else:
          return "Pongase serio mi raico, coloque una lista válida"

#===================================================================================
def InsertionSort(lista):
    if isinstance(lista, list) and lista != []:
        largo = len(lista)
        # En este loop entra cada elemento de la lista
        for i in range(1, largo):
            valor = lista[i]
            pos = i

            while pos > 0 and lista[pos-1] > valor:
                print("El numero ",lista[pos],"por ",lista[pos-1])
                lista[pos] = lista[pos-1]
                print(lista)
                pos -= 1

            lista[pos] = valor

        return lista

    else:
        return "Mi bro, coloque una lista válida"
