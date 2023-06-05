"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import time
import csv
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller(a):
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    
    filesize = ''
    filesize2 = ''
    
    if a == 1:
        filesize = 'wolfs\BA-Grey-Wolf-tracks-utf8-5pct.csv'
        filesize2 = 'wolfs\BA-Grey-Wolf-individuals-utf8-5pct.csv'
    elif a == 2:
        filesize = 'wolfs\BA-Grey-Wolf-tracks-utf8-10pct.csv'
        filesize2 = 'wolfs\BA-Grey-Wolf-individuals-utf8-10pct.csv'
    elif a == 3:
        filesize = 'wolfs\BA-Grey-Wolf-tracks-utf8-20pct.csv'
        filesize2 = 'wolfs\BA-Grey-Wolf-individuals-utf8-20pct.csv'
    elif a == 4:
        filesize = 'wolfs\BA-Grey-Wolf-tracks-utf8-30pct.csv'
        filesize2 = 'wolfs\BA-Grey-Wolf-individuals-utf8-30pct.csv'
    elif a == 5:
        filesize = 'wolfs\BA-Grey-Wolf-tracks-utf8-50pct.csv'
        filesize2 = 'wolfs\BA-Grey-Wolf-individuals-utf8-50pct.csv'
    elif a == 6:
        filesize = 'wolfs\BA-Grey-Wolf-tracks-utf8-80pct.csv'
        filesize2 = 'wolfs\BA-Grey-Wolf-individuals-utf8-80pct.csv'
    elif a == 7:
        filesize = 'wolfs\BA-Grey-Wolf-tracks-utf8-large.csv'
        filesize2 = 'wolfs\BA-Grey-Wolf-individuals-utf8-large.csv'
    elif a == 8:
        filesize = 'wolfs\BA-Grey-Wolf-tracks-utf8-small.csv'
        filesize2 = 'wolfs\BA-Grey-Wolf-individuals-utf8-small.csv'
    
    
    control = {
        'model': None
    }

    control['model'] = model.new_data_structs()
    
    return control, filesize, filesize2

# Funciones para la carga de datos
def loadDatos(control, filename, filename2):
    data_structs = control['model'] 
    id = 0
    tagsfile = cf.data_dir + filename
    tagsfile2 = cf.data_dir + filename2
    print("----ARCHIVO CARGADO------\n")
    print(tagsfile)

    input_file = csv.DictReader(open(tagsfile, encoding="utf-8"))
    input_file2 = csv.DictReader(open(tagsfile2, encoding="utf-8"))
    
    #Creacion de listas con la informacion de ambos archivos
    
    for track in input_file:
        model.add_data_tracks(data_structs, track)
        id += 1
    id_2 = 0
    for wolf in input_file2:
        model.add_data_wolfs(data_structs, wolf)
        id_2 += 1
    
    #---------------------------------------------------------
    
    maxLat, minLat, maxLon, minLon = model.getArea(data_structs)
    
    
    #---------------------------------------------------------
    #Creacion del mapa lobo-tracks  
    
    model.addMAPIdTrack(data_structs)
    
    #---------------------------------------------------------
    #Creacion de los nodos del grafo
    
    #Nodos de punto de seguimiento
    
    data_structs, track_nodes =model.addTrackNode(data_structs)    

    
    #Nodos de puntos de encuentro
    
    model.addMeetingNode(data_structs)
    #---------------------------------------------------------
    
    #---------------------------------------------------------
    
    #Creacion de arcos
    
    model.connectWolfPoints(data_structs)

    
    #Union de Meeting points
    
    data_structs = model.connectMeetingPoints(data_structs)
    meeting_edges = model.countMeeting_edges(data_structs)
    
    #Union de track points
    
    
    lt_carga = model.getGraphInformation(data_structs)

    
    #---------------------------------------------------------
    #Fin de la carga de datos  
    
    
    return data_structs, track_nodes, meeting_edges, maxLat, minLat, maxLon, minLon, lt_carga 

    
def load_data(control, filename,filename2, memflag):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    # toma el tiempo al inicio del proceso
    start_time = getTime()
    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    data_structs, track_nodes, meeting_edges, maxLat, minLat, maxLon, minLon, lt_carga = loadDatos(control, filename, filename2)
     # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)    
    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return data_structs, track_nodes,meeting_edges,  maxLat, minLat, maxLon, minLon, lt_carga,delta_time, delta_memory
    else:
        # respuesta sin medir memoria
        return data_structs, track_nodes,meeting_edges, maxLat, minLat, maxLon, minLon ,lt_carga,delta_time

#Esta funcion es la que permite recortar las listas de forma linda
def recortarLista(list):
    return model.recortarLista(list)

def recortarListaThree(list):
    return model.recortarLista2(list)

def firstFive(list):
    return model.firstFive(list)


# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control, memflag, origen, destino):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    start_time = getTime()
    ds = control["model"]

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    req1,flag, nWolf, nMeet, disttot = model.req_1(ds, origen, destino)
     # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)    
    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return req1, delta_time, delta_memory, flag, nWolf, nMeet, disttot

    else:
        # respuesta sin medir memoria
        return req1, delta_time, flag, nWolf, nMeet, disttot


def req_2(control,memflag, origen, destino):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    start_time = getTime()
    ds = control["model"]

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    req1,flag, nWolf, nMeet, disttot = model.req_2(ds, origen, destino)
     # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)    
    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return req1, delta_time, delta_memory, flag, nWolf, nMeet, disttot

    else:
        # respuesta sin medir memoria
        return req1, delta_time, flag, nWolf, nMeet, disttot


def req_3(control, memflag):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    start_time = getTime()
    ds = control["model"]

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    ltFinal, componentes, kosarajuMap,ltComponentes = model.req_3(ds)
     # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)    
    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return ltFinal, componentes, kosarajuMap,ltComponentes,delta_time, delta_memory
    else:
        return ltFinal, componentes,kosarajuMap,ltComponentes,delta_time


def req_4(control, memflag, origen, destino):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    start_time = getTime()
    ds = control["model"]

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    NodoMascercano_O, tablaOrigen, distMin1, NodoMascercano_D, tabladestino, distMin2,r2, nWolf, nMeet, disttot, r4 = model.req_4(ds, origen, destino)
     # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)    
    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return NodoMascercano_O, delta_time, delta_memory, tablaOrigen, distMin1, NodoMascercano_D, tabladestino, distMin2,r2, nWolf, nMeet, disttot, r4

    else:
        # respuesta sin medir memoria
        return NodoMascercano_O, delta_time, tablaOrigen, distMin1, NodoMascercano_D, tabladestino, distMin2,r2, nWolf, nMeet, disttot, r4


def req_5(control,memflag,origen,distancia,minMP):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    
    start_time = getTime()
    ds = control["model"]

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    nodos, dist = model.req_5(ds, origen, distancia, minMP)
     # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)    
    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return nodos, dist, delta_time, delta_memory

    else:
        # respuesta sin medir memoria
        return nodos,dist, delta_time

def req_6(control, memflag, FechaI, FechaF, Sex):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    start_time = getTime()
    ds = control["model"]

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    wolfmax, wolfmix, wolfmxInfo, wolfminInfo, nodesRMAX, nodesRMIN, wolfMAXRute ,wolfMINRute = model.req_6(ds, FechaI, FechaF, Sex)
     # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)    
    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return wolfmax, delta_time, delta_memory, wolfmix, wolfmxInfo, wolfminInfo, nodesRMAX, nodesRMIN, wolfMAXRute ,wolfMINRute
    else:
        # respuesta sin medir memoria
        return wolfmax, delta_time, wolfmix, wolfmxInfo, wolfminInfo, nodesRMAX, nodesRMIN, wolfMAXRute ,wolfMINRute


def req_7(control, memflag, dateStart, dateEnd, minTemp, maxTemp):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    start_time = getTime()
    ds = control["model"]

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    numVertex, numArcos, connectedComponents_Manadas, ltFinal = model.req_7(ds, dateStart, dateEnd, minTemp, maxTemp)
     # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)    
    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return numVertex, numArcos, connectedComponents_Manadas, ltFinal ,delta_time, delta_memory
    else:
        return numVertex, numArcos, connectedComponents_Manadas, ltFinal ,delta_time


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed


# Funciones para medir la memoria utilizada


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory

