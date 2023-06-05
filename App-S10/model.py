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
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
import datetime
from haversine import haversine, Unit
assert cf
import sys

default_limit=1000
sys.setrecursionlimit(default_limit*1000)

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    analyzer={"puntos_seguimiento": None,
              "puntos_seguimiento2":None,
              "posiciones": None,
              "lobos":None,
              "puntos_encuentro":None,
              "eventos":None,
              "search":None,
              "minlat":None,
              "maxlat":None,
              "minlong":None,
              "maxlong": None,
              "scc":None,
              "info_lobos":None,
              "nodos_lobo":None,
              "tiempo_nodos":None,
              "paths":None,
              "temp_nodos":None}
    analyzer["puntos_seguimiento"]=gr.newGraph(directed=True)
    analyzer["puntos_seguimiento2"]=gr.newGraph(directed=False)
    analyzer["posiciones"]=mp.newMap()
    analyzer["lobos"]=lt.newList(datastructure="ARRAY_LIST")
    analyzer["puntos_encuentro"]=lt.newList(datastructure="ARRAY_LIST")
    analyzer["eventos"]=lt.newList(datastructure="ARRAY_LIST")
    analyzer["search"]=mp.newMap()
    analyzer["minlat"]=9999999999999
    analyzer["minlong"]=9999999999999
    analyzer["maxlat"]=0
    analyzer["maxlong"]=-9999999999999
    analyzer["info_lobos"]=mp.newMap()
    analyzer["nodos_lobo"]=mp.newMap()
    analyzer["tiempo_nodos"]=mp.newMap()
    analyzer["temp_nodos"]=mp.newMap()


    return analyzer


    


# Funciones para agregar informacion al modelo

def ord_data(file, analyzer):
    datos=lt.newList(datastructure="ARRAY_LIST")
    minlat=analyzer["minlat"]
    maxlat=analyzer["maxlat"]
    minlong=analyzer["minlong"]
    maxlong=analyzer["maxlong"]

    for dato in file:
        dato["location-long"]=round(float(dato["location-long"]), 3)
        dato["location-lat"]=round(float(dato["location-lat"]), 3)
        if dato["location-lat"]<minlat:
            minlat=dato["location-lat"]
            analyzer["minlat"]=minlat
        if dato["location-lat"]>maxlat:
            analyzer["maxlat"]=maxlat
            maxlat=dato["location-lat"]
        if dato["location-long"]<minlong:
            minlong=dato["location-long"]
            analyzer["minlong"]=minlong
        if dato["location-long"]>maxlong:
            maxlong=dato["location-long"]
            analyzer["maxlong"]=maxlong

        lt.addLast(datos, dato)
    datos=merg.sort(datos, ord_by_time)
    return datos

def add_data(analyzer, last_data, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    origin=format_vertex(last_data)
    destination=format_vertex(data)
    lat1=last_data["location-lat"]
    long1=last_data["location-long"]
    lat2=data["location-lat"]
    long2=data["location-long"]
    lastfecha=datetime.datetime.strptime(last_data["timestamp"], "%Y-%m-%d %H:%M")
    fecha=datetime.datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M")
    p1=(lat1,long1)
    p2=(lat2,long2)
    distance=abs(haversine(p1,p2))
    last_temp=last_data["external-temperature"]
    temp=data["external-temperature"]
    addpunto(analyzer, origin)
    addpunto(analyzer, destination)
    addConnection(analyzer, origin, destination, distance)
    punto_encuentro(analyzer, origin)
    punto_encuentro(analyzer, destination)
    tiempo_nodos(analyzer, origin, lastfecha)
    tiempo_nodos(analyzer, destination, fecha)
    temp_nodos(analyzer, origin,last_temp)
    temp_nodos(analyzer, origin, temp)
    add_nodos_lobo(analyzer, origin)
    add_nodos_lobo(analyzer, destination)


    return analyzer

def addlobo(analyzer, lobo):
    lt.addLast(analyzer["lobos"], lobo)



    
# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass

def addpunto(analyzer, punto):
    """
    Adiciona una estación como un vertice del grafo
    """
    
    if not gr.containsVertex(analyzer['puntos_seguimiento'], punto):
        gr.insertVertex(analyzer['puntos_seguimiento'], punto)

    if not gr.containsVertex(analyzer['puntos_seguimiento2'], punto):
        gr.insertVertex(analyzer['puntos_seguimiento2'], punto)

    

    return analyzer

def punto_encuentro(analyzer, punto):
   
    mapa=analyzer["posiciones"]

    
    split=punto.split("_")
    coord=split[0]+"_"+split[1]
    

    if mp.contains(mapa, coord):
        entry=mp.get(mapa, coord)
        lista=me.getValue(entry)
        if not lt.isPresent(lista,punto):
            lt.addLast(lista, punto)
    else:
        mp.put(mapa,coord, lt.newList(datastructure="ARRAY_LIST"))
        entry=mp.get(mapa, coord)
        lista=me.getValue(entry)
        if not lt.isPresent(lista, punto):
            lt.addLast(lista, punto)
        

    return analyzer

def add_nodos_lobo(analyzer, nodo):
    mapa=analyzer["nodos_lobo"]
    
    split=nodo.split("_")
    id=split[2]+"_"+split[3]
    if len(split)>=5:
        id+=("_"+split[4])
        
    if not mp.contains(mapa,id):
        lista=lt.newList()
        lt.addLast(lista,nodo)
        mp.put(mapa, id, lista)
    else:
        entry=mp.get(mapa, id)
        lista=me.getValue(entry)
        lt.addLast(lista, nodo)

    return analyzer
    


   



def puntos_encuentro(analyzer):
    lista_nueva=analyzer["puntos_encuentro"]
    mapa=analyzer["posiciones"]
    
    for posicion in lt.iterator(mp.keySet(mapa)):
        entry=mp.get(mapa, posicion)
        lista=me.getValue(entry)
        
        if lt.size(lista)>1:
            lt.addLast(lista_nueva, posicion)    
    
    return analyzer

def conectar_puntos_encuentro(analyzer):
    grafo=analyzer["puntos_seguimiento"]
    grafo2=analyzer["puntos_seguimiento2"]
    puntos_encuentro=analyzer["puntos_encuentro"]
    mapa=analyzer["posiciones"]
    for punto in lt.iterator(puntos_encuentro):
        gr.insertVertex(grafo, punto)
        gr.insertVertex(grafo2, punto)
    for punto in lt.iterator(puntos_encuentro):
        entry=mp.get(mapa, punto)
        lista=me.getValue(entry)
        for lobo in lt.iterator(lista):
            gr.addEdge(grafo, punto, lobo, 0)
            gr.addEdge(grafo, lobo, punto, 0)
            gr.addEdge(grafo2, lobo, punto, 0)
    return analyzer    

def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['puntos_seguimiento'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['puntos_seguimiento'], origin, destination, distance)

    edge = gr.getEdge(analyzer['puntos_seguimiento2'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['puntos_seguimiento2'], origin, destination, distance)

    
        
    return analyzer

def tiempo_nodos(analyzer, nodo, fecha):
    mapa=analyzer["tiempo_nodos"]
    if not mp.contains(mapa, nodo):
        mp.put(mapa, nodo, fecha)
    return analyzer

def temp_nodos(analyzer, nodo,temp):
    mapa=analyzer["tiempo_nodos"]
    if not mp.contains(mapa, nodo):
        mp.put(mapa, nodo, temp)

    return analyzer
    


# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(analyzer, origen, destino):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    analyzer["search"]=dfs.DepthFirstSearch(analyzer["puntos_seguimiento"], origen)
    camino=dfs.hasPathTo(analyzer["search"], destino)
    path=dfs.pathTo(analyzer["search"], destino)
    cant_puntos=0
    
    
    for punto in lt.iterator(path):
        if lt.isPresent(analyzer["puntos_encuentro"], punto):
            cant_puntos+=1
    cant_nodos=lt.size(path)
    cant_seguimiento=cant_nodos-cant_puntos
    distancia=0
    lstpunto=None
    for punto in lt.iterator(path):
        if lstpunto != None:
            
            edge=(gr.getEdge(analyzer["puntos_seguimiento2"], lstpunto, punto))
            
            d=edge["weight"]
            
            distancia+=float(d)

        lstpunto=punto
    path=invert_list(path)
    primeros5=lt.subList(path, 1, 6)
    ult5=lt.subList(path, (lt.size(path)-4), 5)
    
    lista_final=lt.newList()
    lstpunto=None
    for punto in lt.iterator(primeros5):
        if lstpunto != None:
            
            distanciax=gr.getEdge(analyzer["puntos_seguimiento2"], lstpunto, punto )
            
            pos=posicion(lstpunto)
            entry=mp.get(analyzer["posiciones"], pos)
            lista_lobos=me.getValue(entry)
            num_lobos=lt.size(lista_lobos)
            split=lstpunto.split("_")
            lat=split[0]
            long=split[1]
            
            
            dict={}
            dict["punto"]=lstpunto
            dict["longitud"]=long
            dict["latitud"]=lat
            if lt.isPresent(analyzer["puntos_encuentro"], lstpunto):
                dict["individual count"]=num_lobos
            else: 
                dict["individual count"]=1
            dict["Lobos"]=[]
            if num_lobos<=6:
                for x in lt.iterator(lista_lobos):
                    split=x.split("_")
                    if len(split)>=3:
                        id=split[2]+"_"+split[3]
                    if len(split)>=5:
                        id+=("_"+split[4])
                    dict["Lobos"].append(id)
            else:
                prim3=lt.subList(lista_lobos, 1,3)
                ult3=lt.subList(lista_lobos, (lt.size(lista_lobos)-3),3)
                lista=unir_listas(prim3, ult3)
                
                for x in lt.iterator(lista):
                    split=x.split("_")
                    if len(split)>=3:
                        id=split[2]+"_"+split[3]
                    if len(split)>=5:
                        id+=("_"+split[4])
                    dict["Lobos"].append(id)
            dict["edge to"]=punto
            dict["edge distance"]=round(distanciax["weight"],2)
            lt.addLast(lista_final, dict)
            
        lstpunto=punto

    lstpunto=None
    for punto in lt.iterator(ult5):
        if lstpunto != None:
            
            distanciax=gr.getEdge(analyzer["puntos_seguimiento"], lstpunto, punto )
            
            pos=posicion(lstpunto)
            entry=mp.get(analyzer["posiciones"], pos)
            lista_lobos=me.getValue(entry)
            num_lobos=lt.size(lista_lobos)
            split=lstpunto.split("_")
            lat=split[0]
            long=split[1]
                
            
            dict={}
            dict["punto"]=lstpunto
            dict["longitud"]=long
            dict["latitud"]=lat
            if lt.isPresent(analyzer["puntos_encuentro"],lstpunto):
                dict["individual count"]=num_lobos
            else: 
                dict["individual count"]=1

            dict["Lobos"]=[]
            if num_lobos<=6:
                for x in lt.iterator(lista_lobos):
                    split=x.split("_")
                    if len(split)>=3:
                        id=split[2]+"_"+split[3]
                    if len(split)>=5:
                        id+=("_"+split[4])
                    dict["Lobos"].append(id)
                    
            else:
                prim3=lt.subList(lista_lobos, 1,3)
                ult3=lt.subList(lista_lobos, (lt.size(lista_lobos)-3),3)
                lista=unir_listas(prim3, ult3)
                
                for x in lt.iterator(lista):
                    split=x.split("_")
                    if len(split)>=3:
                        id=split[2]+"_"+split[3]
                    if len(split)>=5:
                        id+=("_"+split[4])
                    dict["Lobos"].append(id)
                    
            dict["edge to"]=punto
            dict["edge distance"]=round(distanciax["weight"],2)
            
            lt.addLast(lista_final, dict)
        lstpunto=punto
            
    lstpunto=lt.getElement(path, lt.size(path))

    pos=posicion(lstpunto)
    entry=mp.get(analyzer["posiciones"], pos)
    lista_lobos=me.getValue(entry)
    num_lobos=lt.size(lista_lobos)
    split=lstpunto.split("_")
    lat=split[0]
    long=split[1]
                
            
    dict={}
    dict["punto"]=lstpunto
    dict["longitud"]=long
    dict["latitud"]=lat
            

    dict["individual count"]=num_lobos
    if num_lobos<=6:
        dict["Lobos"]=lt.iterator(lista_lobos)
    else:
        prim3=lt.subList(lista_lobos, 1,3)
        ult3=lt.subList(lista_lobos, (lt.size(lista_lobos)-3),3)
        lista=unir_listas(prim3, ult3)
        dict["Lobos"]=lt.iterator(lista)
    dict["edge to"]="UNKNOWN"
    dict["edge distance"]="UNKNOWN"
    lt.addLast(lista_final, dict)
            

    return camino, distancia,cant_nodos,cant_puntos,cant_seguimiento, lista_final


def req_2(analyzer, origen, destino):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    analyzer["search"]=bfs.BreadhtFisrtSearch(analyzer["puntos_seguimiento"], origen)
    camino=bfs.hasPathTo(analyzer["search"], destino)
    path=bfs.pathTo(analyzer["search"], destino)
    cant_puntos=0
    
    
    for punto in lt.iterator(path):
        if lt.isPresent(analyzer["puntos_encuentro"], punto):
            cant_puntos+=1
    cant_nodos=lt.size(path)
    cant_seguimiento=cant_nodos-cant_puntos
    distancia=0
    lstpunto=None
    for punto in lt.iterator(path):
        if lstpunto != None:
            
            edge=(gr.getEdge(analyzer["puntos_seguimiento2"], lstpunto, punto))
            
            d=edge["weight"]
            
            distancia+=float(d)

        lstpunto=punto
    path=invert_list(path)
    primeros5=lt.subList(path, 1, 6)
    ult5=lt.subList(path, (lt.size(path)-4), 5)
    
    lista_final=lt.newList()
    lstpunto=None
    for punto in lt.iterator(primeros5):
        if lstpunto != None:
            
            distanciax=gr.getEdge(analyzer["puntos_seguimiento2"], lstpunto, punto )
            
            pos=posicion(lstpunto)
            entry=mp.get(analyzer["posiciones"], pos)
            lista_lobos=me.getValue(entry)
            num_lobos=lt.size(lista_lobos)
            split=lstpunto.split("_")
            lat=split[0]
            long=split[1]
            
            
            dict={}
            dict["punto"]=lstpunto
            dict["longitud"]=long
            dict["latitud"]=lat
            if lt.isPresent(analyzer["puntos_encuentro"], lstpunto):
                dict["individual count"]=num_lobos
            else: 
                dict["individual count"]=1
            dict["Lobos"]=[]
            if num_lobos<=6:
                for x in lt.iterator(lista_lobos):
                    split=x.split("_")
                    if len(split)>=3:
                        id=split[2]+"_"+split[3]
                    if len(split)>=5:
                        id+=("_"+split[4])
                    dict["Lobos"].append(id)
            else:
                prim3=lt.subList(lista_lobos, 1,3)
                ult3=lt.subList(lista_lobos, (lt.size(lista_lobos)-3),3)
                lista=unir_listas(prim3, ult3)
                
                
                for x in lt.iterator(lista):
                    split=x.split("_")
                    if len(split)>=3:
                        id=split[2]+"_"+split[3]
                    if len(split)>=5:
                        id+=("_"+split[4])
                    dict["Lobos"].append(id)
            dict["edge to"]=punto
            dict["edge distance"]=round(distanciax["weight"],2)
            lt.addLast(lista_final, dict)
            
        lstpunto=punto

    lstpunto=None
    for punto in lt.iterator(ult5):
        if lstpunto != None:
            
            distanciax=gr.getEdge(analyzer["puntos_seguimiento"], lstpunto, punto )
            
            pos=posicion(lstpunto)
            entry=mp.get(analyzer["posiciones"], pos)
            lista_lobos=me.getValue(entry)
            num_lobos=lt.size(lista_lobos)
            split=lstpunto.split("_")
            lat=split[0]
            long=split[1]
                
            
            dict={}
            dict["punto"]=lstpunto
            dict["longitud"]=long
            dict["latitud"]=lat
            if lt.isPresent(analyzer["puntos_encuentro"],lstpunto):
                dict["individual count"]=num_lobos
            else: 
                dict["individual count"]=1

            dict["Lobos"]=[]
            
            if num_lobos<=6:
                for x in lt.iterator(lista_lobos):
                    split=x.split("_")
                    if len(split)>=3:
                        id=split[2]+"_"+split[3]
                    if len(split)>=5:
                        id+=("_"+split[4])
                    dict["Lobos"].append(id)
            else:
                prim3=lt.subList(lista_lobos, 1,3)
                ult3=lt.subList(lista_lobos, (lt.size(lista_lobos)-3),3)
                lista=unir_listas(prim3, ult3)
                
                for x in lt.iterator(lista):
                    split=x.split("_")
                    if len(split)>=3:
                        id=split[2]+"_"+split[3]
                    if len(split)>=5:
                        id+=("_"+split[4])
                    dict["Lobos"].append(id)
            dict["edge to"]=punto
            dict["edge distance"]=round(distanciax["weight"],2)
            lt.addLast(lista_final, dict)
        lstpunto=punto
            
    lstpunto=lt.getElement(path, lt.size(path))

    pos=posicion(lstpunto)
    entry=mp.get(analyzer["posiciones"], pos)
    lista_lobos=me.getValue(entry)
    num_lobos=lt.size(lista_lobos)
    split=lstpunto.split("_")
    lat=split[0]
    long=split[1]
                
            
    dict={}
    dict["punto"]=lstpunto
    dict["longitud"]=long
    dict["latitud"]=lat
            

    dict["individual count"]=num_lobos
    if num_lobos<=6:
        dict["Lobos"]=lt.iterator(lista_lobos)
    else:
        prim3=lt.subList(lista_lobos, 1,3)
        ult3=lt.subList(lista_lobos, (lt.size(lista_lobos)-3),3)
        lista=unir_listas(prim3, ult3)
        dict["Lobos"]=lt.iterator(lista)
    dict["edge to"]="UNKNOWN"
    dict["edge distance"]="UNKNOWN"
    lt.addLast(lista_final, dict)
            

    return camino, distancia,cant_nodos,cant_puntos,cant_seguimiento, lista_final


def req_3(analyzer):

    """
    Función que soluciona el requerimiento 3
    """
    grafo=analyzer["puntos_seguimiento"]
    analyzer["scc"]=scc.KosarajuSCC(grafo)
    num_manadas=scc.connectedComponents(analyzer["scc"])
    
    vertice="m111p47_56p706"
    scc.sccCount(grafo, analyzer["scc"], vertice)
    llaves=mp.keySet(analyzer["scc"]["idscc"])
    
    
    mapa=mp.newMap()
    for llave in lt.iterator(llaves):
        entry=mp.get(analyzer["scc"]["idscc"], llave)
        manada=me.getValue(entry)
        nodo=me.getKey(entry)
        contains=mp.contains(mapa, manada)
        if not contains:
            lista_nueva=lt.newList()
            lt.addLast(lista_nueva, nodo)
            mp.put(mapa, manada, lista_nueva)
        else:
            entry=mp.get(mapa, manada)
            lista=me.getValue(entry)
            lt.addLast(lista, nodo)

    lista_ord=lt.newList()
    keys=mp.keySet(mapa)
    for key in lt.iterator(keys):
        entry=mp.get(mapa, key)
        lista=me.getValue(entry)
        num_nodos=lt.size(lista)
        dict={}
        dict["manada"]=key
        dict["num_nodos"]=num_nodos
        lt.addLast(lista_ord, dict)

    lista_ord=merg.sort(lista_ord, compare_req3)
    top5=lt.subList(lista_ord, 1, 5)
    lista_final=lt.newList()
    
    for manada in lt.iterator(top5):
        dict={}
        dict["SCCID"]=manada["manada"]
        entry=mp.get(mapa, manada["manada"])
        lista_nodos=me.getValue(entry)
        dict["Node IDs"]=[]
        
        top3=lt.subList(lista_nodos, 1, 3)
        ult3=lt.subList(lista_nodos, (lt.size(lista_nodos)-3),3)
        
        for x in lt.iterator(top3):
            dict["Node IDs"].append(x)
        for x in lt.iterator(ult3):
            dict["Node IDs"].append(x)

        dict["SCC Size"]=manada["num_nodos"]
        max=max_lat_long(lista_nodos)
        

        dict["min lat"]=max[2]
        dict["max lat"]=max[3]
        dict["min long"]=max[0]
        dict["max long"]=max[1]
        lista_ids=get_ids(lista_nodos, analyzer)
        dict["Wolf count"]=lt.size(lista_ids)
        dict["Wolf Details"]=get_infolobos(lista_ids, analyzer)

        lt.addLast(lista_final, dict)

    # TODO: Realizar el requerimiento 3
    return num_manadas, lista_final


def req_4(analyzer, lat1, long1, lat2, long2):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    puntos_encuentro=analyzer["puntos_encuentro"]
    dist_inicio=999999999
    dist_final=999999999
    for punto in lt.iterator(puntos_encuentro):
        split=punto.split("_")
        long=split[0]
        lat=split[1]
        long=long.replace("m", "-")
        long=long.replace("p", ".")
        lat=lat.replace("m", "-")
        lat=lat.replace("p", ".")
        p=(float(lat),float(long))
        p1=(float(lat1),float(long1))
        p2=(float(lat2),float(long2))
        distancia_1=haversine(p1, p)
        distancia_2=haversine(p2,p)
        if distancia_1<dist_inicio:
            dist_inicio=distancia_1
            punto_partida=punto
        elif distancia_2<dist_final:
            dist_final=distancia_2
            punto_final=punto
        
        
        
    analyzer['paths'] = djk.Dijkstra(analyzer['puntos_seguimiento'], punto_partida)
    path = djk.pathTo(analyzer['paths'], punto_final)
    distancia=0
    arcos=lt.size(path)
    puntos_encuentro=0
    
    
    for punto in lt.iterator(path):
        weight=punto["weight"]
        distancia+=float(weight)
        va=punto["vertexA"]
        vb=punto["vertexB"]
        if lt.isPresent(analyzer["puntos_encuentro"],va)or lt.isPresent(analyzer["puntos_encuentro"],vb):
            puntos_encuentro+=1
        

    
        
    info_arcosx=info_arcos(path)
    info_nodosx=info_nodos(path, analyzer)
    x=lt.getElement(info_arcosx,(lt.size(info_arcosx)))
    ult_punto=x["tgt-node-id"]
    dict={}
    split=ult_punto.split("_")
    long=split[0]
    lat=split[1]
    long=long.replace("m", "-")
    long=long.replace("p", ".")
    lat=lat.replace("m", "-")
    lat=lat.replace("p", ".")
    dict["node-id"]=punto
    dict["latitud"]=lat
    dict["longitud"]=long
    indiviudalid=[]
    if lt.isPresent(analyzer["puntos_encuentro"], ult_punto):
        entry=mp.get(analyzer["posiciones"],ult_punto)
        lista_lobos=me.getValue(entry)
        for id in lt.iterator(lista_lobos):
            id=format_id(id)
            indiviudalid.append(id)
        dict["indiviudal-id"]=indiviudalid
        dict["individual-count"]=lt.size(lista_lobos)
        
        lt.changeInfo(info_nodosx, lt.size(info_nodosx),dict)
            
    else:
        if len(split)>=3:
            id=split[2]+"_"+split[3]
        if len(split)>=5:
            id+=("_"+split[4])
        dict["indiviudal-id"]=id
        dict["individual-count"]=1
        lt.changeInfo(info_nodosx, lt.size(info_nodosx),dict)
    
    
    


    return dist_inicio, dist_final, distancia, puntos_encuentro,arcos, punto_partida, punto_final,info_arcosx, info_nodosx


def req_5(analyzer, origen, distancia, min_pe):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    grafo=analyzer["puntos_seguimiento2"]
    analyzer["prim"]=prim.prim(grafo)
    
    """try:
        search = initSearch(graph)
        vertices = g.vertices(graph)
        pos = lt.isPresent(vertices, start_vertex)
        if pos != 0:
            lt.exchange(vertices, 1, pos)
        
        for vert in lt.iterator(vertices):
            if not map.get(search['marked'], vert)['value']:
                prim(graph, search, vert)
        
        corridors = get_valid_corridors(graph, search, max_distance, min_encounters)
        corridors.sort(key=lambda x: (x[0], x[1]), reverse=True)
        
        return corridors
    """
    
    return rutas_max, c_migra
    pass


def req_6(analyzer, fecha1, fecha2, sexo):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    f1=datetime.datetime.strptime(fecha1, "%Y-%m-%d %H:%M")
    f2=datetime.datetime.strptime(fecha2, "%Y-%m-%d %H:%M")
    mayor_lobo={}
    mapa=analyzer["nodos_lobo"]
    lobos=mp.keySet(mapa)
    mayor=0
    for lobo in lt.iterator(lobos):
        #print(str(lobo))
        distancia=0
        edges=0
        path=lt.newList()
        entry=mp.get(mapa, lobo)
        lista_lobo=me.getValue(entry)
        #print(str(lista_lobo))
        for dato in lt.iterator(lista_lobo):
            
            entry=mp.get(analyzer["tiempo_nodos"], dato)
            tiempo=me.getValue(entry)
            if tiempo>=f1 and tiempo <=f2:
                if not lt.isPresent(path, dato):
                    lt.addLast(path, dato)
        lstpunto=None  
        for punto in lt.iterator(path):
            
            if lstpunto != None:
            
                edge=(gr.getEdge(analyzer["puntos_seguimiento2"], lstpunto, punto))
                if edge != None:
                    d=edge["weight"]
                    distancia+=float(d)
                    edges+=1
                

            lstpunto=punto
        if mp.contains(analyzer["info_lobos"], lobo):
            entry=mp.get(analyzer["info_lobos"], lobo)
            info_lobo=me.getValue(entry)
            if info_lobo["animal-sex"]==sexo:
                if distancia>mayor:
                    mayor=distancia
                    mayor_lobo=format_info(info_lobo)
                    path_final=path
                    edges_final=edges

    
    xxx=prim3(path_final, analyzer)

    nodos=lt.size(path_final)
        

    return mayor_lobo, mayor,nodos, edges_final,xxx

def req_6b(analyzer, fecha1, fecha2, sexo):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    f1=datetime.datetime.strptime(fecha1, "%Y-%m-%d %H:%M")
    f2=datetime.datetime.strptime(fecha2, "%Y-%m-%d %H:%M")
    mayor_lobo={}
    mapa=analyzer["nodos_lobo"]
    lobos=mp.keySet(mapa)
    menor=9999999999999999
    for lobo in lt.iterator(lobos):
        #print(str(lobo))
        distancia=0
        edges=0
        path=lt.newList()
        entry=mp.get(mapa, lobo)
        lista_lobo=me.getValue(entry)
        #print(str(lista_lobo))
        for dato in lt.iterator(lista_lobo):
            
            entry=mp.get(analyzer["tiempo_nodos"], dato)
            tiempo=me.getValue(entry)
            if tiempo>=f1 and tiempo <=f2:
                if not lt.isPresent(path, dato):
                    lt.addLast(path, dato)
        lstpunto=None  

        for punto in lt.iterator(path):
            #print(str(punto))
            if lstpunto != None:
            
                edge=(gr.getEdge(analyzer["puntos_seguimiento2"], lstpunto, punto))
                if edge != None:
                    d=edge["weight"]
                    distancia+=float(d)
                    edges+=1
                

            lstpunto=punto
        
        if mp.contains(analyzer["info_lobos"], lobo):
            entry=mp.get(analyzer["info_lobos"], lobo)
            info_lobo=me.getValue(entry)
            if info_lobo["animal-sex"]==sexo:
                if distancia<menor and distancia!=0:
                    menor=distancia
                    mayor_lobo=format_info(info_lobo)
                    path_final=path
                    edges_final=edges

    
    xxx=prim3(path_final, analyzer)

    nodos=lt.size(path_final)
        

    return mayor_lobo, menor,nodos, edges_final,xxx


def req_7(analyzer,t1,t2,temp1,temp2):
    """
    Función que soluciona el requerimiento 7
    """
    control7={}
    control7["puntos_seguimiento"]=gr.newGraph(directed=True)
    control7["puntos_seguimiento2"]=gr.newGraph(directed=False)
    control7["posiciones"]=mp.newMap()
    control7["lobos"]=lt.newList(datastructure="ARRAY_LIST")
    control7["puntos_encuentro"]=lt.newList(datastructure="ARRAY_LIST")
    control7["eventos"]=lt.newList(datastructure="ARRAY_LIST")
    control7["search"]=mp.newMap()
    control7["minlong"]=9999999999999
    control7["maxlat"]=0
    control7["maxlong"]=-9999999999999
    control7["info_lobos"]=mp.newMap()
    control7["nodos_lobo"]=mp.newMap()
    control7["tiempo_nodos"]=mp.newMap()
    control7["temp_nodos"]=mp.newMap()
    control7["scc"]=None

    lista=filtrar_eventos(analyzer, t1,t2,temp1,temp2)
    grafo7(lista,control7)
    puntos_encuentro(control7)
    conectar_puntos_encuentro(control7)

    grafo=control7["puntos_seguimiento"]
    control7["scc"]=scc.KosarajuSCC(grafo)
    num_manadas=scc.connectedComponents(control7["scc"])
    
    
    vertice="m111p47_56p706"
    scc.sccCount(grafo, control7["scc"], vertice)
    llaves=mp.keySet(control7["scc"]["idscc"])
    mapa=mp.newMap()
    for llave in lt.iterator(llaves):
        entry=mp.get(control7["scc"]["idscc"], llave)
        manada=me.getValue(entry)
        nodo=me.getKey(entry)
        contains=mp.contains(mapa, manada)
        if not contains:
            lista_nueva=lt.newList()
            lt.addLast(lista_nueva, nodo)
            mp.put(mapa, manada, lista_nueva)
        else:
            entry=mp.get(mapa, manada)
            lista=me.getValue(entry)
            lt.addLast(lista, nodo)

    lista_ord=lt.newList()
    keys=mp.keySet(mapa)
    for key in lt.iterator(keys):
        entry=mp.get(mapa, key)
        lista=me.getValue(entry)
        num_nodos=lt.size(lista)
        dict={}
        dict["manada"]=key
        dict["num_nodos"]=num_nodos
        lt.addLast(lista_ord, dict)

    lista_ord=merg.sort(lista_ord, compare_req3)
    top3=lt.subList(lista_ord, 1, 3)
    u3=lt.subList(lista_ord,(lt.size(lista_ord)-3) ,3)
    lista_final=lt.newList()
    for manada in lt.iterator(top3):
        dict={}
        dict["SCCID"]=manada["manada"]
        entry=mp.get(mapa, manada["manada"])
        lista_nodos=me.getValue(entry)
        dict["Node IDs"]=[]
        
        top3=lt.subList(lista_nodos, 1, 3)
        ult3=lt.subList(lista_nodos, (lt.size(lista_nodos)-3),3)
        
        for x in lt.iterator(top3):
            dict["Node IDs"].append(x)
        for x in lt.iterator(ult3):
            dict["Node IDs"].append(x)

        dict["SCC Size"]=manada["num_nodos"]
        max=max_lat_long(lista_nodos)
        

        dict["min lat"]=max[2]
        dict["max lat"]=max[3]
        dict["min long"]=max[0]
        dict["max long"]=max[1]
        lista_ids=get_ids(lista_nodos, analyzer)
        dict["Wolf count"]=lt.size(lista_ids)
        dict["Wolf Details"]=get_infolobos(lista_ids, analyzer)

        lt.addLast(lista_final, dict)

    for manada in lt.iterator(u3):
        dict={}
        dict["SCCID"]=manada["manada"]
        entry=mp.get(mapa, manada["manada"])
        lista_nodos=me.getValue(entry)
        dict["Node IDs"]=[]
        if lt.size(lista)<=6:
            for x in lt.iterator(lista):
                dict["Node IDs"].append(x)
        else:
            top3=lt.subList(lista_nodos, 1, 3)
            ult3=lt.subList(lista_nodos, (lt.size(lista_nodos)-3),3)
        
            for x in lt.iterator(top3):
                dict["Node IDs"].append(x)
            for x in lt.iterator(ult3):
                dict["Node IDs"].append(x)

        dict["SCC Size"]=manada["num_nodos"]
        max=max_lat_long(lista_nodos)
        

        dict["min lat"]=max[2]
        dict["max lat"]=max[3]
        dict["min long"]=max[0]
        dict["max long"]=max[1]
        lista_ids=get_ids(lista_nodos, analyzer)
        dict["Wolf count"]=lt.size(lista_ids)
        dict["Wolf Details"]=get_infolobos(lista_ids, analyzer)

        lt.addLast(lista_final, dict)

    # TODO: Realizar el requerimiento 7
    return num_manadas, lista_final


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

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

def ord_by_time(data1, data2):
    fecha1=datetime.datetime.strptime(data1["timestamp"], "%Y-%m-%d %H:%M")
    fecha2=datetime.datetime.strptime(data2["timestamp"], "%Y-%m-%d %H:%M")

    if (data1["individual-local-identifier"])>(data2["individual-local-identifier"]):
        return True
    
    elif (data1["individual-local-identifier"])<(data2["individual-local-identifier"]):
    
        return False
    else:
        if fecha1<fecha2:
            return True
        else:
            return False
    
def format_vertex(dato):
    
    long=str(dato["location-long"])
    lat=str(dato["location-lat"])
    long=long.replace("-", "m")
    long=long.replace(".", "p")
    lat=lat.replace("-", "m")
    lat=lat.replace(".", "p")
    id=dato["tag-local-identifier"]+"_"+dato["individual-local-identifier"]
    formato=long+"_"+lat+"_"+id
    return formato

def iterador(lista):
    return lt.iterator(lista)

def size(lista):
    return lt.size(lista)

def degree(grafo, punto):
    return gr.degree(grafo, punto)

def numvertices(grafo):
    return gr.numVertices(grafo)

def vertices(grafo):
    return gr.vertices(grafo)

def arcos(grafo):
    return gr.numEdges(grafo)

def keyset(mapa):
    return mp.keySet(mapa)

def numvertices(grafo):
    return gr.numVertices(grafo)

def cant_puntos_encuentro(analyzer, lista):
    cont=0
    for x in lt.iterator(lista):
        if lt.isPresent(analyzer["puntos_encuentro"], x):
            cont+=1

    return cont

def posicion(xxx):
    split=xxx.split("_")
    pos=split[0]+"_"+split[1]
    return pos

def unir_listas(lista1, lista2):
    lista=lt.newList()
    for x in lt.iterator(lista1):
        lt.addLast(lista, x)

    for x in lt.iterator(lista2):
        lt.addLast(lista, x)
    return lista

def invert_list(lista):
    listax=lt.newList()
    for dato in lt.iterator(lista):
        lt.addFirst(listax, dato)
    return listax

def compare_req3(dato1, dato2):
    num1=dato1["num_nodos"]
    num2=dato2["num_nodos"]
    if num1>num2:
        return True
    else:
        return False
def max_lat_long(lista):
    
    minlat=99999999999
    minlong=9999999999
    maxlat=-99999999999
    maxlong=-999999999

    

    for nodo in lt.iterator(lista):
        split=nodo.split("_")
        lat=split[0]
        long=split[1]
        long=long.replace("m", "-")
        long=long.replace("p", ".")
        lat=lat.replace("m", "-")
        lat=lat.replace("p", ".")
        lat=float(lat)
        long=float(long)
        if lat<minlat:
            minlat=lat
            
        if lat>maxlat:
            maxlat=lat
        if long<minlong:
            minlong=long
            
        if long>maxlong:
            maxlong=long

    return minlat, maxlat, minlong, maxlong

def get_ids(lista, analyzer):
    lista_ids=lt.newList()
    for nodo in lt.iterator(lista):
        if not lt.isPresent(analyzer["puntos_encuentro"], nodo):
            split=nodo.split("_")
            id=split[2]+"_"+split[3]
            if len(split)>=5:
                id+=("_"+split[4])
            if not lt.isPresent(lista_ids, id):
                lt.addLast(lista_ids, id)

    lista_ids=merg.sort(lista_ids, sort_ids)
    return lista_ids

def mapa_lobos(analyzer):
    for lobo in lt.iterator(analyzer["lobos"]):
        id=lobo["tag-id"]+"_"+lobo["animal-id"]
        contains=mp.contains(analyzer["info_lobos"], id)
        if not contains:
            mp.put(analyzer["info_lobos"], id, lobo)

    return analyzer

def get_infolobos(lista, analyzer):
    dict={}
    cont=1
    if lt.size(lista)>6:
        top3=lt.subList(lista, 1, 3)
        u3=lt.subList(lista, lt.size(lista)-2, 3)
        for id in lt.iterator(top3):
        

            contains=mp.contains(analyzer["info_lobos"],id)
        
            if contains:
                entry=mp.get(analyzer["info_lobos"], id)
                info_lobo=me.getValue(entry)
                dict2=format_info(info_lobo)
                dict["Lobo "+str(cont)]=dict2
                cont+=1
        cont=lt.size(lista)-2
        for id in lt.iterator(u3):
        

            contains=mp.contains(analyzer["info_lobos"],id)
        
            if contains:
                entry=mp.get(analyzer["info_lobos"], id)
                info_lobo=me.getValue(entry)
                dict2=format_info(info_lobo)
                dict["Lobo "+str(cont)]=dict2
                cont+=1

    else:
        for id in lt.iterator(lista):
        
            contains=mp.contains(analyzer["info_lobos"],id)
        
            if contains:
                entry=mp.get(analyzer["info_lobos"], id)
                info_lobo=me.getValue(entry)
                dict2=format_info(info_lobo)
                dict["Lobo "+str(cont)]=dict2
                cont+=1
    return dict

def format_info(lobo):
    dict={}
    dict["indiviudal-id"]=lobo["animal-id"]+"_"+lobo["tag-id"]
    if lobo["animal-sex"]=="":
        dict["animal-sex"]="UNKNOWN"
    else:
        dict["animal-sex"]=lobo["animal-sex"]
    
    if lobo["animal-life-stage"]=="":
        dict["animal-life-stage"]="UNKNOWN"
    else:
        dict["animal-life-stage"]=lobo["animal-life-stage"]

    if lobo["study-site"]=="":
        dict["study-site"]="UNKNOWN"
    else:
        dict["study-site"]=lobo["study-site"]

    if lobo["deployment-comments"]=="":
        dict["deployment-comments"]="UNKNOWN"
    else:
        dict["deployment-comments"]=lobo["deployment-comments"]

    return dict

def sort_ids(dato1, dato2):
    if dato1>dato2:
        return True
    else:
        return False
    
def prim3(path, analyzer):
    p3=lt.subList(path, 1, 3)
    u3=lt.subList(path, (lt.size(path)-2),3)
    lista_nueva=lt.newList()
    for node in lt.iterator(p3):
        
        dict={}
        dict["node id"]=node
        split=node.split("_")
        id=split[2]+"_"+split[3]
        if len(split)>=5:
            id+=("_"+split[4])
        long=split[0]
        lat=split[1]
        coord=long+"_"+lat
        long=long.replace("m", "-")
        long=long.replace("p", ".")
        lat=lat.replace("m", "-")
        lat=lat.replace("p", ".")
        dict["longitud"]=long
        dict["latitud"]=lat
        dict["individual id"]=id
        entry=mp.get(analyzer["posiciones"], coord)
        lista=me.getValue(entry)
        count=lt.size(lista)
        dict["Wolf Count"]=count
        lt.addLast(lista_nueva, dict)
    
    
    for node in lt.iterator(u3):
        dict={}
        dict["node id"]=node
        split=node.split("_")
        id=split[2]+"_"+split[3]
        if len(split)>=5:
            id+=("_"+split[4])
        long=split[0]
        lat=split[1]
        coord=long+"_"+lat
        long=long.replace("m", "-")
        long=long.replace("p", ".")
        lat=lat.replace("m", "-")
        lat=lat.replace("p", ".")
        dict["longitud"]=long
        dict["latitud"]=lat
        dict["individual id"]=id
        entry=mp.get(analyzer["posiciones"], coord)
        lista=me.getValue(entry)
        count=lt.size(lista)
        dict["Wolf Count"]=count
        lt.addLast(lista_nueva, dict)

    return lista_nueva

def info_arcos(path):
    lista_nueva=lt.newList()
    p3=lt.subList(path, 1, 3)
    u3=lt.subList(path, (lt.size(path)-2),3)
    for arco in lt.iterator(p3):
        dict={}
        dict["src-node-id"]=arco["vertexA"]
        split=arco["vertexA"].split("_")
        long=split[0]
        lat=split[1]
        long=long.replace("m", "-")
        long=long.replace("p", ".")
        lat=lat.replace("m", "-")
        lat=lat.replace("p", ".")
        dict["location-lat-src"]=lat
        dict["location-long-src"]=long

        dict["tgt-node-id"]=arco["vertexB"]
        split=arco["vertexB"].split("_")
        long=split[0]
        lat=split[1]
        long=long.replace("m", "-")
        long=long.replace("p", ".")
        lat=lat.replace("m", "-")
        lat=lat.replace("p", ".")
        dict["location-lat-tgt"]=lat
        dict["location-long-tgt"]=long

        if len(split)>=3:
            id=split[2]+"_"+split[3]
            if len(split)>=5:
                id+=("_"+split[4])

        else:
            split=arco["vertexA"]
            if len(split)>=3:
                id=split[2]+"_"+split[3]
            if len(split)>=5:
                id+=("_"+split[4])


        dict["individual-id"]=id
        dict["distance"]=arco["weight"]
        lt.addLast(lista_nueva, dict)

    for arco in lt.iterator(u3):
        dict={}
        dict["src-node-id"]=arco["vertexA"]
        split=arco["vertexA"].split("_")
        long=split[0]
        lat=split[1]
        long=long.replace("m", "-")
        long=long.replace("p", ".")
        lat=lat.replace("m", "-")
        lat=lat.replace("p", ".")
        dict["location-lat-src"]=lat
        dict["location-long-src"]=long

        dict["tgt-node-id"]=arco["vertexB"]
        split=arco["vertexB"].split("_")
        long=split[0]
        lat=split[1]
        long=long.replace("m", "-")
        long=long.replace("p", ".")
        lat=lat.replace("m", "-")
        lat=lat.replace("p", ".")
        dict["location-lat-tgt"]=lat
        dict["location-long-tgt"]=long

        if len(split)>=3:
            id=split[2]+"_"+split[3]
            if len(split)>=5:
                id+=("_"+split[4])

        else:
            split=arco["vertexA"].split("_")
            if len(split)>=3:
                id=split[2]+"_"+split[3]
            if len(split)>=5:
                id+=("_"+split[4])


        dict["individual-id"]=id
        dict["distance"]=arco["weight"]
        lt.addLast(lista_nueva, dict)

    lista_nueva=invert_list(lista_nueva)

    return lista_nueva

def info_nodos(path, analyzer):
    lista_nueva=lt.newList()
    p3=lt.subList(path, 1, 3)
    u3=lt.subList(path, (lt.size(path)-2),3)
    for nodo in lt.iterator(p3):
        dict={}
        punto=nodo["vertexA"]
        split=nodo["vertexA"].split("_")
        long=split[0]
        lat=split[1]
        long=long.replace("m", "-")
        long=long.replace("p", ".")
        lat=lat.replace("m", "-")
        lat=lat.replace("p", ".")
        dict["node-id"]=punto
        dict["latitud"]=lat
        dict["longitud"]=long
        indiviudalid=[]
        if lt.isPresent(analyzer["puntos_encuentro"], punto):
            entry=mp.get(analyzer["posiciones"],punto)
            lista_lobos=me.getValue(entry)
            for id in lt.iterator(lista_lobos):
                id=format_id(id)
                indiviudalid.append(id)
            dict["indiviudal-id"]=indiviudalid
            dict["individual-count"]=lt.size(lista_lobos)
            
        else:
            if len(split)>=3:
                id=split[2]+"_"+split[3]
            if len(split)>=5:
                id+=("_"+split[4])
            dict["indiviudal-id"]=id
            dict["individual-count"]=1
        lt.addLast(lista_nueva, dict)
        

    for nodo in lt.iterator(u3):
        dict={}
        punto=nodo["vertexA"]
        split=nodo["vertexA"].split("_")
        long=split[0]
        lat=split[1]
        long=long.replace("m", "-")
        long=long.replace("p", ".")
        lat=lat.replace("m", "-")
        lat=lat.replace("p", ".")
        dict["node-id"]=punto
        dict["latitud"]=lat
        dict["longitud"]=long
        indiviudalid=[]
        if lt.isPresent(analyzer["puntos_encuentro"], punto):
            entry=mp.get(analyzer["posiciones"],punto)
            lista_lobos=me.getValue(entry)
            for id in lt.iterator(lista_lobos):
                id=format_id(id)
                indiviudalid.append(id)
            dict["indiviudal-id"]=indiviudalid
            dict["individual-count"]=lt.size(lista_lobos)
            
        else:
            if len(split)>=3:
                id=split[2]+"_"+split[3]
            if len(split)>=5:
                id+=("_"+split[4])
            dict["indiviudal-id"]=id
            dict["individual-count"]=1
        lt.addLast(lista_nueva, dict)

        
    
    

    
    lista_nueva=invert_list(lista_nueva)
    return lista_nueva

def format_id(punto):
    split=punto.split("_")
    if len(split)>=3:
            id=split[2]+"_"+split[3]
    if len(split)>=5:
        id+=("_"+split[4])
    return id

def filtrar_eventos(analyzer, t1,t2,temp1,temp2):
    t1=datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M")
    t2=datetime.datetime.strptime(t2, "%Y-%m-%d %H:%M")
    temp1=float(temp1)
    temp2=float(temp2)
    lista_todo=analyzer["eventos"]
    lista_filtrada=lt.newList(datastructure="ARRAY_LIST")
    for dato in lt.iterator(lista_todo):
        temp=dato["external-temperature"]
        time=dato["timestamp"]
        time=datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")
        temp=float(temp)
        if time>=t1 and time<=t2:
            if temp>=temp1 and temp<temp2:
                lt.addLast(lista_filtrada, dato)

    return lista_filtrada

def grafo7(lista,control):
    last_dato=None
    for dato in iterador(lista):
        if last_dato is not None:
            samelobo=dato["individual-local-identifier"]==last_dato["individual-local-identifier"]
            sameevent=dato["event-id"]==last_dato["event-id"]
            if samelobo and not sameevent: 
                addg7(control, last_dato, dato)
        last_dato=dato

    
def addg7(analyzer, last_data,data):
    origin=format_vertex(last_data)
    destination=format_vertex(data)
    lat1=last_data["location-lat"]
    long1=last_data["location-long"]
    lat2=data["location-lat"]
    long2=data["location-long"]
    lastfecha=datetime.datetime.strptime(last_data["timestamp"], "%Y-%m-%d %H:%M")
    fecha=datetime.datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M")
    p1=(lat1,long1)
    p2=(lat2,long2)
    distance=abs(haversine(p1,p2))
    last_temp=last_data["external-temperature"]
    temp=data["external-temperature"]
    addpunto(analyzer, origin)
    addpunto(analyzer, destination)
    addConnection(analyzer, origin, destination, distance)
    punto_encuentro(analyzer, origin)
    punto_encuentro(analyzer, destination)
    tiempo_nodos(analyzer, origin, lastfecha)
    tiempo_nodos(analyzer, destination, fecha)
    temp_nodos(analyzer, origin,last_temp)
    temp_nodos(analyzer, origin, temp)
    add_nodos_lobo(analyzer, origin)
    add_nodos_lobo(analyzer, destination)
    return analyzer