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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import datetime
import math
import numpy as np
from tabulate import tabulate
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import dfo
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
from math import radians, cos, sin, asin, sqrt
assert cf
import folium

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs(data_type):
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    data_structs = {
            "encuentro": None,
            'lista_encuentros': None,
            'lista_seguimientos': None,
            'wolfs': None,
            'timestamp': None,
            "grafoDirigido": None,
            'latitudes': None,
            'longitudes': None,
            'temperaturas': None}
            

    
    data_structs['wolfs'] = mp.newMap(numelements = 1000, 
                            maptype = "PROBING",
                            loadfactor = 4)
    
    data_structs['lista_encuentros'] = lt.newList(datastructure = "ARRAY_LIST")

    data_structs['lista_seguimientos'] = lt.newList(datastructure = "ARRAY_LIST")

    data_structs["encuentro"] = mp.newMap(numelements = 25000,
                            maptype= data_type,
                            loadfactor = 4)

    data_structs["grafoDirigido"] = gr.newGraph(datastructure = "ADJ_LIST", 
                                                directed = True,
                                                size = 50)
    
    
    data_structs['latitudes'] = lt.newList(datastructure = "ARRAY_LIST")
    
    data_structs['longitudes'] = lt.newList(datastructure = "ARRAY_LIST")
    
    data_structs["temp"] = {}
    
    return data_structs

def new_graph_info(structs: dict):
    structs["encuentro"] = mp.newMap(numelements = 25000,
                            maptype = "CHAINING",
                            loadfactor = 4)
    structs['seguimiento'] = mp.newMap(numelements = 50,
                                              maptype = "PROBING",
                                              loadfactor = 0.7)
    structs['temp_graph'] = gr.newGraph(datastructure = "ADJ_LIST", 
                                                directed = True,
                                                size = 50)
    structs['lista_seguimientos'] = lt.newList(datastructure = "ARRAY_LIST")
    structs['lista_encuentros'] = lt.newList(datastructure = "ARRAY_LIST")
    return structs

def create_sub_graph(oldgraph, newgraph, vertexs):
    for vertex in lt.iterator(vertexs):
        if not gr.containsVertex(newgraph, vertex):
            gr.insertVertex(newgraph, vertex)
    for vertex in lt.iterator(vertexs):
        adjecentE = gr.adjacentEdges(oldgraph, vertex)
        for edge in lt.iterator(adjecentE):
            contrainsA = gr.containsVertex(newgraph, edge["vertexA"])
            contrainsB = gr.containsVertex(newgraph, edge["vertexB"])
            notcontrainsE = (gr.getEdge(newgraph, edge["vertexA"], edge["vertexB"]) == None)
            if contrainsA and contrainsB and notcontrainsE:
                gr.addEdge(newgraph, edge["vertexA"], edge["vertexB"], edge["weight"])
    return newgraph

def add_wolfs_tracks(data_structs,data):

    id_unico = data["individual-local-identifier"] + "_" + data["tag-local-identifier"]
    data["id"] = id_unico
    
    longitud = float(data["location-long"]) 
    latitud = float(data["location-lat"]) 

    longitud = round(longitud, 3)
    latitud = round(latitud, 3)

    lt.addLast(data_structs['latitudes'], latitud)
    lt.addLast(data_structs['longitudes'], longitud)

    longitud = str(longitud).replace("-", "m")
    latitud = str(latitud).replace("-", "m")
    longitud = longitud.replace(".", "p")
    latitud = latitud.replace(".", "p")

    direccion = longitud + "_" + latitud
    data["track_id"] = direccion + "_" + id_unico
    punto_seguimiento = data["track_id"]
    
    contains_wolfs = mp.contains(data_structs["wolfs"], id_unico)
    
    if contains_wolfs == True:
        entry = mp.get(data_structs["wolfs"], id_unico)
        wolfs_info = me.getValue(entry)
        add_timestamp(wolfs_info,data)

    if contains_wolfs == False:

        wolfs_info = {'info': None, 'tracks': None}
        wolfs_info['info'] = lt.newList(datastructure = "ARRAY_LIST")
        wolfs_info['timestamp'] = om.newMap(omaptype = "RBT", cmpfunction=compareDates)
        add_timestamp(wolfs_info,data)
        mp.put(data_structs["wolfs"],id_unico, wolfs_info)

    contains_encuentro = mp.get(data_structs["encuentro"], direccion)

    if contains_encuentro == None:
        lista_seguimiento = lt.newList(datastructure = "ARRAY_LIST", cmpfunction=compareTracks)
        lt.addLast(lista_seguimiento, punto_seguimiento)
        mp.put(data_structs["encuentro"], direccion, lista_seguimiento)

    else:
        entry_encuentro = mp.get(data_structs["encuentro"], direccion)
        lista_seguimiento = me.getValue(entry_encuentro)
        if not lt.isPresent(lista_seguimiento, punto_seguimiento):
            lt.addLast(lista_seguimiento, punto_seguimiento)


    
        
def add_wolfs_info(data_structs,data):

    id_unico = data["animal-id"] + "_" + data["tag-id"]
    data["id-individual"] = id_unico
    
    contains = mp.contains(data_structs["wolfs"], id_unico)

    if contains == True:
        entry = mp.get(data_structs["wolfs"], id_unico)
        wolf_info = me.getValue(entry)
        lt.addLast(wolf_info['info'], data)
       
    else:
        wolf_info = {'info': None, 'timestamp': None}
        wolf_info['info'] = lt.newList(datastructure = "ARRAY_LIST")
        lt.addLast(wolf_info['info'], data)
        mp.put(data_structs["wolfs"], id_unico, wolf_info)



def add_timestamp(data_structs,data):

    map = data_structs["timestamp"]
    wolf = {
        "punto_seguimiento": data["track_id"],
        "punto": (round(float(data["location-lat"]), 3), round(float(data["location-long"]), 3)),
        "temperature": data["external-temperature"],
        "id": data["id"]
    }
    occdate = data["timestamp"]

    wolfdate = datetime.datetime.strptime(occdate, '%Y-%m-%d %H:%M')
    date = wolfdate.date()
    time = wolfdate.time()
    entry = om.get(map, wolfdate.combine(date,time))
    
    if entry is None:
        lista_puntos_seguimiento = lt.newList(datastructure = "ARRAY_LIST", cmpfunction=compareTracks)
        lt.addLast(lista_puntos_seguimiento, wolf)
        om.put(map, wolfdate.combine(date,time), lista_puntos_seguimiento)
    else:
        lista_puntos_seguimiento = me.getValue(entry)
        lt.addLast(lista_puntos_seguimiento, wolf)
    
def crearGrafoEncuentro(data_structs):

    dirigido = data_structs['grafoDirigido']

    contador = 0


    for punto_encuentro in lt.iterator(mp.keySet(data_structs["encuentro"])):
        entry = mp.get(data_structs["encuentro"], punto_encuentro)
        lista_grande = me.getValue(entry)

        if lt.size(lista_grande) >= 2:

            lt.addLast(data_structs['lista_encuentros'], punto_encuentro)

            if not gr.containsVertex(dirigido, punto_encuentro):
                gr.insertVertex(dirigido, punto_encuentro)

        for punto_seguimiento in lt.iterator(lista_grande):

            lt.addLast(data_structs['lista_seguimientos'], punto_seguimiento)
            
            if not gr.containsVertex(dirigido, punto_seguimiento):
                gr.insertVertex(dirigido, punto_seguimiento)
        
            if gr.containsVertex(dirigido, punto_encuentro):
                edge1 = gr.getEdge(dirigido, punto_encuentro, punto_seguimiento)
                if edge1 is None:
                    gr.addEdge(dirigido, punto_encuentro, punto_seguimiento, 0)
                    contador += 1
                edge2 = gr.getEdge(dirigido, punto_seguimiento, punto_encuentro)
                if edge2 is None:
                    gr.addEdge(dirigido, punto_seguimiento, punto_encuentro, 0)
                    contador += 1

    return contador

            

def crearGrafoSeguimiento(data_structs):

    wolfs = data_structs["wolfs"]
    wolf_id = mp.keySet(wolfs)

    contador = 0


    for wolf_id in lt.iterator(mp.keySet(wolfs)):
        entry = mp.get(wolfs, wolf_id)
        wolfs_info = me.getValue(entry)
        mapa = wolfs_info['timestamp']

        fechas = om.keySet(mapa)

        current = None

        for fecha in lt.iterator(fechas):
           
            puntos = om.get(mapa, fecha)
            lista_puntos = me.getValue(puntos)
            lista_puntos = lt.getElement(lista_puntos, 0)

            if current == None:
                current = lista_puntos
          
            else:
                if current['punto_seguimiento'] != lista_puntos['punto_seguimiento']:
                    d = CalculateDistance(current['punto'], lista_puntos['punto'])
                    gr.addEdge(data_structs["grafoDirigido"], current['punto_seguimiento'], lista_puntos['punto_seguimiento'], d)
                    current = lista_puntos
                    contador += 1
    return contador

def wolfs_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    wolfs = data_structs["wolfs"]
    total_wolfs = mp.size(wolfs)
    total_wolfs_tracks = 0
    total_wolfs_info = 0

    for wolf in lt.iterator(mp.keySet(wolfs)):
        entry = mp.get(wolfs, wolf)
        wolfs_info = me.getValue(entry)

        if wolfs_info['timestamp'] is not None and wolfs_info['info'] is not None:
            total_wolfs_tracks +=1
        
        if wolfs_info['timestamp'] is not None:
            total_wolfs_info += lt.size(om.valueSet(wolfs_info['timestamp']))


    return total_wolfs, total_wolfs_tracks, total_wolfs_info

def wolfs_data_size(data_structs):
    
    wolfs = data_structs["wolfs"]
    size = 0

    for wolf in lt.iterator(mp.keySet(wolfs)):
        entry = mp.get(wolfs, wolf)
        lista_grande = me.getValue(entry)
        i = 1
        for list in lt.iterator(lista_grande):
            if i ==1 and lt.isEmpty(list) == False:
                size += lt.size(list)
                i += 1

    return size

def organizarL(data_structs):
    latitudes = data_structs['latitudes']
    longitudes = data_structs['longitudes']
    merg.sort(latitudes, compareLatitudes)
    merg.sort(longitudes, compareLongitudes)
    return latitudes, longitudes


def req_1(data_structs, initial, destination, modo):
    """
    Función que soluciona el requerimiento 1
    """
    grafo = data_structs["grafoDirigido"]
    containsInitial = gr.containsVertex(grafo, initial)
    containsDestination = gr.containsVertex(grafo, destination)
    if containsInitial and containsDestination:
        if modo == "DFS":
            search = dfs.DepthFirstSearch(grafo, initial)
            haspath = dfs.hasPathTo(search, destination)
            if haspath:
                ipath = dfs.pathTo(search, destination)
                path = invertList(ipath)
                nG = getGatheringPoints(data_structs, path)
                nT = getTrackingPoints(data_structs, path)
                w = getWeight(grafo, path)
                return path, nG, nT, w
            else:
                return None
        elif modo == "BFS":
            search = bfs.BreadhtFisrtSearch(grafo, initial)
            haspath = bfs.hasPathTo(search, destination)
            if haspath:
                ipath = bfs.pathTo(search, destination)
                path = invertList(ipath)
                nG = getGatheringPoints(data_structs, path)
                nT = getTrackingPoints(data_structs, path)
                w = getWeight(grafo, path)
                return path, nG, nT, w
            else:
                return None
    else:
        return None


def req_2(data_structs, initial, destination):
    """
    Función que soluciona el requerimiento 2
    """
    grafo = data_structs["grafoDirigido"]
    containsInitial = gr.containsVertex(grafo, initial)
    containsDestination = gr.containsVertex(grafo, destination)
    if containsInitial and containsDestination:
        search = bfs.BreadhtFisrtSearch(grafo, initial)
        haspath = bfs.hasPathTo(search, destination)
        if haspath:
            ipath = bfs.pathTo(search, destination)
            path = invertList(ipath)
            nG = getGatheringPoints(data_structs, path)
            nT = getTrackingPoints(data_structs, path)
            w = getWeight(grafo, path)
            return path, nG, nT, w
        else:
            return None
    else:
        return None

def getGatheringPoints(control, path: lt):
    num = 0
    for point in lt.iterator(path):
        if lt.isPresent(control['lista_encuentros'], point):
            num = num + 1
    return num

def getTrackingPoints(control, path: lt):
    num = 0
    for point in lt.iterator(path):
        if lt.isPresent(control['lista_seguimientos'], point):
            num = num + 1
    return num

def getWeight(graph, path: lt):
    weight = 0
    previous = None
    for current in lt.iterator(path):
        if previous != None:
            weight = gr.getEdge(graph, previous, current)["weight"] + weight
        previous = current
    return weight

def invertList(path):
    inverted = lt.newList(datastructure="SINGLE_LINKED")
    size = lt.size(path)
    for node in range(size):
        lt.addLast(inverted, lt.removeLast(path))
    return inverted

def generateListPath(path, control, remove):
    lista = []
    for node in lt.iterator(path):
        pos = node.split("_")
        if 'm' in pos[0]:
            lon = pos[0].replace("m", "-")
        if 'p' in lon:
            lon = lon.replace("p", ".")
        if 'p' in pos[1]:
            lat = pos[1].replace("p", ".")
        if 'm' in lat:
            lat = lat.replace("m", "-")
        if lt.isPresent(control['lista_encuentros'], node):
            individuals = []
            for individual in lt.iterator(me.getValue(mp.get(control["encuentro"], node))):
                individuals.append(individual)
            members = ", ".join(individuals)
            num = len(individuals)
        else:
            members = node
            num = 1
        nextpos = lt.isPresent(path, node) + 1
        if nextpos > lt.size(path):
            next = "Unknown"
            weight = "Unkmown"
        else:
            next = lt.getElement(path, nextpos)
            weight = gr.getEdge(control["grafoDirigido"], node, next)["weight"]
        element = [lon, lat, node, members, num, next, weight]
        lista.append(element)
    if remove:
        lista.pop()
    return lista

def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass


def req_4(data_structs, origen_lon, origen_lat, dest_lon, dest_lat):
    """
    Función que soluciona el requerimiento 4
    """
    distance1 = 1000000
    distance2 = 1000000

    for punto_encuentro in lt.iterator(mp.keySet(data_structs["encuentro"])):
    
        if gr.containsVertex(data_structs["grafoDirigido"], punto_encuentro):
            punto_lon, punto_lat = noFormat(punto_encuentro)
            distance_origen = haversine(float(origen_lon), float(origen_lat), float(punto_lon), float(punto_lat))
            distance_destino = haversine(float(punto_lon), float(punto_lat), float(dest_lon), float(dest_lat))
            
            if distance_origen <= distance1:
                punto_cercano_origen = punto_encuentro
                distance1 = distance_origen
            if distance_destino <= distance2:
                punto_cercano_destino = punto_encuentro
                distance2 = distance_destino
                

    grafo_camino = djk.Dijkstra(data_structs["grafoDirigido"], punto_cercano_origen)
    hasPath = djk.hasPathTo(grafo_camino, punto_cercano_destino)

    if hasPath == True:
        distTo = djk.distTo(grafo_camino, punto_cercano_destino)
        path = djk.pathTo(grafo_camino, punto_cercano_destino)
        trips_edges = lt.size(path)
        nodes = trips_edges + 1
        lista_puntos = lt.newList(datastructure = "ARRAY_LIST")
        
        for punto in lt.iterator(path):
            lt.addFirst(lista_puntos, punto)
        
        first_3 = lt.subList(lista_puntos, 1, 3)
        last_3 = lt.subList(lista_puntos, lt.size(lista_puntos)-2, 3)

        return punto_cercano_origen, punto_cercano_destino, round(distance1,3), round(distance2,3),trips_edges, nodes, distTo, first_3, last_3
    
    else:
        return punto_cercano_origen, punto_cercano_destino, round(distance1,3), round(distance2,3),  None, None, None, None, None
    
    

def req_5(data_structs, minGathering, maxdistance, origin):
    """
    Función que soluciona el requerimiento 5
    """
    routes = {}
    acumulated = 0
    useList = []
    checked = []
    paths = getPaths(data_structs, origin, routes, maxdistance, acumulated, minGathering, useList, checked)
    return paths

def getPaths(control, origin, dic, maxdis, ac, ming, uL, checked):
    search = djk.Dijkstra(control["grafoDirigido"], origin)
    uL.append(origin)
    checked = [] + uL
    for gathering_point in lt.iterator(control["lista_encuentros"]):
        checked.append(gathering_point)
        if gathering_point not in uL:
            dis = djk.distTo(search, gathering_point)
            if (ac + dis) < maxdis:
                ac = ac + dis
                uL.append(gathering_point)
                getPaths(control, gathering_point, dic, maxdis, ac, ming, uL, checked)
        entries = len(checked)
        if entries == lt.size(control["lista_encuentros"]):
            if len(uL) >= int(ming):
                path = []
                visible = []
                current = uL[0]
                for u in uL:
                    if current != u:
                        current = u
                    else:
                        s = djk.Dijkstra(control["GrafoDirigido"], current)
                        part = djk.pathTo(s, u)
                        for node in lt.iterator(part):
                            if node not in control["lista_encuentros"]:
                                visible.append(1)
                            else:
                                visible.append(lt.size(me.getValue(mp.get(control["encuentro"], node))))
                        path.append(part)
                        current = u
                dic[uL] = {"path": path,
                           "weight": ac,
                           "animals": visible}
            return dic

def req_6(data_structs, fecha_inicial, fecha_final, sex):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    wolfs_ids = data_structs["wolfs"]

    distancia_menor = 1000000
    distancia_mayor = 0
    contador = 0

    for id in lt.iterator(mp.keySet(wolfs_ids)):
        distance_puntos = 0
        entry = mp.get(wolfs_ids, id)
        wolfs_info = me.getValue(entry)

        info = wolfs_info['info']['elements'][0]

        if info['animal-sex'] == sex:
            
            mapa_fechas = wolfs_info['timestamp']
            datos_fechas = om.values(mapa_fechas, fecha_inicial, fecha_final)
            vertices = lt.newList(datastructure = "ARRAY_LIST")
            if lt.isEmpty(datos_fechas) == False:
                contador += 1
                new_graph = gr.newGraph(datastructure = "ADJ_LIST", directed = True, size = 50)
                for element in lt.iterator(datos_fechas):
                    punto_seguimiento = element['elements'][0]
                    gr.insertVertex(new_graph, punto_seguimiento['punto_seguimiento'])
                    lt.addLast(vertices, punto_seguimiento['punto_seguimiento'])
                   
                    if lt.size(vertices) > 1:
                        first_element = lt.getElement(vertices, lt.size(vertices)-1)
                        gr.addEdge(new_graph, first_element, punto_seguimiento['punto_seguimiento'], 0)
                        lon1,lat1 = noFormat(first_element)
                        lon2,lat2 = noFormat(punto_seguimiento['punto_seguimiento'])
                        distance_puntos += haversine(float(lon1), float(lat1), float(lon2), float(lat2))

                if distance_puntos <= distancia_menor:
                    distancia_menor = distance_puntos
                    id_menor = id
                    graph_menor = new_graph
                    vertices_menor = vertices
                    
                if distance_puntos >= distancia_mayor:
                    distancia_mayor = distance_puntos
                    id_mayor = id
                    graph_mayor = new_graph
                    vertices_mayor = vertices

    
    arcos_mayor = lt.size(gr.edges(graph_mayor))
    nodos_mayor = arcos_mayor + 1
    if lt.size(vertices_mayor) > 6:
        first_3_mayor = lt.subList(vertices_mayor, 1, 3)
        last_3_mayor = lt.subList(vertices_mayor, lt.size(vertices_mayor)-2, 3)
    else:
        first_3_mayor = vertices_mayor
        last_3_mayor = None

    arcos_menor = lt.size(gr.edges(graph_menor))
    nodos_menor = arcos_menor + 1
    
    
    if lt.size(vertices_menor) > 6:
        first_3_menor = lt.subList(vertices_menor, 1, 3)
        last_3_menor = lt.subList(vertices_menor, lt.size(vertices_menor)-2, 3)
    else:
        first_3_menor = vertices_menor
        last_3_menor = None

    total_distance_menor = 0

    entry_idmenor = mp.get(wolfs_ids, id_menor)
    menorwolf_info = me.getValue(entry_idmenor)
    map_menorwolf_info = menorwolf_info['timestamp']
    puntos_menor = om.valueSet(map_menorwolf_info)
    i = 0
    current = None
    
    for punto in lt.iterator(puntos_menor):
        current = punto['elements'][0]['punto']
        if i> 0:
        
            total_distance_menor  += CalculateDistance(current, menor_anterior)
        
        menor_anterior = current
        i += 1


    total_distance_mayor = 0
    entry_idmayor = mp.get(wolfs_ids, id_mayor)
    mayorwolf_info = me.getValue(entry_idmayor)
    map_mayorwolf_info = mayorwolf_info['timestamp']
    puntos1 = om.valueSet(map_mayorwolf_info)
    i = 0
    for punto in lt.iterator(puntos1):
        punto = punto['elements'][0]['punto']
        if i > 0:
            if punto_anterior != punto:
                distancia = CalculateDistance(punto_anterior, punto)
                total_distance_mayor += distancia

        punto_anterior = punto
        i += 1


    return id_menor, distancia_menor, nodos_menor, arcos_menor, first_3_menor, last_3_menor, id_mayor, distancia_mayor, nodos_mayor, arcos_mayor, first_3_mayor, last_3_mayor, contador, total_distance_menor, total_distance_mayor



def noFormatPuntoSeguimiento(str):
    punto = str.split("_")
    if len(punto) > 2:
        for i in range(2, len(punto)):
            if i == 2:
                wolf_id = punto[2]
            else:
                wolf_id+= "_" + punto[i]

    else:
        wolf_id = None
    
    return wolf_id


def req_7(data_structs, lowtime, hightime, lowtemp, hightemp):
    """
    Función que soluciona el requerimiento 7
    """
    new_graph_info(data_structs["temp"])
    graphInfo = data_structs["temp"]
    wolfs = data_structs["wolfs"]
    lowsuf = datetime.datetime.strptime("00:00", '%H:%M').time()
    highsuf = datetime.datetime.strptime("23:59", '%H:%M').time()
    lowtime = datetime.datetime.strptime(lowtime, '%Y-%m-%d')
    lowdate = lowtime.date()
    lowtime = lowtime.combine(lowdate, lowsuf)
    hightime = datetime.datetime.strptime(hightime, '%Y-%m-%d')
    highdate = hightime.date()
    hightime = hightime.combine(highdate, highsuf)
    
    ################### GET THE USABLE VALUES IN THE TIME AND TEMPERATURE ###################
    for wolf_id in lt.iterator(mp.keySet(wolfs)):
        entry = mp.get(wolfs, wolf_id)
        wolfs_info = me.getValue(entry)
        times = om.values(wolfs_info['timestamp'], lowtime, hightime)
        for time in lt.iterator(times):
            for info in lt.iterator(time):
                temp = float(info["temperature"])
                if (temp >= float(lowtemp)) and (temp <= float(hightemp)):
                    tracking = {"point": info["punto"],
                                "tracking": info["punto_seguimiento"],
                                "id" : info["id"]}
                    exists = mp.contains(graphInfo['seguimiento'], info["id"])
                    if exists:
                        value = mp.get(graphInfo['seguimiento'], info["id"])
                        track = me.getValue(value)
                        lt.addLast(track, tracking)
                    else:
                        lista = lt.newList(datastructure = "SINGLE_LINKED")
                        lt.addLast(lista, tracking)
                        mp.put(graphInfo['seguimiento'], info["id"], lista)
                    lt.addLast(graphInfo['lista_seguimientos'], info["punto_seguimiento"])
                    punto = info["punto"]
                    lon = punto[1]
                    lat = punto[0]
                    lon = str(lon).replace("-", "m")
                    lat = str(lat).replace("-", "m")
                    lon = lon.replace(".", "p")
                    lat = lat.replace(".", "p")
                    encuentro = lon + "_" + lat
                    contains = mp.contains(graphInfo["encuentro"], encuentro)
                    if contains:
                        entry_encuentro = mp.get(graphInfo["encuentro"], encuentro)
                        lista_seguimiento = me.getValue(entry_encuentro)
                        if not lt.isPresent(lista_seguimiento, info["punto_seguimiento"]):
                            lt.addLast(lista_seguimiento, info["punto_seguimiento"])
                    else:
                        seguimientos=lt.newList(datastructure="ARRAY_LIST", cmpfunction=compareTracks)
                        lt.addLast(seguimientos, info["punto_seguimiento"])
                        mp.put(graphInfo["encuentro"], encuentro, seguimientos)
                  
    ################### INSERT THE GATHERING POINTS TO THE GRAPH ###################
    for gathering_point in lt.iterator(mp.keySet(graphInfo["encuentro"])):
        entry = mp.get(graphInfo["encuentro"], gathering_point)
        values = me.getValue(entry)
        if lt.size(values) >= 2:
            if not gr.containsVertex(graphInfo['temp_graph'], gathering_point):
                gr.insertVertex(graphInfo['temp_graph'], gathering_point)
                lt.addLast(graphInfo["lista_encuentros"], gathering_point)
        for tracking_point in lt.iterator(values):
            if not gr.containsVertex(graphInfo['temp_graph'], tracking_point):
                gr.insertVertex(graphInfo['temp_graph'], tracking_point)
            if gr.containsVertex(graphInfo['temp_graph'], gathering_point):
                edge1 = gr.getEdge(graphInfo['temp_graph'], gathering_point, tracking_point)
                if edge1 is None:
                    gr.addEdge(graphInfo['temp_graph'], gathering_point, tracking_point, 0)
                edge2 = gr.getEdge(graphInfo['temp_graph'], tracking_point, gathering_point)
                if edge2 is None:
                    gr.addEdge(graphInfo['temp_graph'], tracking_point, gathering_point, 0)
    
    ################### INSERT THE TRACKING POINTS EDGES TO THE NEW GRAPH ###################
    for wolf in lt.iterator(mp.keySet(graphInfo["seguimiento"])):
        current = None
        for seguimiento in lt.iterator(me.getValue(mp.get(graphInfo["seguimiento"], wolf))):
            if current == None:
                current = seguimiento
            else:
                if current["tracking"] != seguimiento["tracking"]:
                    d = CalculateDistance(current['point'], seguimiento['point'])
                    gr.addEdge(graphInfo["temp_graph"], current['tracking'], seguimiento['tracking'], d)
                current = seguimiento
    
    ################### CALCULATE SCC REQUIREMENT ###################
    kosaraju = scc.KosarajuSCC(graphInfo["temp_graph"])
    stcoco = kosaraju["idscc"]
        
    ################### GET INFO FOR ANSWER ###################
    sccelements = mp.newMap(numelements=1000, maptype="PROBING", loadfactor=0.5)
    organizer = lt.newList(datastructure="SINGLE_LINKED")
    longest = lt.newList(datastructure="SINGLE_LINKED")
    for point in lt.iterator(mp.keySet(stcoco)):
        e = mp.get(stcoco, point)
        sccid = me.getValue(e)
        inorder = mp.contains(sccelements, sccid)
        if inorder:
            scclist = me.getValue(mp.get(sccelements, sccid))
            lt.addLast(scclist, point)
        else:  
            scclist = lt.newList(datastructure="SINGLE_LINKED")
            lt.addLast(scclist, point)
            mp.put(sccelements, sccid, scclist)


    for element in lt.iterator(mp.keySet(sccelements)):
        l = me.getValue(mp.get(sccelements, element))
        newgraph = gr.newGraph(datastructure="ADJ_LIST", directed=True)
        minmax = getMinMax(l)
        i = {"sccid": element,
             "list": l,
             "len": lt.size(l),
             "latInfo": minmax[1],
             "lonInfo": minmax[0],
             "gatNum": getGatheringPoints(graphInfo, l),
             "subgraph": create_sub_graph(graphInfo["temp_graph"], newgraph, l)}
        lt.addLast(organizer, i)

    for component in lt.iterator(organizer):
        long = dfo.DepthFirstOrder(component["subgraph"])
        path = stackToList(long['post'])
        longpath, weight = getLongestPath(component["subgraph"], path)
        minmax = getMinMax(longpath)
        j = {"SCCid": component["sccid"],
             "size": component["len"],
             "path": longpath,
             "len": lt.size(longpath),
             "latInfo": minmax[1],
             "lonInfo": minmax[0],
             "node": lt.size(longpath),
             "edges": lt.size(longpath) - 1,
             "weight": weight}
        lt.addLast(longest, j)
    merg.sort(organizer, compareNum)
    merg.sort(longest, compareWeight)
    return kosaraju, organizer, longest


def stackToList(stack):
    lista = lt.newList(datastructure="SINGLE_LINKED")
    while not st.isEmpty(stack):
        lt.addLast(lista, st.pop(stack))
    return lista

def getLongestPath(graph, path):
    if lt.size(path) > 3:
        o = 0
    longest = lt.newList(datastructure="SINGLE_LINKED")
    max = {"dist": 0,
           "v": lt.firstElement(path)}
    vertexs = {}
    marked = []
    starter = {"dist": 0,
               "vertex": lt.firstElement(path),
               "from": None}
    vertexs[starter["vertex"]] = starter
    for vertex in lt.iterator(path):
        if vertex != lt.firstElement(path):
            info = {"dist": - math.inf,
                    "vertex": vertex,
                    "from": None}
            vertexs[info["vertex"]] = info
    for vertex in vertexs:
        marked.append(vertex)
        adjacent = gr.adjacents(graph, vertex)
        for adj in lt.iterator(adjacent):
            if adj not in marked:
                sum = vertexs[vertex]["dist"] + gr.getEdge(graph, vertex, adj)["weight"]
                if (vertexs[adj]["dist"] < sum):
                    vertexs[adj]["dist"] = sum
                    vertexs[adj]["from"] = vertex 
        if vertexs[vertex]["dist"] > max["dist"]:
            max["dist"] = vertexs[vertex]["dist"]
            max["v"] = vertexs[vertex]["vertex"]
    previous = max["v"]
    while previous != None:
        lt.addFirst(longest, previous)
        previous = vertexs[previous]["from"]
    return longest, max["dist"]

def getMinMax(lista, stack = False):
    if stack:
        minlat, minlon = noFormat(st.pop(lista))
        maxlat, maxlon = minlat, minlon
        while not st.isEmpty(lista):
            node = st.pop(lista)
            lon, lat = noFormat(node)
            if float(lon) > float(maxlon):
                maxlon = lon
            if float(lon) < float(minlon):
                minlon = lon
            if float(lat) > float(maxlat):
                maxlat = lat
            if float(lat) < float(minlat):
                minlat = lat
        return (maxlon, minlon), (maxlat, minlat)
    else:
        minlon, minlat = noFormat(lt.firstElement(lista))
        maxlon, maxlat = noFormat(lt.firstElement(lista))
        for node in lt.iterator(lista):
            lon, lat = noFormat(node)
            if float(lon) > float(maxlon):
                maxlon = lon
            if float(lon) < float(minlon):
                minlon = lon
            if float(lat) > float(maxlat):
                maxlat = lat
            if float(lat) < float(minlat):
                minlat = lat
        return (maxlon, minlon), (maxlat, minlat)
        

def generateListSCC(info, control):
    table = []
    for s in lt.iterator(info):
        path = s["list"]
        DispNode = []
        contador = 1
        wolfList = []
        WolfTable =[]
        continuation = False
        for node in lt.iterator(path):
            v = node.split("_")
            lon = v[0]
            lat = v[1]
            direccion = lon + "_" + lat
            wolf = node.replace(direccion + "_", "")
            if (wolf not in wolfList) and ("p" not in wolf):
                wolfList.append(wolf)
            if lt.size(path) > 6:
                if contador < 4 or contador > (lt.size(path) - 3):
                    DispNode.append(node)
                elif not continuation:
                    DispNode.append("...")
                    continuation = True
                contador +=1
            else:
                DispNode.append(node)
        pathlist = ", ".join(DispNode)
        wolfTable = createWolfTable(wolfList, control)
        element = [s["sccid"], 
                   pathlist, 
                   s["len"], 
                   s["latInfo"][1], 
                   s["latInfo"][0],
                   s["lonInfo"][1], 
                   s["lonInfo"][0],
                   len(wolfList)]
        element.append(wolfTable)
        table.append(element)
        WolfTable.append(wolfTable)
    return table, WolfTable

def createListLongest(info):
    table = []
    for track in lt.iterator(info):
        contador = 1
        DispNode = []
        path = track["path"]
        continuation = False
        for node in lt.iterator(path):
            if lt.size(path) > 6:
                if contador < 4 or contador > (lt.size(path) - 3):
                    DispNode.append(node)
                elif not continuation:
                    DispNode.append("...")
                    continuation = True
                contador +=1
            else:
                DispNode.append(node)
        pathlist = ", ".join(DispNode)
        element = [track["SCCid"],
                   track["size"],
                   track["latInfo"][1], 
                   track["latInfo"][0],
                   track["lonInfo"][1], 
                   track["lonInfo"][0],
                   track["node"],
                   track["edges"],
                   track["weight"],
                   pathlist]
        table.append(element)
    return table

def createWolfTable(wolfList, control):
    headers = ["id",
               "a-sex",
               "life-stage",
               "s-site",
               "d-comments"]
    table = []
    for wolf in wolfList:
        wolfInfo = lt.firstElement(me.getValue(mp.get(control["wolfs"], wolf))["info"])

        if '' == wolfInfo["animal-sex"]:
            wolfInfo["animal-sex"] = "Unknown"
        if '' == wolfInfo["animal-life-stage"]:
            wolfInfo["animal-life-stage"] = "Unknown"
        if '' == wolfInfo["study-site"]:
            wolfInfo["study-site"] = "Unknown"
        if '' == wolfInfo["deployment-comments"]:
            wolfInfo["deployment-comments"] = "Unknown"

        element = [wolf,
                   wolfInfo["animal-sex"],
                   wolfInfo["animal-life-stage"],
                   wolfInfo["study-site"],
                   wolfInfo["deployment-comments"]]
        
        table.append(element)

    return tabulate(table, 
                    headers, 
                    tablefmt="grid",
                    maxcolwidths=[14,7,7,7,14],stralign="left",numalign="left")

def req_8_1(data_structs, initial, destination, modo):
    """
    Función que soluciona el requerimiento 8
    """
    r = req_1(data_structs, initial, destination, modo)
    camino = r[0]

    mapa = folium.Map(location = [58.096, -113.248], zoom_start=8, tiles="Stamen Terrain")
    
    for vertices in lt.iterator(camino):
        pos = vertices.split("_")
        largo = len(pos)

        if largo == 2:
            if 'm' in pos[0]:
                longitud = pos[0].replace("m", "-")
            if 'p' in longitud:
                longitud = longitud.replace("p", ".")
            if 'p' in pos[1]:
                latitud = pos[1].replace("p", ".")
            if 'm' in latitud:
                latitud = latitud.replace("m", "-")

            folium.Marker([float(latitud), float(longitud)], popup = "Punto de encuentro", icon=folium.Icon(color="red", icon="info-sign")).add_to(mapa)

        if largo == 4:

            if 'm' in pos[0]:
                longitud = pos[0].replace("m", "-")
            if 'p' in longitud:
                longitud = longitud.replace("p", ".")
            if 'p' in pos[1]:
                latitud = pos[1].replace("p", ".")
            if 'm' in latitud:
                latitud = latitud.replace("m", "-")

            id_lobo = str(pos[2]) + "-" + str(pos[3])
            folium.Marker([float(latitud), float(longitud)], popup = str(id_lobo), icon=folium.Icon(color="green")).add_to(mapa)

    return mapa

def req_8_2(data_structs, initial, destination):
    """
    Función que soluciona el requerimiento 8
    """
    r = req_2(data_structs, initial, destination)
    camino = r[0]

    mapa = folium.Map(location = [58.096, -113.248], zoom_start=8, tiles="Stamen Terrain")
    
    for vertices in lt.iterator(camino):
        pos = vertices.split("_")
        largo = len(pos)

        if largo == 2:
            if 'm' in pos[0]:
                longitud = pos[0].replace("m", "-")
            if 'p' in longitud:
                longitud = longitud.replace("p", ".")
            if 'p' in pos[1]:
                latitud = pos[1].replace("p", ".")
            if 'm' in latitud:
                latitud = latitud.replace("m", "-")
                
            folium.Marker([float(latitud), float(longitud)], popup = "Punto de encuentro", icon=folium.Icon(color="red", icon="info-sign")).add_to(mapa)
        
        if largo == 4:

            if 'm' in pos[0]:
                longitud = pos[0].replace("m", "-")
            if 'p' in longitud:
                longitud = longitud.replace("p", ".")
            if 'p' in pos[1]:
                latitud = pos[1].replace("p", ".")
            if 'm' in latitud:
                latitud = latitud.replace("m", "-")

            id_lobo = str(pos[2]) + "-" + str(pos[3])
            folium.Marker([float(latitud), float(longitud)], popup = str(id_lobo), icon=folium.Icon(color="green")).add_to(mapa)

    return mapa

def noFormat(str1):

    if 'm' in str1:
        str1 = str1.replace("m", "-")
    if 'p' in str1:
        str1 = str1.replace("p", ".")
    
    if '_' in str1:
        str1 = str1.split("_")
    
    return str1[0], str1[1]

def CalculateDistance(c1, c2):
    p1 = (math.radians(c1[0]), math.radians(c1[1]))
    p2 = (math.radians(c2[0]), math.radians(c2[1]))
    
    plat = (p2[0] - p1[0])/2
    plon = (p2[1] - p1[1])/2
    sin2lat = (math.sin(plat) ** 2)
    sin2lon = (math.sin(plon) ** 2)
    cos1 = math.cos(p1[0])
    cos2 = math.cos(p2[0])
    
    h = sin2lat + cos1 * cos2 * sin2lon
    haversine = math.asin(math.sqrt(h))
    
    return round(2 * haversine * 6371, 3)

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return round(c * r,3)


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    x = date1
    y = date2
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
    
def compareNum(data1, data2):
    num1 = data1["gatNum"]
    num2 = data2["gatNum"]
    if num1 > num2:
        return True
    else:
        return False
    
def compareWeight(data1, data2):
    w1 = data1["weight"]
    w2 = data2["weight"]
    if w1 > w2:
        return True
    else:
        return False
    
def compareTime(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    t1 = datetime.datetime.strptime(data_1["timestamp"], '%Y-%m-%d %H:%M')
    t2 = datetime.datetime.strptime(data_2["timestamp"], '%Y-%m-%d %H:%M')

    if (t1 < t2):
        return True
    else:
        return False
    
def comparePunto(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    if (data_1 < data_2):
        return True
    else:
        return False
    
def compareSize(element1, element2):
    if int(element1['size']) <  int(element2['size']):
        return True
    else:
        return False

    
def compareLongitudes(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    if (int(data_1) < int(data_2)):
        return True
    else:
        return False
    
def compareLatitudes(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    if ((data_1) < (data_2)):
        return True
    else:
        return False
    
def compareTracks(data1,data2):

    #id_unico1 = data1[-5:]
    #id_unico2 = data2[-5:]

    #int(id_unico1)
    #int(id_unico2)

    if (data1 < data2):
        return 1
    elif (data1 > data2):
        return -1
    else:
        return 0


def compareWolfs(data1,data2):

    id_unico1 = data1[1:4] + data1[5:8] + data1[9:11] + data1[12:15]
    id_unico2 = data2[1:4] + data2[5:8] + data2[9:11] + data2[12:15]

    int(id_unico1)
    int(id_unico2)

    if (id_unico1 < id_unico2):
        return True
    else:
        return False
# Funciones de ordenamiento


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass

def sorttime(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    for wolf in lt.iterator(mp.valueSet(data_structs)):
        merg.sort(wolf, compareTime)
