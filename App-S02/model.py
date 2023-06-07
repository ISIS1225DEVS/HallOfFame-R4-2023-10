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
from math import radians, cos, sin, asin, sqrt
assert cf

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
    analyzer = {
            "events":None,
            'points': None,
            'connections': None,
            'components': None,
            'paths': None,
            "search": None,
            "graph":None,
            "allEvents":None,
            "hashEncuentros":None,
            "infoLobos":None
        }

    analyzer['wolfHash'] = mp.newMap(numelements=14000,
                                     maptype='PROBING')

    analyzer['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                    directed=False,
                                              size=100000)
    analyzer["allEvents"] = lt.newList("ARRAY_LIST")

    analyzer['hashEncuentros'] = mp.newMap(numelements=140000,
                                     maptype='PROBING')
    
    analyzer['infoLobos'] = mp.newMap(numelements=140000,
                                     maptype='PROBING')

    return analyzer

def new_data_structs2():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    analyzer = {
            "graph":None,
            "allEvents":None,
            "hashEncuentros":None,
            "infoLobos":None
        }

    analyzer['wolfHash'] = mp.newMap(numelements=14000,
                                     maptype='PROBING')

    analyzer['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                    directed=False,
                                              size=100000)
    analyzer["allEvents"] = lt.newList("ARRAY_LIST")

    analyzer['hashEncuentros'] = mp.newMap(numelements=140000,
                                     maptype='PROBING')
    
    analyzer['infoLobos'] = mp.newMap(numelements=140000,
                                     maptype='PROBING')

    return analyzer


# Funciones para agregar informacion al modelo

def add_data1(analyzer, event):
    """
    Función para agregar nuevos elementos a la lista
    """
    eventsList=analyzer["allEvents"]
    wolfHash=analyzer["wolfHash"]
    entry=mp.get(wolfHash,event["ID"])
    lt.addLast(eventsList,event)

    if entry is None:
        wolfList=lt.newList("ARRAY_LIST")
        lt.addLast(wolfList,event)
        mp.put(wolfHash,event["ID"],wolfList)
        
    else:
        wolfList=me.getValue(entry)
        esta=False
        for eventInList in lt.iterator(wolfList):
            if eventInList["formatoNodo"]==event["formatoNodo"]:
                esta=True
        if esta==False:
            lt.addLast(wolfList,event)

    return analyzer

def add_dataFile2(analyzer, event):
    """
    Función para agregar nuevos elementos a la lista
    """
    hashInfo=analyzer["infoLobos"]
    mp.put(hashInfo,event["ID"],event)
    
    return analyzer


def addGraph(analyzer):
    wolfGraph=analyzer["graph"]
    wolfHash=analyzer["wolfHash"]
    hashKeys=mp.keySet(wolfHash)
    for key in lt.iterator(hashKeys):
        wolfList=me.getValue(mp.get(wolfHash,key))
        gr.insertVertex(wolfGraph,lt.getElement(wolfList,0)["formatoNodo"])
        for i in range(1,lt.size(wolfList)):
            gr.insertVertex(wolfGraph,lt.getElement(wolfList,i)["formatoNodo"])
            gr.addEdge(wolfGraph,lt.getElement(wolfList,i-1)["formatoNodo"],
                       lt.getElement(wolfList,i)["formatoNodo"],dist(lt.getElement(wolfList,i)["location-long"],
                                                                     lt.getElement(wolfList,i)["location-lat"],
                                                                     lt.getElement(wolfList,i-1)["location-long"],
                                                                     lt.getElement(wolfList,i-1)["location-lat"]))
        #BUSCAR PUNTOS DE ENCUENTRO
    reconocidos=lt.size(hashKeys)
    numeroDeEventos=lt.size(analyzer["allEvents"])
    totalVertices=gr.numVertices(wolfGraph)
    totalArcos=gr.numEdges(wolfGraph)
    return analyzer

def addMeetingPoint(analyzer):

    grafo=analyzer['graph']
    listaEventos=analyzer["allEvents"]
    hashEncuentros=analyzer["hashEncuentros"]
    for event in lt.iterator(listaEventos):
        entry=mp.get(hashEncuentros,event["latLong"])
        if entry is None:
            listaLatYLong=lt.newList("ARRAY_LIST")
            lt.addLast(listaLatYLong,event)
            mp.put(hashEncuentros,event["latLong"],listaLatYLong)
        else:
            listaEventosEnLugar=me.getValue(entry)
            yaEsta=False
            for eventoEnLista in lt.iterator(listaEventosEnLugar):
                if event["formatoNodo"]==eventoEnLista["formatoNodo"]:
                    yaEsta=True
            if yaEsta==False:
                lt.addLast(listaEventosEnLugar,event)

    listaUbicaciones=mp.keySet(hashEncuentros)
    for ubicacion in lt.iterator(listaUbicaciones):
        listaUbicacion=me.getValue(mp.get(hashEncuentros,ubicacion))
        if lt.size(listaUbicacion)==1:
            mp.remove(hashEncuentros,lt.firstElement(listaUbicacion)["latLong"])

    listaUbicaciones=mp.keySet(hashEncuentros)
    for ubicacion in lt.iterator(listaUbicaciones):
        listaUbicacion=me.getValue(mp.get(hashEncuentros,ubicacion))
        gr.insertVertex(grafo,ubicacion)
        for point in lt.iterator(listaUbicacion):
            gr.addEdge(grafo,point["formatoNodo"],ubicacion)
    print(gr.numVertices(grafo),gr.numEdges(grafo))
    

# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


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


def req_1(analyzer,punto1,punto2):
    """
    Función que soluciona el requerimiento 1
    """
    grafo=analyzer["graph"]
    caminos=dfs.DepthFirstSearch(grafo,punto1)
    pila=dfs.pathTo(caminos,punto2)
    return pila


def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(analyzer):
    """
    Función que soluciona el requerimiento 3
    """
    componentes=scc.KosarajuSCC(analyzer["graph"])
    hashConectados=mp.newMap()
    for key in lt.iterator(mp.keySet(componentes["idscc"])):
        value=me.getValue(mp.get(componentes["idscc"],key))
        entry=mp.get(hashConectados,value)
        if entry is None:
            hashElements=mp.newMap()
            listaConectados=lt.newList()
            lt.addLast(listaConectados,key)
            mp.put(hashElements,"puntos",listaConectados)
            mp.put(hashConectados,value,hashElements)
        else:
            hashElements=me.getValue(entry)
            listaConectados=me.getValue(mp.get(hashElements,"puntos"))
            lt.addLast(listaConectados,key)
    
    #BUSCAR LOBOS POR MANADA

    for key in lt.iterator(mp.keySet(hashConectados)):
        hashElements=me.getValue(mp.get(hashConectados,key))
        listaConectados=me.getValue(mp.get(hashElements,"puntos"))
        hashLobosDelComponente=buscarLobos(analyzer,listaConectados)
        mp.put(hashElements,"lobos",hashLobosDelComponente)

    return hashConectados


def req_4(analyzer,initialP,destP):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4

    cont_trans=0
    dist_total=0
    dict_edges={}
    
    ini=''
    dist_menor_ini=1000000000000
    lon1,lat1=obtener_datos(initialP)
    for i in lt.iterator(analyzer['vertices']):
        dist_est=haversine(lon1,lat1,float(i['Longitude']),float(i['Latitude']))
        if dist_est<dist_menor_ini:
            dist_menor_ini=dist_est
            ini=formatVertex(i)
        if dist_menor_ini==0:
            break
    
    dest=''
    dist_menor_dest=100000000000
    lon2,lat2=obtener_datos(destP)
    for i in lt.iterator(analyzer['vertices']):
        dist_est=haversine(lon2,lat2,float(i['Longitude']),float(i['Latitude']))
        if dist_est<dist_menor_dest:
            dist_menor_dest=dist_est
            dest=formatVertex(i)
        if dist_menor_dest==0:
            break
    
    analyzer['search']=djk.Dijkstra(analyzer['grafo'],ini)
    exist= djk.hasPathTo(analyzer['search'], dest)
    path_new=lt.newList('ARRAY_LIST')
    if exist:
        path= djk.pathTo(analyzer['search'],dest)

        dist=gr.getEdge(analyzer['grafo'],lt.getElement(path,i)['vertexA'],lt.getElement(path,i)['vertexB'])['weight']
        dict_edges[(lt.getElement(path,i)['vertexA'],lt.getElement(path,i)['vertexB'])]=round(dist,2)
        
        dist_total+=dist
        lt.addFirst(path_new,[lt.getElement(path,i)['vertexA'],dist])
        lt.addLast(path_new,[lt.getElement(path,0)['vertexB'],0])

        
        return True, dist_menor_ini, dist_total, dist_menor_dest, lt.size(path_new), cont_trans, path_new,dict_edges
    else:
    
        return False,0, 0, 0, 0,0,0,0,0,


def obtener_datos(string):
    datos = string.split("-")
    dato1 = datos[0]
    dato2 = datos[1]    
    return dato1, dato2

def haversine(punto1, punto2):
    
    lon1,lat1=obtener_datos(punto1)
    lon2,lat2=obtener_datos(punto2)
    lon1=float(lon1)
    lon2=float(lon2)
    lat1=float(lat1)
    lat2=float(lat2)
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)*2 + cos(lat1) * cos(lat2) * sin(dlon/2)*2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

def formatVertex(service):

    name = service['ID'] + '-'
    name = name + service['wolfHash'][4:]
    return name

def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['grafo'], origin, destination)
    if edge is None:
        analyzer['G'].add_edge(origin, destination)
        gr.addEdge(analyzer['grafo'], origin, destination, distance)
    return analyzer


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(analyzer,sexo,start,end):
    """
    Función que soluciona el requerimiento 6
    """
    movimientos=analyzer['wolfHash'].copy()
    informacionLobos=analyzer["infoLobos"]
    for idLobo in lt.iterator(mp.keySet(movimientos)):
        infoLobo=me.getValue(mp.get(informacionLobos,idLobo))
        sexoLobo=infoLobo["animal-sex"]
        if sexoLobo != sexo:
            mp.remove(movimientos,idLobo)

    for lobo in lt.iterator(mp.keySet(movimientos)):
        nuevaLista=lt.newList()
        listaMovimientos=me.getValue(mp.get(movimientos,lobo))
        for movimiento in lt.iterator(listaMovimientos):
            evaluacion=evaluarTiempo(movimiento,start,end)
            if evaluacion==True:
                lt.addLast(nuevaLista,movimiento)
        listaMovimientos=nuevaLista
        distanciaRecorrida=calcularDistancia(listaMovimientos)
        infoLobo=me.getValue(mp.get(informacionLobos,lobo))
        infoLobo["dist"]=distanciaRecorrida
    return movimientos



def req_7(analyzer):
    """
    Función que soluciona el requerimiento 7
    """
    componentes=scc.KosarajuSCC(analyzer["graph"])
    hashConectados=mp.newMap()
    for key in lt.iterator(mp.keySet(componentes["idscc"])):
        value=me.getValue(mp.get(componentes["idscc"],key))
        entry=mp.get(hashConectados,value)
        if entry is None:
            hashElements=mp.newMap()
            listaConectados=lt.newList()
            lt.addLast(listaConectados,key)
            mp.put(hashElements,"puntos",listaConectados)
            mp.put(hashConectados,value,hashElements)
        else:
            hashElements=me.getValue(entry)
            listaConectados=me.getValue(mp.get(hashElements,"puntos"))
            lt.addLast(listaConectados,key)
    
    #BUSCAR LOBOS POR MANADA

    for key in lt.iterator(mp.keySet(hashConectados)):
        hashElements=me.getValue(mp.get(hashConectados,key))
        listaConectados=me.getValue(mp.get(hashElements,"puntos"))
        hashLobosDelComponente=buscarLobos(analyzer,listaConectados)
        mp.put(hashElements,"lobos",hashLobosDelComponente)

    return hashConectados


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

def sortListByTime(analyzer):
    wolfKeys=mp.keySet(analyzer["wolfHash"])
    # print(lt.size(wolfKeys))
    for key in lt.iterator(wolfKeys):
        wolfList=me.getValue(mp.get(analyzer["wolfHash"],key))
        merg.sort(wolfList,sortTime)
    return analyzer

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



def sortTime(event1,event2):
    """
    Función encargada de ordenar la lista con los datos
    """
    time1 = event1["timestamp"]+":00"
    time2 = event2["timestamp"]+":00"
    time1Format = datetime.datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
    time2Format = datetime.datetime.strptime(time2, "%Y-%m-%d %H:%M:%S")
    if time1Format < time2Format:
        return 1
    else:
        return 0

#FUNCIONES FORMATO

def enFormatoID(event):
    return event["individual-local-identifier"]+"_"+event["tag-local-identifier"]

def enFormatoID2(event):
    return event["animal-id"]+"_"+event["tag-id"]

def enFormato(event):
    long=str(round(float(event["location-long"]),3))
    lat=str(round(float(event["location-lat"]),3))
    long=long.replace("-","m")
    long=long.replace(".","p")
    lat=lat.replace("-","m")
    lat=lat.replace(".","p")
    return long+"_"+lat+"_"+event["individual-local-identifier"]+"_"+event["tag-local-identifier"]

def enFormatoLatLong(event):
    long=str(round(float(event["location-long"]),3))
    lat=str(round(float(event["location-lat"]),3))
    long=long.replace("-","m")
    long=long.replace(".","p")
    lat=lat.replace("-","m")
    lat=lat.replace(".","p")
    return long+"_"+lat
#OTRAS FUNCIONES

def dist(long1,lat1,long2,lat2):
    """
    Función que soluciona el requerimiento 6
    """
    latitud1=math.radians(float(lat1)) #LATITUD DE REFERENCIA
    longitud1=math.radians(float(long1)) #LONGITUD DE REFERENCIA
    latitud2=math.radians(float(lat2))
    longitud2=math.radians(float(long2))
    a=math.sin((latitud2-latitud1)/2)**2
    b=math.cos(latitud1)*math.cos(latitud2)
    c=math.sin((longitud2-longitud1)/2)**2
    D=2*math.asin(math.sqrt(a+b*c))*6371
    return round(D,3)

def buscarLobos(analyzer,listaConectados):
    infoLobos=analyzer["infoLobos"]
    listaEventos=analyzer["allEvents"]
    hashInfoLobos=mp.newMap()
    minLat=181
    maxLat=-181
    minLong=181
    maxLong=-181
    for movimiento in lt.iterator(listaConectados):
        for evento in lt.iterator(listaEventos):
            if movimiento==evento["formatoNodo"]:
                infoLobo=me.getValue(mp.get(infoLobos,evento["ID"]))
                mp.put(hashInfoLobos,evento["ID"],infoLobo)
                if round(float(evento["location-long"]),3)>maxLong:
                    maxLong=round(float(evento["location-long"]),3)
                if round(float(evento["location-long"]),3)<minLong:
                    minLong=round(float(evento["location-long"]),3)

                if round(float(evento["location-lat"]),3)>maxLat:
                    maxLat=round(float(evento["location-lat"]),3)
                if round(float(evento["location-lat"]),3)<minLat:
                    minLat=round(float(evento["location-lat"]),3)
    mp.put(hashInfoLobos,"maxLat",maxLat)
    mp.put(hashInfoLobos,"minLat",minLat)
    mp.put(hashInfoLobos,"maxLong",maxLong)
    mp.put(hashInfoLobos,"minLong",minLong)
    return hashInfoLobos

def evaluarTiempo(movimiento,start,end):

    pertenece=False
    time1 = start + ":00"
    time2 = end + ":00"
    time1 = datetime.datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
    time2 = datetime.datetime.strptime(time2, "%Y-%m-%d %H:%M:%S")

    timeMov=movimiento["timestamp"] + ":00"
    timeMov=datetime.datetime.strptime(timeMov, "%Y-%m-%d %H:%M:%S")
    if timeMov>time1 and timeMov<time2:
        pertenece=True
    return pertenece

def calcularDistancia(listaMovimientos):
    distanciaTotal=0
    for i in range(0,lt.size(listaMovimientos)-2):
        long1=lt.getElement(listaMovimientos,i)["location-long"]
        lat1=lt.getElement(listaMovimientos,i)["location-lat"]
        long2=lt.getElement(listaMovimientos,i+1)["location-long"]
        lat2=lt.getElement(listaMovimientos,i+1)["location-lat"]
        distancia=dist(long1,lat1,long2,lat2)
        distanciaTotal+=distancia
    return round(distanciaTotal,3)

def evaluarTiempoYClima(event,start,end,min,max):

    pertenece=False
    time1 = start + ":00"
    time2 = end + ":00"
    time1 = datetime.datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
    time2 = datetime.datetime.strptime(time2, "%Y-%m-%d %H:%M:%S")

    timeMov=event["timestamp"] + ":00"
    timeMov=datetime.datetime.strptime(timeMov, "%Y-%m-%d %H:%M:%S")
    if timeMov>time1 and timeMov<time2 and float(event["external-temperature"])>min and float(event["external-temperature"])<max:
        pertenece=True
    return pertenece

def buscarInfo(analyzer,nodo):
    informacion=None
    allEvents=analyzer["allEvents"]
    for evento in lt.iterator(allEvents):
        if evento["formatoNodo"]==nodo:
            informacion=evento
    return informacion
