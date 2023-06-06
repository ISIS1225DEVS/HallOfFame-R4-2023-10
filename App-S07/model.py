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


import datetime
import config as cf
import math 
import sys
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as m
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
default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""


"""Estructura de datos"""

def newdatastructs():
    
    datastructs = {"puntos_muestreo": None,
        "componentes_1": None,    
        "componentes_2": None,               
        "caminos": None,
        "search": None,
        "search_1": None,
        "arbol": None}
    
    datastructs["lobos_puntos_e"] = m.newMap(numelements=40,
                                     maptype="CHAINING",
                                     cmpfunction=None)
    
    datastructs["lobos_puntos_s"] = m.newMap(numelements=47,
                                     maptype="CHAINING",
                                     cmpfunction=None)

    datastructs["lobos_valor"] = m.newMap(numelements=47,
                                     maptype="CHAINING",
                                     cmpfunction=None)

    datastructs["conexiones"] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=2392,
                                              cmpfunction=None)
    
    datastructs["conexiones_1"] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=2392,
                                              cmpfunction=None)
    datastructs["conexiones_2"] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=2392,
                                              cmpfunction=None)
    
    return datastructs

"""Carga de datos"""

def anadir_data(datastructs, lobo):
    
    lobo_id = lobo["animal-id"]+"_"+lobo["tag-id"]
    
    entrada = m.get(datastructs["lobos_valor"], lobo_id)
    
    if (entrada is None):
        m.put(datastructs["lobos_valor"], lobo_id, lobo)

         
    return datastructs

def anadir_data1(datastructs, punto_m):
    
    lobo_id = punto_m["individual-local-identifier"]+"_"+punto_m["tag-local-identifier"]
    punto_m["identificador_s"] = formato_punto_muestreo(punto_m, "seguimiento")
    formato_hora(punto_m)
    
    entrada =  m.get(datastructs["lobos_puntos_s"], lobo_id)
    
    if (entrada is None):
        entrada_lobo = nueva_entrada()
        lt.addLast(entrada_lobo["lista_puntos_s"], punto_m)
        m.put(datastructs["lobos_puntos_s"], lobo_id, entrada_lobo)
    else: 
        entrada_lobo = me.getValue(entrada)
        entrada_lobo["tamaño"] +=1
        lt.addLast(entrada_lobo["lista_puntos_s"], punto_m)
        
    return datastructs

def anadir_data2(datastructs, punto_m):
    
    punto_m["identificador_s"] = formato_punto_muestreo(punto_m, "seguimiento")
    punto_m["identificador_e"] = formato_punto_muestreo(punto_m, "encuentro")

    entrada =  m.get(datastructs["lobos_puntos_e"], punto_m["identificador_e"])
    
    if (entrada is None):
        entrada_punto_e = nueva_entrada1()
        lt.addLast(entrada_punto_e["lista_puntos_e"], punto_m )
        m.put(datastructs["lobos_puntos_e"], punto_m["identificador_e"], entrada_punto_e)
    else: 
        entrada_punto_e = me.getValue(entrada)
        entrada_punto_e["tamaño"] +=1
        lt.addLast(entrada_punto_e["lista_puntos_e"], punto_m)
        
    return datastructs

def anadir_grafo(datastructs):
    
    puntos_e = m.keySet(datastructs["lobos_puntos_e"])
    
    
    for punto_e in lt.iterator(puntos_e):
        entrada = me.getValue(m.get(datastructs["lobos_puntos_e"], punto_e))
        if entrada["tamaño"] >= 2:
            gr.insertVertex(datastructs["conexiones"], punto_e)
            for punto_s in lt.iterator(entrada["lista_puntos_e"]):
                gr.insertVertex(datastructs["conexiones"], punto_s["identificador_s"])
                gr.addEdge(datastructs["conexiones"], punto_e, punto_s["identificador_s"])
                gr.addEdge(datastructs["conexiones"], punto_s["identificador_s"], punto_e)
        elif entrada["tamaño"] < 2:
            punto_s = lt.firstElement(entrada["lista_puntos_e"])
            gr.insertVertex(datastructs["conexiones"], punto_s["identificador_s"])

    lobos = m.keySet(datastructs["lobos_puntos_s"])

    for lobo in lt.iterator(lobos):
        entrada = me.getValue(m.get(datastructs["lobos_puntos_s"], lobo))
        if entrada["tamaño"] >= 2:
            i = 1
            while i < lt.size(entrada["lista_puntos_s"]):
                elemento = lt.getElement(entrada["lista_puntos_s"], i)
                elemento_1 = lt.getElement(entrada["lista_puntos_s"], i+1)
                gr.addEdge(datastructs["conexiones"], elemento["identificador_s"], elemento_1["identificador_s"], distancia(elemento, elemento_1))
                i +=1
            
    return datastructs

def anadir_grafo_1(datastructs):
    
    puntos_e = m.keySet(datastructs["lobos_puntos_e"])
    
    for punto_e in lt.iterator(puntos_e):
        entrada = me.getValue(m.get(datastructs["lobos_puntos_e"], punto_e))
        if entrada["tamaño"] >= 2:
            gr.insertVertex(datastructs["conexiones_1"], punto_e)
            for punto_s in lt.iterator(entrada["lista_puntos_e"]):
                gr.insertVertex(datastructs["conexiones_1"], punto_s["identificador_s"])
                gr.addEdge(datastructs["conexiones_1"], punto_e, punto_s["identificador_s"])
                gr.addEdge(datastructs["conexiones_1"], punto_s["identificador_s"], punto_e)
        elif entrada["tamaño"] < 2:
            punto_s = lt.firstElement(entrada["lista_puntos_e"])
            gr.insertVertex(datastructs["conexiones_1"], punto_s["identificador_s"])
            

    lobos = m.keySet(datastructs["lobos_puntos_s"])

    for lobo in lt.iterator(lobos):
        entrada = me.getValue(m.get(datastructs["lobos_puntos_s"], lobo))
        if entrada["tamaño"] >= 2:
            i = 1
            while i < lt.size(entrada["lista_puntos_s"]):
                elemento = lt.getElement(entrada["lista_puntos_s"], i)
                elemento_1 = lt.getElement(entrada["lista_puntos_s"], i+1)
                gr.addEdge(datastructs["conexiones_1"], elemento["identificador_s"], elemento_1["identificador_s"], distancia(elemento, elemento_1))
                i +=1
            
    return datastructs

def nueva_entrada():
    
    entrada = {"lista_puntos_s": None, "tamaño": None}
    entrada["lista_puntos_s"] = lt.newList("ARRAY_LIST", cmpfunction=cmp_orden)
    entrada["tamaño"] = 1
    
    return entrada

def nueva_entrada1():
    
    entrada = {"lista_puntos_e": None, "tamaño": None}
    entrada["lista_puntos_e"] = lt.newList("ARRAY_LIST", cmpfunction=cmp_orden)
    entrada["tamaño"] = 1
    
    return entrada

"""Formato y arreglos"""

def componentes_conectadas(datastructs, numero):
   
    datastructs["componentes"+"_"+numero] = scc.KosarajuSCC(datastructs["conexiones"])
    
    return datastructs

def costos_minimos_caminos(datastructs, punto_muestra_inicial):

    datastructs["caminos"] = djk.Dijkstra(datastructs["conexiones"], punto_muestra_inicial)

    return datastructs

def distancia (punto_1, punto_2):
    
    latitud2 = radianes(round(float(punto_2["location-lat"]),3))
    longitud2 = radianes(round(float(punto_2["location-long"]), 3))
    latitud1 = radianes(round(float(punto_1["location-lat"]), 3))
    longitud1 = radianes(round(float(punto_1["location-long"]),3))
    dlon = longitud2-longitud1
    dlat = latitud2 - latitud1
    a = (math.sin(dlat/2))**2+math.cos(latitud1)*math.cos(latitud2)*(math.sin(dlon/2))**2
    c = 2 * math.asin(math.sqrt(a))
    distancia = 6371 * c
    
    return distancia

def radianes(grados):
    
    radianes = grados * (math.pi/180)
    
    return radianes

def formato_hora(punto_m):
    
    hora = punto_m["timestamp"]
    punto_m["timestamp"] = datetime.datetime.strptime(hora, "%Y-%m-%d %H:%M")
    
    return None

def mst(datastructs, origen):
    
    datastructs["arbol"] = prim.PrimMST(datastructs["conexiones_1"], origen)
    
    return datastructs

def formato_punto_muestreo(punto_muestreo, clase):
 
    if clase == "seguimiento":
        longitud = str(round(float(punto_muestreo["location-long"]), 3)).replace("-","m")
        longitud= longitud.replace(".", "p")
        latitud = str(round(float(punto_muestreo["location-lat"]),3)).replace(".", "p")
        individual = punto_muestreo["individual-local-identifier"]+"_"+punto_muestreo["tag-local-identifier"]
        identificador = longitud+"_"+latitud+"_"+individual
    elif clase == "encuentro":
        longitud = str(round(float(punto_muestreo["location-long"]), 3)).replace("-","m")
        longitud= longitud.replace(".", "p")
        latitud = str(round(float(punto_muestreo["location-lat"]),3)).replace(".", "p")
        identificador = longitud+"_"+latitud    

    return identificador

def cmp_orden(punto_m, ultimo_m):
    
    hora_ult = ultimo_m["timestamp"]
    hora_pres = punto_m["timestamp"]
  
    if hora_pres<hora_ult:
        return True
    else:
        return False
    
def cmp_tamaño(elemento, elemento_1):

    tamano = elemento[0]
    tamano_1= elemento_1[1]
    
    if tamano>tamano_1:
        return True
    else:
        return False
    
    

"""Requerimientos """


def req_1(datastructs, origen, destino):
    
    """Núcleo"""

    datastructs["search"] = dfs.DepthFirstSearch(datastructs["conexiones"], origen)
    camino = dfs.hasPathTo(datastructs["search"], destino)
    if camino == True:
        camino = dfs.pathTo(datastructs["search"],destino)
           
    """Vista"""      
    
    
      
    return camino


def req_2(datastructs, origen, destino):
    
    """Núcleo"""
    
    datastructs["search_1"] = bfs.BreadhtFisrtSearch(datastructs["conexiones"], origen)
    camino = bfs.hasPathTo(datastructs["search_1"], destino)
    if camino == True:
        camino = bfs.pathTo(datastructs["search_1"],destino)

    """Vista"""

    total_puntos_e = 0
    distancia_total = 0
    total_puntos_s = 0
    camino_lst = lt.newList("ARRAY_LIST")
    while st.isEmpty(camino) is False: 
        punto_m = st.pop(camino)
        lt.addLast(camino_lst, punto_m)
    
    prim_last_5 = []
    for i in lt.iterator(camino_lst):
        prim_last_5.append(i)
    j=0
    top=[]
    while j<6:
        top.append(prim_last_5[j])
        j+=1
    k=-5
    while k!=0:
        top.append(prim_last_5[len(prim_last_5)+k])
        k+=1
    total_camino= lt.size(camino_lst)
      
    
    return camino_lst, top, total_camino


def req_3(datastructs, numero):
    
    componentes_conectadas(datastructs, numero)
    cantidad_componentes = scc.connectedComponents(datastructs["componentes"])
    
    mapa_i= datastructs["componentes"]["idscc"]
    puntos_m = m.keySet(mapa_i)
    
    mapa_idscc = m.newMap(numelements=356,
                                     maptype="CHAINING",
                                     cmpfunction=None)

    for punto_m in lt.iterator(puntos_m):
        idscc = me.getValue(m.get(mapa_i, punto_m))
        entrada = m.get(mapa_idscc, idscc)
        if (entrada is None):
            lista_idscc= lt.newList("ARRAY_LIST")
            lt.addLast(lista_idscc,punto_m)
            m.put(mapa_idscc, idscc, lista_idscc)
        else:
            lista_idscc = me.getValue(entrada)
            lt.addLast(lista_idscc, punto_m)
            

    return mapa_idscc, cantidad_componentes


def req_4(datastructs, origen, destino):
    
    costos_minimos_caminos(datastructs, origen)
    camino = djk.hasPathTo(datastructs["caminos"], destino)
    if camino == True:
        camino = djk.pathTo(datastructs["caminos"],destino)
        costo = djk.distTo(datastructs["caminos"], destino)
    
    return camino, costo


def req_5(datastructs, origen, distancia, num_min):

    datastructs["arbol"] = prim.PrimMST(datastructs["conexiones_1"], origen)
    dict={}
    best=""
    dato_mejor= distancia
    
    arbol_fechas_keys = om.keySet(datastructs["arbol"]["edgeTo"])
    for dia in lt.iterator(arbol_fechas_keys):
        llave_valor_entrada = om.get(datastructs["arbol"]["edgeTo"], dia)
        if (llave_valor_entrada["key"]) == origen:
            for i in llave_valor_entrada["value"]:
                com=origen
                peso=0
                com= origen+" "+str(i)
                peso+= float(om.get(datastructs["arbol"]["distTo"], dia))
                if peso<distancia:
                    dict["com"]=peso
                    req_5(datastructs,i,distancia, num_min )
            contador=0
            mejor=[]
            for h in dict.keys:
                d= h.split(" ")
                for encuentros in d:
                     
                    if m.contains(datastructs["lobos_puntos_e"], encuentros)==True:
                        contador+=1
                if contador == num_min:
                    mejor.append(h)
            datos=[]
            for g in dict.values:
                datos.append(g)
            datos.sort()
            dato_mejor= datos[len(datos)-1]

            for k in mejor:
                if dict[k]==dato_mejor:
                    best= k
    return best, dato_mejor

def req_6(datastructs, fecha_inicial, fecha_final, sexo):
    
    mapa_lobo = datastructs["lobos_valor"]
    mapa_punto_s = datastructs["lobos_puntos_s"]
    mapa_lobo_sexo = m.newMap(numelements=47,
                                     maptype="CHAINING",
                                     cmpfunction=None)
    lobos = m.keySet(mapa_lobo)
    
    for lobo in lt.iterator(lobos):
        entrada = me.getValue(m.get(mapa_lobo, lobo))
        if entrada["animal-sex"] == sexo:
            entrada_1 = me.getValue(m.get(mapa_punto_s, lobo))
            entrada_1 = entrada_1["lista_puntos_s"]
            for punto_s in lt.iterator(entrada_1):
                if punto_s["timestamp"] == fecha_inicial:
                    origen = punto_s["identificador_s"]
                elif punto_s["timestamp"] == fecha_final:
                    destino = punto_s["identificador_s"]
        ejes = lt.newList("ARRAY_LIST")
        lt.addFirst(ejes, origen)
        lt.addLast(ejes, destino)
        m.put(mapa_lobo_sexo, lobo, ejes)

    for lobo in lt.iterator(lobos):
        entrada = me.getValue(m.get(mapa_lobo_sexo, lobo))
        origen = lt.firstElement(entrada)
        destino = lt.lastElement(entrada)
        datastructs["search_1"] = bfs.BreadhtFisrtSearch(datastructs["conexiones"], origen)
        camino = bfs.hasPathTo(datastructs["search_1"], destino)
        if camino == True:
            camino = bfs.pathTo(datastructs["search_1"],destino)
        camino_lst = lt.newList("ARRAY_LIST")
        while st.isEmpty(camino) is False: 
            punto_m = st.pop(camino)
            lt.addLast(camino_lst, punto_m)
        m.put(mapa_lobo_sexo, lobo, camino_lst)
    
    
    for lobo in lt.iterator(lobos):
        entrada = me.getValue(m.get(mapa_lobo_sexo, lobo))
        lista_conteo = lt.newList("ARRAY_LIST")
        lt.addFirst(lista_conteo, lt.size(entrada))
        i = 1
        distancia_total = 0
        while i < lt.size(entrada):
            punto_mpa = lt.getElement(entrada, i)
            punto_mpr = lt.getElement(entrada, i+1)
            distancia_total += gr.getEdge(punto_mpa, punto_mpr)
        lt.addLast(lista_conteo, distancia_total)
        m.put(mapa_lobo_sexo, lobo, lista_conteo) 
        
    mayor_distancia = 0
    ind_mayor_distancia = ""
    ruta_larga = 0
    ind_ruta_larga = ""
    menor_distancia = 0
    ind_menor_distancia = ""
    ruta_corta = 0
    ind_ruta_corta = ""
    
    for lobo in lt.iterator(lobos):
        entrada = me.getValue(m.get(mapa_lobo_sexo, lobo))
        if lt.firstElement(entrada) > ruta_larga:
            ruta_larga = lt.firstElement(entrada)
            ind_ruta_larga = lobo
        if lt.firstElement(entrada) < ruta_corta:
            ruta_corta = lt.firstElement(entrada)
            ind_ruta_corta = lobo
        if lt.lastElement(entrada) > mayor_distancia:
            mayor_distancia = lt.lastElement(entrada)
            ind_mayor_distancia = lobo
        if lt.lastElement(entrada) < menor_distancia:
            ind_menor_distancia = lobo
            
    
    
    return ind_ruta_larga, ind_mayor_distancia, ind_ruta_corta, ind_menor_distancia


def req_7(datastructs, fecha_inicial, fecha_final, tem_min, tem_max):
    
    
    puntos_e = m.keySet(datastructs["lobos_puntos_e"])
    
    for punto_e in lt.iterator(puntos_e):
        entrada = me.getValue(m.get(datastructs["lobos_puntos_e"], punto_e))
        if entrada["tamaño"] >= 2:
            gr.insertVertex(datastructs["conexiones_1"], punto_e)
            for punto_s in lt.iterator(entrada["lista_puntos_e"]):
                if (punto_s["timestamp"]>= fecha_inicial) and (punto_s["timestamp"]<= fecha_final) and (tem_min <= punto_s["external-temperature"]) and (tem_max >= punto_s["external-temperature"]):
                    gr.insertVertex(datastructs["conexiones_1"], punto_s["identificador_s"])
                    gr.addEdge(datastructs["conexiones_1"], punto_e, punto_s["identificador_s"])
                    gr.addEdge(datastructs["conexiones_1"], punto_s["identificador_s"], punto_e)
        elif entrada["tamaño"] < 2:
            punto_s = lt.firstElement(entrada["lista_puntos_e"])
            if (punto_s["timestamp"]>= fecha_inicial) and (punto_s["timestamp"]<= fecha_final) and (tem_min <= punto_s["external-temperature"]) and (tem_max >= punto_s["external-temperature"]):
                gr.insertVertex(datastructs["conexiones_1"], punto_s["identificador_s"])
                
            
    lobos = m.keySet(datastructs["lobos_puntos_s"])

    for lobo in lt.iterator(lobos):
        entrada = me.getValue(m.get(datastructs["lobos_puntos_s"], lobo))
        if entrada["tamaño"] >= 2:
            i = 1
            while i < lt.size(entrada["lista_puntos_s"]):
                if (elemento["timestamp"]>= fecha_inicial) and (elemento["timestamp"]<= fecha_final) and (tem_min <= elemento["external-temperature"]) and (tem_max >= elemento["external-temperature"]):
                    elemento = lt.getElement(entrada["lista_puntos_s"], i)
                    x = True
                if (elemento_1["timestamp"]>= fecha_inicial) and (elemento_1["timestamp"]<= fecha_final) and (tem_min <= elemento_1["external-temperature"]) and (tem_max >= elemento_1["external-temperature"]):        
                    elemento_1 = lt.getElement(entrada["lista_puntos_s"], i+1)
                    y = True
                if (x == True) and (y == True):
                    gr.addEdge(datastructs["conexiones_1"], elemento["identificador_s"], elemento_1["identificador_s"], distancia(elemento, elemento_1))
                i +=1
    
    mapa_idscc, cantidad_componentes= req_3(datastructs, "2")
    
    manadas = m.keySet(mapa_idscc)
    
    lista_tamaño = lt.newList("ARRAY_LIST")
    
    for manada in lt.iterator(manadas):
        entrada = me.getValue(m.get(mapa_idscc, manada))
        tupla = lt.size(entrada), manada
        lt.addLast(lista_tamaño, tupla)

    merg.sort(lista_tamaño, cmp_tamaño)
    
    manada_1_max = lt.firstElement(lista_tamaño)
    manada_1_max = me.getValue(m.get(mapa_idscc, manada_1_min[1]))
    manada_2_max = lt.getElement(lista_tamaño, 2)
    manada_2_max = me.getValue(m.get(mapa_idscc, manada_2_min[1]))
    manada_3_max = lt.getElement(lista_tamaño, 3)
    manada_3_max = me.getValue(m.get(mapa_idscc, manada_3_min[1]))
    manada_1_min = lt.lastElement(lista_tamaño)
    manada_1_min = me.getValue(m.get(mapa_idscc, manada_1_min[1]))
    manada_2_min = lt.getElement(lista_tamaño, cantidad_componentes-1)
    manada_2_min = me.getValue(m.get(mapa_idscc, manada_2_min[1]))
    manada_3_min = lt.getElement(lista_tamaño, cantidad_componentes-2)
    manada_3_min = me.getValue(m.get(mapa_idscc, manada_3_min[1]))
    
    vertices = gr.vertices()
    origen = lt.firstElement(vertices)
    destino = lt.lastElement(vertices)
    
    datastructs["search"] = dfs.DepthFirstSearch(datastructs["conexiones"], origen)
    camino = dfs.hasPathTo(datastructs["search"], destino)
    if camino == True:
        camino = dfs.pathTo(datastructs["search"],destino)
        
    camino_lst = lt.newList("ARRAY_LIST")
    while st.isEmpty(camino) is False: 
        punto_m = st.pop(camino)
        lt.addLast(camino_lst, punto_m)
        

        
    return cantidad_componentes, manada_1_max, manada_2_max, manada_3_max, manada_1_min, manada_2_min, manada_3_min, camino_lst