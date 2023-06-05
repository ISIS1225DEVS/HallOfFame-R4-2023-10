"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
assert cf
from tabulate import tabulate
import traceback
import threading

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador 
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    
    size =  chooseFileSize() 
    control = controller.new_controller(size)
    return control



def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control,filename, filename2,memflag):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    data = controller.load_data(control, filename, filename2,memflag)
    return data


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    
    origen = chooseOrigenPoint()
    destino = chooseDestinyPoint()
    print("Desea observar el uso de memoria? (True/False)")
    mem = input("Respuesta: ")
    mem = castBoolean(mem)
    if mem ==True:
       ans, delta_time, delta_memory, flag, nWolf, nMeet, dist = controller.req_1(control, mem, origen, destino)
    else:
        ans, delta_time, flag, nWolf, nMeet, dist = controller.req_1(control, mem, origen, destino)
    
        
    print("============REQ 1 imputs============")
    print("NODO INICIAL: "+str(origen))
    print("NODO FINAL: "+str(destino)+"\n")
    
    print("CREANDO ARBOL DFS...")
    print("OBSERVADO SI "+str(destino)+" ESTA EN EL ARBOL")
    print("RESPUESTA: "+str(flag)+"\n")
    
    print("BUSCANDO UN CAMINO ENTRE "+str(origen)+" Y "+str(destino)+"...")
    print("CREANDO DETALLES DE RESPUESTA...\n")
 
 
    print("============REQ 1 Answer============")
    print("TOTAL DE NODOS EN EL CAMINO: " +str(nWolf+nMeet))
    print("EL TOTAL DE NODOS DE ENCUENTRO: "+str(nMeet))
    print("EL TOTAL DE NODOS DE SEGUIMINETO: "+str(nWolf))
    print("EL TOTAL DE LA DISTANCIA RECORRIDA: "+str(dist)+" km")
    
    headers = ['location long-aprox', 'location lat-aprox', 'node-id', 'individual-ids', 'individual count','edge-to', 'distance to next']
    tabulateLindo2(ans, headers)
    if mem == True:
        print("Tiempo [ms]: ", str(delta_time), "||",
              "Memoria [kB]: ",str(delta_memory))
    else:
        print("Tiempo [ms]: ", str(delta_time))
    return None


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    origen = chooseOrigenPoint()
    destino = chooseDestinyPoint()
    print("Desea observar el uso de memoria? (True/False)")
    mem = input("Respuesta: ")
    mem = castBoolean(mem)
    
    if mem ==True:
       ans, delta_time, delta_memory, flag, nWolf, nMeet, dist = controller.req_2(control, mem, origen, destino)
    else:
        ans, delta_time, flag, nWolf, nMeet, dist = controller.req_2(control, mem, origen, destino)
    
        
    print("============REQ 2 imputs============")
    print("NODO INICIAL: "+str(origen))
    print("NODO FINAL: "+str(destino)+"\n")
    
    print("CREANDO ARBOL DFS...")
    print("OBSERVADO SI "+str(destino)+" ESTA EN EL ARBOL")
    print("RESPUESTA: "+str(flag)+"\n")
    
    print("BUSCANDO UN CAMINO ENTRE "+str(origen)+" Y "+str(destino)+"...")
    print("CREANDO DETALLES DE RESPUESTA...\n")
 
 
    print("============REQ 2 Answer============")
    print("TOTAL DE NODOS EN EL CAMINO: " +str(nWolf+nMeet))
    print("EL TOTAL DE NODOS DE ENCUENTRO: "+str(nMeet))
    print("EL TOTAL DE NODOS DE SEGUIMINETO: "+str(nWolf))
    print("EL TOTAL DE LA DISTANCIA RECORRIDA: "+str(dist)+" km")
    
    headers = ['lat', 'long', 'id', 'indi ids', 'wolf count','edge-to', 'dist to next']
    tabulateLindo2(ans, headers)
    if mem == True:
        print("Tiempo [ms]: ", str(delta_time), "||",
              "Memoria [kB]: ",str(delta_memory))
    else:
        print("Tiempo [ms]: ", str(delta_time))
    return None


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    print("Desea observar el uso de memoria? (True/False)")
    mem = input("Respuesta: ")
    mem = castBoolean(mem)
    if mem ==True:
       ltFinal,componentes_conectados, kosarajuMap,ltComponentes,delta_time, delta_memory = controller.req_3(control, mem)
    else:
        ltFinal,componentes_conectados, kosarajuMap,ltComponentes, delta_time= controller.req_3(control, mem)
        
    headers = ['ID MANADA', 'NODE ID', 'TAMAÑO MANADA', 'MIN-LAT', 'MAX-LAT', 'MIN-LONG', 'MAX-LONG', 'WOLF COUNT', 'WOLF DETAILS']
    headers2 = ['id', 'sex', 'stu_site', 'dep_com']
    
    print("============REQ 3 Answer============ \n")
    
    print(f'El total de componentes conectados es: {componentes_conectados} \n')
    
    print("Se muestran los primeros 5 componentes conectados del grafo\n")
    
    ltFinal_Recortada = controller.firstFive(ltFinal)
    
    tabulateLindoReq3(ltFinal_Recortada,headers, headers2)
    
    
    
    
    if mem == True:
        print("Tiempo [ms]: ", str(delta_time), "||",
              "Memoria [kB]: ",str(delta_memory))
    else:
        print("Tiempo [ms]: ", str(delta_time))
        
    print('Hay manadas :)')

    return None

def tabulateLindoReq3(lista, headers, headers2):
    matriz = []
    for registro in lt.iterator(lista):
        fila = []
        info = registro['elements']
        size = info[2]
        for data in info:
            if type(data) == dict and data['size'] == size:
                dataLindo = data['elements']
                if data['size'] > 1:
                    first3 = dataLindo[:3]
                    last3 = dataLindo[-3:]
                    combined = first3 + ['...'] + last3
                    data = combined
                else:
                    data = dataLindo
            else:
                if type(data) == dict:
                    dataLindo = data['elements']
                    data = tabulateLindoReq3_2(dataLindo, headers2)
            fila.append(data)
        matriz.append(fila)
        
    print(tabulate(matriz, headers, tablefmt="grid", maxcolwidths=[10, 15, 10, 10, 10, 10, 10, 10, 70], maxheadercolwidths=[10, 15, 10, 10, 10, 10, 10 ,10, 70]))
    
def tabulateLindoReq3_2(lista, headers2):
    matriz = []
    for listaLinda in lista:
        fila = []
        for registro in lt.iterator(listaLinda):
            
            fila.append(registro)
        matriz.append(fila)
    return tabulate(matriz, headers2, tablefmt="grid", maxcolwidths=[15, 15,15, 15], maxheadercolwidths=[15, 15, 15, 15])



def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 
    lon_or = input("Ingrese longitud de origen: ")
    lat_or = input("Ingrese latitud de origen: ")
    origen = (float(lat_or),float(lon_or))
    lon_des = input("Ingrese longitud de origen: ")
    lat_des = input("Ingrese longitud de origen: ")
    destino = (float(lat_des), float(lon_des))
    print("Desea observar el uso de memoria? (True/False)")
    mem = input("Respuesta: ")
    mem = castBoolean(mem)
    if mem ==True:
       NodoMascercano_O, delta_time, delta_memory, tablaOrigen, distMin1, NodoMascercano_D, tabladestino, distMin2,r2, nWolf, nMeet, disttot, r4 = controller.req_4(control, mem, origen, destino)
    else:
       NodoMascercano_O, delta_time, tablaOrigen, distMin1, NodoMascercano_D, tabladestino, distMin2,r2, nWolf, nMeet, disttot, r4 = controller.req_4(control, mem, origen, destino)

    headers1 = ['node id', 'long', 'lat', 'indivs-IDs']
    headers2 = ['node', 'long', 'lat', 'next', 'long', 'lat', 'dist_to']
    headers3 = ['node', 'long', 'lat', 'ind ids', 'ind count']
    
    print("============REQ 4 imputs============")
    print("NODO INICIAL: "+str(origen))
    print("NODO FINAL: "+str(destino)+"\n")
    
    print("============REQ 4 Answer============\n")
    
    print("Distiancia desde el origen dado "+str(distMin1)+"[KM]")
    print(tabulate([tablaOrigen['elements']], headers1,tablefmt="grid",maxcolwidths=20, maxheadercolwidths=20))
    print("Distiancia desde el destino dado "+str(distMin2)+"[KM]")
    print(tabulate([tabladestino['elements']], headers1,tablefmt="grid",maxcolwidths=20, maxheadercolwidths=20))
    print("\n")
    
    print("------------Detalles de ruta----------")
    print("Primeros 3 y ultimos 3 arcos")
    print("Distancia recorrida desde el origen "+NodoMascercano_O+" hasta el destino "+NodoMascercano_D+" es de "+str(disttot))
    tabulateLindo2(r2, headers2)
    
    print("\n")
    print("------------Detalles de nodos----------")
    print("Primeros 3 y ultimos 3 nodos")
    tabulateLindo2(r4, headers3)
    if mem == True:
        print("Tiempo [ms]: ", str(delta_time), "||",
              "Memoria [kB]: ",str(delta_memory))
    else:
        print("Tiempo [ms]: ", str(delta_time))
    return None


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    origen=input("ingrese el nodo de origen ")
    distancia=float(input("distancia "))
    minMP=float(input("min puntos de encuentro "))
    print("Desea observar el uso de memoria? (True/False)")
    memflag = input("Respuesta: ")
    memflag = castBoolean(memflag)
    resp=controller.req_5(control,memflag,origen,distancia,minMP)
    if memflag is True:
        print(f"Con un tiempo de {resp[2]} ms y un consumo de memoria de {resp[3]}, los resultados son los siguientes:")
        print("\n")
        print(f"Se visitaron los puntos {resp[0]} y se recorrió una distancia de {resp[1]} kms.")
    else:
        print(f"Con un tiempo de {resp[2]} ms, los resultados son los siguientes:")
        print("\n")
        print(f"Se visitaron los puntos {resp[0]} y se recorrió una distancia de {resp[1]} kms.")
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
        # TODO: Imprimir el resultado del requerimiento 2
    print("============REQ 4 imputs============\n")    
    genero = input("Ingrese el genereo de los lobis(f,m): ")
    fechaIn = input("Ingrese la fecha inicial de estudio('%Y-%m-%d %H:%M'): ")
    fechaF = input("Ingrese la fecha fianal de estudio('%Y-%m-%d %H:%M'): ")
    mem = input("Respuesta: ")
    mem = castBoolean(mem)
    
    if mem ==True:
       wolfmax, delta_time, delta_memory, wolfmix, wolfmxInfo, wolfminInfo, nodesRMAX, nodesRMIN, wolfMAXRute ,wolfMINRute = controller.req_6(control, mem, fechaIn, fechaF, genero)
    else:
        wolfmax, delta_time, wolfmix, wolfmxInfo, wolfminInfo, nodesRMAX, nodesRMIN, wolfMAXRute ,wolfMINRute = controller.req_6(control, mem, fechaIn, fechaF, genero)
        
    print("============REQ 4 Answer============\n")
    
    print("El lobo que mas distancia recorre en las coniciones dadas es: "+str(wolfmax[0]))
    print("Este recorre una distancia total de: "+str(wolfmax[1]))    
    
    headers1 = ['indiv id', 'taxon', 'etapa de vida', 'sitio de estudio', 'distancia recorrida', 'comentarios']
    print(tabulate([wolfmxInfo['elements']], headers1))#,tablefmt="grid",maxcolwidths=20, maxheadercolwidths=20)) 
    
    print(" y su ruta fue: ")
    headers2 = ['node-id', 'long', 'lat', 'ind-id', 'ind-count']
    tabulateLindo2(wolfMAXRute, headers2)   
    print("Compuesta por "+str(nodesRMAX)+" Nodos, y "+str(nodesRMAX-1)+" Arcos")
    
    print("El lobo que menos distancia recorre en las coniciones dadas es: "+str(wolfmix[0]))
    print("Este recorre una distancia total de: "+str(wolfmix[1]))    
    
    headers1 = ['indiv id', 'taxon', 'etapa de vida', 'sitio de estudio', 'distancia recorrida', 'comentarios']
    print(tabulate([wolfminInfo['elements']], headers1,tablefmt="grid",maxcolwidths=20, maxheadercolwidths=20))    
    
    print(" y su ruta fue: ")
    headers2 = ['node-id', 'long', 'lat', 'ind-id', 'ind-count']
    tabulateLindo2(wolfMINRute, headers2)   
    print("Compuesta por "+str(nodesRMIN)+" Nodos, y "+str(nodesRMIN-1)+" Arcos")
    if mem == True:
        print("Tiempo [ms]: ", str(delta_time), "||",
              "Memoria [kB]: ",str(delta_memory))
    else:
        print("Tiempo [ms]: ", str(delta_time))
    return None
     

def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    
    minDate = chooseminDate()
    maxDate = choosemaxDate()
    minTemp = chooseminTemp()
    maxTemp = choosemaxTemp()
    print("Desea observar el uso de memoria? (True/False)")
    mem = input("Respuesta: ")
    mem = castBoolean(mem)
    
    if mem ==True:
       numVertex, numArcos, connectedComponents_Manadas, ltFinal, delta_time, delta_memory= controller.req_7(control, mem, minDate, maxDate, minTemp, maxTemp)
    else:
        numVertex, numArcos, connectedComponents_Manadas, ltFinal, delta_time= controller.req_7(control, mem, minDate, maxDate, minTemp, maxTemp)
    
    headers = ['ID MANADA', 'NODE ID', 'TAMAÑO MANADA', 'MIN-LAT', 'MAX-LAT', 'MIN-LONG', 'MAX-LONG', 'WOLF COUNT', 'WOLF DETAILS']
    headers2 = ['id', 'sex', 'stu_site', 'dep_com']
    
    print("============REQ 7 Answer============ \n")
    
    print(f'El total de vertices del digrafo es: {numVertex}')
    
    print(f'El total de arcos del digrafo es: {numArcos}\n')
    
    print(f'El total de componentes conectados es: {connectedComponents_Manadas} \n')
    
    print("Se muestran los primeros 3 y los ultimmos 3 manadas fuertemente conectadas del grafo\n")
    
    ltFinal_Recortada = controller.recortarListaThree(ltFinal)
    
    tabulateLindoReq7(ltFinal_Recortada,headers, headers2)  
    
    if mem == True:
        print("Tiempo [ms]: ", str(delta_time), "||",
              "Memoria [kB]: ",str(delta_memory))
    else:
        print("Tiempo [ms]: ", str(delta_time))
        
    print('Pasó todo, de todito :)\n')

def tabulateLindoReq7(lista, headers, headers2):
    matriz = []
    for registro in lt.iterator(lista):
        fila = []
        info = registro['elements']
        size = info[2]
        for data in info:
            if type(data) == dict and data['size'] == size:
                dataLindo = data['elements']
                if data['size'] >= 1:
                    first3 = dataLindo[:3]
                    last3 = dataLindo[-3:]
                    combined = first3 + ['...'] + last3
                    data = combined
                    
                elif type(data) == list:
                    data_super_lindo = dataLindo[0]['elements']
                    tabulateLindoReq7_2(data_super_lindo, headers2)
                else:
                    data = dataLindo
    
            else:
                if type(data) == dict:
                    dataLindo = data['elements']
                    data = tabulateLindoReq7_2(dataLindo, headers2)
                elif type(data) == list:
                    dataLindo = data[0]['elements']
                    data = tabulateLindoReq7_2(dataLindo, headers2)
            fila.append(data)
        matriz.append(fila)
        
    print(tabulate(matriz, headers, tablefmt="grid", maxcolwidths=[10, 15, 10, 10, 10, 10, 10, 10, 70], maxheadercolwidths=[10, 15, 10, 10, 10, 10, 10 ,10, 70]))
    
def tabulateLindoReq7_2(lista, headers2):
    matriz = []
    for listaLinda in lista:
        fila = []
        for registro in lt.iterator(listaLinda):
            
            fila.append(registro)
        matriz.append(fila)
    return tabulate(matriz, headers2, tablefmt="grid", maxcolwidths=[15, 15,15, 15], maxheadercolwidths=[15, 15, 15, 15])

def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass

#-------------------------------------------------#
# Funciones para hacer los inputs

def chooseFileSize():
    print("==================== Bienvenidos al Reto 4 ====================\n")
    print('1: Datos al 5%')
    print('2: Datos al 10%')
    print('3: Datos al 20%')
    print('4: Datos al 30%')
    print('5: Datos al 50%')
    print('6: Datos al 80%')
    print('7: Datos al 100%')
    print('8: Datos small\n')
    
    working = True 
    while working:
        inputs = input('Seleccione el porcentaje de datos que quiere utilizar: ')
        if int(inputs) == 1:   
            return int(inputs)
        elif int(inputs) == 2:
            return int(inputs)
        elif int(inputs) == 3:
            return int(inputs)
        elif int(inputs) == 4:
            return int(inputs)
        elif int(inputs) == 5:
            return int(inputs)
        elif int(inputs) == 6:
            return int(inputs)
        elif int(inputs) == 7:
            return int(inputs)
        elif int(inputs) == 8:
            return int(inputs)        
        else: 
            print('Presione un numero valido')

def chooseOrigenPoint():
    print('Escriba el punto de origen:')
    return input('Respuesta: ')

def chooseDestinyPoint():
    print('Escriba el punto de destino:')
    return input('Respuesta: ')

def chooseminTemp():
    print('Escriba la temperatura minima:')
    return input('Respuesta: ')

def choosemaxTemp():
    print('Escriba la temperatura maxima:')
    return input('Respuesta: ')

def chooseminDate():
    print('Escriba la fecha inicial del análisis:')
    return input('Respuesta: ')

def choosemaxDate():
    print('Escriba la fecha final del análisis:')
    return input('Respuesta: ')


# Funciones para imprimir los resultados de los requerimientos


def tabulateLindoCarga(lista, headers):
    matriz = []
    for registro in lt.iterator(lista):
        fila = []
        info = registro['elements']
        for data in info:
            fila.append(data)
        matriz.append(fila)
    print(tabulate(matriz, headers, tablefmt="grid",maxcolwidths=30, maxheadercolwidths=30))

def tabulateLindo(list, headers):
    matriz = []
    for registro in lt.iterator(list):
        fila = []
        for header in headers:
            fila.append(registro[header])
        matriz.append(fila)
    print(tabulate(matriz, headers, tablefmt="grid",maxcolwidths=18, maxheadercolwidths=18))
    
def tabulateLindo2(list, headers):
    matriz = []
    for registro in lt.iterator(list):
        fila = []
        for thing in lt.iterator(registro):
            fila.append(thing)
        matriz.append(fila)
    print(tabulate(matriz, headers, tablefmt="grid",maxcolwidths=20, maxheadercolwidths=20))


def printLoadDataAnswer(answer, mem):
    """
    Imprime los datos de tiempo y memoria de la carga de datos y los requerimientos
    """
    if mem == True:
        print("Tiempo [ms]: ", f"{answer[8]:.3f}", "||",
              "Memoria [kB]: ", f"{answer[9]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{answer[8]:.3f}")


def printReqAnswer(answer):
    
    '''
    f
    Imprime los datos de tiempo y memoria de los requerimientos 1 y 2
    
    '''
    if len(answer) == 3:
        print("Tiempo [ms]: ", f"{answer[1]:.3f}", "||",
              "Memoria [kB]: ", f"{answer[2]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{answer[1]:.3f}")

def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False
    
#-------------------------------------------------#

# Se crea el controlador asociado a la vista
control, filename, filename2 = new_controller()
print(filename, filename2)
# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)

    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        try:
            if int(inputs) == 1:
                print("Desea observar el uso de memoria? (True/False)")
                memflag = input("Respuesta: ")
                memflag = castBoolean(memflag)
                print("Cargando información de los archivos ....\n")
                data = load_data(control,filename, filename2,memflag)
                ds = data[0]
                track_nodes = data[1]
                meeting_edges = data[2]
                maxLat = data[3]
                minLat = data[4]
                maxLong = data[5]
                minLong = data[6]
                lt_carga = data[7]
                
                headers = ['location-long-aprox', 'location-lat-aprox', 'node-id', 'indvidual-id', 'adjacent nodes']
                
                print('------------------Información del seguimiento de lobos y puntos de encuentro-----------\n')
                print('------------------Información de lobos y eventos-----------\n')

                size_wolf = lt.size(ds["data_wolfs"])
                size_tracks = lt.size(ds['data_tracks'])
                print(f'Numero de lobos: {size_wolf}')
                print(f'Numero de lobos con datos: {size_wolf}')
                print(f'Numero de eventos de seguimiento: {size_tracks} \n')
                
                print(f'------------------Información de los nodos-----------\n')
                
                vertex_total = gr.numVertices(ds["connections"])
                meeting_nodes = vertex_total - track_nodes
                print(f'EL total de vertices de puntos de encuentro {meeting_nodes}')
                print(f'EL total de vertices de puntos de seguimiento {track_nodes}')
                print(f'EL total de vertices reconocidos del grafo {vertex_total}\n')
                
                print('------------------Información de los arcos-----------\n')
            
                edges_total = gr.numEdges(ds["connections"])
                tracking_edges = edges_total - meeting_edges
                
                print(f'El total de arcos creado entre puntos de seguimiento es: {meeting_edges}')
                print(f'El total de arcos creado entre puntos de seguimiento es: {tracking_edges}')
                print(f'El total de arcos creado entre puntos de encuentro es: {edges_total}\n')
                
                print('------------------Información del digrafo-----------\n')
                print(f'El total de vertices del digrafo es: {vertex_total}')
                print(f'El total de arcos del digrafo es: {edges_total}\n')
                
                print('------------------Area del grafo-----------\n')
                
                print(f'La latitud minima es: {minLat}')
                print(f'La latitud maxima es: {maxLat}')
                print(f'La longitud minima es: {minLong}')
                print(f'La longitud maxima es: {maxLong}\n')
                
                print('------------------Información de los nodos de seguimiento-----------\n')
                
                ltFinal = controller.recortarLista(lt_carga)
                
                print(f'Se muestran los primeros 5 y ultimos 5 nodos del grafo\n')
                
                tabulateLindoCarga(ltFinal,headers)
                
                
                
                printLoadDataAnswer(data, memflag)
            
                print('Pasó todo :)\n')       
                
                   
            elif int(inputs) == 2:
                print_req_1(control)

            elif int(inputs) == 3:
                print_req_2(control)

            elif int(inputs) == 4:
                print_req_3(control)

            elif int(inputs) == 5:
                print_req_4(control)

            elif int(inputs) == 6:
                print_req_5(control)

            elif int(inputs) == 7:
                print_req_6(control)

            elif int(inputs) == 8:
                print_req_7(control)

            elif int(inputs) == 9:
                print_req_8(control)

            elif int(inputs) == 0:
                working = False
                print("\nGracias por utilizar el programa")
                
            else:
                print("Opción errónea, vuelva a elegir.\n")
        except Exception as exp:
            print("ERR:", exp)
            traceback.print_exc()
    sys.exit(0)

