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
import math
import datetime
import sys
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
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""
sys.setrecursionlimit(1048576)

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    data_structs = {}
    data_structs['wolf_individuals'] = mp.newMap(numelements=22, maptype='PROBING', loadfactor=0.5)
    data_structs['wolf_tracks_graph'] = gr.newGraph(datastructure='ADJ_LIST', directed = True, size= 200000)
    data_structs['wolf_individual_track'] = mp.newMap(numelements = 22, maptype='PROBING', loadfactor=0.5)
    data_structs['wolf_tracks_ids'] = mp.newMap(numelements= 50000, maptype='PROBING', loadfactor=0.5)
    data_structs['MTPs'] = lt.newList(datastructure='ARRAY_LIST', cmpfunction=standard_compare)
    data_structs['all_tracks'] = lt.newList(datastructure='ARRAY_LIST', cmpfunction=standard_compare)
    data_structs['distance_tree'] = om.newMap('BST', standard_compare)
    data_structs['longitudes'] = []
    data_structs['latitudes'] = []
    return data_structs

###----------------###
### Requerimientos ###
###----------------###

def req_1(data_structs, punto_partida, punto_llegada):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1

    grafo = data_structs['wolf_tracks_graph']
    dfs_structs = dfs.DepthFirstSearch(grafo, punto_partida)
    path = dfs.pathTo(dfs_structs, punto_llegada)
    if path != None:
        list_result = lt.newList('ARRAY_LIST')
        distancia_total = 0
        puntos_encuentro = 0
        index = 1
        while index <= lt.size(path):
            elem = lt.getElement(path, index)
            dict_elem = {}
            dict_elem['Identificador'] = elem
            dict_elem['Latitud'] = id_to_coords(elem)[0]
            dict_elem['Longitud'] = id_to_coords(elem)[1]
            puntos_encuentro += 1
            if index != lt.size(path):
                next_elem = lt.getElement(path, index + 1)
                next_elem_lat = id_to_coords(next_elem)[0]
                next_elem_long = id_to_coords(next_elem)[1]
                distance = haversine(float(dict_elem['Longitud']),float(dict_elem['Latitud']), float(next_elem_long), float(next_elem_lat))
                dict_elem['Distancia al próximo lobo'] = distance
                distancia_total += distance
            else:
                dict_elem['Distancia al próximo lobo'] = '--'
            if is_MTP(elem):
                first_last_n_elems_list(gr.adjacents(grafo, elem), 3)
                wolves_MTP = gr.adjacents(grafo, elem)
                list_wolves_transit = first_last_n_elems_list(wolves_MTP, 3)
                list_wolves = []
                for wolf in lt.iterator(list_wolves_transit):
                    list_wolves.append(wolf)
                dict_elem['Primeros y últimos tres lobos que transitan por el punto'] = list_wolves
            else:
                dict_elem['Primeros y últimos tres lobos que transitan por el punto'] = 'Desconocido'
            lt.addLast(list_result, dict_elem)
            index += 1
        return first_last_n_elems_list(list_result, 5), distancia_total, puntos_encuentro, path
    return lt.newList(), 0, 0

def req_2(data_structs, punto_partida, punto_llegada):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    grafo = data_structs['wolf_tracks_graph']
    bfs_structs = bfs.BreadthFirstSearch(grafo, punto_partida)
    path = bfs.pathTo(bfs_structs, punto_llegada)
    if path != None:
        list_result = lt.newList('ARRAY_LIST')
        distancia_total = 0
        puntos_encuentro = 0
        index = 1
        while index <= lt.size(path):
            elem = lt.getElement(path, index)
            dict_elem = {}
            dict_elem['Identificador'] = elem
            dict_elem['Latitud'] = id_to_coords(elem)[0]
            dict_elem['Longitud'] = id_to_coords(elem)[1]
            puntos_encuentro += 1
            if index != lt.size(path):
                next_elem = lt.getElement(path, index + 1)
                next_elem_lat = id_to_coords(next_elem)[0]
                next_elem_long = id_to_coords(next_elem)[1]
                distance = haversine(float(dict_elem['Longitud']),float(dict_elem['Latitud']), float(next_elem_long), float(next_elem_lat))
                dict_elem['Distancia al próximo lobo'] = distance
                distancia_total += distance
            else:
                dict_elem['Distancia al próximo lobo'] = '--'
            if is_MTP(elem):
                first_last_n_elems_list(gr.adjacents(grafo, elem), 3)
                wolves_MTP = gr.adjacents(grafo, elem)
                list_wolves_transit = first_last_n_elems_list(wolves_MTP, 3)
                list_wolves = []
                for wolf in lt.iterator(list_wolves_transit):
                    list_wolves.append(wolf)
                dict_elem['Primeros y últimos tres lobos que transitan por el punto'] = list_wolves
            else:
                dict_elem['Primeros y últimos tres lobos que transitan por el punto'] = 'Desconocido'
            lt.addLast(list_result, dict_elem)
            index += 1
        return first_last_n_elems_list(list_result, 5), distancia_total, puntos_encuentro, path
    return lt.newList(), 0, 0


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    

    grafo = data_structs['wolf_tracks_graph']
    componentes_conectados  = scc.KosarajuSCC(grafo)
    num_manadas = componentes_conectados['components']
    mapa_manadas = mp.newMap(numelements=100)
    info_lobos = data_structs['wolf_individuals']
    for vertex in lt.iterator(mp.keySet(componentes_conectados['idscc'])):
        num_componente = me.getValue(mp.get(componentes_conectados['idscc'], vertex))
        if not mp.contains(mapa_manadas, num_componente):
            component_filter = mp.newMap(numelements=4)
            MTP_list = lt.newList(datastructure='ARRAY_LIST', cmpfunction=standard_compare)
            seg_table = mp.newMap(numelements=50)
            list_todos = lt.newList(datastructure='ARRAY_LIST', cmpfunction=standard_compare)
            lt.addLast(list_todos, vertex)
            if is_MTP(vertex):
                lt.addLast(MTP_list, vertex)
            else:
                id_lobo = seg_id_to_coords_id(vertex)[2]
                add_to_hash_table(seg_table, id_lobo, vertex)
            
            mp.put(component_filter, 'MTP',MTP_list)
            mp.put(component_filter,'seg', seg_table)
            mp.put(component_filter, 'todos', list_todos)
            mp.put(mapa_manadas,num_componente, component_filter )
        else:
            component_filter = me.getValue(mp.get(mapa_manadas, num_componente)) 
            MTP_list = me.getValue(mp.get(component_filter, 'MTP'))
            seg_table = me.getValue(mp.get(component_filter, 'seg'))
            todos = me.getValue(mp.get(component_filter, 'todos'))
            lt.addLast(todos, vertex)
            if is_MTP(vertex):
                lt.addLast(MTP_list, vertex)
            else:
                id_lobo = seg_id_to_coords_id(vertex)[2]
                add_to_hash_table(seg_table, id_lobo, vertex)
     
    list_result = lt.newList(datastructure='ARRAY_LIST')
    for manada in lt.iterator(mp.keySet(mapa_manadas)):
        info_manada = {}
        lobos_manada = lt.newList('ARRAY_LIST')
        filtro_MTPs = me.getValue(mp.get(mapa_manadas, manada))
        MTP_list = me.getValue(mp.get(filtro_MTPs, 'MTP'))
        seg_map = me.getValue(mp.get(filtro_MTPs, 'seg'))
        lista_todos = me.getValue(mp.get(filtro_MTPs, 'todos'))
        info_manada['Codigo manada'] = manada
        info_manada['Tamaño SCC'] = lt.size(lista_todos)
        info_manada['Primeros y últimos puntos'] = first_last_n_elems_list(lista_todos, 3)['elements']
        info_manada['Num lobos'] = lt.size(mp.keySet(seg_map))
        primeros_ultimos_lobos = first_last_n_elems_list(mp.keySet(seg_map), 3)
        
        list_lats = lt.newList('ARRAY_LIST')
        list_longs = lt.newList('ARRAY_LIST')
        for node in lt.iterator(lista_todos):
            long_nod = id_to_coords(node)[1]
            lat_nod = id_to_coords(node)[0]
            lt.addLast(list_lats, lat_nod)
            lt.addLast(list_longs, long_nod)
        merg.sort(list_lats, sort_criteria_standard)
        merg.sort(list_longs, sort_criteria_standard)
        
        info_manada['Latitud mínima'] = lt.lastElement(list_lats)
        info_manada['Latitud máxima'] = lt.firstElement(list_lats)
        
        info_manada['Longitud mínima'] = lt.lastElement(list_longs)
        info_manada['Longitud máxima'] = lt.firstElement(list_longs)
        
        for lobo_seg in lt.iterator(primeros_ultimos_lobos):
            info_lobo = {}
            datos = me.getValue(mp.get(info_lobos, lobo_seg))
            info_lobo['Identificador'] = datos['individual-id']
            info_lobo['Taxonomía'] = datos['animal-taxon']
            info_lobo['Ciclo de vida'] = datos['animal-life-stage']
            info_lobo['Sexo'] = datos['animal-sex']
            info_lobo['Lugar de estudio'] = datos['study-site']
            lt.addLast(lobos_manada, info_lobo)
        info_manada['Primeros y últimos tres lobos en la manada'] = lobos_manada
        lt.addLast(list_result, info_manada)  
    merg.sort(list_result, sort_criteria_dominancia)
    
    return num_manadas, list_result, mapa_manadas, componentes_conectados['idscc'] 


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs, punto_partida, distancia, num_puntos):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    distancia= round(float(distancia)/2, 3)
    routes=djk.Dijkstra(data_structs["wolf_tracks_graph"], punto_partida)
    validRoutes=om.newMap(omaptype="BST")
    
    points = gr.vertices(data_structs["wolf_tracks_graph"])
    
    for mpt in lt.iterator(points):
        path = djk.pathTo(routes,mpt)
        if path:
            coste = round(djk.distTo(routes, mpt), 3)
            numpoints = st.size(path)
            if coste <= distancia and numpoints >= int(num_puntos):
                om.put(validRoutes, coste, mpt)
    
    posibilities = om.size(validRoutes)
    
    extensivePath = lt. newList()
    corredores = om.keySet(validRoutes)
    
    for distance in lt.iterator(corredores):
        corredorPoint = om.get(validRoutes, distance)["value"]
        path= djk.pathTo(routes, corredorPoint)
        infopath = newPointExtensivePath(data_structs, path, distance, corredorPoint)
        lt.addLast(extensivePath, infopath)
        
    extensivePath= merg.sort(extensivePath, cmp_path_distance)  
    return {"extensivePath": extensivePath, "posibilities": posibilities}             
    


def cmp_path_distance(elem1, elem2):
    if elem1[0] > elem2[0]:
        return 1
    elif elem1[0] == elem2[0]:
        return 0
    else:
        return -1

def newPointExtensivePath(data_structs, path, distance, extensivenode):
    extensivePath= {
        "Points Count": None,
        "Path Distance": None,
        "Point list": None,
        "Animalcount": None
    }
    extensivePath["Points Count"] = st.size(path) + 1
    extensivePath["Path distance"] = distance
    animalCount = lt. newList(datastructure="ARRAY_LIST",cmpfunction=standard_compare)
    pointList=lt.newList(datastructure="ARRAY_LIST",cmpfunction=standard_compare)
    while not st. isEmpty(path):
        point = st.pop(path)
        point=point["vertexA"]
        if mp.contains(data_structs["MTPs"], point):
            lb=mp.get(data_structs["MTPs"], point)["value"]["element"]
            lt.addLast(animalCount, str(len(lb)))
        else:
            lt.addLast(animalCount, "1")
        lt.addLast(pointList, point)
        extensivePath["Point list"] = str(pointList["elements"]).replace("[", "").replace("]", "").replace("'", "")+","+extensivenode
        if mp.contains(data_structs["MTPs"], extensivenode):
            lb= mp.get(data_structs["MTPs"], extensivenode)["value"]["elements"]
            lt.addLast(animalCount, str(len(lb)))
        else:
            lt.addLast(animalCount, "1")
        
        extensivePath["Animal Count"] = str(animalCount["elements"]).replace("[", "").replace("]", "").replace("'", "")
        return extensivePath

def req_6(data_structs, initial_date_str, final_date_str, animal_sex):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    alternate_datastructs = new_data_structs()
    alternate_datastructs['wolf_tracks_graph'] = gr.newGraph(datastructure='ADJ_LIST', directed = True, size= 200000)
    tree = alternate_datastructs['distance_tree']
    
    list_all_tracks = data_structs['all_tracks']
    
    individuals = data_structs['wolf_individuals']
    initial_date = str_to_datetime(initial_date_str)
    final_date = str_to_datetime(final_date_str)
    for track in lt.iterator(list_all_tracks):
        track_date = track['timestamp']
        track_id = track['individual-id']
        track_sex = me.getValue(mp.get(individuals, track_id))['animal-sex']
        if track_date >= initial_date and track_date <= final_date and track_sex == animal_sex:
            add_seg(alternate_datastructs,track, False)
    
    trace_paths(alternate_datastructs)
    
    #El camino más largo es simplemente es el camino completo que recorrió el lobo durante el intervalo, 
    # en este requerimiento podría hacerse sin grafos, pero para utilizar las estructuras de datos, los utilizaremos
    graph = alternate_datastructs['wolf_tracks_graph']
    
    min_distance = om.minKey(alternate_datastructs['distance_tree'])
    max_distance = om.maxKey(alternate_datastructs['distance_tree'])
    
    min_id = me.getValue(om.get(tree, min_distance))
    max_id = me.getValue(om.get(tree, max_distance))
    
    min_wolf_info = me.getValue(mp.get(individuals, min_id))
    max_wolf_info = me.getValue(mp.get(individuals, max_id))
    
    min_wolf_info['Distancia recorrida'] = min_distance
    max_wolf_info['Distancia recorrida'] = max_distance
    
    #Lobo más largo
    tracks_lobo_max = me.getValue(mp.get(alternate_datastructs['wolf_individual_track'], max_id))
    
    list_result_max = lt.newList('ARRAY_LIST')
    distance_max = 0
    num_vertices_max = 0
    num_edges_max = 0
    for index in range(1,lt.size(tracks_lobo_max)+1):
        track = lt.getElement(tracks_lobo_max, index)
        if gr.containsVertex(graph, track['animal-seg-id']):
            num_vertices_max += 1
            dict_vertex = {}
            dict_vertex['Vertex-id'] = track['animal-seg-id']
            vertex_longitude = track['location-long']
            vertex_latitude = track['location-lat']
            dict_vertex['Longitude'] = vertex_longitude
            dict_vertex['Latitude'] = vertex_latitude
            if gr.containsVertex(graph, id_MTP(vertex_longitude, vertex_latitude)):
                dict_vertex['Individuals in location'] = gr.degree(graph, id_MTP(vertex_longitude, vertex_latitude))
            else:
                dict_vertex['Individuals in location'] = 1
            dict_vertex['Individual id'] = max_id
            if index != lt.size(tracks_lobo_max):
                next_track = lt.getElement(tracks_lobo_max, index + 1)
            if gr.getEdge(graph,track['animal-seg-id'], next_track['animal-seg-id']) != None:
                num_edges_max +=1
                distance_max += gr.getEdge(graph,track['animal-seg-id'], next_track['animal-seg-id'])['weight']
            lt.addLast(list_result_max, dict_vertex)
            
    #Lobo más corto
    tracks_lobo_min = me.getValue(mp.get(alternate_datastructs['wolf_individual_track'], min_id))
    
    list_result_min = lt.newList('ARRAY_LIST')
    distance_min = 0
    num_vertices_min = 0
    num_edges_min = 0
    for index in range(1,lt.size(tracks_lobo_min)+1):
        track = lt.getElement(tracks_lobo_min, index)
        if gr.containsVertex(graph, track['animal-seg-id']):
            num_vertices_min += 1
            dict_vertex = {}
            dict_vertex['Vertex-id'] = track['animal-seg-id']
            vertex_longitude = track['location-long']
            vertex_latitude = track['location-lat']
            dict_vertex['Longitude'] = vertex_longitude
            dict_vertex['Latitude'] = vertex_latitude
            if gr.containsVertex(graph, id_MTP(vertex_longitude, vertex_latitude)):
                dict_vertex['Individuals in location'] = gr.degree(graph, id_MTP(vertex_longitude, vertex_latitude))
            else:
                dict_vertex['Individuals in location'] = 1
            dict_vertex['Individual id'] = min_id
            if index != lt.size(tracks_lobo_min):
                next_track = lt.getElement(tracks_lobo_min, index + 1)
            if gr.getEdge(graph,track['animal-seg-id'], next_track['animal-seg-id']) != None:
                num_edges_min +=1
                distance_min += gr.getEdge(graph,track['animal-seg-id'], next_track['animal-seg-id'])['weight']
            lt.addLast(list_result_min, dict_vertex)
        min_wolf_info_list = lt.newList('ARRAY_LIST')
        lt.addLast(min_wolf_info_list, min_wolf_info)
        
        max_wolf_info_list = lt.newList('ARRAY_LIST')
        lt.addLast(max_wolf_info_list, max_wolf_info)
    return min_wolf_info_list, max_wolf_info_list, first_last_n_elems_list (list_result_min, 3), first_last_n_elems_list (list_result_max, 3), distance_min, num_edges_min, num_vertices_min, distance_max, num_edges_max, num_vertices_max




def req_7(data_structs, initial_date_str, final_date_str, min_temp, max_temp):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    alternate_data_structs = new_data_structs()
    alternate_data_structs['wolf_tracks_graph'] = gr.newGraph(datastructure='ADJ_LIST', directed = True, size= 200000)

    initial_date = str_to_datetime(initial_date_str)
    final_date = str_to_datetime(final_date_str)
    
    individuals = data_structs['wolf_individuals']
    all_tracks = data_structs['all_tracks']
    
    alternate_data_structs['wolf_individuals'] = individuals
    
    for track in lt.iterator(all_tracks):
        track_timestamp = track['timestamp']
        track_wolf_temperature = float(track['external-temperature'])
        if track_timestamp >= initial_date and track_timestamp <= final_date and track_wolf_temperature >= min_temp and track_wolf_temperature <= max_temp:
            add_seg(alternate_data_structs, track)
    
    trace_paths(alternate_data_structs)
    grafo = alternate_data_structs['wolf_tracks_graph']
    num_vertices = gr.numVertices(grafo)
    num_edges = gr.numEdges(grafo)
    result_req_3 = req_3(alternate_data_structs)
    
    num_manadas = result_req_3[0]
    lista = result_req_3[1]
    mapa_manadas= result_req_3[2]
    vertex_components = result_req_3[3]
    #Para hallar el camino más largo, implementaremos un algoritmo que recorre todos los vértices del componente en orden
    list_result = lt.newList('ARRAY_LIST')
    grafo = alternate_data_structs['wolf_tracks_graph']
    for info in lt.iterator(lista):
        codigo_manada = info['Codigo manada']
        size_manadas = info['Tamaño SCC']

        distance = 0
        
        LP_vertices = []
        LP_latitudes = []
        LP_longitudes = []
        list_manada = me.getValue(mp.get(me.getValue(mp.get(mapa_manadas, codigo_manada)), 'todos'))
        LP_node = 0
        LP_edges = 0
        
        tabla_edges = mp.newMap()
        tabla_vertices = mp.newMap()
        
        for vertex in lt.iterator(list_manada):



            LP_vertices.append(vertex)
            LP_latitudes.append(id_to_coords(vertex)[0])
            LP_longitudes.append(id_to_coords(vertex)[1])
            LP_node += 1
            for edge in lt.iterator(gr.adjacentEdges(grafo, vertex)):
                va_comp = me.getValue(mp.get(vertex_components, edge['vertexA']))
                vb_comp = me.getValue(mp.get(vertex_components, edge['vertexB']))
                if va_comp == codigo_manada and vb_comp == codigo_manada:
                    if not mp.contains(tabla_edges, str(edge)):
                        mp.put(tabla_edges, str(edge), None)
                        LP_edges += 1
                        distance += edge['weight']


        max_long = max(LP_longitudes)
        max_lat = max(LP_latitudes)
        min_long = min(LP_longitudes)
        min_lat = min(LP_latitudes)
        
        dict_path = {}
        dict_path['Component ID'] = codigo_manada
        dict_path['SCC size'] = size_manadas
        dict_path['Minimum latitude'] = min_lat
        dict_path['Maximum latitude'] = max_lat
        dict_path['Minimum longitude'] = min_long
        dict_path['Maximum longitude'] = max_long
        dict_path['Nodes count'] = LP_node
        dict_path['Edges count'] = LP_edges
        dict_path['Distance'] = distance
        dict_path['Details'] = LP_vertices[0:5]
        
        lt.addLast(list_result, dict_path)
    return num_manadas, lista, mapa_manadas, first_last_n_elems_list(list_result, 5), num_vertices, num_edges
            
def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    return  data_structs['wolf_individual_track'], data_structs['MTPs']

###--------------------------###
### Funciones de comparación ###
###--------------------------###

def mpq_edges_weight_cmp(edge_1, edge_2):
    if edge_1['weight'] < edge_2['weight']:
        return 1
    elif edge_1['weight'] == edge_2['weight']:
        return 0
    else:
        return -1
    
def tree_compare_tuple(wolf_1, wolf_2):
    if wolf_1[0] > wolf_2[0]:
        return 1
    elif wolf_1[0] == wolf_2[0]:
        return 0
    else:
        return -1
    
def sort_criteria_dominancia(manada1, manada2): 
    if manada1['Tamaño SCC'] > manada2['Tamaño SCC']:
        return True
    else:
        return False
    
def sort_criteria_datetime(event_1, event_2):
    if event_1['timestamp'] > event_2['timestamp']:
        return True
    else:
        return False
    
def sort_criteria_standard(event_1, event_2):
    if event_1 > event_2:
        return True
    else:
        return False

def standard_compare(elem1, elem2):
    if elem1>elem2:
        return 1
    elif elem1 == elem2:
        return 0
    else:
        return -1
    
def compare_wolf_individual_animal_id(individual_1, individual_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    if individual_1['individual-id'] < individual_2['individual-id']:
        return 1
    elif individual_1 == individual_2:
        return 0
    else:
        return -1
    
def compare_wolf_track_datetime(track_1, track_2):
    if track_1['timestamp'] > track_2['timestamp']:
        return 1
    elif track_1['timestamp'] == track_2['timestamp']:
        return 0
    else:
        return -1

###--------------------------–###
### Funciones de construcción ###
###---------------------------###

def trace_paths(data_structs):
    graph = data_structs['wolf_tracks_graph']
    track_wolves = data_structs['wolf_individual_track']
    tree_distances = data_structs['distance_tree']
    for wolf_compound_id in lt.iterator(mp.keySet(track_wolves)):
        wolf_list = me.getValue(mp.get(track_wolves, wolf_compound_id))
        merg.sort(wolf_list, sort_criteria_datetime)
        total_distance = 0
        count = 0 
        size = lt.size(wolf_list)
        for elem1 in lt.iterator(wolf_list):
            count += 1
            if count != size:
                elem2 = lt.getElement(wolf_list, count + 1)
                
                elem1_long = elem1['location-long']
                elem1_lat = elem1['location-lat']
                elem2_long = elem2['location-long']
                elem2_lat = elem2['location-lat']
                
                distance = haversine(elem1_long, elem1_lat, elem2_long, elem2_lat)
                
                if distance > 0 and (elem1['timestamp'] != elem2['timestamp']):
                    id_seg1 = elem1['animal-seg-id']
                    id_seg2 = elem2['animal-seg-id']
                    if gr.getEdge(graph, id_seg1, id_seg2) == None:
                        total_distance += distance
                    add_edge(graph, id_seg1, id_seg2, distance)
        tree_distances = om.put(tree_distances, total_distance, wolf_compound_id)
    
def add_seg (data_structs, wolf_track, is_directed = True):
    graph = data_structs['wolf_tracks_graph']
    individual_id = wolf_track['individual-id']
    wolf_track_MTP = id_MTP(wolf_track['location-long'], wolf_track['location-lat'])
    wolf_track_seg_id = id_seg(wolf_track['location-long'], wolf_track['location-lat'], individual_id)
    wolf_track['animal-seg-id'] = wolf_track_seg_id

    add_to_hash_table(data_structs['wolf_tracks_ids'], wolf_track_MTP, wolf_track_seg_id)
    add_to_hash_table(data_structs['wolf_individual_track'], individual_id, wolf_track, compare_wolf_track_datetime)
    if not gr.containsVertex(graph, wolf_track_seg_id):

        insert_vertex(graph, wolf_track_seg_id) 
        
        list_MTP = me.getValue(mp.get(data_structs['wolf_tracks_ids'], wolf_track_MTP)) 
        num_dif_elems_MTP = lt.size(list_MTP)
        
        if num_dif_elems_MTP > 1:
            if not gr.containsVertex(graph, wolf_track_MTP):
                insert_vertex(graph, wolf_track_MTP)
                lt.addLast(data_structs['MTPs'], wolf_track_MTP)
                for elem in lt.iterator(lt.subList(list_MTP, 1, lt.size(list_MTP)-1)):
                    add_edge(graph, wolf_track_MTP, elem)
                    if is_directed:
                        add_edge(graph, elem, wolf_track_MTP)
            add_edge(graph, wolf_track_MTP, wolf_track_seg_id)
            if is_directed:
                add_edge(graph, wolf_track_seg_id, wolf_track_MTP)  
                
            

def add_wolf_track(data_structs, wolf_track):
    timestamp_str = wolf_track['timestamp']
    wolf_track['timestamp'] = str_to_datetime(timestamp_str)
    
    wolf_track_lat_str = wolf_track['location-lat']
    wolf_track['location-lat'] = round_up_str(wolf_track_lat_str,3)
    wolf_track_long_str = wolf_track['location-long']
    wolf_track['location-long'] = round_up_str(wolf_track_long_str,3)
    
    data_structs['longitudes'].append(wolf_track['location-long'])
    data_structs['latitudes'].append(wolf_track['location-lat'])
    
    individual_id = str(wolf_track['individual-local-identifier']) + '_' + str(wolf_track['tag-local-identifier'])
    wolf_track['individual-id'] = individual_id
    

    lt.addLast(data_structs['all_tracks'], wolf_track)
    
    add_seg(data_structs, wolf_track) 


    

def add_wolf_individual(data_structs, wolf_data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    individual_id = str(wolf_data['animal-id']) + '_' + str(wolf_data['tag-id'])
    wolf_data['individual-id'] = individual_id
    wolf_individuals = data_structs['wolf_individuals']
    if not mp.contains(wolf_individuals, individual_id):
        mp.put(wolf_individuals, individual_id, wolf_data)

def add_to_hash_table(hash_table, key, value, cmp_function_list = None ):
    if not mp.contains(hash_table, key):
        list_filter = lt.newList(datastructure='ARRAY_LIST', cmpfunction = cmp_function_list)
        lt.addLast(lst = list_filter, element = value)
        mp.put(map = hash_table, key = key, value = list_filter)
    else:
        list_filter = me.getValue(mp.get(map = hash_table, key = key))
        lt.addLast(lst = list_filter, element = value)

def add_to_hash_table_MTP(hash_table, MTP, seg_id):
    if not mp.contains(hash_table, MTP):
        list_filter = lt.newList(datastructure='ARRAY_LIST', cmpfunction = standard_compare)
        lt.addLast(lst = list_filter, element = seg_id)
        mp.put(map = hash_table, key = MTP, value = list_filter)
    else:
        seg_id_compound = seg_id_to_coords_id(seg_id)[2]
        list_filter = me.getValue(mp.get(map = hash_table, key = MTP))
        if not list_contains_wolf(list_filter, seg_id_compound):
            lt.addLast(lst = list_filter, element = seg_id)
###--------------------------–###        
###   Funciones misceláneas   ###
###--------------------------–###

def round_up_str(num_str, dig):
    num = float(num_str)
    return round(num, dig)

def  id_to_coords(id_mtp):
    long = id_mtp.split('_')[0]
    lat = id_mtp.split('_')[1]
    long = long.replace('m','-')
    long = long.replace('p','.')
    
    lat = lat.replace('m','-')
    lat = lat.replace('p','.')
    return float(lat), float(long)

def seg_id_to_coords_id(seg_id):
    id_seg_list = seg_id.split('_')
    long = id_seg_list[0]
    lat = id_seg_list[1]
    
    individual_id = '_'.join(id_seg_list[2:])
    
    long = long.replace('m','-')
    long = long.replace('p','.')
    
    lat = lat.replace('m','-')
    lat = lat.replace('p','.')

    return float(lat), float(long), individual_id
    

def id_MTP(long, lat):
    long = str(round_up_str(long,3))
    lat = str(round_up_str(lat,3))
    
    result = long + '_' + lat
    
    result = result.replace('-', 'm')
    result = result.replace('.','p')
    return result

def id_seg(long, lat, individual_id):
    long = str(round_up_str(long,3))
    lat = str(round_up_str(lat,3))
       
    result = long + '_' + lat + '_' + str(individual_id)
    result = result.replace('-', 'm')
    result = result.replace('.','p')
    return result

def str_to_datetime(timestamp):
    timestamp_list = timestamp.split(' ')
    timestamp_date = timestamp_list[0]
    timestamp_time = timestamp_list[1]
    
    timestamp_time_list = timestamp_time.split(':')
    timestamp_date_list = timestamp_date.split('-')
    
    year = int(timestamp_date_list[0].lstrip())
    month = int(timestamp_date_list[1].lstrip())
    day = int(timestamp_date_list[2].lstrip())
    
    hour = int(timestamp_time_list[0].lstrip())
    minute = int(timestamp_time_list[1].lstrip())
    
    datetime_ = datetime.datetime(year,month, day, hour, minute)
    return datetime_

def haversine(long1_deg, lat1_deg, long2_deg, lat2_deg):
    long1 = long1_deg*(math.pi)/180
    lat1 = lat1_deg*(math.pi)/180
    long2 = long2_deg*(math.pi)/180
    lat2 = lat2_deg*(math.pi)/180
    r = 6371
    A = (math.sin((lat2-lat1)/2))**2
    B = math.cos(lat2)*math.cos(lat1)
    C = (math.sin((long2-long1)/2))**2
    d = 2*r*(math.sqrt((A+(B*C))))
    return d
    
def first_last_n_elems_list(list, n):
    if lt.size(list) <= 2*n:
        return list
    else:
        first_n_elems = lt.subList(list, 1, n)
        last_n_elems = lt.subList(list, lt.size(list)-n, n)
        list_result = lt.newList(datastructure='ARRAY_LIST')
        for list in (first_n_elems,last_n_elems):
            for elem in lt.iterator(list):
                lt.addLast(list_result,elem)
        return list_result

def is_MTP(id):
    elem_long = float(id_to_coords(id)[1])
    elem_lat = float(id_to_coords(id)[0])
    elem_MTP = id_MTP(elem_long, elem_lat)
    if id == elem_MTP:
        return True
    return False

def list_contains_wolf(list, compound_id):
    for elem in lt.iterator(list):
        elem_id = seg_id_to_coords_id(elem)[2]
        if elem_id == compound_id:
            return True
    return False

def negate_graph(graph):
    greverse = gr.newGraph(size=gr.numVertices(graph),
                            directed=True,
                            cmpfunction=graph['cmpfunction']
                            )

    lstvert = gr.vertices(graph)
    for vert in lt.iterator(lstvert):
        insert_vertex(greverse, vert)

    for vert in lt.iterator(lstvert):
        lstadjeg = gr.adjacentEdges(graph, vert)
        for adj in lt.iterator(lstadjeg):
            add_edge(greverse, adj, vert)
    return greverse

def insert_to_tree(map, key, data):
    if not om.contains(map, key):
        list_key = lt.newList('ARRAY_LIST')
        lt.addLast(list_key, data)
        om.put(map, key, list_key)
    else:
        key_value = me.getValue(om.get(map, key))
        lt.addLast(key_value, data)
    return map

def add_edge(graph, elem1, elem2, weight= 0):
    edge = gr.getEdge(graph, elem1, elem2)
    if edge == None:
        gr.addEdge(graph, elem1, elem2, weight)
        
def insert_vertex(graph, vertex):
    if not gr.containsVertex(graph, vertex):
        gr.insertVertex(graph, vertex)
    