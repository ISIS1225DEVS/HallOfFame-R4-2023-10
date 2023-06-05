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
from DISClib.Utils import error as error
from haversine import haversine, Unit
from datetime import datetime
import sys

sys. setrecursionlimit(2**20)

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
    
    data_tracks: lista de tracks
    data_wolfs: lista de lobos
    connections: grafo con las especificaciones del reto
    wolf_map_by_track: mapa con los tracks de los lobos
    
    """
    #TODO: Inicializar las estructuras de datos
    
    try: 
    
        tracker = {
            
            'data_tracks': None,
            'data_wolfs': None,
            'connections': None,
            'wolf_map_by_track': None, 
            #'connections_not': None 
        }
        
        tracker['data_tracks'] = lt.newList('ARRAY_LIST', compareWolfID)
        
        tracker['data_wolfs'] = lt.newList('ARRAY_LIST', compareWolfID)
        
        tracker['wolf_map_by_track'] = mp.newMap(100, maptype='PROBING', cmpfunction=compareWolfID)
        
        tracker['connections'] = gr.newGraph(datastructure='ADJ_LIST', 
                                             directed=True, size=10000, cmpfunction=compareWolfID)
        
        #tracker['connections_not'] = gr.newGraph(datastructure='ADJ_LIST',
                                                      #directed= True, size=10000, cmpfunction=compareWolfID)
        tracker['Meet-Nodes'] = lt.newList('ARRAY_LIST')
        tracker['Wolf-Nodes'] = lt.newList('ARRAY_LIST')
        return tracker
    except Exception as exp:
        error.reraise(exp, 'model.new_tracker: Error creando el tracker de lobos')


# Funciones para agregar informacion al modelo (listas)

def add_data_tracks(tracker, data):
    """
    Adiciona un nuevo dato al modelo, lista del archivo de tracks
    """
    
    lt.addLast(tracker['data_tracks'], data)
    
    return None 

def add_data_wolfs(tracker, data):
    """
    Adiciona un nuevo dato al modelo, lista del archivo de wolfs
    """
    
    lt.addLast(tracker['data_wolfs'], data)
    
    return None

#-----------------------------------------------------------------------------

# Funciones para agregar informacion al modelo (mapas)

def addMAPIdTrack(tracker):
    '''
    
    Adiciona información a un mapa los tracks de los lobos
    
    '''
    
    data_wolf = tracker['data_wolfs']
    data_tracks = tracker['data_tracks']
    
    for wolf_lindo in lt.iterator(data_wolf):
        id_wolf_individual = createIndividualID(wolf_lindo)
        for track_lindo in lt.iterator(data_tracks):
            id_wolf_track = createIndividualID_tracks(track_lindo)
            if id_wolf_track == id_wolf_individual:
                addTrackMapIND(tracker, id_wolf_track, track_lindo)

def addTrackMapIND(tracker, id_individual, track):
    '''
    Adiciona  a una ubicacion un lobo al mapa correspondiente
    '''
        
    entry = mp.get(tracker['wolf_map_by_track'], id_individual)
    if entry is None:
        lst_track = lt.newList('ARRAY_LIST', compareWolfs)
        lt.addLast(lst_track, track)
        mp.put(tracker['wolf_map_by_track'], createIndividualID_tracks(track), lst_track)
    else:
        lst_track = entry['value']
        lt.addLast(lst_track, track)
    return tracker

def sortWolfTracksbyDate(tracker):
    
    mapa_tracks = tracker['wolf_map_by_track']
    
    ltKeys = mp.keySet(mapa_tracks)
    
    for key in lt.iterator(ltKeys):
        ltTracks = mp.get(mapa_tracks, key)['value']
        if lt.size(ltTracks) > 1:
            ltTracks = merg.sort(ltTracks, compareWolfTracksbyDate)
        mp.put(mapa_tracks, key, ltTracks)
    
    return mapa_tracks
    
def compareWolfTracksbyDate(track1, track2):
    
    date1 = track1['timestamp']
    date2 = track2['timestamp']
    
    #formato = '%d/%m/%Y %H:%M'
    formato = '%Y-%m-%d %H:%M'
    date1R = datetime.strptime(date1, formato)
    date2R = datetime.strptime(date2, formato)
    if date1R < date2R:
        return True
    if date1R == date2R:
        return compareDates3(track1,track2)
   
def compareWolfTracksbyDist(track1, track2):
    
    dist1 = track1[1]
    dist2 = track2[1]
    
    if dist1 > dist2:
        return True
    else:
        return False 

def compareDates3(track1, track2):
    """
    Compara dos fechas
    """
    
    formato = '%Y-%m-%d %H:%M'

    date1 = track1['timestamp']
    date2 = track2['timestamp']
    date1R = datetime.strptime(date1,formato)
    date2R = datetime.strptime(date2, formato)
    #if (date1R.date() == date2R.date()):
    #   return 0
    return (date1R < date2R)
 
#Creacion del grafo segun el pdf del reto
#Inciso (a)

def createIndividualID(wolf):
    '''
    
    Archivo: indidividuals
    
    Crear un ID único de cada lobo (<<individual-id>>) se propone unir el identificador del
    animal con el identificador del collar GPS con que se siguen a los animales <<animal-id>>_<<tagid>> 
    (ej.: de “32263B” y “32263” pasa a ser “32263B_32263”)
    
    '''
    final = ''
    animalID = wolf['animal-id']
    tagID = wolf['tag-id']
    
    final = animalID + '_' + tagID
    
    return final

def createIndividualID_tracks(track):
    
    '''
    
    Archivo: tracks
    
    Crear un ID único de cada lobo (<<individual-id>>) se propone unir el identificador del
    animal con el identificador del collar GPS con que se siguen a los animales <<animal-id>>_<<tagid>> 
    (ej.: de “32263B” y “32263” pasa a ser “32263B_32263”)
    
    '''
    
    final =''
    tag_local_identifier = track['tag-local-identifier']
    individual_local_identifier = track['individual-local-identifier']
    
    final = individual_local_identifier + '_' + tag_local_identifier
    
    return final



def roundCoords(data):
    
    long = data['location-long']
    lat = data['location-lat']
    
    long = long.replace('-', '')
    lat = lat.replace('-', '')
    
    long_lindo = float(long)
    lat_lindo = float(lat)
    
    roundLong = round(long_lindo, 3)
    roundLat = round(lat_lindo, 3)
    
    roundLong = str(roundLong)
    roundLat = str(roundLat)
    
    return roundLong, roundLat

#Funciones que formatean los datos para que se ajusten al reto

def createMeetingPoint(data):
    
    '''
    Los puntos de encuentro son espacios comunes frecuentados por distintos animales y definidos por
    la aproximación de los datos GPS (longitud y latitud) a la cuarta cifra decimal. Para identificar
    eficientemente estos puntos deben utilizar un ID compuesto teniendo en cuenta la longitud y latitud
    de este con el formato <<location-long>>_<<location-lat>>. (ej.: un evento con los datos de
    location-long: -115.792 y location-lat: 58.198, el identificador del vértice será “m115p792_58p198”).
    
    '''
    final = ''
    
    long, lat  = roundCoords(data)
    
    long = 'm'+ long.replace(".", "p")
    
    lat = lat.replace(".", "p")
    
    final = long + '_' + lat
    
    
    return final 
    
def createTrackPointID(data):
    '''
    
    Los puntos de seguimiento de los individuos son las posiciones (longitud y latitud) de cada uno de
    los lobos que pueden estar cerca de los puntos de encuentro. Para identificar cualquier vértice de
    seguimiento deben crear un ID compuesto teniendo en cuenta la longitud, la latitud y el identificador
    del animal con el formato <<location-long>>_<<location-lat>>_<<individual-id>>. (ej.:
    un evento con los datos de location-long: -115.792, location-lat: 58.198 e individual-id:
    35260_35260, el identificador del vértice será “m115p792_58p198_35260_35260”).
        
    '''
    final = ''
    
    long, lat  = roundCoords(data)
    

    
    long = 'm'+ long.replace(".", "p")
    
    lat = lat.replace(".", "p")
    
    wolfID = createIndividualID_tracks(data)
    
    final = long + '_' + lat + '_' + wolfID

    return final 




#--------------------------------------------------------------------------------
#Funcion para calcular distancia entre dos puntos

    

def calculateHarvesineDistance(origin, destination):
    
    '''
    Calcula la distancia entre dos puntos por medio de la fórmula de Harvesine
    
    '''
    
    latitudeLindo1 = float(origin['location-lat'])
    longitudeLindo1 = float(origin['location-long'])
    latitudeLindo2 = float(destination['location-lat'])
    longitudeLindo2 = float(destination['location-long'])
    
    point1 = (round(latitudeLindo1,3), round(longitudeLindo1,3))
    point2 = (round(latitudeLindo2,3), round(longitudeLindo2,3))
    
    distance = haversine(point1, point2)
    
    return distance

#--------------------------------------------------------------------------------

#Funcion para obtener el area del grafo

def getArea(tracker):
    
    data_tracks = tracker['data_tracks']
    
    minLat = 100000000000
    maxLat = -100000000000
    
    minLong = 100000000000
    maxLong = -100000000000
    
    for data in lt.iterator(data_tracks):
        lat = round(float(data['location-lat']), 3)
        long = round(float(data['location-long']),3)
        
        if lat > maxLat:
            maxLat = lat
        if lat < minLat:
            minLat = lat
        if long > maxLong:
            maxLong = long
        if long < minLong:
            minLong = long
    
    return maxLat, minLat, maxLong, minLong
        
def recortarLista(list):
    
    '''
    Funcion que retorna los primeros 5 y los ultimos 3 elementos de una lista dada.
    '''
    
    filtrado = lt.newList() #Lista que contiene las 3 primeras y las 3 ultimas
    first = lt.subList(list, 1, 5) #Mis tres primeros datos
    five_last =lt.size(list)-5 #Mis ultimos 3 datos  
    last = lt.subList(list, five_last+1, 5) #Sublista con los 3 ultimos 
    
    for element in lt.iterator(first): #Ciclo que une los tres primeros elementos
        lt.addLast(filtrado, element)
        
    for element in lt.iterator(last): #Ciclo que une los ultimos tres elementos
        lt.addLast(filtrado, element)
    return filtrado

def recortarListaThree(list):
    
    '''
    Funcion que retorna los primeros 5 y los ultimos 3 elementos de una lista dada.
    '''
    
    filtrado = lt.newList() #Lista que contiene las 3 primeras y las 3 ultimas
    first = lt.subList(list, 1, 3) #Mis tres primeros datos
    five_last =lt.size(list)-3 #Mis ultimos 3 datos  
    last = lt.subList(list, five_last+1, 3) #Sublista con los 3 ultimos 
    
    for element in lt.iterator(first): #Ciclo que une los tres primeros elementos
        lt.addLast(filtrado, element)
        
    for element in lt.iterator(last): #Ciclo que une los ultimos tres elementos
        lt.addLast(filtrado, element)
    return filtrado
        
def recortarLista2(list):
    
    '''
    Funcion que retorna los primeros 5 y los ultimos 5 elementos de una lista dada.
    '''
    
    filtrado = lt.newList() #Lista que contiene las 3 primeras y las 3 ultimas
    first = lt.subList(list, 1, 3) #Mis tres primeros datos
    five_last =lt.size(list)-3 #Mis ultimos 3 datos  
    last = lt.subList(list, five_last+1, 3) #Sublista con los 3 ultimos 
    
    for element in lt.iterator(first): #Ciclo que une los tres primeros elementos
        lt.addLast(filtrado, element)
        
    for element in lt.iterator(last): #Ciclo que une los ultimos tres elementos
        lt.addLast(filtrado, element)
    return filtrado



def firstFive(list):
    if len(list["elements"])>=5:
        filtrado = lt.newList('ARRAY_LIST')
        first = lt.subList(list, 1, 5)
        for element in lt.iterator(first):
            lt.addLast(filtrado, element)
        return filtrado
    else: 
        return list
#--------------------------------------------------------------------------------    
 
#Funciones para agregar nodos al grafo 
def addTrackNode(tracker):
    
    '''
    Adiciona a un punto de seguimiento como registo al grafo
    
    '''
    try:
        
        ltTracks = getTrackIDs(tracker)
        
        for ids in lt.iterator(ltTracks):
            if not gr.containsVertex(tracker['connections'], ids):
                gr.insertVertex(tracker['connections'], ids)
        track_nodes = gr.numVertices(tracker['connections'])
        
        return tracker, track_nodes 
    except Exception as exp:
        error.reraise(exp, 'model.add_wolf: Error al agregar un evento al grafo') 
        
def addMeetingNode(tracker):
    
    '''
    Adiciona los puntos de encuentro como nodos al grafo
    
    '''
    
    try:
        
        lista_ids = getMeetingPointsID(tracker)
        
        for id_meeting_point in lt.iterator(lista_ids):
            if not gr.containsVertex(tracker['connections'], id_meeting_point):
                gr.insertVertex(tracker['connections'], id_meeting_point)
                lt.addLast(tracker['Meet-Nodes'],id_meeting_point)
        return tracker
    
        
    except Exception as exp:
        error.reraise(exp, 'model.add_wolf: Error al agregar un punto de encuentro al grafo')

#--------------------------------------------------------------------------------

#Funciones auxiliares para la creacion de los nodos
def hashMeetingPoints(tracker):
    
    '''
    Se crea un mapa con los puntos de encuentro de los lobos
    
    '''
    
    meetingPoints_map = mp.newMap(100, maptype='PROBING', cmpfunction=compareWolfID)
    
    for data in lt.iterator(tracker['data_tracks']):
        meetingPoint = createMeetingPoint(data)
        entry = mp.get(meetingPoints_map, meetingPoint)
        if entry is None:
            contador = 1   
            ltWolf = lt.newList('ARRAY_LIST')
            lt.addLast(ltWolf, data['tag-local-identifier'])
        
            mp.put(meetingPoints_map, meetingPoint, (contador, ltWolf))
        else:
            contador_f = entry['value'][0]
            contador_f += 1
            ltwolf_f = entry['value'][1]
            lt.addLast(ltwolf_f, data['tag-local-identifier'])
            mp.put(meetingPoints_map, meetingPoint, (contador_f, ltwolf_f))
        
    return meetingPoints_map


def getMeetingPointsID(tracker):
    
    mapa = hashMeetingPoints(tracker)
    keys = mp.keySet(mapa)
    
    listaIds = lt.newList('ARRAY_LIST')
    
    for llave in lt.iterator(keys):
        ltwolf = mp.get(mapa, llave)['value'][1]
        if lt.size(ltwolf) >= 2:
            firstWolf = lt.firstElement(ltwolf)
            lt.removeFirst(ltwolf)
            for wolf in lt.iterator(ltwolf):
                if wolf != firstWolf:
                    if lt.isPresent(listaIds, llave) == 0:
                        lt.addLast(listaIds, llave)
    return listaIds



def getTrackIDs(tracker):
    
    '''
    Funcion que retorna una lista con los ids de los trayectos de los lobos

    Parametro: tracker
    
    Lee la lista de los datos de los trayectos de los lobos
    
    Retorna: listaIds
    
    Lista con los ids de los trayectos de los lobos, en el formato "m115p792_58p198_35260_35260"
    '''
    
    listaIds = lt.newList('ARRAY_LIST')
    
    for data in lt.iterator(tracker['data_tracks']):
        trackID = createTrackPointID(data)
        
        if trackID not in listaIds['elements']:
        
            lt.addLast(listaIds, trackID)
        else:
            pass
    
    return listaIds

#--------------------------------------------------------------------------------

#Funciones para agregar arcos al grafo


def connectWolfPoints(tracker): #Optimizar FIXME
    
    '''
    Funcion que conecta dos tracking points de un mismo lobo
    
    Parametros: tracker
    
    Donde el tracker ya contiene los vértices de los meeting point y tracking points.
    
    Retorna: tracker
    
    Donde el tracker ya contiene los arcos de los tracking points y todo lo mencionado previamente.

    '''
    #Mapa de lobos-tracks, donde la llave es el individual id y el valor es una lista de los tracks de ese lobo
    map_wolf_tracks = sortWolfTracksbyDate(tracker) 
    
    ltKeys = mp.keySet(map_wolf_tracks) #Lista de llaves del mapa
    
    for wolf in lt.iterator(ltKeys):
        ltTracks = mp.get(map_wolf_tracks, wolf)['value'] #Lista de tracks de un lobo
        if lt.size(ltTracks) > 1:
            for i in range(lt.size(ltTracks) - 1):
                track1 = lt.getElement(ltTracks, i)
                track2 = lt.getElement(ltTracks, i + 1)
                track1_lindo = createTrackPointID(track1)
                track2_lindo = createTrackPointID(track2)
                if track1_lindo != track2_lindo:
                    gr.addEdge(tracker['connections'], track1_lindo, track2_lindo, calculateHarvesineDistance(track1, track2))
    return tracker

def connectMeetingPoints(tracker): #En mis libros está bien y funciona lindo
    
    '''
    Función que conecta bidireccionalmente los puntos de encuentro 
    de dos lobos que alguna vez se han encontrado en una ubicación dada sin importar el tiempo.
    
    Parametros: tracker
    
    Donde el tracker ya contiene los vértices de los meeting point y tracking point junto con los arcos de los 
    tracking points.
    
    Retorna: tracker
    
    Donde el tracker ya contiene los arcos de los meeting points y todo lo mencionado previamente.
    
    ''' 
    
    ltMeetingPoints = getMeetingPointsID(tracker) #Lista de los meeting points existentes
    
    ltTrackingPoints = getTrackIDs(tracker) #Lista de los tracking points existentes
    for meeting_point in lt.iterator(ltMeetingPoints):
        for track in lt.iterator(ltTrackingPoints):
            track_lindo = getMeetingPointFromTrackingPoint(track) #Obtener el meeting point de un tracking point

            if meeting_point == track_lindo:
                gr.addEdge(tracker['connections'], track, meeting_point, 0)
                gr.addEdge(tracker['connections'], meeting_point, track, 0)
    #meeting_edges = gr.numEdges(tracker['connections'])

    return tracker#, meeting_edges
def countMeeting_edges(tracker):
    ltArcs = gr.edges(tracker['connections'])
    count = 0
    for i in lt.iterator(ltArcs):
        if i['weight'] == 0:
            count +=1
    return count


def getMeetingPointFromTrackingPoint(trackID):
    
    '''
    
    Función que obtiene el meeting point de un tracking point, es decir la ubicación del track de ese lobo
    en el formato de los meeting points.
    
    Parametro:
    
    TrackID: ID del punto de seguimiento en el formato "m115p792_58p198_35260_35260"
    
    retorna: ID del punto de encuentro de ese punto de seguimiento en el formato "m115p792_58p198"
    
    '''
    
    final = ''
    
    track_splt = trackID.split('_')
    
    final = track_splt[0] + '_' + track_splt[1]
    
    return final

#-------------------------------------------------------------------------------------------    
#Funciones para obtener la información del grafo

#Funcion para obtener la información de nodos y arcos del grafo

def getGraphInformation(tracker):
    
    
    node_list = gr.vertices(tracker['connections'])
    
    ltAns = lt.newList('ARRAY_LIST')
    
    for node in lt.iterator(node_list):
        ltNode = lt.newList('ARRAY_LIST')
        flag = meetingOrTracking(node)
        if flag == True:
            coords = getLocationFromNode(node)
            individual = getIndividualFromNode(node)
            adjacents = gr.adjacents(tracker['connections'], node)
            size = lt.size(adjacents)
            lt.addLast(ltNode, coords[0])
            lt.addLast(ltNode, coords[1])
            lt.addLast(ltNode, node)
            lt.addLast(ltNode, individual)
            lt.addLast(ltNode, size)
            lt.addLast(ltAns, ltNode)
        else:
            coords = getLocationFromNode(node)
            adjacents = gr.adjacents(tracker['connections'], node)
            size = lt.size(adjacents)
            lt.addLast(ltNode, coords[0])
            lt.addLast(ltNode, coords[1])
            lt.addLast(ltNode, node)
            for mini_node in lt.iterator(adjacents):
                individual = mini_node
            lt.addLast(ltNode, individual)
            lt.addLast(ltNode, size)
            lt.addLast(ltAns, ltNode)
        
        
    lt.addLast(ltAns, ltNode)   
    
    


    return ltAns 

def meetingOrTracking(node):
    
    contador = node.count('_')
    
    if contador == 1:
        return False
    else:
        return True

def getLocationFromNode(node):
    
    long = ''
    lat = ''
    
    node_lindo = node.replace('m', '-')
    node_lindo = node_lindo.replace('p', '.')
    node_lindo = node_lindo.split('_')
    
    long = node_lindo[0]
    lat = node_lindo[1]

        
    return long, lat
    
def getIndividualFromNode(node):
    node_lindo = node.split('_')
    individual = ''
    
    individual = node_lindo[2] + '_' + node_lindo[3]

    
    return individual
    
# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


def compareWolfID(wolf, keyValuesWolf):
    """
    Funcion para comparar dos lobos 
    """
    wolfCode = keyValuesWolf['key']
    
    if (wolf == wolfCode):
        return 0
    elif (wolf > wolfCode):
        return 1
    else:
        return -1
    

def compareWolfs(wolf1, wolf2):
    """
    Funcion para comparar dos lobos 
    """
    wolfCode1 = wolf1['animal-id']
    wolfCode2 = wolf2['animal-id']
    
    if (wolfCode1 == wolfCode2):
        return 0
    elif (wolfCode1 > wolfCode2):
        return 1
    else:
        return -1

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


def req_1(tracker, meeting_point1 , meeting_point2):
    """
    Función que soluciona el requerimiento 1 (Usar DFS)
    """
    # TODO: Realizar el requerimiento 1
    
    dfs_structure = dfs.DepthFirstSearch(tracker['connections'], meeting_point1)
    
    flag = dfs.hasPathTo(dfs_structure, meeting_point2)
    
    if flag:
        ltpath_st = dfs.pathTo(dfs_structure, meeting_point2)
        
    ltpath = lt.newList("ARRAY_LIST")
    while st.isEmpty(ltpath_st)!=True:
        a = st.pop(ltpath_st)
        lt.addLast(ltpath,a)
        
    
    nWolf = 0
    nMeet = 0 
    disttot = 0 
    r1 = lt.newList('ARRAY_LIST')
    cont = 1
    for i in lt.iterator(ltpath):
        ltrow = lt.newList('ARRAY_LIST')
        if i.count("_") == 1:
            nMeet += 1 
        else:
            nWolf += 1
        long, lat = revertirfromato(i)
        wolfs_str, wolfs = getWolfFromNode(tracker, i)
        indCount = lt.size(wolfs) 
        if cont == lt.size(ltpath):
            edgeTo = 'Unknown'
        else:
           edgeTo = lt.getElement(ltpath, cont + 1)
           
        if edgeTo != 'Unknown':
            dist = round((gr.getEdge(tracker['connections'], i, edgeTo))['weight'],3)
            disttot+= dist 
        else:
            dist = 'Unknown'
         
        #headers = ['lat', 'long', 'id', 'indi ids', 'wolf count','edge-to', 'dist']
        lt.addLast(ltrow,(long))
        lt.addLast(ltrow,(lat))
        lt.addLast(ltrow,(i))
        lt.addLast(ltrow,(wolfs_str))
        lt.addLast(ltrow,(indCount))
        lt.addLast(ltrow,(edgeTo))
        lt.addLast(ltrow,(dist))

        lt.addLast(r1,ltrow)
        cont += 1
    r2 = recortarLista(r1)
    return r2, flag, nWolf, nMeet, disttot
        

def revertirfromato(node):
    nodelt = node.split('_')
    nodelt[0]=nodelt[0].replace('p', '.')
    nodelt[0]=nodelt[0].replace('m', '-')
    nodelt[1]=nodelt[1].replace('p', '.')
    nodelt[1]=nodelt[1].replace('m', '-')
    long = nodelt[0]
    lat = nodelt[1]
    return long, lat

def getWolfFromNode(tracker, node):
    conectWolf = gr.adjacents(tracker['connections'],node)
    ret = ""
    ret2 = lt.newList()
    for i in lt.iterator(conectWolf):
        parts = i.split('_')
        if len(parts)==4:
            wolf = parts[2]+"_"+parts[3]
            if ret != "":
                ret= ret+", "+wolf
            else:
                ret = wolf
            lt.addLast(ret2, wolf)   
        if len(parts)==5:
            wolf = parts[2]+"_"+parts[3]+"_"+parts[4]
            if ret != "":
                ret= ret+", "+wolf
            else:
                ret = wolf
            lt.addLast(ret2, wolf)
    return ret, ret2
 
def listaFromMap(mapa):
    '''
    Crea una lista desde el mapa
    '''
    respuesta2 = lt.newList('ARRAY_LIST')
    llaves = mp.keySet(mapa)
    for llave in lt.iterator(llaves):
        if llave != None:
            valor = (llave, me.getValue(mp.get(mapa, llave)))
            lt.addLast(respuesta2, valor)
    return respuesta2 
 
        
def req_2(tracker, meeting_point1 , meeting_point2):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    bfs_structure = bfs.BreadhtFisrtSearch(tracker['connections'], meeting_point1)
    
    flag = bfs.hasPathTo(bfs_structure, meeting_point2)
    
    if flag:
        ltpath_st = bfs.pathTo(bfs_structure, meeting_point2)
    
    ltpath = lt.newList("ARRAY_LIST")
    while st.isEmpty(ltpath_st)!=True:
        a = st.pop(ltpath_st)
        lt.addLast(ltpath,a)
        
    
    nWolf = 0
    nMeet = 0 
    disttot = 0 
    r1 = lt.newList('ARRAY_LIST')
    cont = 1
    for i in lt.iterator(ltpath):
        ltrow = lt.newList('ARRAY_LIST')
        if i.count("_") == 1:
            nMeet += 1 
        else:
            nWolf += 1
        long, lat = revertirfromato(i)
        wolfs_str, wolfs = getWolfFromNode(tracker, i)
        indCount = lt.size(wolfs) 
        if cont == lt.size(ltpath):
            edgeTo = 'Unknown'
        else:
           edgeTo = lt.getElement(ltpath, cont + 1)
           
        if edgeTo != 'Unknown':
            dist = round((gr.getEdge(tracker['connections'], i, edgeTo))['weight'],3)
            disttot+= dist 
        else:
            dist = 'Unknown'
         
        #headers = ['lat', 'long', 'id', 'indi ids', 'wolf count','edge-to', 'dist']
        lt.addLast(ltrow,(long))
        lt.addLast(ltrow,(lat))
        lt.addLast(ltrow,(i))
        lt.addLast(ltrow,(wolfs_str))
        lt.addLast(ltrow,(indCount))
        lt.addLast(ltrow,(edgeTo))
        lt.addLast(ltrow,(dist))

        lt.addLast(r1,ltrow)
        cont += 1
    r2 = recortarLista(r1)
    return r2, flag, nWolf, nMeet, disttot


def req_3(tracker):
    """
    Paramétros: El tracker de los lobos
    
    Como guardabosques del área deseo conocer los territorios de las manadas8 de lobos presentes dentro del
    hábitat del bosque. Cuantas manadas existen, quienes son sus miembros, sus características, los puntos de
    encuentro que frecuentan y las posiciones que dominan.
    
    Retorna: Estructura de datos que contiene las manadas, cantidad de elementos fuertemente conectados del grafo
    
    
    """
    data_wolf = tracker['data_wolfs']
    
    kosarajuMap = scc.KosarajuSCC(tracker['connections'])

    ltNodes = mp.keySet(kosarajuMap['idscc'])

    connectedComponents = scc.connectedComponents(kosarajuMap)
    
    mapaComponentes = mp.newMap(1000, maptype='PROBING', cmpfunction=compareWolfID)
    
    for node in lt.iterator(ltNodes):
        componentID = mp.get(kosarajuMap['idscc'], node)['value']
        entry = mp.get(mapaComponentes, componentID)
        if entry is None:
            ltNode = lt.newList('ARRAY_LIST')
            lt.addLast(ltNode, node)
            
            mp.put(mapaComponentes, componentID, ltNode)
        else:
            ltNode = entry['value']
            lt.addLast(ltNode, node)
            mp.put(mapaComponentes, componentID, ltNode)
            

    ltComponentes = listaFromMap(mapaComponentes)
    
    componentSorted = merg.sort(ltComponentes, compareSize)
    
    ltFinal = lt.newList('ARRAY_LIST')
    
    for component in lt.iterator(componentSorted):
        ltComponent =lt.newList('ARRAY_LIST')
        componentIdentificator, ltStrongNodes = component
        lt.addLast(ltComponent, componentIdentificator) #(ID de la manada)
        lt.addLast(ltComponent, ltStrongNodes) #Lista de nodos fuertemente conectados (manada)    
        size = lt.size(ltStrongNodes) #Cantidad de nodos fuertemente conectados (manada)
        lt.addLast(ltComponent, size) 

        maxLat = -100000000000
        minLat = 100000000000
        
        maxLong = -100000000000
        minLong = 100000000000
        
        wolfCount = 0
        
        ltIndividuals = lt.newList('ARRAY_LIST')
        
        
        for node in lt.iterator(ltStrongNodes):
            
            coords = getLocationFromNode(node)
            
            long = float(coords[0])
            lat = float(coords[1])
            
            if long > maxLong:
                maxLong = long
            if long < minLong:
                minLong = long
            if lat > maxLat:
                maxLat = lat
            if lat < minLat:
                minLat = lat
            
            
            flag = meetingOrTracking(node)
            
            if flag:
                individual = getIndividualFromNode(node)
            
                if lt.isPresent(ltIndividuals, individual) == 0:
                    lt.addLast(ltIndividuals, individual)
                    wolfCount += 1
        
        lt.addLast(ltComponent, minLat)
        lt.addLast(ltComponent, maxLat)
        lt.addLast(ltComponent, minLong)
        lt.addLast(ltComponent, maxLong)
        lt.addLast(ltComponent, wolfCount)
        ltIndividuosComponent = lt.newList('ARRAY_LIST')
        for individuo in lt.iterator(ltIndividuals):
            
            
            individuo_split = individuo.split('_')
            individuo_animalID = individuo_split[0]
            individuo_tagID = individuo_split[1]
            
            for wolf in lt.iterator(data_wolf):
                wolf_animalID = wolf['animal-id']
                wolf_tagID = wolf['tag-id']
                
                if (wolf_animalID == individuo_animalID) and (wolf_tagID == individuo_tagID):
                    ltSingleWolf = lt.newList('ARRAY_LIST')
                    lt.addLast(ltSingleWolf, individuo)
                    sex = wolf['animal-sex']
                    life_stage = wolf['animal-life-stage']
                    study_site = wolf['study-site'] 
                    comments = wolf['deployment-comments']
                    if sex == '':
                        sex = 'Unknown'
                    if life_stage == '':
                        life_stage = 'Unknown'
                    if study_site == '':
                        study_site = 'Unknown'
                    if comments == '':
                        comments = 'Unknown'
                    
                    lt.addLast(ltSingleWolf, sex)
                    lt.addLast(ltSingleWolf, life_stage)
                    lt.addLast(ltSingleWolf, study_site)
                    lt.addLast(ltSingleWolf, comments)
                    lt.addLast(ltIndividuosComponent, ltSingleWolf)
        lt.addLast(ltComponent, ltIndividuosComponent)
        
            
        lt.addLast(ltFinal, ltComponent)



    return ltFinal, connectedComponents, kosarajuMap,ltComponentes
def compareSize(lista1, lista2):
    
    lista1 = lista1[1]
    lista2 = lista2[1]
    
    size1 = lt.size(lista1)
    size2 = lt.size(lista2)
    

    if size1 > size2:
        return True
    if size1 == size2:
        return compareSize2(lista1,lista2)
    

def compareSize2(lista1, lista2): 
    """
    Compara dos fechas
    """
    

    
    size1 = lt.size(lista1)
    size2 = lt.size(lista2)


    return (size1 < size2)





def req_4(tracker,origen,destino):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    NodoMascercano_O, distMin1 = NodoMascercano(tracker,origen)
    NodoMascercano_D, distMin2 = NodoMascercano(tracker,destino)
    
    bfs_structure = djk.Dijkstra(tracker['connections'], NodoMascercano_O)
    
    flag = djk.hasPathTo(bfs_structure, NodoMascercano_D)
    
    if flag:
        ltpath_st = djk.pathTo(bfs_structure, NodoMascercano_D)
    
    ltpath = lt.newList("ARRAY_LIST")
    while st.isEmpty(ltpath_st)!=True:
        a = st.pop(ltpath_st)
        lt.addLast(ltpath,a)
        
    tablaOrigen = lt.newList("ARRAY_LIST")
    longO, latO = revertirfromato(NodoMascercano_O)
    lt.addLast(tablaOrigen,NodoMascercano_O)
    lt.addLast(tablaOrigen,longO)
    lt.addLast(tablaOrigen,latO)
    lt.addLast(tablaOrigen,  getWolfFromNode(tracker, NodoMascercano_O)[0])
    
    tabladestino = lt.newList("ARRAY_LIST")
    longD, latD = revertirfromato(NodoMascercano_D)
    lt.addLast(tabladestino,NodoMascercano_D)
    lt.addLast(tabladestino,longD)
    lt.addLast(tabladestino,latD)
    lt.addLast(tabladestino,  getWolfFromNode(tracker, NodoMascercano_D)[0])
    
    nWolf = 0
    nMeet = 0 
    disttot = 0 
    #numWolfInds = 0
    r1 = lt.newList('ARRAY_LIST')
    r3 = lt.newList('ARRAY_LIST')
    listaNodos = lt.newList('ARRAY_LIST')

    for i in lt.iterator(ltpath):
        actual = i['vertexA']
        edgeTo = i['vertexB']
       
        if lt.isPresent(listaNodos,actual) == False:
            lt.addLast(listaNodos,actual)
        if lt.isPresent(listaNodos,edgeTo) == False:
            lt.addLast(listaNodos,edgeTo)
        
        ltrow = lt.newList('ARRAY_LIST')
       
        long, lat = revertirfromato(actual)
        wolfs_str, wolfs = getWolfFromNode(tracker, actual)
        indCount = lt.size(wolfs) 

        edgeTolat,edgeToLog = revertirfromato(edgeTo)
           
        dist = i['weight']
        disttot+= dist 
        
        #headers = ['lat', 'long', 'id', 'indi ids', 'wolf count','edge-to', 'dist']
        lt.addLast(ltrow,(actual))
        lt.addLast(ltrow,(long))
        lt.addLast(ltrow,(lat))
        lt.addLast(ltrow,(edgeTo))
        lt.addLast(ltrow,(edgeToLog))
        lt.addLast(ltrow,(edgeTolat))
        lt.addLast(ltrow,(dist))
        lt.addLast(r1,ltrow)

    for i in lt.iterator(listaNodos):
        ltrow2 = lt.newList('ARRAY_LIST')
        long, lat = revertirfromato(i)
        wolfs_str, wolfs = getWolfFromNode(tracker, i)
        indCount = lt.size(wolfs) 
    
        lt.addLast(ltrow2,(i))
        lt.addLast(ltrow2,(long))
        lt.addLast(ltrow2,(lat))
        lt.addLast(ltrow2,(wolfs_str))
        lt.addLast(ltrow2,(indCount))
        lt.addLast(r3,ltrow2)
        
    r2 = recortarLista2(r1)
    r4 = recortarLista2(r3)
    return NodoMascercano_O, tablaOrigen, distMin1, NodoMascercano_D, tabladestino, distMin2,r2, nWolf, nMeet, disttot, r4
    

def NodoMascercano(tracker, nodoA):
    nodos = tracker['Meet-Nodes']
    DistMin = 1_000_000
    MasCercano = ""
    for i in lt.iterator(nodos):
        long1, lat1 = revertirfromato(i)
        nodoB = (float(lat1),float(long1))
        dist_to = haversine(nodoA,nodoB)
        if dist_to < DistMin:
            MasCercano = i
            DistMin = dist_to
    return MasCercano, DistMin

def req_5(data_structs, origen, maxdist, minMP):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    datos=data_structs["connections"]
    maxdist=maxdist/2
    mst=prim.PrimMST(datos,origen)
    dist=0
    visitados=lt.newList("ARRAY_LIST")
    actual=origen
    listatree=om.valueSet(mst["edgeTo"])
   
    for i in lt.iterator(listatree):
        format=i["vertexA"].split("_")
        nodof="_".join(format[:2])
        if nodof==actual:
            lt.addLast(visitados,i["vertexB"])
            actual=i["vertexB"]
            dist+=i["weight"]
        if dist>=maxdist or lt.size(visitados)>=minMP: 
            break          
    vislist=visitados["elements"]
    return vislist, dist

    

def req_6(tracker,FechaI_raw, FechaF_raw, Sex):
    """
    Función que soluciona el requerimiento 6
    """ 
    # TODO: Realizar el requerimiento 6
    formato = '%Y-%m-%d %H:%M'
    FechaI = datetime.strptime(FechaI_raw, formato)
    FechaF = datetime.strptime(FechaF_raw, formato)
    
    wolfs_TOT = tracker['data_wolfs']
    wolf_sex = lt.newList('ARRAY_LIST')
    for i in lt.iterator(wolfs_TOT):
        AnimalSex = i['animal-sex']
        if AnimalSex == Sex:
            lt.addLast(wolf_sex, i)
    
    wolf_tracks_TOT = tracker['data_tracks']
    wolf_tracks_Dates = lt.newList('ARRAY_LIST')
    for i in lt.iterator(wolf_tracks_TOT):
        date = i['timestamp']
        #formato = '%d/%m/%Y %H:%M'
        formato = '%Y-%m-%d %H:%M'
        date1 = datetime.strptime(date, formato)  
        if FechaI < date1 and date1 < FechaF:
            lt.addLast(wolf_tracks_Dates, i)
    
    wolfMap_new = mp.newMap(100, maptype='PROBING', cmpfunction=compareWolfID)
    
    for wolf_lindo in lt.iterator(wolf_sex):
        id_wolf_individual = createIndividualID(wolf_lindo)
        for track_lindo in lt.iterator(wolf_tracks_Dates):
            id_wolf_track = createIndividualID_tracks(track_lindo)
            if id_wolf_track == id_wolf_individual:
                addTrackMapReq6(wolfMap_new, id_wolf_track, track_lindo)

    wolfMap_new = sortWolfTracksbyDateReq6(wolfMap_new)
    
    wolfByDist = lt.newList('ARRAY_LIST')
    WolfKeys = mp.keySet(wolfMap_new)
    
    for i in lt.iterator(WolfKeys):
        wolfDist = wolf_dist(i,wolfMap_new)
        thing = (i, wolfDist)
        lt.addLast(wolfByDist, thing)
        
    wolfByDist = merg.sort(wolfByDist, compareWolfTracksbyDist)

    wolfmxInfo = lt.newList('ARRAY_LIST')
    wolfminInfo = lt.newList('ARRAY_LIST')
    wolfmax = lt.getElement(wolfByDist, 1)
    wolfmix = lt.getElement(wolfByDist, lt.size(wolfByDist))
    
    wolfMAXRuteRaw = lt.newList('ARRAY_LIST')
    wolfMINRuteRaw = lt.newList('ARRAY_LIST')
    
    for i in lt.iterator(wolf_sex):
        if createIndividualID(i) == wolfmax[0]:
            lt.addLast(wolfmxInfo,wolfmax[0])
            lt.addLast(wolfmxInfo,i['animal-taxon'])
            lt.addLast(wolfmxInfo,i['animal-life-stage'])
            lt.addLast(wolfmxInfo,i['study-site'])
            lt.addLast(wolfmxInfo,wolfmax[1])
            lt.addLast(wolfmxInfo,i['deployment-comments'])
            
            
        if createIndividualID(i) == wolfmix[0]:
            lt.addLast(wolfminInfo,wolfmix[0])
            lt.addLast(wolfminInfo,i['animal-taxon'])
            lt.addLast(wolfminInfo,i['animal-life-stage'])
            lt.addLast(wolfminInfo,i['study-site'])
            lt.addLast(wolfminInfo,wolfmix[1])
            lt.addLast(wolfminInfo,i['deployment-comments'])
            
    wolfMaxTracks  = mp.get(wolfMap_new,wolfmax[0])['value'] 
    wolfMinTracks  = mp.get(wolfMap_new,wolfmix[0])['value'] 
        
    for i in lt.iterator(wolfMaxTracks):
        fila = lt.newList('ARRAY_LIST')
        lt.addLast(fila, createTrackPointID(i))
        lt.addLast(fila, i['location-long'])
        lt.addLast(fila, i['location-lat'])
        lt.addLast(fila, wolfmax[0])
        lt.addLast(fila, 1)
        lt.addLast(wolfMAXRuteRaw,fila)
        
    for i in lt.iterator(wolfMinTracks):
        fila = lt.newList('ARRAY_LIST')
        lt.addLast(fila, createTrackPointID(i))
        lt.addLast(fila, i['location-long'])
        lt.addLast(fila, i['location-lat'])
        lt.addLast(fila, wolfmix[0])
        lt.addLast(fila, 1)
        lt.addLast(wolfMINRuteRaw,fila)
        
    nodesRMAX = lt.size(wolfMAXRuteRaw)    
    nodesRMIN= lt.size(wolfMINRuteRaw)
    
    if nodesRMAX > 6:
        wolfMAXRute = recortarLista2(wolfMAXRuteRaw)
    else:
        wolfMAXRute = wolfMAXRuteRaw
    
    if nodesRMIN > 6:    
        wolfMINRute = recortarLista2(wolfMINRuteRaw)
    else:
        wolfMINRute = wolfMINRuteRaw
    
    return wolfmax, wolfmix, wolfmxInfo, wolfminInfo, nodesRMAX, nodesRMIN, wolfMAXRute ,wolfMINRute 

def addTrackMapReq6(wolfMap_new, id_individual, track):
    '''
    Adiciona  a una ubicacion un lobo al mapa correspondiente
    '''
    entry = mp.get(wolfMap_new, id_individual)
    if entry is None:
        lst_track = lt.newList('ARRAY_LIST', compareWolfs)
        lt.addLast(lst_track, track)
        mp.put(wolfMap_new, createIndividualID_tracks(track), lst_track)
    else:
        lst_track = entry['value']
        lt.addLast(lst_track, track)
    return wolfMap_new

def sortWolfTracksbyDateReq6(wolfMap_new):
        
    ltKeys = mp.keySet(wolfMap_new)
    
    for key in lt.iterator(ltKeys):
        ltTracks = mp.get(wolfMap_new, key)['value']
        if lt.size(ltTracks) > 1:
            ltTracks = merg.sort(ltTracks, compareWolfTracksbyDate)
        mp.put(wolfMap_new, key, ltTracks)
    
    return wolfMap_new

def wolf_dist(key, wolfMap_new):
    dist_tot = 0
    cont = 1
    wolf_list = mp.get(wolfMap_new, key)['value']
    for i in lt.iterator(wolf_list):
        long_act = i['location-long']
        lat_act = i['location-lat']
        pointA = (round(float(lat_act),3), round(float(long_act),3))
        if cont != lt.size(wolf_list):
            next_track = lt.getElement(wolf_list, cont+1) 
            long_next =next_track['location-long'] 
            lat_next = next_track['location-lat']
            pointB = (round(float(lat_next),3), round(float(long_next),3))
            dist =  haversine(pointA, pointB)
            dist_tot += dist
        cont +=1 
    return dist_tot

def req_7(tracker, dateStart, dateEnd, minTemp, maxTemp):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    
    dateStart = fechaLinda(dateStart)
    dateEnd = fechaLinda(dateEnd)
    
    data_tracks = tracker['data_tracks']
    
    data_wolf = tracker['data_wolfs']
    
    ltTracksFiltered = lt.newList('ARRAY_LIST')
    
    #Filtro de información para que tenga los parametros de fecha y temperatura
    
    for track in lt.iterator(data_tracks):
        
        date = track['timestamp']
        date = fechaLinda(date)
        
        if dateStart <= date <= dateEnd and minTemp <= track['external-temperature'] <= maxTemp:
            lt.addLast(ltTracksFiltered, track)
        else:
            pass

    #Creación del grafo

    graphManadas = gr.newGraph(datastructure="ADJ_LIST",
             directed=True,
             size=1000,
             cmpfunction=None)
    
    #Creacion del mapa auxiliar
    
    mapaManadas = mp.newMap(1000, maptype='PROBING', cmpfunction=compareWolfID)
    
    #Creación de los nodos
    
    #Tracking points
    
    listatrackIDS = getTrackIDsReq7(ltTracksFiltered) #Lista de los ids de los trayectos de los lobos
    
    listaMPIDs = getMeetingPointsIDReq7(ltTracksFiltered) #Lista de los ids de los puntos de encuentro de los lobos
    
    graphManadas_pt1 = addTrackNodeReq7(graphManadas, listatrackIDS) #Adiciona los nodos de los trayectos de los lobos al grafo
    
    #Meeting points
    
    listaMeetingPoints = getMeetingPointsIDReq7(ltTracksFiltered) #Lista de los ids de kos trayectos de los lobos
    
    graphManadas_tuple = addMeetingNodeReq7(graphManadas_pt1, listaMeetingPoints) #Adiciona los nodos de los puntos de encuentro al grafo
    

    
    #Creación de los arcos
        
    addMAPIdTrackReq7(mapaManadas, data_wolf, ltTracksFiltered) #Adiciona los tracks de los lobos al mapa
    
    graphManadas_Connected = connectWolfPointsReq7(graphManadas_tuple, mapaManadas) #Conecta los puntos de seguimiento de los lobos
    
    graphManadas_Final = connectMeetingPointsReq7(graphManadas_Connected, listaMPIDs, data_tracks) #Conecta los puntos de encuentro de los lobos
    
    #Fin de la creación del grafo
    
    #Elementos para la impresión
    
    numVertex = gr.numVertices(graphManadas_Final)
    numArcos = gr.numEdges(graphManadas_Final)
    
    #Reconocimiento de los componentes fuertmente conectados de las manadas
    
    mapaKosaraju_Manadas = scc.KosarajuSCC(graphManadas_Final)
    
    ltStrongNodes_Manadas = mp.keySet(mapaKosaraju_Manadas['idscc'])
    
    connectedComponents_Manadas = scc.connectedComponents(mapaKosaraju_Manadas)
    
    mapaComponentes = mp.newMap(1000, maptype='PROBING', cmpfunction=compareWolfID)
    
    for node in lt.iterator(ltStrongNodes_Manadas):
        componentID = mp.get(mapaKosaraju_Manadas['idscc'], node)['value']
        entry = mp.get(mapaComponentes, componentID)
        if entry is None:
            ltNode = lt.newList('ARRAY_LIST')
            lt.addLast(ltNode, node)
            mp.put(mapaComponentes, componentID, ltNode)
        else:
            ltNode = entry['value']
            lt.addLast(ltNode, node)
            mp.put(mapaComponentes, componentID, ltNode)
            
    
    ltComponentes = listaFromMap(mapaComponentes)
    
    componentSorted = merg.sort(ltComponentes, compareSize)
    
    ltFinal = lt.newList('ARRAY_LIST')
    
    for component in lt.iterator(componentSorted):
        ltComponent =lt.newList('ARRAY_LIST')
        componentIdentificator, ltStrongNodes = component
        lt.addLast(ltComponent, componentIdentificator) #(ID de la manada)
        lt.addLast(ltComponent, ltStrongNodes) #Lista de nodos fuertemente conectados (manada)    
        size = lt.size(ltStrongNodes) #Cantidad de nodos fuertemente conectados (manada)
        lt.addLast(ltComponent, size) 

        maxLat = -100000000000
        minLat = 100000000000
        
        maxLong = -100000000000
        minLong = 100000000000
        
        wolfCount = 0
        
        ltIndividuals = lt.newList('ARRAY_LIST')
        
        
        for node in lt.iterator(ltStrongNodes):
            
            coords = getLocationFromNode(node)
            
            long = float(coords[0])
            lat = float(coords[1])
            
            if long > maxLong:
                maxLong = long
            if long < minLong:
                minLong = long
            if lat > maxLat:
                maxLat = lat
            if lat < minLat:
                minLat = lat
            
            
            flag = meetingOrTracking(node)
            
            if flag:
                individual = getIndividualFromNode(node)
            
                if lt.isPresent(ltIndividuals, individual) == 0:
                    lt.addLast(ltIndividuals, individual)
                    wolfCount += 1
        
        lt.addLast(ltComponent, minLat)
        lt.addLast(ltComponent, maxLat)
        lt.addLast(ltComponent, minLong)
        lt.addLast(ltComponent, maxLong)
        lt.addLast(ltComponent, wolfCount)
        ltIndividuosComponent = lt.newList('ARRAY_LIST')
        for individuo in lt.iterator(ltIndividuals):
            
            
            individuo_split = individuo.split('_')
            individuo_animalID = individuo_split[0]
            individuo_tagID = individuo_split[1]
            
            for wolf in lt.iterator(data_wolf):
                wolf_animalID = wolf['animal-id']
                wolf_tagID = wolf['tag-id']
                
                if (wolf_animalID == individuo_animalID) and (wolf_tagID == individuo_tagID):
                    ltSingleWolf = lt.newList('ARRAY_LIST')
                    lt.addLast(ltSingleWolf, individuo)
                    sex = wolf['animal-sex']
                    life_stage = wolf['animal-life-stage']
                    study_site = wolf['study-site'] 
                    comments = wolf['deployment-comments']
                    if sex == '':
                        sex = 'Unknown'
                    if life_stage == '':
                        life_stage = 'Unknown'
                    if study_site == '':
                        study_site = 'Unknown'
                    if comments == '':
                        comments = 'Unknown'
                    
                    lt.addLast(ltSingleWolf, sex)
                    lt.addLast(ltSingleWolf, life_stage)
                    lt.addLast(ltSingleWolf, study_site)
                    lt.addLast(ltSingleWolf, comments)
                    lt.addLast(ltIndividuosComponent, ltSingleWolf)
        lt.addLast(ltComponent, ltIndividuosComponent)
        
            
        lt.addLast(ltFinal, ltComponent)
                
    return numVertex, numArcos, connectedComponents_Manadas, ltFinal

def getTrackIDsReq7(lista):
    
    '''
    Funcion que retorna una lista con los ids de los trayectos de los lobos

    Parametro: tracker
    
    Lee la lista de los datos de los trayectos de los lobos
    
    Retorna: listaIds
    
    Lista con los ids de los trayectos de los lobos, en el formato "m115p792_58p198_35260_35260"
    '''
    
    listaIds = lt.newList('ARRAY_LIST')
    
    for data in lt.iterator(lista):
        trackID = createTrackPointID(data)
        
        if trackID not in listaIds['elements']:
        
            lt.addLast(listaIds, trackID)
        else:
            pass
    
    return listaIds

def addTrackNodeReq7(graph, listIDS):
    
    '''
    Adiciona a un punto de seguimiento como registo al grafo
    
    '''
    try:
        
        
        
        for ids in lt.iterator(listIDS):
            if not gr.containsVertex(graph, ids):
                gr.insertVertex(graph, ids)
        track_nodes = gr.numVertices(graph)
        
        return graph, track_nodes 
    except Exception as exp:
        error.reraise(exp, 'model.addTrackNode_Req7: Error al agregar un evento al grafo') 


#Funciones auxiliares para la creacion de los nodos
def hashMeetingPointsReq7(lista):
    
    '''
    Se crea un mapa con los puntos de encuentro de los lobos
    
    '''
    
    meetingPoints_map = mp.newMap(100, maptype='PROBING', cmpfunction=compareWolfID)
    
    for data in lt.iterator(lista):
        meetingPoint = createMeetingPoint(data)
        entry = mp.get(meetingPoints_map, meetingPoint)
        if entry is None:
            contador = 1   
            ltWolf = lt.newList('ARRAY_LIST')
            lt.addLast(ltWolf, data['tag-local-identifier'])
        
            mp.put(meetingPoints_map, meetingPoint, (contador, ltWolf))
        else:
            contador_f = entry['value'][0]
            contador_f += 1
            ltwolf_f = entry['value'][1]
            lt.addLast(ltwolf_f, data['tag-local-identifier'])
            mp.put(meetingPoints_map, meetingPoint, (contador_f, ltwolf_f))
        
    return meetingPoints_map


def getMeetingPointsIDReq7(lista):
    
    mapa = hashMeetingPointsReq7(lista)
    keys = mp.keySet(mapa)
    
    listaIds = lt.newList('ARRAY_LIST')
    
    for llave in lt.iterator(keys):
        ltwolf = mp.get(mapa, llave)['value'][1]
        if lt.size(ltwolf) >= 2:
            firstWolf = lt.firstElement(ltwolf)
            lt.removeFirst(ltwolf)
            for wolf in lt.iterator(ltwolf):
                if wolf != firstWolf:
                    if lt.isPresent(listaIds, llave) == 0:
                        lt.addLast(listaIds, llave)
    return listaIds


def addMeetingNodeReq7(graph, lista):
    
    '''
    Adiciona los puntos de encuentro como nodos al grafo
    
    '''
    
    try:
        
        graph = graph[0] 
        
        for id_meeting_point in lt.iterator(lista):
            if not gr.containsVertex(graph, id_meeting_point):
                gr.insertVertex(graph, id_meeting_point)
        return graph
    
        
    except Exception as exp:
        error.reraise(exp, 'model.add_wolf: Error al agregar un punto de encuentro al grafo')
    

def sortWolfTracksbyDateReq7(mapa):
    
    mapa_tracks = mapa
    
    ltKeys = mp.keySet(mapa_tracks)
    
    for key in lt.iterator(ltKeys):
        ltTracks = mp.get(mapa_tracks, key)['value']
        if lt.size(ltTracks) > 1:
            ltTracks = merg.sort(ltTracks, compareWolfTracksbyDate)
        mp.put(mapa_tracks, key, ltTracks)
    
    return mapa_tracks


def addMAPIdTrackReq7(mapa, listaWolf, ListaTrack):
    '''
    
    Adiciona información a un mapa los tracks de los lobos
    
    '''
    
    data_wolf = listaWolf
    data_tracks = ListaTrack
    
    for wolf_lindo in lt.iterator(data_wolf):
        id_wolf_individual = createIndividualID(wolf_lindo)
        for track_lindo in lt.iterator(data_tracks):
            id_wolf_track = createIndividualID_tracks(track_lindo)
            if id_wolf_track == id_wolf_individual:
                addTrackMapINDReq7(mapa, id_wolf_track, track_lindo)

def addTrackMapINDReq7(mapa, id_individual, track):
    '''
    Adiciona  a una ubicacion un lobo al mapa correspondiente
    
    '''
        
    entry = mp.get(mapa, id_individual)
    if entry is None:
        lst_track = lt.newList('ARRAY_LIST', compareWolfs)
        lt.addLast(lst_track, track)
        mp.put(mapa, createIndividualID_tracks(track), lst_track)
    else:
        lst_track = entry['value']
        lt.addLast(lst_track, track)
    return mapa


def connectWolfPointsReq7(graph, mapa): #Optimizar FIXME
    
    '''
    Funcion que conecta dos tracking points de un mismo lobo
    
    Parametros: tracker
    
    Donde el tracker ya contiene los vértices de los meeting point y tracking points.
    
    Retorna: tracker
    
    Donde el tracker ya contiene los arcos de los tracking points y todo lo mencionado previamente.

    '''
    #Mapa de lobos-tracks, donde la llave es el individual id y el valor es una lista de los tracks de ese lobo
    map_wolf_tracks = sortWolfTracksbyDateReq7(mapa) 
    
    ltKeys = mp.keySet(map_wolf_tracks) #Lista de llaves del mapa
    
    for wolf in lt.iterator(ltKeys):
        ltTracks = mp.get(map_wolf_tracks, wolf)['value'] #Lista de tracks de un lobo
        if lt.size(ltTracks) > 1:
            for i in range(lt.size(ltTracks) - 1):
                track1 = lt.getElement(ltTracks, i)
                track2 = lt.getElement(ltTracks, i + 1)
                track1_lindo = createTrackPointID(track1)
                track2_lindo = createTrackPointID(track2)
                if track1_lindo != track2_lindo:
                    gr.addEdge(graph, track1_lindo, track2_lindo, calculateHarvesineDistance(track1, track2))
    return graph


def connectMeetingPointsReq7(graph, listaIDS, data_tracks): #En mis libros está bien y funciona lindo
    
    '''
    Función que conecta bidireccionalmente los puntos de encuentro 
    de dos lobos que alguna vez se han encontrado en una ubicación dada sin importar el tiempo.
    
    Parametros: tracker
    
    Donde el tracker ya contiene los vértices de los meeting point y tracking point junto con los arcos de los 
    tracking points.
    
    Retorna: tracker
    
    Donde el tracker ya contiene los arcos de los meeting points y todo lo mencionado previamente.
    
    ''' 
    
    ltMeetingPoints = listaIDS #Lista de los meeting points existentes
    
    ltTrackingPoints = getTrackIDsReq7(data_tracks) #Lista de los tracking points existentes
    for meeting_point in lt.iterator(ltMeetingPoints):
        for track in lt.iterator(ltTrackingPoints):
            track_lindo = getMeetingPointFromTrackingPoint(track) #Obtener el meeting point de un tracking point

            if meeting_point == track_lindo:
                gr.addEdge(graph, track, meeting_point, 0)
                gr.addEdge(graph, meeting_point, track, 0)
    #meeting_edges = gr.numEdges(tracker['connections'])

    return graph#, meeting_edges


def getTrackIDsReq7(lista):
    
    '''
    Funcion que retorna una lista con los ids de los trayectos de los lobos

    Parametro: tracker
    
    Lee la lista de los datos de los trayectos de los lobos
    
    Retorna: listaIds
    
    Lista con los ids de los trayectos de los lobos, en el formato "m115p792_58p198_35260_35260"
    '''
    
    listaIds = lt.newList('ARRAY_LIST')
    
    for data in lt.iterator(lista):
        trackID = createTrackPointID(data)
        
        if trackID not in listaIds['elements']:
        
            lt.addLast(listaIds, trackID)
        else:
            pass
    
    return listaIds

def fechaLinda(fecha):
    
    fechaLinda = ''
    
    fechaLinda = datetime.strptime(fecha, "%Y-%m-%d %H:%M")
    
    return fechaLinda


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
