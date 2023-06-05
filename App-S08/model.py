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
assert cf
import geopy as geo
from geopy import distance
import math as mt
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
    data_structs = {"dirigido": None,
                    "no_dirigido":None,
                    "mp_lobos":None,
                    "lt_lobos_a2" :None,
                    "lt_todos": None,
                    "mp_puntos":None}
    
    data_structs["dirigido"] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000)
    data_structs["no_dirigido"] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000)
    data_structs["mp_lobos"] = mp.newMap(20, 
                                   maptype="PROBING",
                                   loadfactor=0.5) 
    data_structs["mp_lobos_a2"] = mp.newMap(20, 
                                   maptype="PROBING",
                                   loadfactor=0.5)
    
    data_structs["lt_lobos_a2"] = lt.newList("ARRAY_LIST")
    data_structs["lt_todos"] = lt.newList("ARRAY_LIST")
    data_structs["mp_puntos"] =mp.newMap(20,
                                        maptype="PROBING",
                                        loadfactor=0.5)
    data_structs["puntos_encuentro"] = lt.newList("ARRAY_LIST")
    data_structs["Fechas"] = om.newMap(omaptype="RBT", cmpfunction=compareFecha)
    return data_structs

# Funciones para agregar informacion al modelo

def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    lt.addLast(data_structs["lt_todos"], data)
    lon_lat_lobo1 = formato_coo_id(data)
    lon_lat = formato_coo(data)
    add_lobo_mp(data_structs, data)
    add_puntos(data_structs, lon_lat, data)
    add_vertice(data_structs["dirigido"], lon_lat_lobo1)
    add_vertice(data_structs["no_dirigido"], lon_lat_lobo1)
    om_fechas(data_structs, data)

def add_data2(data_structs, data):
    lt.addLast(data_structs["lt_lobos_a2"], data)
    add_lobo_mp_a2(data_structs, data)
    #add_lobo_mp(data_structs, data)
    
# Funciones para creacion de datos

def add_lobo_mp_a2(data_structs, data):
    mp_lobos = data_structs["mp_lobos_a2"]
    lobo_id = str(data["animal-id"])
    tag_id = str(data["tag-id"])
    lobo = lobo_id+"_"+tag_id
    existelobo = mp.contains(mp_lobos, lobo)
    if existelobo:
        entry = mp.get(mp_lobos, lobo)
        lobo_id = me.getValue(entry)
    else:
        lobo_id = lt.newList("ARRAY_LIST")
        mp.put(mp_lobos, lobo, lobo_id)
    lt.addLast(lobo_id, data)
    return data_structs

def formato_coo(data):
    lon = float(data["location-long"])
    lon = str(round(lon,3))
    lon = lon.replace("-", "m")
    lon = lon.replace(".", "p")
    lat = float(data["location-lat"])
    lat = str(round(lat,3))
    lat = lat.replace("-", "m")
    lat = lat.replace(".", "p")
    resulatdo = lon+"_"+lat
    return resulatdo

def formato_coo_id(data):
    lon_lat = formato_coo(data)
    id_lobo = str(data["individual-local-identifier"])
    id_tag = str(data["tag-local-identifier"])
    resulatdo = lon_lat+"_"+id_lobo+"_"+id_tag
    return resulatdo

def distancia_fn (data, data_fin):
    longitud_1 = float(data["location-long"])
    longitud_1 = round(longitud_1,3)
    latitud_1 = float(data["location-lat"])
    latitud_1 = round(latitud_1,3)
    longitud_2 = float(data_fin["location-long"])
    longitud_2 = round(longitud_2,3)
    latitud_2 = float(data_fin["location-lat"])
    latitud_2 = round(latitud_2,3)
    longitud_1, longitud_2, latitud_1, latitud_2 = map(mt.radians, [longitud_1, longitud_2, latitud_1, latitud_2])
    resta_longitud=(longitud_2-longitud_1)/2
    resta_latitudes=(latitud_2-latitud_1)/2
    cos_lat_1= mt.cos(latitud_1)
    cos_lat_2= mt.cos(latitud_2)
    raiz=mt.sqrt((mt.sin(resta_latitudes)**2)+(cos_lat_1*cos_lat_2*(mt.sin(resta_longitud)**2)))
    total=2*(mt.asin(raiz))*6371.009
    return round(total,3)

def add_vertice(data_structs, lon_lat_lobo):
    if not gr.containsVertex(data_structs, lon_lat_lobo):
        gr.insertVertex(data_structs, lon_lat_lobo)
    return data_structs

def auxiliar(data_structs):
    mp_lobos = data_structs["mp_lobos"]
    llaves = mp.keySet(mp_lobos)
    for llave in lt.iterator(llaves):
        lobo = mp.get(mp_lobos, llave)
        lista_lobo = me.getValue(lobo)
        merg.sort(lista_lobo, cmp_lobos_by_antiguo_reciente)
        a = 1
        b = 2
        while b <= lt.size(lista_lobo):
            if lt.size(lista_lobo) > 1:
                vertice_A = (lt.getElement(lista_lobo, a))
                vertice_B = (lt.getElement(lista_lobo, b))
                distancia = distancia_fn(vertice_A, vertice_B)
                if distancia > 0:
                    vertice_A = formato_coo_id(vertice_A)
                    vertice_B = formato_coo_id(vertice_B)
                    add_arcos(data_structs, vertice_A, vertice_B, distancia) 
                a+=1
                b+=1
    return data_structs
    
def add_arcos(data_structs, verticeA, verticeB, distancia):
    edge = gr.getEdge(data_structs["dirigido"], verticeA, verticeB)
    if edge is None:
        gr.addEdge(data_structs["dirigido"], verticeA, verticeB, distancia)
        edge_nd = gr.getEdge(data_structs["dirigido"], verticeB, verticeA)
        if edge_nd != None and distancia > 0:
            gr.addEdge(data_structs["no_dirigido"], verticeA, verticeB, distancia)
    return data_structs

def add_lobo_mp(data_structs, data):
    mp_lobos = data_structs["mp_lobos"]
    lobo_id = str(data["individual-local-identifier"])
    tag_id = str(data["tag-local-identifier"])
    lobo = lobo_id+tag_id
    existelobo = mp.contains(mp_lobos, lobo)
    if existelobo:
        entry = mp.get(mp_lobos, lobo)
        lobo_id = me.getValue(entry)
    else:
        lobo_id = lt.newList("ARRAY_LIST")
        mp.put(mp_lobos, lobo, lobo_id)
    lt.addLast(lobo_id, data)
    return data_structs
    
def add_puntos(data_structs, lon_lat, data):
    mp_puntos = data_structs["mp_puntos"] 
    existe_punto = mp.contains(mp_puntos, lon_lat)
    if existe_punto:
        entry = mp.get(mp_puntos, lon_lat)
        lobo_id = me.getValue(entry)
    else:
        lobo_id = lt.newList("ARRAY_LIST")
        mp.put(mp_puntos, lon_lat, lobo_id)
    existe = False
    for a in lt.iterator(lobo_id):
        coordenadas = formato_coo(a)
        if lon_lat == coordenadas and data["individual-local-identifier"] == a["individual-local-identifier"] and data["tag-local-identifier"] == a["tag-local-identifier"]: #ademas del id de lobo. es el tag tambien
            existe = True
    if not existe:
        lt.addLast(lobo_id, data)
    return data_structs

# Funciones auxiliares

def puntos_enc_m(data_structs):
    puntos_encuentr = lt.newList("ARRAY_LIST")
    mp_puntos = data_structs["mp_puntos"]
    llaves_p = mp.keySet(mp_puntos)
    for llave_p in lt.iterator(llaves_p):
        coor = mp.get(mp_puntos, llave_p)
        lista_coor = me.getValue(coor)
        if lt.size(lista_coor) > 1:
            lt.addLast(puntos_encuentr, llave_p)
    for cada_lon_lat in lt.iterator(puntos_encuentr):
        add_vertice(data_structs["dirigido"], cada_lon_lat)
        add_vertice(data_structs["no_dirigido"], cada_lon_lat)
    data_structs["puntos_encuentro"] = puntos_encuentr
    return puntos_encuentr

def conectar_p_encu(data_structs): 
    mp_puntos = data_structs["mp_puntos"]
    llaves_p = mp.keySet(mp_puntos)
    for llave_p in lt.iterator(llaves_p):
        coor = mp.get(mp_puntos, llave_p)
        lista_coor = me.getValue(coor)
        if lt.size(lista_coor) > 1:
            for dato in lt.iterator(lista_coor):
                comparar = formato_coo(dato)
                verticeA = formato_coo_id(dato)
                if comparar == llave_p:
                    add_arcos(data_structs, llave_p, verticeA, 0)
                    add_arcos(data_structs, verticeA, llave_p, 0)
                    gr.addEdge(data_structs["no_dirigido"], llave_p, verticeA, 0)
    return data_structs

def primeros_ultimos(data_structs):
    #añadir a lista los datos de un nodo.
    lista_vertices = gr.vertices(data_structs["dirigido"])
    longi_menor = 500
    longi_mayor = -500
    lati_menor = 500
    lati_mayor = -500
    for cada_vertice in lt.iterator(lista_vertices):  
        lon, lat = inverso_coo(cada_vertice)
        if lon > longi_mayor:
            longi_mayor = lon
        if lon < longi_menor:
            longi_menor = lon
        if lat > lati_mayor:
            lati_mayor = lat
        if lat < lati_menor:
            lati_menor = lat
    primeros = lt.subList(lista_vertices, 1, 5)
    ultimos = lt.subList(lista_vertices, lt.size(lista_vertices)-4, 5)
    tabla = lt.newList()
    for eleme in lt.iterator(primeros):
        tabu = tabular_datos_carga(data_structs, eleme)
        lt.addLast(tabla, tabu)
    for dato in lt.iterator(ultimos):
        tabu2 = tabular_datos_carga(data_structs, dato)
        lt.addLast(tabla, tabu2)
    return tabla, lati_mayor, lati_menor, longi_mayor, longi_menor

def tabular_datos_carga(data_structs, nodo):
    lon, lat = inverso_coo(nodo)
    retorno = {"LON_APROX": lon,
               "LAT_APROX": lat,
               "NODE_ID": nodo,
               "INDIVIDUAL_ID":0,
               "ADJACENT_NODES":lt.size(gr.adjacentEdges(data_structs["dirigido"], nodo))}
    spl = nodo.split("_")
    if len(spl) == 4:
        id_individuo = spl[2]+"_"+spl[3]
        retorno["INDIVIDUAL_ID"] = id_individuo
    elif len(spl) == 5:
        id_individuo = spl[2]+"_"+spl[3]+"_"+spl[4]
        retorno["INDIVIDUAL_ID"] = id_individuo
    elif len(spl) == 2: #es punto de encuentro
        lista_adya = gr.adjacentEdges(data_structs["dirigido"], nodo)
        lst = []
        for adyacente in lt.iterator(lista_adya):
            nodo_adya = adyacente["vertexB"]
            spl = nodo_adya.split("_")
            if len(spl) == 4:
                id_individuo = spl[2]+"_"+spl[3]
            elif len(spl) == 5:
                id_individuo = spl[2]+"_"+spl[3]+"_"+spl[4]
            lst.append(id_individuo)
        string = ", ".join(lst)
        retorno["INDIVIDUAL_ID"] = string
    return retorno
    
def req_1(data_structs, vertexA, vertexB):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    if not gr.containsVertex(data_structs["dirigido"], vertexA):
        return False
    if not gr.containsVertex(data_structs["dirigido"], vertexB):
        return False
    search = dfs.DepthFirstSearch(data_structs["dirigido"], vertexA)
    camino  = dfs.pathTo(search, vertexB)
    existe = str(dfs.hasPathTo(search, vertexB))
    tama_cam = st.size(camino)
    punto_encuentro = 0
    vertices_seg = 0
    lista_distancia = lt.newList()
    for dato in lt.iterator(camino):
        lt.addLast(lista_distancia, dato)
        tama = dato.split("_")
        if len(tama) == 2:
            punto_encuentro +=1
        else:
            vertices_seg +=1
    distancia = 0
    i = 0
    while i < lt.size(lista_distancia):
        act = lt.getElement(lista_distancia, i)
        sig = lt.getElement(lista_distancia, i+1)
        act_lon = inverso_coo(act)[0]
        act_lat = inverso_coo(act)[1]
        sig_lon = inverso_coo(sig)[0]
        sig_lat = inverso_coo(sig)[1]
        distancia += harvesine_simple(act_lon, act_lat, sig_lon, sig_lat)
        i+=1
    
    tabular = tabularR1_R2(data_structs, camino)
    return existe, tama_cam, punto_encuentro, vertices_seg, tabular, round(distancia,6)

def inverso_coo(vertice):
    lt_ll = vertice.split("_")
    lon = lt_ll[0].replace("p",".").replace("m","-")
    lat = lt_ll[1].replace("p",".").replace("m","-")
    return float(lon), float(lat)

def harvesine_simple(longitud_1, latitud_1, longitud_2, latitud_2):
    longitud_1, longitud_2, latitud_1, latitud_2 = map(mt.radians, [longitud_1, longitud_2, latitud_1, latitud_2])
    resta_longitud=(longitud_2-longitud_1)/2
    resta_latitudes=(latitud_2-latitud_1)/2
    raiz=mt.sqrt((mt.sin(resta_latitudes)**2)+(mt.cos(latitud_1)*mt.cos(latitud_2)*(mt.sin(resta_longitud)**2)))
    total=2*(mt.asin(raiz))*6371.009
    return round(total,3)
def tabular_datos(eleme, data_structs):
    lon = inverso_coo(eleme)[0]
    lat = inverso_coo(eleme)[1]
    elemento = {"LON_APROX":lon,
                "LAT_APROX":lat,
                "NODE_ID": eleme,
                "INDIVIDUAL_ID":lt.newList(),
                "INDIVIDUAL_COUNT": 0,
                "EDGE_TO": 0,
                "EDGE_DISTANCE[km]":0}
    for ind in lt.iterator(gr.adjacents(data_structs["dirigido"], eleme)):
        spl = ind.split("_")
        if len(spl) == 4:
            id_individuo = spl[2]+"_"+spl[3]
            if not lt.isPresent(elemento["INDIVIDUAL_ID"], id_individuo):
                lt.addLast(elemento["INDIVIDUAL_ID"],id_individuo)
        elif len(spl) == 5:
            id_individuo = spl[2]+"_"+spl[3]+"_"+spl[4]
            if not lt.isPresent(elemento["INDIVIDUAL_ID"], id_individuo):
                lt.addLast(elemento["INDIVIDUAL_ID"],id_individuo)
    elemento["INDIVIDUAL_COUNT"] = lt.size(elemento["INDIVIDUAL_ID"])
    lst = []
    for eleme in lt.iterator(elemento["INDIVIDUAL_ID"]):
        if lt.size(elemento["INDIVIDUAL_ID"]) > 6:
            prims = lt.subList(elemento["INDIVIDUAL_ID"], 1, 3)
            ults = lt.subList(elemento["INDIVIDUAL_ID"], lt.size(elemento["INDIVIDUAL_ID"])-2, 3)
            for i in lt.iterator(prims):
                lst.append(i)
            for a in lt.iterator(ults):
                lst.append(a)
        else:
            lst.append(eleme)
    elemento["INDIVIDUAL_ID"] = lst
    string = ", ".join(elemento["INDIVIDUAL_ID"])
    elemento["INDIVIDUAL_ID"] = string
    return elemento

def req_2(data_structs, vertex_i, vertex_f ):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    if not gr.containsVertex(data_structs["dirigido"], vertex_i):
        return False
    if not gr.containsVertex(data_structs["dirigido"], vertex_f):
        return False
    find = bfs.BreadhtFisrtSearch(data_structs["dirigido"], vertex_i)
    path = bfs.pathTo(find, vertex_f)
    existe = str(bfs.hasPathTo(find,vertex_f))
    puntos_encuentro = 0
    vertices_seguidos = 0
    lista_recorrido = lt.newList()
    for dato in lt.iterator(path):
        lt.addLast(lista_recorrido, dato)
        nodo = dato.split("_")
        if len(nodo) == 2:
            puntos_encuentro += 1
        else:
            vertices_seguidos +=1
    nodes = lt.size(lista_recorrido)
    distancia = 0
    i =0
    while i < lt.size(lista_recorrido):
        act = lt.getElement(lista_recorrido, i)
        sig = lt.getElement(lista_recorrido, i+1)
        act = (inverso_coo(act)[0],inverso_coo(act)[1])
        sig = (inverso_coo(sig)[0], inverso_coo(sig)[1])
        distancia += harvesine_simple(act[0], act[1], sig[0], sig[1])
        i+=1
    tabla = tabularR1_R2(data_structs, path)
    return existe, nodes, puntos_encuentro, vertices_seguidos, tabla, round(distancia,6)
    
def tabularR1_R2(data_structs,camino):
    tabular = lt.newList("ARRAY_LIST")
    while not st.isEmpty(camino):
        eleme = st.pop(camino)
        elemento = tabular_datos(eleme, data_structs)
        lt.addLast(tabular, elemento)
    a = 1
    while a <= lt.size(tabular):
        siguiente = lt.getElement(tabular, a+1)
        actual = lt.getElement(tabular, a)
        actual["EDGE_TO"] = siguiente["NODE_ID"]
        longitud_1 = float(actual["LON_APROX"])
        latitud_1 = float(actual["LAT_APROX"])
        longitud_2 = float(siguiente["LON_APROX"])
        latitud_2 = float(siguiente["LAT_APROX"])
        actual["EDGE_DISTANCE[km]"] = harvesine_simple(longitud_1, latitud_1, longitud_2, latitud_2)
        a+=1
        if a == lt.size(tabular):
            siguiente["EDGE_TO"] = "Desconocido"
            siguiente["EDGE_DISTANCE[km]"] = "Desconocido"
            break
    return tabular

def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    kosaraju = scc.KosarajuSCC(data_structs["dirigido"])
    conectados = scc.connectedComponents(kosaraju)
    mapa_ids = kosaraju["idscc"]
    mapa_nuevo = mp.newMap(20, maptype="PROBING", loadfactor=0.5)
    for llaves in lt.iterator(mp.keySet(mapa_ids)):
        valores = me.getValue(mp.get(mapa_ids, llaves))
        agregar_id(mapa_nuevo, valores, llaves)
    lt_ordenar_mayor = lt.newList()
    for keys in lt.iterator(mp.keySet(mapa_nuevo)):
        lista = me.getValue(mp.get(mapa_nuevo, keys))
        lt.addLast(lt_ordenar_mayor, lt.size(lista)) 
    merg.sort(lt_ordenar_mayor, ordenar_mayor)
    top = lt.newList()
    a=1
    for tamano in lt.iterator(lt_ordenar_mayor):
        for llave in lt.iterator(mp.keySet(mapa_nuevo)):
            lista = me.getValue(mp.get(mapa_nuevo, llave))
            if lt.size(lista) == tamano:
                anadir = {"IDSCC":llave, "NODE_IDS":lista}
                lt.addLast(top, anadir)
                break
        a+=1
        if a == 6:
            break
    tabular = tabla_req3(data_structs, top)
    return conectados, tabular

def tabla_req3(data_structs, lista):
    resultado = lt.newList()
    i = 1
    while i < 6:
        lt_datos = lt.getElement(lista, i)
        dic = {"SCCID":lt_datos["IDSCC"],
               "NODE_IDs":None,
               "SCC_SIZE":lt.size(lt_datos["NODE_IDS"]),
               "MIN-LAT": 0,
               "MAX-LAT": 0,
               "MIN-LON": 0,
               "MAX-LON": 0,
               "WOLF_COUNT":0,
               "WOLF_DETAILS":lt.newList()}
        if lt.size(lt_datos["NODE_IDS"]) >6:
            prim3 = lt.subList(lt_datos["NODE_IDS"], 1, 3)
            ult3 = lt.subList(lt_datos["NODE_IDS"], lt.size(lt_datos["NODE_IDS"])-2, 3)
            lista_ids = lt.newList()
            for datoA in lt.iterator(prim3):
                lt.addLast(lista_ids, datoA)
            for datoB in lt.iterator(ult3):
                lt.addLast(lista_ids, datoB)
        else:
            lista_ids = lt_datos["NODE_IDS"]
        lst = []
        for cada_u in lt.iterator(lista_ids):
            lst.append(cada_u)
            if len(lst) == 3:
                lst.append("...")
        string = ", ".join(lst)
        dic["NODE_IDs"] = string
        longi_menor = 500
        longi_mayor = -500
        lati_menor = 500
        lati_mayor = -500
        lt_nodos = lt.newList()
        for todos_nodos in lt.iterator(lt_datos["NODE_IDS"]):
            lon, lat = inverso_coo(todos_nodos)
            if lon > longi_mayor:
                longi_mayor = lon
            if lon < longi_menor:
                longi_menor = lon
            if lat > lati_mayor:
                lati_mayor = lat
            if lat < lati_menor:
                lati_menor = lat
            partes = todos_nodos.split("_")
            if len(partes) == 4:
                id_lobo = partes[2]+"_"+partes[3]
                if not lt.isPresent(lt_nodos, id_lobo):
                    lt.addLast(lt_nodos, id_lobo)
            elif len(partes) == 5:
                id_lobo = partes[2]+"_"+partes[3]+"_"+partes[4]
                if not lt.isPresent(lt_nodos, id_lobo):
                    lt.addLast(lt_nodos, id_lobo)
        dic["WOLF_COUNT"] = lt.size(lt_nodos)
        if lt.size(lt_nodos) > 6:
            primeros = lt.subList(lt_nodos, 1, 3)
            ultimos = lt.subList(lt_nodos, lt.size(lt_nodos)-2, 3)
            for id_lob in lt.iterator(primeros):
                dicc = detalles_lobo(data_structs, id_lob)
                lt.addLast(dic["WOLF_DETAILS"], dicc)
            for id_lob2 in lt.iterator(ultimos):
                dicc = detalles_lobo(data_structs, id_lob2)
                lt.addLast(dic["WOLF_DETAILS"], dicc)
        else:  
            for id_lob in lt.iterator(lt_nodos):
                dicc = detalles_lobo(data_structs, id_lob)
                lt.addLast(dic["WOLF_DETAILS"], dicc)
        dic["MAX-LAT"] = lati_mayor
        dic["MIN-LAT"] = lati_menor
        dic["MAX-LON"] = longi_mayor
        dic["MIN-LON"] = longi_menor
        lt.addLast(resultado, dic)
        i+=1
    return resultado
        
def detalles_lobo(data_structs, id_lobo):
    lt_lobos_detalles = data_structs["lt_lobos_a2"]
    detalles = {"id_individual":id_lobo,
                "animal_sex":"Desconocido",
                "life_stage":"Desconocido",
                "study_site":"Desconocido",
                "deployment_comments":"Desconocido"}
    
    for cada_lobo in lt.iterator(lt_lobos_detalles): #id_lobo+_+id_tag
        id_ind = str(cada_lobo["animal-id"])
        id_tag = str(cada_lobo["tag-id"])
        if id_lobo == id_ind+"_"+id_tag:
            if cada_lobo["animal-sex"] != "":
                detalles["animal_sex"] = cada_lobo["animal-sex"]
            if cada_lobo["animal-life-stage"] != "":
                detalles["life_stage"] = cada_lobo["animal-life-stage"]
            if cada_lobo["study-site"] != "":
                detalles["study_site"] = cada_lobo["study-site"]
            if cada_lobo["deployment-comments"] != "":
                detalles["deployment_comments"] = cada_lobo["deployment-comments"]
            break
    return detalles
        
def agregar_id(mapa, llave, data):
    existelobo = mp.contains(mapa, llave)
    if existelobo:
        entry = mp.get(mapa, llave)
        lobo_id = me.getValue(entry)
    else:
        lobo_id = lt.newList("ARRAY_LIST")
        mp.put(mapa, llave, lobo_id)
    lt.addLast(lobo_id, data)

def ordenar_mayor(dato1, dato2):
    if (dato1) > (dato2):
        return True
    else:
        return False

def req_4(data_structs, localizacion_1, localizacion_2):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4}
    latitud_i = float(localizacion_1[1])
    longitud_i = float(localizacion_1[0])
    pos_i= (latitud_i, longitud_i)
    
    latitud_f = float(localizacion_2[1])
    longitud_f = float(localizacion_2[0])
    pos_f = (latitud_f, longitud_f)
    distancia_i = 900000000000
    distancia_f = 900000000000
    vertice_cerca_i = 0
    vertice_cerca_f = 0
    nodos = data_structs["puntos_encuentro"]
    for vertex_i in lt.iterator(nodos):
        long_temp = inverso_coo(vertex_i)[0]
        lat_temp = inverso_coo(vertex_i)[1]
        pos_temp = (lat_temp,long_temp)
        distancia_temp_i = distance.distance(pos_i, pos_temp).km
        if distancia_temp_i < distancia_i:
            vertice_cerca_i = vertex_i
            distancia_i = distancia_temp_i
        if distancia_i == 0:
            #encontro la mas cercana
            break
 
    for vertex_f in lt.iterator(nodos):
        long_temp = inverso_coo(vertex_f)[0]
        lat_temp = inverso_coo(vertex_f)[1]
        pos_temp_f = (lat_temp,long_temp)
        distancia_temp_f = distance.distance(pos_f, pos_temp_f).km
        if distancia_temp_f < distancia_f:
            vertice_cerca_f = vertex_f
            distancia_f = distancia_temp_f
        if distancia_f == 0:
            #encontro la mas cercana
            break
 
    recorrido = djk.Dijkstra(data_structs["dirigido"], vertice_cerca_i)
    costo = djk.distTo(recorrido, vertice_cerca_f)
    total_nodos = djk.pathTo(recorrido, vertice_cerca_f)
    if total_nodos is None:
        return False
    num_nodos = st.size(total_nodos)
    tabla1 = tablas_peq_req4(data_structs, vertice_cerca_i)
    tabla2 = tablas_peq_req4(data_structs, vertice_cerca_f)
    
    tabular2 = lt.newList("ARRAY_LIST")
    while not st.isEmpty(total_nodos):
        eleme = st.pop(total_nodos)
        elemento = tabla2_r4(eleme, data_structs)
        lt.addLast(tabular2, elemento)
        
    return round(costo,3), round(distancia_i,3), round(distancia_f,3), tabla1, tabla2, num_nodos, tabular2
            
def tablas_peq_req4(data_structs, nodo):
    resultado = lt.newList()
    data = {"node_id":nodo,
            "long_aprox":0,
            "lat_aprox":0,
            "individual_id":lt.newList()}
    lon, lat = inverso_coo(nodo)
    data["long_aprox"] = lon
    data["lat_aprox"] = lat
    lt_adyacentes = gr.adjacentEdges(data_structs["dirigido"], nodo)
    for individuo in lt.iterator(lt_adyacentes):
        partes = individuo["vertexB"].split("_")
        if len(partes) == 4:
            id_lobo = partes[2]+"_"+partes[3]
            if not lt.isPresent(data["individual_id"], id_lobo):
                lt.addLast(data["individual_id"], id_lobo)
        elif len(partes) == 5:
            id_lobo = partes[2]+"_"+partes[3]+"_"+partes[4]
            if not lt.isPresent(data["individual_id"], id_lobo):
                lt.addLast(data["individual_id"], id_lobo)
    lst = []
    for cada_adyacente in lt.iterator(data["individual_id"]):
        lst.append(cada_adyacente)
    string = ", ".join(lst)
    data["individual_id"] = string
    lt.addLast(resultado, data)
    return resultado
        
def tabla2_r4(eleme, data_structs):
    lon1, lat1 = inverso_coo(eleme["vertexA"])
    lon2, lat2 = inverso_coo(eleme["vertexB"])
    distancia = harvesine_simple(lon1, lat1, lon2, lat2)
    data = {"src_node_id":eleme["vertexA"],
                "lat_src":lat1,
                "lon_src":lon1,
                "tgt_node_id":eleme["vertexB"],
                "lat_tgt":lat2,
                "lon_tgt":lon2,
                "individual_id":lt.newList(),
                "distance[km]":distancia}
    for ind in lt.iterator(gr.adjacents(data_structs["dirigido"], eleme["vertexA"])):
        partes = ind.split("_")
        if len(partes) == 4:
            id_lobo = partes[2]+"_"+partes[3]
            if not lt.isPresent(data["individual_id"], id_lobo):
                lt.addLast(data["individual_id"], id_lobo)
        elif len(partes) == 5:
            id_lobo = partes[2]+"_"+partes[3]+"_"+partes[4]
            if not lt.isPresent(data["individual_id"], id_lobo):
                lt.addLast(data["individual_id"], id_lobo)
    lst = []
    for cada_adyacente in lt.iterator(data["individual_id"]):
        lst.append(cada_adyacente)
    string = ", ".join(lst)
    data["individual_id"] = string
    return data   


def req_5(data_structs, origen, distancia_max, puntos_min):
    """
    Función que soluciona el requerimiento 5
    """
    #DATOS INICIALES
    grafo = data_structs["no_dirigido"]
    recorrido_0 = lt.newList("ARRAY_LIST")
    lt.addLast(recorrido_0, origen)
    dato_0 = (0, recorrido_0)
    distancia = distancia_max/2
    caminos = lt.newList("ARRAY_LIST")
    cola_distancias = mpq.newMinPQ(cmp_menor_distancia)
    mpq.insert(cola_distancias, dato_0)
    
    while mpq.isEmpty(cola_distancias) == False:
        dato = mpq.delMin(cola_distancias)
        distancia_act = dato[0]
        recorrido_act = dato[1]
        nodo_act = lt.lastElement(recorrido_act)
        
        #OBTENER LONGITUD Y LATITUD
        nodo_act = nodo_act.replace("m", "-")
        nodo_act = nodo_act.replace("p", ".")
        spl = nodo_act.split("_")
        lon_act = float(spl[0])
        lat_act = float(spl[1])
        
        if (distancia_act <= distancia) and (len(recorrido_act) >= puntos_min):
            lt.addLast(caminos, dato)
            
        if (distancia_act <= distancia) and (len(recorrido_act) < puntos_min):
            for v in gr.adjacents(grafo, nodo_act):
                #OBTENER LONGITUD Y LATITUD
                v = v.replace("m", "-")
                v = v.replace("p", ".")
                spl = v.split("_")
                lon = float(spl[0])
                lat = float(spl[1])
                #NUEVOS DATOS
                distancia_new = distancia_act + harvesine_simple(lon_act, lat_act, lon, lat)
                recorrido_new = lt.addLast(v)
                dato_new = (distancia_new, recorrido_new)
                mpq.insert(dato_new)
           
    merg.sort(caminos, cmp_mas_puntos)
    
    #RESULTADOS
    num_max = lt.size(caminos) #1
    corredor_max = lt.firstElement(caminos) #2
    secuencia = corredor_max[1] #2A
    puntos_enc = lt.size(secuencia) #2B
    distancia_rec = corredor_max[0] #2C
    #2D: La secuencia del número posible de individuos visibles en el trayecto
    return num_max, corredor_max, secuencia, puntos_enc, distancia_rec
    
    

def cmp_mas_puntos(dato1, dato2):
    if lt.size(dato1[1]) > lt.size(dato2[1]):
        return True
    else:
        return False
  
def cmp_menor_distancia(dato1, dato2):
    if dato1[0] < dato2[0]:
        return True
    else:
        return False

def req_6(data_structs, fecha1, fecha2, sexo):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    lista_intervalo = om.values(data_structs["Fechas"], fecha1, fecha2)

    mapa_nuevo = mp.newMap(20, 
                            maptype="PROBING",
                            loadfactor=0.5)
    for cada_fecha in lt.iterator(lista_intervalo):
        for evento in lt.iterator(cada_fecha["Datos_fecha"]):
            id_lobo = evento["individual-local-identifier"]
            id_tag = evento["tag-local-identifier"]
            id_vertice = id_lobo+"_"+id_tag
            cada_lobo = lt.firstElement(me.getValue(mp.get(data_structs["mp_lobos_a2"], id_vertice)))
            if cada_lobo["animal-sex"] == sexo:
                existelobo = mp.contains(mapa_nuevo, id_vertice)
                if existelobo:
                    entry = mp.get(mapa_nuevo, id_vertice)
                    lobo_id = me.getValue(entry)
                    lon2 = float(lt.lastElement(lobo_id["Datos"])["location-long"])
                    lat2 = float(lt.lastElement(lobo_id["Datos"])["location-lat"])
                    lon1 = float(evento["location-long"])
                    lat1 = float(evento["location-lat"])
                    lobo_id["Distancia"] += harvesine_simple(lon1, lat1, lon2, lat2)
                    lt.addLast(lobo_id["Nodos"], evento)
                else:
                    lobo_id = {"Datos":lt.newList(), 
                            "Distancia": 0,
                            "Nodos":lt.newList()}
                    mp.put(mapa_nuevo, id_vertice, lobo_id)
                lt.addLast(lobo_id["Datos"], evento)
    
    mas_distancia = 0
    menos_distancia = 5000000
    id_menos = ""
    id_mas = ""
    mas_nodo = ""
    menos_nodo = ""
    lista_nodos_mas = ""
    lista_nodos_menos = ""
    llaves_nuevo = mp.keySet(mapa_nuevo)
    for cada_llave in lt.iterator(llaves_nuevo):
        lista_data_dis = me.getValue(mp.get(mapa_nuevo, cada_llave))
        dist = lista_data_dis["Distancia"]
        cant_nodos = lt.size(lista_data_dis["Nodos"])
        if dist > mas_distancia:
            mas_distancia = dist
            id_mas = cada_llave
            mas_nodo = cant_nodos
            lista_nodos_mas = lista_data_dis["Nodos"]
        if dist < menos_distancia:
            menos_distancia = dist
            id_menos = cada_llave
            menos_nodo = cant_nodos
            lista_nodos_menos = lista_data_dis["Nodos"]

    mas = tabla_peq6(data_structs, id_mas, sexo, mas_distancia)
    menos = tabla_peq6(data_structs, id_menos, sexo, menos_distancia)
    menos_nodos = lt.size(lista_nodos_menos) 
    mas_nodos = lt.size(lista_nodos_mas) 
    tabla_menos = auxiliar_r6(lista_nodos_menos, data_structs)
    tabla_mas = auxiliar_r6(lista_nodos_mas, data_structs)
    return mas, menos, round(mas_distancia,3), round(menos_distancia,3), tabla_menos, menos_nodos, tabla_mas, mas_nodos

def auxiliar_r6(lista_nodos, data_structs):
    if lt.size(lista_nodos) > 6:
        primeros = lt.subList(lista_nodos, 1, 3)
        ultimos = lt.subList(lista_nodos, lt.size(lista_nodos)-2, 3)
        todos =lt.newList()
        for a in lt.iterator(primeros):
            lt.addLast(todos,a)
        for i in lt.iterator(ultimos):
            lt.addLast(todos,i)
    else:
        todos =lista_nodos
    tabla = lt.newList()
    i = 1
    while i <= lt.size(todos):
        dato = lt.getElement(todos, i)
        elemento = tabla_gr_r6(dato, data_structs) 
        lt.addLast(tabla, elemento)  
        i+=1 
    return tabla
    
def om_fechas(data_structs, data):
    fechas = data_structs["Fechas"]    
    if data["timestamp"] != "":
        fecha_csv = data["timestamp"]
    else:
        fecha_csv = ""
    existefecha = om.contains(fechas, fecha_csv)
    if existefecha:
        entry = om.get(fechas, fecha_csv)
        fecha = me.getValue(entry)
    else:
        fecha = new_fecha(fecha_csv)
        om.put(fechas, fecha_csv, fecha)
    lt.addLast(fecha["Datos_fecha"], data)
    
    om_temps = fecha["Om_temperaturas"]
    if data["external-temperature"] != "":
        temp_csv = float(data["external-temperature"])
    else:
        temp_csv = ""
    existetemp = om.contains(om_temps, temp_csv)
    if existetemp:
        entry = om.get(om_temps, temp_csv)
        temperatura = me.getValue(entry)
    else:
        temperatura = lt.newList()
        om.put(om_temps, temp_csv, temperatura)
    lt.addLast(temperatura, data)
    
def new_fecha(fecha):
    entrada = {"Fecha": "", "Datos_fecha": None, "Om_temperaturas":None}
    entrada["Fecha"] = fecha
    entrada["Datos_fecha"] = lt.newList()
    entrada["Om_temperaturas"] = om.newMap(omaptype="RBT", cmpfunction=compare)
    return entrada

def tabla_peq6(data_structs, id_lobo, sexo, distancia):
    resultado = lt.newList()
    datos = {"individual_id": id_lobo,
             "animal_taxon":"Desconocido",
             "animal_life_stage":"Desconocido",
             "animal_sex":sexo,
             "study_site":"Desconocido",
             "travel_dist":distancia,
             "deployment_comments": "Desconocido"}
    lobo = lt.firstElement(me.getValue(mp.get(data_structs["mp_lobos_a2"], id_lobo)))
    if lobo["animal-taxon"] != "":
        datos["animal_taxon"] = lobo["animal-taxon"]
    if lobo["animal-life-stage"] != "":
        datos["animal_life_stage"] = lobo["animal-life-stage"]
    if lobo["study-site"] != "":
        datos["study_site"] = lobo["study-site"] 
    if lobo["deployment-comments"] != "":
        datos["deployment_comments"] = lobo["deployment-comments"]
    lt.addLast(resultado, datos)
    return resultado

def tabla_gr_r6(cada_lobo, data_structs):
    dato = {"node_id":0,
        "long_aprox":0,
        "lat_aprox":0,
        "individual_id":0,
        "individual_count":0}
    
    dato["long_aprox"] = round(float(cada_lobo["location-long"]),3)
    dato["lat_aprox"] = round(float(cada_lobo["location-lat"]),3)
    dato["individual_id"] = cada_lobo["individual-local-identifier"]+"_"+cada_lobo["tag-local-identifier"]
    cadena = str(dato["long_aprox"])+"_"+str(dato["lat_aprox"])+"_"+str(dato["individual_id"])
    dato["node_id"] = cadena.replace(".","p").replace("-","m")
    if len(dato["node_id"].split("_")) > 2:
        dato["individual_count"] = 1
    else:
        dato["individual_count"] = lt.size(gr.adjacentEdges(data_structs["dirigido"], dato["node_id"]))
    return dato

def req_7(data_structs, fecha1, fecha2, temp_max, temp_min):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    nuevo_grafo = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000)
    todos_lobos = lt.newList()
    longi_latis = lt.newList()
    lista_intervalo = om.values(data_structs["Fechas"], fecha1, fecha2)
    #z=1
    for cada_fecha in lt.iterator(lista_intervalo):
        #om_temps = cada_fecha["Om_temperaturas"]
        #print(om_temps)
        #for cada_temp in lt.iterator(om.values(om_temps, temp_max, temp_min)): #ACA ESTA RARO
        #if float(lt.getElement(cada_fecha["Datos_fecha"],z)["external-temperature"]) <=temp_max or float(lt.getElement(cada_fecha["Datos_fecha"],z)["external-temperature"])>=temp_min:
        for evento in lt.iterator(cada_fecha["Datos_fecha"]):
            if float(evento["external-temperature"]) <=temp_max or float(evento["external-temperature"])>=temp_min:
                lt.addLast(todos_lobos, evento)
                lon_lat_lobo = formato_coo_id(evento)
                lon_lat = formato_coo(evento)
                lt.addLast(longi_latis, lon_lat)
                add_vertice(nuevo_grafo, lon_lat_lobo) #AÑADIR VERTICES DE SEGUIMIENTO
        #z+=1
    print(lt.size(todos_lobos))
    a = 1
    b = 2
    while b <= lt.size(todos_lobos): #AÑADIR ARCOS ENTRE P.SEGUIMIENTO
        if lt.size(todos_lobos) > 1:
            vertice_A = (lt.getElement(todos_lobos, a))
            vertice_B = (lt.getElement(todos_lobos, b))
            distancia = distancia_fn(vertice_A, vertice_B)
            if distancia > 0:
                vertice_A = formato_coo_id(vertice_A)
                vertice_B = formato_coo_id(vertice_B)
                edge = gr.getEdge(nuevo_grafo, vertice_A, vertice_B)
                if edge is None:
                    gr.addEdge(nuevo_grafo, vertice_A, vertice_B, distancia)
        a+=1
        b+=1
    c = 1
    mp_puntos = mp.newMap(20,maptype="PROBING",loadfactor=0.5)
    for lon_lat in lt.iterator(longi_latis): 
        data = lt.getElement(todos_lobos, c)
        existe_punto = mp.contains(mp_puntos, lon_lat)
        if existe_punto:
            entry = mp.get(mp_puntos, lon_lat)
            lobo_id = me.getValue(entry)
        else:
            lobo_id = lt.newList("ARRAY_LIST")
            mp.put(mp_puntos, lon_lat, lobo_id)
        existe = False
        for a in lt.iterator(lobo_id):
            coordenadas = formato_coo(a)
            if lon_lat == coordenadas and data["individual-local-identifier"] == a["individual-local-identifier"] and data["tag-local-identifier"] == a["tag-local-identifier"]: #ademas del id de lobo. es el tag tambien
                existe = True
        if not existe:
            lt.addLast(lobo_id, data)
        if c > lt.size(todos_lobos):
            break
        c+=1
    puntos_encuentr = lt.newList("ARRAY_LIST")
    llaves_p = mp.keySet(mp_puntos) #AÑADIR PUNTOS DE ENCUENTRO
    for llave_p in lt.iterator(llaves_p):
        coor = mp.get(mp_puntos, llave_p)
        lista_coor = me.getValue(coor)
        if lt.size(lista_coor) > 1:
            lt.addLast(puntos_encuentr, llave_p)
    for cada_lon_lat in lt.iterator(puntos_encuentr):
        add_vertice(nuevo_grafo, cada_lon_lat)
    llaves_p = mp.keySet(mp_puntos) #CONECTAR PUNTOS DE ENCUENTRO
    for llave_p in lt.iterator(llaves_p):
        coor = mp.get(mp_puntos, llave_p)
        lista_coor = me.getValue(coor)
        if lt.size(lista_coor) > 1:
            for dato in lt.iterator(lista_coor):
                comparar = formato_coo(dato)
                verticeA = formato_coo_id(dato)
                if comparar == llave_p:
                    edge = gr.getEdge(nuevo_grafo, llave_p, verticeA)
                    if edge is None:
                        gr.addEdge(nuevo_grafo, llave_p, verticeA, 0)
                    edge2 = gr.getEdge(nuevo_grafo, verticeA, llave_p)
                    if edge2 is None:
                        gr.addEdge(nuevo_grafo, verticeA, llave_p, 0)

    #print(gr.numVertices(nuevo_grafo))
    #print(gr.numEdges(nuevo_grafo))
    conectados, tabular = req_8_3(nuevo_grafo, data_structs)
    return gr.numVertices(nuevo_grafo), gr.numEdges(nuevo_grafo), conectados, tabular

def req_8_3(data_structs, data_grande):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    kosaraju = scc.KosarajuSCC(data_structs)
    conectados = scc.connectedComponents(kosaraju)
    mapa_ids = kosaraju["idscc"]
    mapa_nuevo = mp.newMap(20, maptype="PROBING", loadfactor=0.5)
    for llaves in lt.iterator(mp.keySet(mapa_ids)):
        valores = me.getValue(mp.get(mapa_ids, llaves))
        agregar_id(mapa_nuevo, valores, llaves)
    lt_ordenar_mayor = lt.newList()
    for keys in lt.iterator(mp.keySet(mapa_nuevo)):
        lista = me.getValue(mp.get(mapa_nuevo, keys))
        lt.addLast(lt_ordenar_mayor, lt.size(lista)) 
    merg.sort(lt_ordenar_mayor, ordenar_mayor)
    top = lt.newList()
    a=1
    for tamano in lt.iterator(lt_ordenar_mayor):
        for llave in lt.iterator(mp.keySet(mapa_nuevo)):
            lista = me.getValue(mp.get(mapa_nuevo, llave))
            if lt.size(lista) == tamano:
                anadir = {"IDSCC":llave, "NODE_IDS":lista}
                lt.addLast(top, anadir)
                break
        a+=1
    lt_fin = lt.newList()
    if lt.size(top) >6:
        primeros = lt.subList(top,1,3)
        ultimos = lt.subList(top,lt.size(top)-2,3)
        for a in lt.iterator(primeros):
            lt.addLast(lt_fin, a)
        for e in lt.iterator(ultimos):
            lt.addLast(lt_fin, e)
    else:
        lt_fin = top
    tabular = tabla_req3(data_grande, lt_fin)
    return conectados, tabular

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
    if data_1 > data_2:
        return 1
    else:
        return 0

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

def cmp_lobos_by_antiguo_reciente(lobo1, lobo2):
    if (lobo1["timestamp"]) < (lobo2["timestamp"]):
        return True
    else:
        return False
    
def compareFecha(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass

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

