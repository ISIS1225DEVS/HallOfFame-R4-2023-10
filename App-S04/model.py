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
import datetime as d
import math
import sys
from haversine import haversine
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.ADT import indexminpq as pq
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
import folium
from tabulate import tabulate
import math as m
assert cf

default_limit = 10000
sys.setrecursionlimit(default_limit*10)


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_catalog():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #Inicializar las estructuras de datos
    catalog = {
        'map': None,
        'map_spec': None,
        'pedict':None,
        'grafo': None,
        'grafo_d': None
    }
    catalog['map'] = mp.newMap(45,maptype='PROBING',loadfactor=0.5)
    catalog['map_spec'] = mp.newMap(45,maptype='PROBING',loadfactor=0.5)
    catalog['grafo'] = gr.newGraph(datastructure='ADJ_LIST',directed=False,size=100000)
    catalog['grafo_d'] = gr.newGraph(datastructure='ADJ_LIST',directed=True,size=100000)
    return catalog


# Funciones para agregar informacion al modelo

def add_data(catalog, llave, valor):
    """
    Función para agregar elementos al mapa del catalog['map']
    """
    mapa = catalog['map']
    conjunto = mp.get(mapa, llave)
    if conjunto != None:
        lista = me.getValue(conjunto)
        lt.addLast(lista, valor)
    else:
        lista = lt.newList('ARRAY_LIST')
        lt.addLast(lista, valor)
        mp.put(mapa, llave, lista)
    return catalog

def add_data_spec(catalog, llave, valor):
    """
    Función para agregar elementos al mapa del catalog['map_spec']
    """
    mapa = catalog['map_spec']
    mp.put(mapa, llave, valor)
    return catalog

# Funciones para manejo de datos

def agrupar_data(catalog):
    """
    Agrupa los datos en el mapa catalog['data'] y construye el grafo a medida que lo hace
    """
    mapa_lobos = catalog['map']
    mapa_ordenado = mp.newMap(45,maptype='PROBING',loadfactor=0.5)
    # Diccionario para chequear los puntos de encuentro del grafo
    pe = {}
    # Diccionario auxiliar par chequear los puntos recorridos por el lobo
    pl = {}
    grafo = catalog['grafo']
    grafo_d = catalog['grafo_d']
    for lobo in lt.iterator(mp.keySet(mapa_lobos)):
        # obtener el diccionario llave: valor: del mapa, llave
        dic = mp.get(mapa_lobos, lobo)
        # obtener los valores para dicha llave
        lista = me.getValue(dic)
        merg.sort(lista,sort_criteria_carga)
        mp.put(mapa_ordenado,dic['key'],lista)
        last_key = ''
        for event in lt.iterator(lista):
            key = data_key_generator(event)
            pe_key = data_key_generator_pe(event)
            idlobo = data_id_generator(event)     
            # Si es el primer evento
            if last_key == '':
                gr.insertVertex(grafo,key)
                gr.insertVertex(grafo_d,key)
                if pe_key not in pe:
                    pe[pe_key]=[key]
                else:
                    # Caso de primeros 2 lobos que genera un punto de encuentro
                    if len(pe[pe_key]) == 1:
                        gr.insertVertex(grafo,pe_key)
                        gr.addEdge(grafo,pe[pe_key][0],pe_key)
                        gr.insertVertex(grafo_d,pe_key)
                        gr.addEdge(grafo_d,pe[pe_key][0],pe_key)
                        gr.addEdge(grafo_d,pe_key,pe[pe_key][0])
                    pe[pe_key]+=[key]
                    gr.addEdge(grafo,key,pe_key)
                    gr.addEdge(grafo_d,key,pe_key)
                    gr.addEdge(grafo_d,pe_key,key)
                pl[idlobo]=[key]
                last_key = key
            # Si este no es un punto repetido
            elif (last_key != key) and (key not in pl[idlobo]):
                gr.insertVertex(grafo,key)
                gr.insertVertex(grafo_d,key)
                peso = peso_arco(last_key,key)
                gr.addEdge(grafo,last_key,key,peso)
                gr.addEdge(grafo_d,last_key,key,peso)
                if pe_key not in pe:
                    pe[pe_key]=[key]
                else:
                    # Caso de primeros 2 lobos que genera un punto de encuentro
                    if len(pe[pe_key]) == 1:
                        gr.insertVertex(grafo,pe_key)
                        gr.addEdge(grafo,pe[pe_key][0],pe_key)
                        gr.insertVertex(grafo_d,pe_key)
                        gr.addEdge(grafo_d,pe[pe_key][0],pe_key)
                        gr.addEdge(grafo_d,pe_key,pe[pe_key][0])
                    pe[pe_key]+=[key]
                    gr.addEdge(grafo,key,pe_key)
                    gr.addEdge(grafo_d,key,pe_key)
                    gr.addEdge(grafo_d,pe_key,key)
                pl[idlobo] += [key]
                last_key = key
            elif key in pl[idlobo]:
                peso = peso_arco(last_key,key)
                ed = gr.getEdge(grafo_d,last_key,key)
                end = gr.getEdge(grafo,last_key,key)
                if ed is None and pl[idlobo][-1] != key:
                    gr.addEdge(grafo_d,last_key,key,peso)
                if end is None:
                    gr.addEdge(grafo,last_key,key,peso)
                pl[idlobo] += [key]
                last_key = key
    catalog['pedict'] = pe
    catalog['map'] = mapa_ordenado
    return catalog

def distancia(lat1, lon1, lat2, lon2):
    
    distancia_final = 2*(m.asin(m.sqrt(pow(m.sin((lat2-lat1)/2), 2)+(m.cos(lat1)*m.cos(lat2)*pow(m.sin((lon2-lon1)/2), 2)))))*6371
    return distancia_final

def distancia_n(par1, par2):
    
    par1 = ajustar_dato_i(par1)
    par2 = ajustar_dato_i(par2)
    
    lon1 = float(par1.split("_")[0])
    lat1 = float(par1.split("_")[1])
    lon2 = float(par2.split("_")[0])
    lat2 = float(par2.split("_")[1])

    distancia_final = 2*(m.asin(m.sqrt(pow(m.sin((lat2-lat1)/2), 2)+(m.cos(lat1)*m.cos(lat2)*pow(m.sin((lon2-lon1)/2), 2)))))*6371
    return distancia_final

# Funciones para creacion de datos
def ajustar_dato(dato):
    final = dato.replace(".", "p")
    final = final.replace("-", "m")
    return final

def ajustar_dato_i(dato):
    final = dato.replace("p", ".")
    final = final.replace("m", "-")
    return final

def data_id_generator(lobo):
    """
    Crea una llave para el mapa catalog['map'] para un lobo
    """
    id = '{}_{}'.format(lobo['individual-local-identifier'],lobo['tag-local-identifier'])
    return id 

def data_id_generator_spec(lobo):
    """
    Crea una llave para el mapa catalog['map_spec'] para un lobo
    """
    id = '{}_{}'.format(lobo['animal-id'],lobo['tag-id'])
    return id 

def data_key_generator(lobo):
    """
    Crea una llave para el grafos catalog['grafos'] para un lobo
    """
    laf = float(lobo['location-lat'])
    lof = float(lobo['location-long'])
    long = round(lof,3)
    lat = round(laf,3)
    id = data_id_generator(lobo)
    key = "{}_{}_{}".format(long,lat,id)
    key = key.replace('.', 'p')
    key = key.replace('-', 'm')
    return key

def data_key_generator_pe(lobo):
    """
    Crea una llave para el grafos catalog['grafos'] para un punto de encuentro
    """
    laf = float(lobo['location-lat'])
    lof = float(lobo['location-long'])
    long = round(lof,3)
    lat = round(laf,3)
    key = "{}_{}".format(long,lat)
    key = key.replace('.', 'p')
    key = key.replace('-', 'm')
    return key

def new_data_pos(lobo):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    lat = str(round(float(lobo["location-lat"]), 3))
    lat = ajustar_dato(lat)
    long = str(round(float(lobo["location-long"]), 3))
    long = ajustar_dato(long)
    str_final = long + "_" + lat
    
    return str_final

def ajustar_dato(dato):
    final = dato.replace(".", "p")
    final = final.replace("-", "m")
    return final

def peso_arco(p1,p2):
    """
    Encuentra la distancia en km entre dos coordenadas (ambas entradas como valores de los grafos), se usa para el peso de los arcos
    """
    p1lat = float(p1.split('_')[1].replace('p','.').replace('m','-'))
    p1lon = float(p1.split('_')[0].replace('p','.').replace('m','-'))
    p2lat = float(p2.split('_')[1].replace('p','.').replace('m','-'))
    p2lon = float(p2.split('_')[0].replace('p','.').replace('m','-'))
    p1 = (p1lat,p1lon)
    p2 = (p2lat,p2lon)
    return (round(haversine(p1,p2),3))

def ajustar_dato_i(dato):
    final = dato.replace("p", ".")
    final = final.replace("m", "-")
    return final

def es_puntoencuentro(vertice):
    lista = vertice.split("_")
    if len(lista) == 2:
        return True
    else:
        return False
    
def id_a_coord_pe(vertice):
    lista = vertice.split("_")
    long = ajustar_dato_i(lista[0])
    lat = ajustar_dato_i(lista[1])
    return lat, long
 
def get_id(vertice):
    lista = vertice.split("_")  
    if len(lista) == 4:  
        id_lobo = lista[2] + "_" + lista[3]
    else:
        id_lobo = lista[2] + "_" + lista[3] + "_" + lista[4]  
    return id_lobo

def ajustar_dato_i(dato):
    final = dato.replace("p", ".")
    final = final.replace("m", "-")
    return final

def get_long_lat(vertice):
    lista = vertice.split("_")  
    long = ajustar_dato_i(lista[0])
    lat = ajustar_dato_i(lista[1])
    return long, lat
        
def añadir_lista_pe(vertice, lista_adj, previo, dist):
    lista_final = lt.newList("ARRAY_LIST")
    lat, lon = id_a_coord_pe(vertice)
    str_individual = ""
    for lobo in lt.iterator(lista_adj):
        str_individual += (get_id(lobo) + ",")
    str_individual = str_individual.strip()
    lt.addLast(lista_final, lon)
    lt.addLast(lista_final, lat)
    lt.addLast(lista_final, vertice)
    lt.addLast(lista_final, str_individual)
    lt.addLast(lista_final, str(lt.size(lista_adj)))
    lt.addLast(lista_final, previo)
    lt.addLast(lista_final, dist)
    return lista_final["elements"]

def añadir_lista_ps(vertice, previo, dist):
    lista_final = lt.newList("ARRAY_LIST")
    lat, lon = id_a_coord_pe(vertice)
    lt.addLast(lista_final, lon)
    lt.addLast(lista_final, lat)
    lt.addLast(lista_final, vertice)
    lt.addLast(lista_final, get_id(vertice))
    lt.addLast(lista_final, str(1))
    lt.addLast(lista_final, previo)
    lt.addLast(lista_final, dist)
    return lista_final["elements"]
    


def req_1(catalog, identificador_origen, identificador_destino):
    """
    Función que soluciona el requerimiento 1
    """
    grafo_nod = catalog["grafo"]
    mapa_dfs = dfs.DepthFirstSearch(grafo_nod, identificador_origen)
    dist = 0
    total_pe = 0
    total_ps = 0 
    anterior = None
    lista_final = lt.newList("ARRAY_LIST")
    lista_tab = lt.newList("ARRAY_LIST")
    mapafo = folium.Map(location=[56.805562, -111.727874])
    list_polyline = []
    
    if dfs.hasPathTo(mapa_dfs, identificador_destino):
        pila = dfs.pathTo(mapa_dfs, identificador_destino)
        for vertice in lt.iterator(pila):
            if anterior != None:
                latf, lonf = id_a_coord_pe(anterior)
                edge = gr.getEdge(catalog["grafo"], anterior, vertice)
                dist += edge["weight"]
                if es_puntoencuentro(vertice):
                    total_pe += 1
                    lt_adj = gr.adjacents(grafo_nod,vertice)
                    lt.addFirst(lista_final, añadir_lista_pe(vertice, lt_adj, anterior, edge["weight"]))   
                    lat, lon = id_a_coord_pe(vertice)
                    list_polyline.append((float(lat),float(lon)))
                    if latf == lat and lonf == lon:
                        folium.Marker([lat, lon],  
                                    tooltip=vertice, 
                                    icon=folium.Icon(color="blue", 
                                                    icon="info-sign")).add_to(mapafo)
                else:
                    lt.addFirst(lista_final, añadir_lista_ps(vertice, anterior, edge["weight"])) 
                    total_ps += 1
                    lat, lon = id_a_coord_pe(vertice)
                    list_polyline.append((float(lat),float(lon)))
                    if latf != lat and lonf != lon:
                        folium.Marker([lat, lon],  
                                    tooltip=vertice, 
                                    icon=folium.Icon(color="blue", 
                                                    icon="info-sign")).add_to(mapafo)
                anterior = vertice
            else:
                total_pe += 1
                lt_adj = gr.adjacents(grafo_nod,vertice)
                lt.addFirst(lista_final, añadir_lista_pe(vertice, lt_adj, "Unknown", "Unknown"))
                lat, lon = id_a_coord_pe(vertice)
                list_polyline.append((float(lat),float(lon)))
                folium.Marker([lat, lon],  
                                  tooltip=vertice, 
                                  icon=folium.Icon(color="blue", 
                                                   icon="info-sign")).add_to(mapafo)
                anterior = vertice
        
        folium.PolyLine(list_polyline, tooltip="Coast").add_to(mapafo)
        
        if lt.size(lista_final) > 10:
            lt.addLast(lista_tab, lt.getElement(lista_final, 1))
            lt.addLast(lista_tab, lt.getElement(lista_final, 2))
            lt.addLast(lista_tab, lt.getElement(lista_final, 3))
            lt.addLast(lista_tab, lt.getElement(lista_final, 4))
            lt.addLast(lista_tab, lt.getElement(lista_final, 5))
            lt.addLast(lista_tab, lt.getElement(lista_final, lt.size(lista_final) - 4))
            lt.addLast(lista_tab, lt.getElement(lista_final, lt.size(lista_final) - 3))
            lt.addLast(lista_tab, lt.getElement(lista_final, lt.size(lista_final) - 2))
            lt.addLast(lista_tab, lt.getElement(lista_final, lt.size(lista_final) - 1))
            lt.addLast(lista_tab, lt.getElement(lista_final, lt.size(lista_final)))
        else:
            lista_tab = lista_final
        
        print("")
        return dist, total_pe, total_ps, lista_tab["elements"], mapafo
            
                
def req_2(catalog, identificador_origen, identificador_destino):
    """
    Función que soluciona el requerimiento 2
    """
    grafo_nod = catalog["grafo_d"]
    mapa_bfs = bfs.BreadhtFisrtSearch(grafo_nod, identificador_origen)
    dist = 0 
    anterior = None
    total_pe = 0
    total_ps = 0
    mapafo1 = folium.Map(location=[56.805562, -111.727874])
    list_polyline = []
    lista_final = lt.newList("ARRAY_LIST")
    
    if bfs.hasPathTo(mapa_bfs, identificador_destino):
        pila = bfs.pathTo(mapa_bfs, identificador_destino)
        for vertice in lt.iterator(pila):
            if anterior != None:
                latf, lonf = id_a_coord_pe(anterior)
                edge = gr.getEdge(catalog['grafo'], anterior, vertice)
                dist += edge["weight"]
                if es_puntoencuentro(vertice):
                    total_pe += 1
                    lt_adj = gr.adjacents(grafo_nod,vertice)
                    lt.addFirst(lista_final, añadir_lista_pe(vertice, lt_adj, anterior, edge["weight"]))
                    lat, lon = id_a_coord_pe(vertice)
                    list_polyline.append((float(lat),float(lon)))
                    if latf == lat and lonf == lon:
                        folium.Marker([lat, lon],  
                                    tooltip=vertice, 
                                    icon=folium.Icon(color="red", 
                                                    icon="info-sign")).add_to(mapafo1)   
                else:
                    lt.addFirst(lista_final, añadir_lista_ps(vertice, anterior, edge["weight"])) 
                    total_ps += 1
                    lat, lon = id_a_coord_pe(vertice)
                    list_polyline.append((float(lat),float(lon)))
                    if latf != lat and lonf != lon:
                        folium.Marker([lat, lon],  
                                    tooltip=vertice, 
                                    icon=folium.Icon(color="green", 
                                                    icon="info-sign")).add_to(mapafo1)
                anterior = vertice
            else:
                if es_puntoencuentro(vertice):
                    total_pe += 1
                    lt_adj = gr.adjacents(grafo_nod,vertice)
                    lt.addFirst(lista_final, añadir_lista_pe(vertice, lt_adj, "Unknown", "Unknown"))
                    lat, lon = id_a_coord_pe(vertice)
                    list_polyline.append((float(lat),float(lon)))
                    folium.Marker([lat, lon],  
                                  tooltip=vertice, 
                                  icon=folium.Icon(color="blue", 
                                                   icon="info-sign")).add_to(mapafo1)
                    anterior = vertice
        
        folium.PolyLine(list_polyline, tooltip="Coast").add_to(mapafo1)
        
        if lt.size(lista_final) > 10:
            lista_tab = lt.newList("ARRAY_LIST")
            lt.addLast(lista_tab, lt.getElement(lista_final, 1))
            lt.addLast(lista_tab, lt.getElement(lista_final, 2))
            lt.addLast(lista_tab, lt.getElement(lista_final, 3))
            lt.addLast(lista_tab, lt.getElement(lista_final, 4))
            lt.addLast(lista_tab, lt.getElement(lista_final, 5))
            lt.addLast(lista_tab, lt.getElement(lista_final, lt.size(lista_final) - 4))
            lt.addLast(lista_tab, lt.getElement(lista_final, lt.size(lista_final) - 3))
            lt.addLast(lista_tab, lt.getElement(lista_final, lt.size(lista_final) - 2))
            lt.addLast(lista_tab, lt.getElement(lista_final, lt.size(lista_final) - 1))
            lt.addLast(lista_tab, lt.getElement(lista_final, lt.size(lista_final)))
        else:
            lista_tab = lista_final
            
        return dist, total_pe, total_ps, lista_tab["elements"], mapafo1

def elemento_a_lista_3(scc_id, lista, info_lobos):
    
    lista_lobos = lt.newList("ARRAY_LIST")
    lista_final = lt.newList("ARRAY_LIST")
        
    lista_tab1 = []
    str_nodos = ""
    lobo_1 = lt.getElement(lista, 1)
    long_min, lat_min = get_long_lat(lobo_1)
    long_max = long_min
    lat_max = lat_min
    
    for lobo in lt.iterator(lista):
        long, lat = get_long_lat(lobo)
        if long < long_min:
            long_min = long
        elif lat < lat_min:
            lat_min = lat
        elif long > long_max:
            long_max = long
        elif lat > lat_max:
            lat_max = lat    
        
        str_nodos += lobo + ","
        if not(es_puntoencuentro(lobo)):
            id_lobo = get_id(lobo)
            if not(lt.isPresent(lista_lobos, id_lobo)):
                lt.addLast(lista_lobos,id_lobo)
                conjunto = mp.get(info_lobos, id_lobo)
                info_lobo = me.getValue(conjunto)
                
                sex = info_lobo["animal-sex"]
                if sex == None:
                    sex = "Unknown"
                stage = info_lobo["animal-life-stage"]
                if stage == None:
                    stage = "Unknown"
                site = info_lobo["study-site"]
                if site == None:
                    site = "Unknown"
                comment = info_lobo["deployment-comments"]
                if comment == None:
                    comment = "Unknown"
                lista_tab1.append([id_lobo,sex,stage,site,comment])
            
    headers = ["individual-id",
                "animal-sex",
                "animal-life-stage",
                "study-site",
                "deployment-comments"]
    lst_tab_final = []
    if len(lista_tab1) > 6:
        lst_tab_final.append(lista_tab1[0])
        lst_tab_final.append(lista_tab1[1])
        lst_tab_final.append(lista_tab1[2])
        lst_tab_final.append(lista_tab1[-3])
        lst_tab_final.append(lista_tab1[-2])
        lst_tab_final.append(lista_tab1[-1])
    else:
        lst_tab_final = lista_tab1

    tabla_ind = tabulate(lst_tab_final, headers, tablefmt="grid", maxcolwidths=12, maxheadercolwidths=12)
    str_nodos = str_nodos.strip()
    lt_str_nodos = str_nodos.split(",")
    str_nodos_f = 0
    if len(lt_str_nodos) > 10:
        str_nodos_f = (lt_str_nodos[0] + ",\n" +
                    lt_str_nodos[1] + ",\n" +
                    lt_str_nodos[2] + ",\n" +
                    "..." + ",\n" +
                    lt_str_nodos[-4] + ",\n" +
                    lt_str_nodos[-3] + ",\n" +
                    lt_str_nodos[-2])
    
    lt.addLast(lista_final, scc_id)
    lt.addLast(lista_final, str_nodos_f)
    lt.addLast(lista_final, lt.size(lista))
    lt.addLast(lista_final, lat_min)
    lt.addLast(lista_final, lat_max)
    lt.addLast(lista_final, long_max)
    lt.addLast(lista_final, long_min)
    lt.addLast(lista_final, lt.size(lista_lobos))
    lt.addLast(lista_final, tabla_ind)
    return lista_final["elements"]
            
def req_3(catalog):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    grafo = catalog["grafo_d"]
    info_lobos = catalog["map_spec"]
    mapa_scc = scc.KosarajuSCC(grafo)
    num_cc = scc.connectedComponents(mapa_scc)
    mapa_idscc = mapa_scc["idscc"]
    llaves_mapa = mp.keySet(mapa_idscc)
    mapa_cc = mp.newMap(numelements=num_cc, maptype="PROBING")
    mapafo3 = folium.Map(location=[56.805562, -111.727874])
    for id in lt.iterator(llaves_mapa):
        value = me.getValue(mp.get(mapa_idscc, id))
        conjunto_manada = mp.get(mapa_cc, value)
        if conjunto_manada != None:
            lista = me.getValue(conjunto_manada)
            lt.addLast(lista, id)
            mp.put(mapa_cc, value, lista)
        else:
            lista = lt.newList("ARRAY_LIST")
            lt.addLast(lista, id)
            mp.put(mapa_cc, value, lista)
      
    id_manadas = mp.keySet(mapa_cc)  
    lista_final = lt.newList("ARRAY_LIST")   
    for id_manada in lt.iterator(id_manadas):
        conjunto = mp.get(mapa_cc, id_manada)
        lista = me.getValue(conjunto)
        if lt.size(lista) > 1:
            lt.addLast(lista_final, elemento_a_lista_3(id_manada,lista,info_lobos))
    
    merg.sort(lista_final, req_3_sort_criteria)
    lista_tab_final = []
    
    if lt.size(lista_final) > 5:
        lista_tab_final.append(lt.getElement(lista_final, 1))
        lista_tab_final.append(lt.getElement(lista_final, 2))
        lista_tab_final.append(lt.getElement(lista_final, 3))
        lista_tab_final.append(lt.getElement(lista_final, 4))
        lista_tab_final.append(lt.getElement(lista_final, 5))
    else:
        lista_tab_final = lista_final["elements"]
    
    for elemento in lista_tab_final:
        long = (float(elemento[6])+float(elemento[5]))/2
        lat = (float(elemento[4])+float(elemento[3]))/2
        rad = distancia(float(elemento[6]), float(elemento[4]), float(long), float(lat))
        
        folium.Circle(
        radius= rad,
        location=[lat, long],
        popup="Manada",
        color="crimson",
        fill=False,
        ).add_to(mapafo3)
    
    return lista_tab_final, num_cc, mapafo3     

def req_4(data_structs, punto_origen, punto_destino):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    lon_o = punto_origen[1:8]
    lat_o = punto_origen[10:len(punto_origen)-1]
    lon_d = punto_destino[1:8]
    lat_d = punto_destino[10:len(punto_origen)-1]
    grafo_nod = data_structs["grafo"]
    mapa_dfs = dfs.DepthFirstSearch(grafo_nod, punto_origen)
    dist = 0
    total_pe = 0
    total_ps = 0 
    anterior = None
    lista_final = lt.newList("ARRAY_LIST")
    lista_tab = lt.newList("ARRAY_LIST")
    mapafo4 = folium.Map(location=[lon_o, lat_o])
    list_polyline = []
    
    if djk.hasPathTo(mapa_dfs, lat_d):
        pila = djk.pathTo(mapa_dfs, lon_d)
        for vertice in lt.iterator(pila):
            if anterior != None:
                latf, lonf = id_a_coord_pe(anterior)
                edge = gr.getEdge(data_structs["grafo"], anterior, vertice)
                dist += edge["weight"]
                if es_puntoencuentro(vertice):
                    total_pe += 1
                    lt_adj = gr.adjacents(grafo_nod,vertice)
                    lt.addFirst(lista_final, añadir_lista_pe(vertice, lt_adj, anterior, edge["weight"]))   
                    lat, lon = id_a_coord_pe(vertice)
                    list_polyline.append((float(lat),float(lon)))
                    if latf == lat and lonf == lon:
                        folium.Marker([lat, lon],  
                                    tooltip=vertice, 
                                    icon=folium.Icon(color="red", 
                                                    icon="info-sign")).add_to(mapafo4)
                else:
                    lt.addFirst(lista_final, añadir_lista_ps(vertice, anterior, edge["weight"])) 
                    total_ps += 1
                    lat, lon = id_a_coord_pe(vertice)
                    list_polyline.append((float(lat),float(lon)))
                    if latf != lat and lonf != lon:
                        folium.Marker([lat, lon],  
                                    tooltip=vertice, 
                                    icon=folium.Icon(color="green", 
                                                    icon="info-sign")).add_to(mapafo4)
                anterior = vertice
            else:
                total_pe += 1
                lt_adj = gr.adjacents(grafo_nod,vertice)
                lt.addFirst(lista_final, añadir_lista_pe(vertice, lt_adj, "Unknown", "Unknown"))
                lat, lon = id_a_coord_pe(vertice)
                list_polyline.append((float(lat),float(lon)))
                folium.Marker([lat, lon],  
                                  tooltip=vertice, 
                                  icon=folium.Icon(color="blue", 
                                                   icon="info-sign")).add_to(mapafo4)
                anterior = vertice
        
        folium.PolyLine(list_polyline, tooltip="Coast").add_to(mapafo4)
        
        if lt.size(lista_final) > 10:
            lt.addLast(lista_tab, lt.getElement(lista_final, 1))
            lt.addLast(lista_tab, lt.getElement(lista_final, 2))
            lt.addLast(lista_tab, lt.getElement(lista_final, 3))
            lt.addLast(lista_tab, lt.getElement(lista_final, 4))
            lt.addLast(lista_tab, lt.getElement(lista_final, 5))
            lt.addLast(lista_tab, lt.getElement(lista_final, lt.size(lista_final) - 4))
            lt.addLast(lista_tab, lt.getElement(lista_final, lt.size(lista_final) - 3))
            lt.addLast(lista_tab, lt.getElement(lista_final, lt.size(lista_final) - 2))
            lt.addLast(lista_tab, lt.getElement(lista_final, lt.size(lista_final) - 1))
            lt.addLast(lista_tab, lt.getElement(lista_final, lt.size(lista_final)))
        else:
            lista_tab = lista_final
        return dist, total_pe, total_ps, lista_tab["elements"], mapafo4

def req_5_aux(p,d,l,a):
    d = {
        'Puntos de encuentro y seguimiento visitados':p,
        'Distancia recorrida [km]':d,
        'Lista de puntos':l,
        'Secuencia de posibles individuos en el trayecto':a
    }
    return d

def req_5(data_structs,o,d,m):
    """
    Función que soluciona el requerimiento 5
    """
    mapafo5 = folium.Map(location=[56.805562, -111.727874])
    list_polyline = []
    recorrido = round(d/2,3)
    pedict = data_structs['pedict']
    grafo = data_structs['grafo']
    mst = prim.PrimMST(grafo,o)
    path_points = []
    for a in lt.iterator(gr.adjacents(grafo,o)):
        path_points.append(a)
    paths = lt.newList('ARRAY_LIST')
    for a in path_points:
        d = req_5_aux(2,float(mp.get(mst['distTo'],a)['value']),[o,a],[len(path_points),1])
        lt.addLast(paths,d)
    mapkeys = mp.keySet(mst['edgeTo'])
    c = 0
    while (lt.size(paths) + 2) > c:
        for point in lt.iterator(mapkeys):
            et = mp.get(mst['edgeTo'],point)
            va = et['value']['vertexA']
            vb = et['value']['vertexB']
            if (va in path_points) and (vb not in path_points):
                p = 0
                d = 0
                l = []
                a = []
                for e in lt.iterator(paths):
                    if va == e['Lista de puntos'][-1]:
                        if p < e['Puntos de encuentro y seguimiento visitados']:
                            p = e['Puntos de encuentro y seguimiento visitados']
                        if d < e['Distancia recorrida [km]']:
                            d = e['Distancia recorrida [km]']
                        if len(l) < len(e['Lista de puntos']):
                            l = e['Lista de puntos']
                        if len(a) < len(e['Secuencia de posibles individuos en el trayecto']):
                            a = e['Secuencia de posibles individuos en el trayecto']
                np = p + 1
                nd = round(d + mp.get(mst['distTo'],vb)['value'],3)
                nl = l + [vb]
                if vb not in pedict:
                    na = a + [1]
                else:
                    na = a + [lt.size(gr.adjacentEdges(grafo,vb))]
                d = req_5_aux(np,nd,nl,na)
                path_points.append(vb)
                if nd < recorrido and len(nl) > 2:
                    lt.addLast(paths,d)
                else:
                    c += 1
    paths = merg.sort(paths,req_5_sort_criteria_2)
    paths = merg.sort(paths,req_5_sort_criteria)
    del_list = []
    for p in lt.iterator(paths):
        for p2 in lt.iterator(paths):
            if p != p2:
                set1 = set(p['Lista de puntos'])
                set2 = set(p2['Lista de puntos'])
                if set1.issubset(set2) and p not in del_list:
                    del_list.append(p)
    newpaths = lt.newList('ARRAY_LIST')
    for p in lt.iterator(paths):
        if p not in del_list and p['Puntos de encuentro y seguimiento visitados'] >= m:
            lt.addLast(newpaths,p)
            
    lista = lt.getElement(newpaths, 1)["Lista de puntos"]
    for punto in lista:
        long, lat = get_long_lat(punto)
        list_polyline.append((float(lat),float(long)))
        folium.Marker([lat, long],  
                        tooltip=punto, 
                        icon=folium.Icon(color="blue", 
                        icon="info-sign")).add_to(mapafo5)
        
        
    folium.PolyLine(list_polyline, tooltip="Coast").add_to(mapafo5)
    
    return newpaths, mapafo5

def req_6(data_structs, fi, ff, g):
    mapafo6 = folium.Map(location=[56.805562, -111.727874])
    mapafo62 = folium.Map(location=[56.805562, -111.727874])
    list_polyline1 = []
    list_polyline2 = []
    fecha_i = d.datetime.strptime(fi, '%Y-%m-%d %H:%M:%S')
    fecha_f = d.datetime.strptime(ff, '%Y-%m-%d %H:%M:%S')
    mapa = data_structs["map"]
    mapa_spec = data_structs['map_spec']
    pedict = data_structs['pedict']
    grafo = data_structs['grafo']
    listinfo = lt.newList('ARRAY_LIST')
    for id in lt.iterator(mp.keySet(mapa)):
        lista = me.getValue(mp.get(mapa, id))
        spec = me.getValue(mp.get(mapa_spec, id))
        genero = spec['animal-sex']
        recorrido = 0
        primer_punto = ''
        punto_previo = ''
        nodos = 0
        keypaths = []
        for registro in lt.iterator(lista):
            key = data_key_generator(registro)
            pekey = data_key_generator_pe(registro)
            fecha = d.datetime.strptime(registro['timestamp'], '%Y-%m-%d %H:%M')
            if (fecha_i <= fecha <= fecha_f) and (genero == g):
                if punto_previo == '':
                    keypaths.append(key)
                    if pekey in pedict:
                        keypaths.append(key)
                    punto_previo = key
                    primer_punto = key
                    nodos += 1
                elif punto_previo != key:
                    peso = peso_arco(punto_previo,key)
                    recorrido += peso
                    keypaths.append(key)
                    if pekey in pedict:
                        keypaths.append(key)
                    punto_previo = key
                    nodos += 1
        if recorrido > 0:
            pathstablist = []
            for path in keypaths:
                long, lat = get_long_lat(path)
                if path in pedict:
                    ic = gr.degree(grafo,ic)
                else:
                    ic = 1
                info = {
                    'node-id':path,
                    'long':long,
                    'lat':lat,
                    'individual-id':id,
                    'individual-count':ic
                }
                pathstablist.append(info)
            if genero == g:
                info = {
                    'individual-id':id,
                    'animal-taxom':spec['animal-taxon'],
                    'animal-life-stage':spec['animal-life-stage'],
                    'animal-sex':spec['animal-sex'],
                    'study-site':spec['study-site'],
                    'travel-dist':round(recorrido,3),
                    'deployment-comments':spec['deployment-comments']
                }
                path_details = {
                    'num_nodos':nodos,
                    'num_arcos':nodos-1,
                    'max_dist':round(peso_arco(primer_punto,punto_previo),3),
                    'path':pathstablist
                }
                r = {'info': info,
                    'path_details':path_details}
                lt.addLast(listinfo,r)
    merg.sort(listinfo,req_6_sort_criteria)
    
    lista1 = listinfo["elements"][0]["path_details"]["path"]
    lista2 = listinfo["elements"][-1]["path_details"]["path"]
    
    for elemento in lista1:
        lat = elemento["lat"]
        long = elemento["long"]
        list_polyline1.append((float(lat),float(long)))
        folium.Marker([lat, long],  
                        tooltip=elemento["node-id"], 
                        icon=folium.Icon(color="blue", 
                        icon="info-sign")).add_to(mapafo6)
    for elemento in lista2:
        lat = elemento["lat"]
        long = elemento["long"]
        list_polyline2.append((float(lat),float(long)))
        folium.Marker([lat, long],  
                        tooltip=elemento["node-id"], 
                        icon=folium.Icon(color="red", 
                        icon="info-sign")).add_to(mapafo62)
    
    folium.PolyLine(list_polyline1, tooltip="Coast").add_to(mapafo6)  
    folium.PolyLine(list_polyline2, tooltip="Coast").add_to(mapafo62)   
    
    
    return listinfo, mapafo6, mapafo62


def req_7(control, fi, ff, ti, tf):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    fecha_i = d.datetime.strptime(fi, '%Y-%m-%d %H:%M:%S')
    fecha_f = d.datetime.strptime(ff, '%Y-%m-%d %H:%M:%S')
    
    mapa = control["map"]
    mapa_final = mp.newMap(45,maptype='PROBING',loadfactor=0.5)
    grafo7 = gr.newGraph(datastructure='ADJ_LIST', directed=True) 
    
    for id in lt.iterator(mp.keySet(mapa)):
        lista = me.getValue(mp.get(mapa, id))
        lst = lt.newList("ARRAY_LIST")
        for registro in lt.iterator(lista):
            temp = registro["external-temperature"]
            fecha = d.datetime.strptime(registro['timestamp'], '%Y-%m-%d %H:%M')
            if (float(ti) <= float(temp) <= float(tf)) and (fecha_i <= fecha <= fecha_f):
                lt.addLast(lst, registro)       
        if lt.size(lst) != 0:
            mp.put(mapa_final, id, lst)
    # crear el grafo
    pe = {}
    # Diccionario auxiliar par chequear los puntos recorridos por el lobo
    pl = {}
    for lobo in lt.iterator(mp.keySet(mapa_final)):
        # obtener el diccionario llave: valor: del mapa, llave
        dic = mp.get(mapa_final, lobo)
        # obtener los valores para dicha llave
        lista = me.getValue(dic)
        last_key = ''
        for event in lt.iterator(lista):
            key = data_key_generator(event)
            pe_key = data_key_generator_pe(event)
            idlobo = data_id_generator(event)     
            # Si es el primer evento
            if last_key == '':
                gr.insertVertex(grafo7,key)
                if pe_key not in pe:
                    pe[pe_key]=[key]
                else:
                    # Caso de primeros 2 lobos que genera un punto de encuentro
                    if len(pe[pe_key]) == 1:
                        gr.insertVertex(grafo7,pe_key)
                        gr.addEdge(grafo7,pe[pe_key][0],pe_key)
                        gr.addEdge(grafo7,pe_key,pe[pe_key][0])
                    pe[pe_key]+=[key]
                    gr.addEdge(grafo7,key,pe_key)
                    gr.addEdge(grafo7,pe_key,key)
                pl[idlobo]=[key]
                last_key = key
            # Si este no es un punto repetido
            elif (last_key != key) and (key not in pl[idlobo]):
                gr.insertVertex(grafo7,key)
                peso = peso_arco(last_key,key)
                gr.addEdge(grafo7,last_key,key,peso)
                if pe_key not in pe:
                    pe[pe_key]=[key]
                else:
                    # Caso de primeros 2 lobos que genera un punto de encuentro
                    if len(pe[pe_key]) == 1:
                        gr.insertVertex(grafo7,pe_key)
                        gr.addEdge(grafo7,pe[pe_key][0],pe_key)
                        gr.addEdge(grafo7,pe_key,pe[pe_key][0])
                    pe[pe_key]+=[key]
                    gr.addEdge(grafo7,key,pe_key)
                    gr.addEdge(grafo7,pe_key,key)
                pl[idlobo] += [key]
                last_key = key
            elif key in pl[idlobo]:
                peso = peso_arco(last_key,key)
                ed = gr.getEdge(grafo7,last_key,key)
                if ed is None and pl[idlobo][-1] != key:
                    gr.addEdge(grafo7,last_key,key,peso)
                pl[idlobo] += [key]
                last_key = key
        
    info_lobos = control["map_spec"]
    mapa_scc = scc.KosarajuSCC(grafo7)
    num_cc = scc.connectedComponents(mapa_scc)
    print(num_cc)
    mapa_idscc = mapa_scc["idscc"]
    llaves_mapa = mp.keySet(mapa_idscc)
    mapa_cc = mp.newMap(numelements=num_cc, maptype="PROBING")
    mapafo3 = folium.Map(location=[56.530377, -113.513191])
    
    for id in lt.iterator(llaves_mapa):
        value = me.getValue(mp.get(mapa_idscc, id))
        conjunto_manada = mp.get(mapa_cc, value)
        if conjunto_manada != None:
            lista = me.getValue(conjunto_manada)
            lt.addLast(lista, id)
            mp.put(mapa_cc, value, lista)
        else:
            lista = lt.newList("ARRAY_LIST")
            lt.addLast(lista, id)
            mp.put(mapa_cc, value, lista)
      
    id_manadas = mp.keySet(mapa_cc)  
    lista_final = lt.newList("ARRAY_LIST")   
    
    for id_manada in lt.iterator(id_manadas):
        conjunto = mp.get(mapa_cc, id_manada)
        lista = me.getValue(conjunto)
        if lt.size(lista) > 1:
            lt.addLast(lista_final, elemento_a_lista_3(id_manada,lista,info_lobos))
    
    merg.sort(lista_final, req_3_sort_criteria)
    lista_tab_final = []
    
    if lt.size(lista_final) > 5:
        lista_tab_final.append(lt.getElement(lista_final, 1))
        lista_tab_final.append(lt.getElement(lista_final, 2))
        lista_tab_final.append(lt.getElement(lista_final, 3))
        lista_tab_final.append(lt.getElement(lista_final, 4))
        lista_tab_final.append(lt.getElement(lista_final, 5))
    else:
        lista_tab_final = lista_final["elements"]
    
    for elemento in lista_tab_final:
        long = (float(elemento[6])+float(elemento[5]))/2
        lat = (float(elemento[4])+float(elemento[3]))/2
        rad = distancia(float(elemento[6]), float(elemento[4]), float(long), float(lat))
        
        folium.Circle(
        radius= rad,
        location=[lat, long],
        popup="Manada",
        color="crimson",
        fill=False,
        ).add_to(mapafo3)
    
    return lista_tab_final, num_cc, mapafo3 


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


def sort_criteria_carga(data_1, data_2):
    """
    sortCriteria criterio de ordenamiento para carga de datos, compara por tiempo de forma ascendente(resultado final de menor fecha a mayor fecha).
    """
    d1 = d.datetime.strptime(data_1['timestamp'], '%Y-%m-%d %H:%M')
    d2 = d.datetime.strptime(data_2['timestamp'], '%Y-%m-%d %H:%M')
    
    if d1 < d2:
        return True
    else:
        return False
    

def req_3_sort_criteria(l1, l2):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    data_1 = int(l1[2])
    data_2 = int(l2[2])
    
    if data_1 > data_2:
        return True
    else:
        return False

def req_5_sort_criteria(d1, d2):
    """
    Función encargada de ordenar la lista con los datos por 1: Distancia recorrida, 2: # puntos de encuentro y seguimiento visitados
    """    
    if d1['Distancia recorrida [km]'] > d2['Distancia recorrida [km]']:
        return True
    else:
        return False
def req_5_sort_criteria_2(d1, d2):
    """
    Función encargada de ordenar la lista con los datos por 1: Distancia recorrida, 2: # puntos de encuentro y seguimiento visitados
    """    
    if d1['Puntos de encuentro y seguimiento visitados'] > d2['Puntos de encuentro y seguimiento visitados']:
        return True
    else:
        return False
    
def req_6_sort_criteria(d1, d2):
    """
    Función encargada de ordenar la lista con los datos por 1: Distancia recorrida
    """    
    if d1['info']['travel-dist'] > d2['info']['travel-dist']:
        return True
    else:
        return False
