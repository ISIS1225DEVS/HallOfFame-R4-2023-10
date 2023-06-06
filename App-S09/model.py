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
from DISClib.DataStructures import edge as e
from datetime import datetime as dt
import numpy as np
import folium
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
    data_structs={"movimientos":None, "mtp":None, "ps":None, "lobos":None, "filas": None}
    
    data_structs["movimientos"]=gr.newGraph(datastructure='ADJ_LIST', directed=True, size=180000, cmpfunction=compareID)
    
    data_structs["mtp"]=mp.newMap(numelements=260001,maptype='PROBING')
    
    data_structs["ps"]=mp.newMap(numelements=97,maptype='PROBING')
    
    data_structs["lobos"]= mp.newMap(numelements= 97, maptype="PROBING")
    
    data_structs["filas"]=lt.newList(datastructure="ARRAY_LIST")
    
    return data_structs


# Funciones para agregar informacion al modelo


def add_track(data_structs, fila):
    """
    Función para agregar nuevos elementos a la lista
    """
    fila["location-long"]=str(round(float(fila["location-long"]),3))
    fila["location-lat"]=str(round(float(fila["location-lat"]),3))
    add_by_PS(data_structs, fila)
    addMTP_connection(data_structs, fila)
    ps=addPuntoSeguimiento(data_structs, fila)
    lt.addLast(data_structs["filas"], fila)
    
    return ps
    
def add_arcos(data_structs):
    mtps=addMTP(data_structs)
    arcos1=addRouteConnections_MTP(data_structs)
    arcos2=addRouteConnections_PS(data_structs)
    return mtps, arcos1, arcos2
# Funciones para creacion de datos

def addMTP(data_structs):
    llaves=mp.keySet(data_structs["mtp"])
    mtps=lt.newList(datastructure= "ARRAY_LIST")
    for llave in lt.iterator(llaves):
        entry=mp.get(data_structs["mtp"], llave)
        value=me.getValue(entry)
          
        if lt.size(value)>=2:
            lista_lobos= lobos_diferentes(value)
            if lista_lobos== True:  
                id=me.getKey(entry)
                lt.addLast(mtps, {"id": id, "info":value})
                if not gr.containsVertex(data_structs["movimientos"], id):
                    gr.insertVertex(data_structs["movimientos"], id)
            else:
                mp.remove(data_structs["mtp"], llave)
        else:
             mp.remove(data_structs["mtp"], llave)  
    return mtps

def lobos_diferentes(lista):
    
    lista_lobos= lt.newList(datastructure= "ARRAY_LIST")
    
    for lobo in lt.iterator(lista):
        id= lobo["fila"]["individual-local-identifier"]
        if lt.isPresent(lista_lobos, id) == 0:
            lt.addLast(lista_lobos, id)
            if lt.size(lista_lobos)>=2:
                return True
    return False
            
    

def addPuntoSeguimiento(data_structs,fila):
    id=crear_PuntoSeguimiento(fila)
    if not gr.containsVertex(data_structs["movimientos"], id):
        gr.insertVertex(data_structs["movimientos"], id)
        ps= {"id": id, "info":fila}
        
        return ps
    
    return None
        
        
def addLobo (data_structs, fila):
    llave_lobo= fila["animal-id"]+"_"+fila["tag-id"]
    mp.put(data_structs["lobos"], llave_lobo, fila)
    

def addMTP_connection(data_structs, fila):

    llave_MTP= crear_MTP(fila)
    llave_PS= crear_PuntoSeguimiento(fila)
    info={"ps":llave_PS, "fila":fila}
    entry = mp.get(data_structs["mtp"], llave_MTP)
    if entry is None:
        lstroutes = lt.newList(datastructure="ARRAY_LIST", cmpfunction=compareID5)
        lt.addLast(lstroutes, info)
        mp.put(data_structs["mtp"], llave_MTP, lstroutes)
    else:
        lstroutes = entry['value']
        if lt.isPresent(lstroutes, info)==0:
            lt.addLast(lstroutes, info)

        
                    
def add_by_PS(data_structs, fila):
    
    llave_ID= fila["individual-local-identifier"]+"_"+ fila["tag-local-identifier"]
    llave_PS= crear_PuntoSeguimiento(fila)
    info={"ps":llave_PS, "fila":fila}
    
    entry = mp.get(data_structs["ps"], llave_ID)
    
    if entry is None:
        newentry = om.newMap(omaptype="RBT", cmpfunction=cmp_by_hora)
        mp.put(data_structs["ps"], llave_ID, newentry)
    else:
        newentry = me.getValue(entry)
       
    llave2=fila["timestamp"]
    
    om.put(newentry, llave2, info)
    


def addConnection(data_structs, inicio, final, distancia):

    edge = gr.getEdge(data_structs["movimientos"], inicio, final)
    if edge is None:
        gr.addEdge(data_structs["movimientos"], inicio, final, distancia)
        

def addRouteConnections_MTP(data_structs):
    contador=0
    lststops = mp.keySet(data_structs["mtp"])
    for key in lt.iterator(lststops):
        lstroutes = mp.get(data_structs["mtp"],key)['value']
        for route in lt.iterator(lstroutes):
            if gr.containsVertex(data_structs["movimientos"], route["ps"]):
                    addConnection(data_structs, key , route["ps"], 0)
                    addConnection(data_structs, route["ps"] , key, 0)
                    contador+=2
    return contador
                    
                    

def addRouteConnections_PS(data_structs):
    contador=0

    lststops = mp.keySet(data_structs["ps"])
    for key in lt.iterator(lststops):
        arbol = mp.get(data_structs["ps"], key)['value']
        lstroutes=om.keySet(arbol)
        prevrout_fila = None
        prevrout_llave= None
        for route in lt.iterator(lstroutes):
            entry=om.get(arbol, route)
            valor=me.getValue(entry)

            route_llave=valor["ps"]
            route_fila= valor["fila"]
            if prevrout_llave is not None:
                distancia= calcular_distancia(prevrout_fila, route_fila)
                if distancia != 0:
                    
                    addConnection(data_structs, prevrout_llave, route_llave, distancia)
                    contador+=1
            prevrout_llave = route_llave
            prevrout_fila= route_fila
            
    return contador
        
        
def calcular_distancia(fila1, fila2):
    
    lat_1= float(fila1["location-lat"])
    lon_1= float(fila1["location-long"])
    
    lat_2= float(fila2["location-lat"])
    lon_2= float(fila2["location-long"])
    
    lat_1=lat_1*np.pi/180
    lon_1=lon_1*np.pi/180
    lat_2=lat_2*np.pi/180
    lon_2=lon_2*np.pi/180
    
    a=(np.sin((lat_2- lat_1)/2))**2
    
    b=(np.sin((lon_2-lon_1)/2))**2
    
    c=a+np.cos(lat_2)*np.cos(lat_1)*b
    
    d= 2* np.arcsin(np.sqrt(c))*6371
    
    return round(d,3)



#funciones auxiliares


def buscar_menor_columna(data_structs, columna):
    menor_fila=lt.getElement(data_structs["filas"],1)
    menor=float(menor_fila[columna])
    for fila in lt.iterator(data_structs["filas"]):
        if float(fila[columna])<menor:
            menor_fila=fila
            menor=float(fila[columna])
            
    return menor_fila


def buscar_mayor_columna(data_structs, columna):
    mayor_fila=lt.getElement(data_structs["filas"],1)
    mayor=float(mayor_fila[columna])
    for fila in lt.iterator(data_structs["filas"]):
        if float(fila[columna])>mayor:
            mayor_fila=fila
            mayor=float(fila[columna])
            
    return mayor_fila

def buscar_menor_long_lat_lista(lista):  

    menor_id=lt.getElement(lista,1)  
    menor_id_separado=separar_id(menor_id) 
    long_ref= (menor_id_separado)[0] 
    lat_ref= (menor_id_separado)[1] 
    menor_long_ref= devolver_formato(long_ref) 
    menor_lat_ref= devolver_formato(lat_ref)    

    menor_long=float(menor_long_ref) 

    menor_info=lt.newList(datastructure="ARRAY_LIST") 
     
    for id in lt.iterator(lista): 
        long_id=separar_id(id)[0] 
        long= devolver_formato(long_id) 
        if float(long)<menor_long:  
            menor_long=float(long) 
            menor_id=id 

             
    lt.addLast(menor_info, menor_long) 

     

    menor_lat=float(menor_lat_ref)   
    for id in lt.iterator(lista): 
        lat_id=separar_id(id)[1] 
        lat = devolver_formato(lat_id) 
        if float(lat)<menor_lat:  
            menor_lat=float(lat) 
            menor_id=id 
        

    lt.addLast(menor_info, menor_lat)             

    return menor_info  

def buscar_mayor_long_lat_lista(lista):  

    mayor_id=lt.getElement(lista,1)  
    mayor_id_separado=separar_id(mayor_id) 
    long_ref= (mayor_id_separado)[0] 
    lat_ref= (mayor_id_separado)[1] 
    mayor_long_ref= devolver_formato(long_ref) 
    mayor_lat_ref= devolver_formato(lat_ref) 

    mayor_long=float(mayor_long_ref) 

    mayor_info=lt.newList(datastructure="ARRAY_LIST") 


    for id in lt.iterator(lista): 
        long_id=separar_id(id)[0] 
        long= devolver_formato(long_id) 
        if float(long)>mayor_long:  
            mayor_long=float(long) 
            mayor_id=id 
        

    lt.addLast(mayor_info, mayor_long) 

    mayor_lat=float(mayor_lat_ref)   

    for id in lt.iterator(lista): 
        lat_id=separar_id(id)[1] 
        lat = devolver_formato(lat_id) 
        if float(lat)>mayor_lat:  
            mayor_lat=float(lat) 
            mayor_id=id 

             
    lt.addLast(mayor_info, mayor_lat)             

    return mayor_info  


def dar_adyacencias(data_structs, vertice):
    adyacencias=gr.adjacents(data_structs["movimientos"], vertice)
    
    return adyacencias

def dar_lobos_en_adyacencias(data_structs, vertice):
    adyacencias=gr.adjacents(data_structs["movimientos"], vertice)
    identificadores=lt.newList(datastructure="ARRAY_LIST")
    
    if verificar_mtp_o_ps(vertice)=="ps":
        info_id=separar_id_completo(vertice)
        id_vertice=info_id[2]+"_"+info_id[3]
        lt.addLast(identificadores, id_vertice)
    
    for info in lt.iterator(adyacencias):
        if verificar_mtp_o_ps(info)=="ps":
            comp=info.split("_")
            id=[]
            for i in range(2, len(comp)):
                id.append(comp[i])
            id_str="_".join(id)
            if lt.isPresent(identificadores, id_str)==0:
                lt.addLast(identificadores, id_str) 
    
    return identificadores

def dar_lobos_en_adyacencias_lista(lista):
    identificadores=lt.newList(datastructure="ARRAY_LIST")
    
    for info in lt.iterator(lista):
        if verificar_mtp_o_ps(info)=="ps":
            comp=info.split("_")
            id=[]
            for i in range(2, len(comp)):
                id.append(comp[i])
            id_str="_".join(id)
            if lt.isPresent(identificadores,id_str)==0:
                lt.addLast(identificadores, id_str) 
    
    return identificadores


def verificar_mtp_o_ps(vertice):
    if vertice.count("_")==1:
        return "mtp"
    
    else:
        return "ps"
    
def cambiar_formato(dato):
    dato=str(round(float(dato),3))
    nuevo_dato=""
    for caracter in dato:
        if caracter == "-":
            caracter="m"
        if caracter == ".":
            caracter="p"
            
        nuevo_dato=nuevo_dato+caracter
            
    return nuevo_dato

def devolver_formato(dato):
    
    nuevo_dato=""
    for caracter in dato:
        if caracter == "m":
            caracter="-"
        if caracter == "p":
            caracter="."
            
        nuevo_dato=nuevo_dato+caracter
            
    return nuevo_dato

def separar_id(dato):
    
    componentes=[]
    inicio=0
    
    for i in range(0, len(dato)):
        if dato[i] == "_" or i == len(dato)-1:
            info=dato[inicio:i]
            inicio=i+1
            componentes.append(info)
            if len(componentes)==2:
                return componentes
            
    return componentes
            
 
def separar_id_completo(dato):
    
    componentes=[]
    inicio=0
    a=dato.count("_")
    if a==4:
        contador=0
        for i in range(0, len(dato)):
            if contador==2:
                if dato[i] == "_":
                        contador+=1
            else:
                if len(componentes)==3:
                    info=dato[inicio:]
                    componentes.append(info)
                else:
                    if dato[i] == "_":
                        contador+=1
                        info=dato[inicio:i]
                        inicio=i+1
                        componentes.append(info)


    else:
        for i in range(0, len(dato)):
            if len(componentes)==3:
                info=dato[inicio:]
                componentes.append(info)
            else:
                if dato[i] == "_":
                    info=dato[inicio:i]
                    inicio=i+1
                    componentes.append(info)
           
    return componentes 

def crear_MTP(fila):
    long=cambiar_formato(fila["location-long"])
    lat=cambiar_formato(fila["location-lat"])
    
    id=long+"_"+lat
    
    return id
  
    
def crear_PuntoSeguimiento(fila):
    long=cambiar_formato(fila["location-long"])
    lat=cambiar_formato(fila["location-lat"])
    
    id=long+"_"+lat+"_"+fila["individual-local-identifier"]+"_"+fila["tag-local-identifier"]
    
    return id
    
def verificar_tiempo (info1, info2):
    
    info1_fc= info1["timestamp"] 
    tiempo_info1= dt.strptime(info1_fc, "%Y-%m-%d %H:%M")
    info2_fc= info2["timestamp"]
    tiempo_info2= dt.strptime(info2_fc, "%Y-%m-%d %H:%M")
    
    
    if tiempo_info1 < tiempo_info2:
        return True
    else: 
        return False

def verificar_tiempo2 (info1, info2):
    
    info1_fc= info1["timestamp"] 
    tiempo_info1= dt.strptime(info1_fc, "%Y-%m-%d %H:%M")
    info2_fc= info2["timestamp"]
    tiempo_info2= dt.strptime(info2_fc, "%Y-%m-%d %H:%M")
    
    
    if tiempo_info1 <= tiempo_info2:
        return True
    else: 
        return False
      
def encontrar_mtp_mas_cercano(data_structs, vertice):
    
    mtps=mp.keySet(data_structs["mtp"])
    min_llave=lt.getElement(mtps,1)
    min_info=mp.get(data_structs["mtp"], min_llave)["value"]
    min_fila=lt.getElement(min_info, 1)
    min_dist=calcular_distancia(vertice, min_fila["fila"])
    
    for mtp in lt.iterator(mtps):
        info_ref=mp.get(data_structs["mtp"], mtp)["value"]
        fila_ref=lt.getElement(info_ref,1)
        dist=calcular_distancia(vertice, fila_ref["fila"])
        
        if dist < min_dist:
            min_llave=mtp
            min_info=info_ref
            min_fila=fila_ref
            min_dist=dist
            
    return min_llave, min_info, min_fila, min_dist

def encontrar_mayor_distancia (mapa):
    
    llaves = mp.keySet(mapa)
    llave_mayor= lt.getElement(llaves, 1)
    lobo_mayor = mp.get(mapa, llave_mayor)["value"]
    distancia_mayor = lobo_mayor["distancia"]
    
    for llave in lt.iterator(llaves):
        info = mp.get(mapa, llave)["value"]
        distancia = info["distancia"]
        
        if distancia > distancia_mayor:
            distancia_mayor = distancia
            lobo_mayor= info
            llave_mayor = llave
    
    return llave_mayor, round(distancia_mayor, 3)

def encontrar_menor_distancia (mapa):
    
    llaves = mp.keySet(mapa)
    llave_menor= lt.getElement(llaves, 1)
    lobo_menor = mp.get(mapa, llave_menor)["value"]
    distancia_menor = lobo_menor["distancia"]
    
    for llave in lt.iterator(llaves):
        info = mp.get(mapa, llave)["value"]
        distancia = info["distancia"]
        
        if distancia < distancia_menor:
            distancia_menor = distancia
            lobo_menor= info
            llave_menor = llave
    
    return llave_menor, round(distancia_menor, 3)

def dar_lat_long_nodo(nodo):
    info_nodo=separar_id(nodo)
    ubicacion=lt.newList(datastructure="ARRAY_LIST")
    lt.addLast(ubicacion, devolver_formato(info_nodo[0]))
    lt.addLast(ubicacion, devolver_formato(info_nodo[1]))
    return ubicacion
      
def dar_lobo_en_arco(arco):
    vertices=lt.newList(datastructure="ARRAY_LIST")
    lt.addLast(vertices, arco["vertexA"])
    lt.addLast(vertices, arco["vertexB"])
    lobo=dar_lobos_en_adyacencias_lista(vertices)
    
    return lt.getElement(lobo, 1)

def dar_distancia(grafo, vertice1, vertice2):
    arco=gr.getEdge(grafo, vertice1, vertice2)
    peso=e.weight(arco)
    return peso

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass

# creación grafos nuevos

def addConnection_newgraph(grafo, inicio, final, distancia):

    edge = gr.getEdge(grafo, inicio, final)
    if edge is None:
        gr.addEdge(grafo, inicio, final, distancia)     
    
def addRouteConnections_PS_newgraph(data_structs, grafo,  puntos_seguimiento):
    contador=0

    lststops = mp.keySet(data_structs["ps"])
    for key in lt.iterator(lststops):
        arbol = mp.get(data_structs["ps"], key)['value']
        lstroutes=om.keySet(arbol)
        prevrout_fila = None
        prevrout_llave= None
        for route in lt.iterator(lstroutes):
            entry=om.get(arbol, route)
            valor=me.getValue(entry)

            if lt.isPresent(puntos_seguimiento, valor["ps"]) !=0:
                
                route_llave=valor["ps"]
                route_fila= valor["fila"]
                if prevrout_llave is not None:
                    distancia= calcular_distancia(prevrout_fila, route_fila)
                    if distancia != 0:
                        
                        addConnection_newgraph(grafo, prevrout_llave, route_llave, distancia)
                        contador+=1
                prevrout_llave = route_llave
                prevrout_fila= route_fila       
    return contador  

def lobos_diferentes_newgraph(lista, puntos_seguimiento):
    
    lista_lobos= lt.newList(datastructure= "ARRAY_LIST")
    lista_ps = lt.newList(datastructure= "ARRAY_LIST")
    
    
    for lobo in lt.iterator(lista):
        ps= lobo["ps"]
        info_id= separar_id_completo(ps)
        id = info_id[2]+ "_"+ info_id[3]
        if lt.isPresent(lista_lobos, id) == 0 and lt.isPresent(puntos_seguimiento, ps)!=0:
            lt.addLast(lista_ps, ps)
            lt.addLast(lista_lobos, id)
    
    if lt.size(lista_lobos)>= 2:
        return lista_ps
    else:
        return False
            

def addRouteConnections_MTP_newgraph(grafo, mtps):
    contador=0
    for mtp in lt.iterator(mtps):
        for ps in lt.iterator(mtp["pss"]):
            if gr.containsVertex(grafo, mtp["mtp"]):
                    addConnection_newgraph(grafo, mtp["mtp"] , ps, 0)
                    addConnection_newgraph(grafo, ps , mtp["mtp"], 0)
                    contador+=2
    return contador 

def dar_lobo_en_vertice(vertice):
    vertices=lt.newList(datastructure="ARRAY_LIST")
    lt.addLast(vertices, vertice)
    lobo=dar_lobos_en_adyacencias_lista(vertices)
    
    return lt.getElement(lobo, 1)

def darTresPrimeros_Ultimos(lista):
    
    primeros = lt.newList("ARRAY_LIST")
    ultimos = lt.newList("ARRAY_LIST")
    completo = lt.newList("ARRAY_LIST")
    vertice_primero = None
    vertice_ultimo = None
    
    for vertice in lt.iterator(lista):
        if verificar_mtp_o_ps(vertice) == "mtp" and lt.size(primeros)== 0:
            lt.addLast(primeros, vertice)
            vertice_primero = vertice
        if  verificar_mtp_o_ps(vertice) == "mtp" and lt.size(ultimos)== 0 and lt.size(primeros) == 1: 
            lt.addLast(ultimos, vertice)
            vertice_ultimo = vertice
    
    if vertice_primero == None:
        vertice_primero = lt.getElement(lista, 1)
    if vertice_ultimo == None:
        vertice_ultimo = lt.getElement(lista, lt.size(lista)) 
           
    lobo_primero = dar_lat_long_nodo(vertice_primero)
    lobo_ultimo = dar_lat_long_nodo(vertice_ultimo)

    for vertice in lt.iterator(lista):
        if dar_lat_long_nodo(vertice) == lobo_primero and lt.size(primeros)<3:
            lt.addLast(primeros, vertice)
        if dar_lat_long_nodo(vertice) == lobo_ultimo and lt.size(ultimos)<3:
            lt.addLast(ultimos, vertice)
  
    if lt.size(primeros)<3: 
        for vertice in lt.iterator(lista): 
            if lt.isPresent(primeros, vertice) == 0 and lt.isPresent(ultimos, vertice) and lt.size(primeros)<3:
                lt.addLast(primeros, vertice)

    if lt.size(ultimos)<3: 
        for vertice in lt.iterator(lista): 
            if lt.isPresent(primeros, vertice) == 0 and lt.isPresent(ultimos, vertice) and lt.size(ultimos)<3:
                lt.addLast(ultimos, vertice)
      
      
    for vertice in lt.iterator(primeros):
        lt.addLast(completo, vertice)
    
    for vertice in lt.iterator(ultimos):
        lt.addLast(completo, vertice)
           
    
    return completo         
       

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


def req_1(data_structs, origen, destino):
    """
    Función que soluciona el requerimiento 1
    """ 
    if gr.containsVertex(data_structs["movimientos"], origen) and gr.containsVertex(data_structs["movimientos"], destino):
        search=dfs.DepthFirstSearch(data_structs["movimientos"], origen)
        
        a=dfs.hasPathTo(search, destino)
        
        if a is True:
            camino=dfs.pathTo(search, destino)
            
            mtps=0
            pss=0
            distancia=0
            for i in range(1, lt.size(camino)+1):
                vertice=lt.getElement(camino, i)
                if verificar_mtp_o_ps(vertice)=="mtp":
                    mtps+=1
                else:
                    pss+=1
                
                if i<=lt.size(camino)-1:
                    vertice2=lt.getElement(camino, i+1)
                    
                    arco=gr.getEdge(data_structs["movimientos"], vertice2, vertice)
                    distancia+=e.weight(arco)
                    
            info_filas=lt.newList(datastructure="SINGLE_LINKED")
            
            for i in range(1, 6):
                lista=lt.newList(datastructure="ARRAY_LIST")
                llave=lt.getElement(camino, i)
                lt.addLast(lista, llave)
                f=devolver_formato(llave)
                ubicacion=separar_id(f)
                lt.addLast(lista,ubicacion) 
                ids=dar_lobos_en_adyacencias(data_structs, llave)
                lt.addLast(lista,lt.size(ids))
                adyacencias=gr.adjacents(data_structs["movimientos"], llave)
                    
                lt.addFirst(info_filas, lista)
            
            for i in range(lt.size(camino)-5, lt.size(camino)+1):
                lista=lt.newList(datastructure="ARRAY_LIST")
                llave=lt.getElement(camino, i)
                lt.addLast(lista, llave)
                f=devolver_formato(llave)
                ubicacion=separar_id(f)
                lt.addLast(lista,ubicacion) 
                ids=dar_lobos_en_adyacencias(data_structs, llave)
                lt.addLast(lista,lt.size(ids))
                adyacencias=gr.adjacents(data_structs["movimientos"], llave)
                
                lt.addFirst(info_filas, lista)      
                       
            
            mapa=crear_mapa_folium()
        
            trail=[]
            
        
            for nodo in lt.iterator(camino):
                crear_marcador(mapa, nodo)
                crear_ruta(trail, nodo)

            agregar_ruta(mapa, trail)
        
            
            
            
            return distancia, mtps, pss, info_filas, mapa
        else:
            return None
    


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3

    search = scc.KosarajuSCC(data_structs["movimientos"]) 

    cantidad = scc.connectedComponents(search)

    keyset_ref = mp.keySet(data_structs["mtp"])  
    llave_ref= lt.getElement(keyset_ref, 1)  
    cfc= scc.sccCount(data_structs["movimientos"], search, llave_ref)   

    mapa_cfc = mp.newMap(numelements= cantidad//4 , maptype= "CHAINING", loadfactor= 4 )  
    vertices = mp.keySet(cfc["idscc"])   

     
    #reversar 
    for vertice in lt.iterator(vertices):  
        value = mp.get(cfc["idscc"], vertice)  
        id=value["value"]  
        entry = mp.get(mapa_cfc, id)  
        if entry == None:  
            lista = lt.newList(datastructure="ARRAY_LIST")  
            mp.put(mapa_cfc, id, lista)  
        else:  
            lista= mp.get(mapa_cfc, id )["value"]  
        lt.addLast(lista, vertice)  


    #encontrar 5 mayores  
    keyset_cfc= mp.keySet(mapa_cfc)   
    mayor_cfc= mp.newMap(numelements= 11, maptype="PROBING" )  
    lista_mayores = lt.newList("ARRAY_LIST")

    while mp.size(mayor_cfc) < 5:   
        mayor=0  
        for llave in lt.iterator(keyset_cfc):  
            value= mp.get(mapa_cfc, llave)["value"]  
            tamanio= lt.size(value) 
            if tamanio> mayor and mp.contains(mayor_cfc, llave) == False:  
                mayor= tamanio  
                mayor_values = value  
                llave_mayor = llave  
        mp.put(mayor_cfc, llave_mayor, mayor_values)  
        lt.addLast(lista_mayores, llave_mayor)
    

    keyset_mayor_cfc = mp.keySet(mayor_cfc) 
    mapa = mp.newMap(numelements= 11, maptype="PROBING", loadfactor=0.5) 
     

    for llave in lt.iterator(keyset_mayor_cfc):  

        diccionario = {} 
        mp.put(mapa, llave, diccionario) 

    
    
    #encontrar 3 primeros y 3 ultimos  

    for llave in lt.iterator(keyset_mayor_cfc): 
        primeros_ultimos = lt.newList("ARRAY_LIST") 
        value= mp.get(mayor_cfc, llave)["value"]
        if lt.size(value)<=6: 
            for dato in lt.iterator(value):
                lt.addLast(primeros_ultimos, dato)  
      

        else: 
            for i in range (1,4): 
                fila= lt.getElement(value, i) 
                lt.addLast(primeros_ultimos,  fila) 
            for i in range (lt.size(value)-2, lt.size(value)+1): 
                fila= lt.getElement(value, i) 
                lt.addLast(primeros_ultimos,  fila) 

         
        dicc=mp.get(mapa, llave)["value"] 
        dicc["primeros_ultimos"]= primeros_ultimos
     
    #tamaño
    
    for llave in lt.iterator(keyset_mayor_cfc):
        dicc = mp.get(mapa, llave)["value"] 
        value= mp.get(mayor_cfc, llave)["value"]
        dicc["tamaño"]= lt.size(value)
        
    #encontrar lat y long  

    for llave in lt.iterator(keyset_mayor_cfc):  

        value= mp.get(mayor_cfc, llave)["value"]  
        mayor = buscar_mayor_long_lat_lista(value)  
        menor = buscar_menor_long_lat_lista (value)  
        lat_max  = lt.getElement(mayor, 2)  
        long_max = lt.getElement(mayor, 1)  
        lat_min = lt.getElement(menor, 2)  
        long_min = lt.getElement(menor, 1)  

        dicc = mp.get(mapa, llave)["value"] 
        dicc["min_lat"] = lat_min 
        dicc["max_lat"] = lat_max 
        dicc["min_lon"] = long_min 
        dicc["max_lon"] = long_max      
 
    #encontrar lobos 

    for llave in lt.iterator(keyset_mayor_cfc): 
        
        lista_lobos = lt.newList(datastructure= "ARRAY_LIST") 
        value= mp.get(mayor_cfc, llave)["value"] 
        lobos = dar_lobos_en_adyacencias_lista(value) 
        cantidad_lobos = lt.size(lobos) 

        
        if cantidad_lobos <=6: 
            for lobo in lt.iterator(lobos): 
                fila= mp.get(data_structs["lobos"], lobo)["value"] 
                lt.addLast(lista_lobos,fila ) 

        else: 
            for i in range (1,4): 
                lobo= lt.getElement(lobos, i) 
                fila= mp.get(data_structs["lobos"], lobo)["value"] 
                lt.addLast(lista_lobos, fila ) 

            for i in range (lt.size(lobos)-2, lt.size(lobos)+1): 
                lobo= lt.getElement(lobos, i) 
                fila= mp.get(data_structs["lobos"], lobo)["value"] 
                lt.addLast(lista_lobos, fila ) 

 
        dicc=mp.get(mapa, llave)["value"] 
        dicc["cantidad_lobos"] = cantidad_lobos 
        dicc["informacion_lobos"]= lista_lobos 
        
    mapa_folium = crear_mapa_folium()
    lista_color = ["red", "purple", "pink", "darkgreen", 'cadetblue']
    contador = 0 
    for llave in lt.iterator(keyset_mayor_cfc):
        puntos = mp.get(mayor_cfc, llave)["value"]
        entry= mp.get(mapa, llave)["value"]
        
        crear_circulo(mapa_folium, entry["min_lon"], entry["max_lon"], entry["min_lat"], entry["max_lat"], llave, lista_color[contador] )
        contador+= 1
        for punto in lt.iterator(puntos):
            crear_marcador(mapa_folium, punto)
     
        
    return cantidad, mapa, lista_mayores, mapa_folium


def req_4(data_structs, origen, destino):
    """
    Función que soluciona el requerimiento 4
    """
    #info_origen
    mtp_origen=encontrar_mtp_mas_cercano(data_structs, origen)
    mtp_llave_origen=mtp_origen[0]
    mtp_dist_origen=mtp_origen[3]
    
    ubicacion_origen=separar_id(mtp_llave_origen)
    lobos_origen=dar_lobos_en_adyacencias(data_structs, mtp_llave_origen)
    info_origen={"id":mtp_llave_origen, "longitud": devolver_formato(ubicacion_origen[0]), "latitud": devolver_formato(ubicacion_origen[1]), "distancia":mtp_dist_origen, "lobos":lobos_origen}
    
    #info_destino
    mtp_destino=encontrar_mtp_mas_cercano(data_structs, destino)
    mtp_llave_destino=mtp_destino[0]
    mtp_dist_destino=mtp_destino[3]
    
    ubicacion_destino=separar_id(mtp_llave_destino)
    lobos_destino=dar_lobos_en_adyacencias(data_structs, mtp_llave_destino)
    info_destino={"id":mtp_llave_destino, "longitud": devolver_formato(ubicacion_destino[0]), "latitud": devolver_formato(ubicacion_destino[1]), "distancia":mtp_dist_destino, "lobos": lobos_destino}
    
    
    search=djk.Dijkstra(data_structs["movimientos"], mtp_llave_origen)
    
    
    a=djk.hasPathTo(search, mtp_llave_destino)
    
    
    if a is True:
        distancia=djk.distTo(search, mtp_llave_destino)
        
        camino=djk.pathTo(search, mtp_llave_destino)
        
        arcos=lt.newList(datastructure="SINGLE_LINKED")
        for info in lt.iterator(camino):
            lt.addFirst(arcos, info)
        
        nodos=lt.newList(datastructure="ARRAY_LIST")
        for arco in lt.iterator(arcos):
            if lt.isPresent(nodos, arco["vertexA"])==0:
                lt.addLast(nodos, arco["vertexA"])
            if lt.isPresent(nodos, arco["vertexB"])==0:
                lt.addLast(nodos, arco["vertexB"])
        
        mtps=lt.newList(datastructure="ARRAY_LIST")
        for nodo in lt.iterator(nodos):
            if verificar_mtp_o_ps(nodo)=="mtp":
                lt.addLast(mtps, nodo)
                 
        lobos_en_camino=dar_lobos_en_adyacencias_lista(nodos)
    
        mapa=crear_mapa_folium()
        
        trail=[]
        lat_long_origen=(float(origen["location-lat"]), float(origen["location-long"]))
        trail.append(lat_long_origen)
        
        for nodo in lt.iterator(nodos):
            crear_marcador(mapa, nodo)
            crear_ruta(trail, nodo)
        
        lat_long_destino=(float(destino["location-lat"]), float(destino["location-long"]))
        trail.append(lat_long_destino)
        
        crear_punto(mapa, origen["location-long"], origen["location-lat"])
        crear_punto(mapa, destino["location-long"], destino["location-lat"])
        agregar_ruta(mapa, trail)
        
    
        return info_origen, info_destino, distancia, lobos_en_camino, arcos, nodos, mtps, mapa
    
    else:
        return None


def req_6(data_structs, fecha_inicial, fecha_final, sexo):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    
    fecha_inicial= fecha_inicial+ " 00:00"
    fecha_final= fecha_final + " 23:59"
    dicc_fecha_inicial = {"timestamp": fecha_inicial}
    dicc_fecha_final= {"timestamp": fecha_final}
    
    llave_lobos = mp.keySet(data_structs["lobos"])
    lista_lobos = lt.newList(datastructure="ARRAY_LIST")
    
    for llave in lt.iterator(llave_lobos):
        value= mp.get(data_structs["lobos"], llave)["value"]
        if value["animal-sex"] == sexo:
            lt.addLast(lista_lobos, llave)
    
    
    puntos_seguimiento = mp.newMap(numelements= 97 , maptype= "PROBING", loadfactor=0.5)
    puntos_seguimiento_lista = lt.newList("ARRAY_LIST")
    
    llaves_PS = mp.keySet(data_structs["ps"]) 
    
    for llave in lt.iterator(llaves_PS):
        if lt.isPresent(lista_lobos, llave) != 0:
            arbol= mp.get(data_structs["ps"], llave)["value"]
            llaves_arbol= om.keySet(arbol)
            for llave_arbol in lt.iterator(llaves_arbol):
                valor_arbol= om.get(arbol, llave_arbol)["value"]
                fila= valor_arbol["fila"]
                if (verificar_tiempo2(dicc_fecha_inicial, fila) == True) and (verificar_tiempo2(fila, dicc_fecha_final ) == True):
                    lt.addLast(puntos_seguimiento_lista, valor_arbol["ps"])
                    id= valor_arbol["fila"]["individual-local-identifier"]+ "_" + valor_arbol["fila"]["tag-local-identifier"]
                    if mp.contains(puntos_seguimiento, id) == False:
                        new_entry= lt.newList("ARRAY_LIST")
                        mp.put(puntos_seguimiento, id , new_entry)
                    else:
                        new_entry= mp.get(puntos_seguimiento, id)["value"]
                    lt.addLast(new_entry, valor_arbol["ps"])
    
    
    #mtp
    
    
    llaves_mtp= mp.keySet(data_structs["mtp"])
    mtps=lt.newList(datastructure="ARRAY_LIST")
             
    for llave in lt.iterator(llaves_mtp):
        value=mp.get(data_structs["mtp"], llave)["value"]
        lobos=lobos_diferentes_newgraph(value, puntos_seguimiento_lista)
        if lobos is not False:
            info={"mtp": llave, "pss": lobos}
            lt.addLast(mtps, info)
    
    grafo= gr.newGraph(datastructure= "ADJ_LIST", directed= True, size= 90000, cmpfunction=compareID)
    
    for ps in lt.iterator(puntos_seguimiento_lista):
        if not gr.containsVertex(grafo, ps):
            gr.insertVertex(grafo, ps)
            
    for mtp in lt.iterator(mtps):
        if not gr.containsVertex(grafo, mtp["mtp"]):
            gr.insertVertex(grafo, mtp["mtp"])
    
    
    addRouteConnections_PS_newgraph(data_structs, grafo,  puntos_seguimiento_lista)
    addRouteConnections_MTP_newgraph(grafo, mtps)
    
    #distancias
    cantidad_lobos = lt.size(puntos_seguimiento_lista)
    distancia_lobos = mp.newMap(numelements= cantidad_lobos*2+1, maptype= "PROBING", loadfactor=0.5)
    
    arcos= gr.edges(grafo)
    
    for arco in lt.iterator(arcos):
        lobo= dar_lobo_en_arco(arco)
        if mp.contains(distancia_lobos, lobo) == False:
            
            new_entry = {"id": lobo, "distancia": 0}
            mp.put(distancia_lobos, lobo, new_entry)
        else:
            new_entry = mp.get(distancia_lobos, lobo)["value"]
        new_entry["distancia"]+= e.weight(arco)
    
    
    info_mayor = encontrar_mayor_distancia(distancia_lobos)
    info_menor = encontrar_menor_distancia(distancia_lobos)
    
    #mayor
    
    distancia_mayor = info_mayor[1]
    llave_mayor = info_mayor[0]
    fila_mayor = mp.get(data_structs["lobos"], llave_mayor)["value"]
    
    ps_mayor = mp.get(puntos_seguimiento, llave_mayor)["value"]
    
    #travel_dist mayor
    
    mayor_total=mp.get(data_structs["ps"], llave_mayor)["value"]
    keyset_arbol=om.keySet(mayor_total)
    
    travel_dist_mayor=0
    prevrout= lt.getElement(keyset_arbol,1)
    prev_value=om.get(mayor_total, prevrout)["value"]
    prevrout_llave=prev_value["ps"]
    
    for i in range(2, lt.size(keyset_arbol)+1):
        route=lt.getElement(keyset_arbol, i)
        value=om.get(mayor_total, route)["value"]
        route_llave=value["ps"]
        arco=gr.getEdge(data_structs["movimientos"], prevrout_llave, route_llave)
        if arco is not None:
            travel_dist_mayor+=e.weight(arco)
            prevrout_llave = route_llave
    
    # ruta mas larga mayor
    ruta_mayor = lt.newList("ARRAY_LIST")
    
    if lt.size(ps_mayor)<=3:
        primeros_mayores=ps_mayor
        ultimos_mayores=ps_mayor
    else:
        primeros_mayores=lt.subList(ps_mayor, 1, 3)
        ultimos_mayores=lt.subList(ps_mayor, lt.size(ps_mayor)-2, 3)
    
    for ps in lt.iterator(primeros_mayores):
        lt.addLast(ruta_mayor, ps)
        
    for ps in lt.iterator(ultimos_mayores):
        lt.addLast(ruta_mayor, ps)
        
    arcos_mayor=lt.newList(datastructure="ARRAY_LIST")
    for i in range(1, lt.size(ps_mayor)):
        ps1= lt.getElement(ps_mayor, i)
        ps2 = lt.getElement(ps_mayor, i+1)
        arco = gr.getEdge(grafo, ps1, ps2)
        lt.addLast(arcos_mayor, arco)
    
    dicc_mayor={"id": llave_mayor, "fila":fila_mayor, "distancia": distancia_mayor,"nodos":lt.size(ps_mayor),"arcos":lt.size(arcos_mayor), "ruta":ruta_mayor }
    
    #menor
    
    distancia_menor = info_menor[1]
    llave_menor = info_menor[0]
    fila_menor = mp.get(data_structs["lobos"], llave_menor)["value"]
    
    #travel_dist menor
    
    menor_total=mp.get(data_structs["ps"], llave_menor)["value"]
    keyset_arbol=om.keySet(menor_total)
    
    travel_dist_menor=0
    prevrout= lt.getElement(keyset_arbol,1)
    prev_value=om.get(menor_total, prevrout)["value"]
    prevrout_llave=prev_value["ps"]
    
    for i in range(2, lt.size(keyset_arbol)+1):
        route=lt.getElement(keyset_arbol, i)
        value=om.get(menor_total, route)["value"]
        route_llave=value["ps"]
        arco=gr.getEdge(data_structs["movimientos"], prevrout_llave, route_llave)
        if arco is not None:
            travel_dist_menor+=e.weight(arco)
            prevrout_llave = route_llave
    
    # ruta mas larga menor
    
    ps_menor= mp.get(puntos_seguimiento, llave_menor)["value"]
    ruta_menor = lt.newList("ARRAY_LIST")
    
    if lt.size(ps_menor)<=3:
        primeros_menores=ps_menor
        ultimos_menores=ps_menor
    else:
        primeros_menores=lt.subList(ps_menor, 1, 3)
        ultimos_menores=lt.subList(ps_menor, lt.size(ps_menor)-2, 3)
    
    
        
    
    
    for ps in lt.iterator(primeros_menores):
        lt.addLast(ruta_menor, ps)
        
    for ps in lt.iterator(ultimos_menores):
        lt.addLast(ruta_menor, ps)
        
    arcos_menor=lt.newList(datastructure="ARRAY_LIST")
    for i in range(1, lt.size(ps_menor)):
        ps1= lt.getElement(ps_menor, i)
        ps2 = lt.getElement(ps_menor, i+1)
        arco = gr.getEdge(grafo, ps1, ps2)
        lt.addLast(arcos_menor, arco)

    dicc_menor={"id": llave_menor, "fila": fila_menor, "distancia": distancia_menor, "nodos":lt.size(ps_menor),"arcos":lt.size(arcos_menor),"ruta":ruta_menor }
    
    mapa=crear_mapa_folium()
        
    trail1=[]
    trail2 = []
        
    for nodo in lt.iterator(ruta_mayor):
        crear_marcador(mapa, nodo)
        crear_ruta(trail1, nodo)

    for nodo in lt.iterator(ruta_menor):
        crear_marcador(mapa, nodo)
        crear_ruta(trail2, nodo)
        
    agregar_ruta(mapa, trail1)
    agregar_ruta(mapa, trail2)
            
    
    return dicc_mayor, dicc_menor, mapa
    
     
        
def req_7(data_structs, fecha_inicial, fecha_final, temp_min, temp_max):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    
    fecha_inicial= fecha_inicial+ " 00:00"
    fecha_final= fecha_final + " 23:59"
    dicc_fecha_inicial = {"timestamp": fecha_inicial}
    dicc_fecha_final= {"timestamp": fecha_final}
    
    puntos_seguimiento = mp.newMap(numelements= 97 , maptype= "PROBING", loadfactor=0.5)
    puntos_seguimiento_lista = lt.newList("ARRAY_LIST")
    
    llaves_PS = mp.keySet(data_structs["ps"]) 
    
    for llave in lt.iterator(llaves_PS):
        arbol= mp.get(data_structs["ps"], llave)["value"]
        llaves_arbol= om.keySet(arbol)
        for llave_arbol in lt.iterator(llaves_arbol):
            valor_arbol= om.get(arbol, llave_arbol)["value"]
            fila= valor_arbol["fila"]
            if (verificar_tiempo2(dicc_fecha_inicial, fila) == True) and (verificar_tiempo2(fila, dicc_fecha_final ) == True) and (float(temp_min)<=float(fila["external-temperature"])) and (float(temp_max)>=float(fila["external-temperature"])):
                if lt.isPresent(puntos_seguimiento_lista, valor_arbol["ps"])== 0:
                    lt.addLast(puntos_seguimiento_lista, valor_arbol["ps"])
                id= valor_arbol["fila"]["individual-local-identifier"]+ "_" + valor_arbol["fila"]["tag-local-identifier"]
                if mp.contains(puntos_seguimiento, id) == False:
                    new_entry= lt.newList("ARRAY_LIST")
                    mp.put(puntos_seguimiento, id , new_entry)
                else:
                    new_entry= mp.get(puntos_seguimiento, id)["value"]
                lt.addLast(new_entry, valor_arbol["ps"])
    
    
    #mtp
    llaves_mtp= mp.keySet(data_structs["mtp"])
    mtps=lt.newList(datastructure="ARRAY_LIST")
             
    for llave in lt.iterator(llaves_mtp):
        value=mp.get(data_structs["mtp"], llave)["value"]
        lobos=lobos_diferentes_newgraph(value, puntos_seguimiento_lista)
        if lobos is not False:
            info={"mtp": llave, "pss": lobos}
            lt.addLast(mtps, info)
    
    
    grafo= gr.newGraph(datastructure= "ADJ_LIST", directed= True, size= 90000, cmpfunction=compareID)
    
    for ps in lt.iterator(puntos_seguimiento_lista):
        if not gr.containsVertex(grafo, ps):
            gr.insertVertex(grafo, ps)
            
    for mtp in lt.iterator(mtps):
        if not gr.containsVertex(grafo, mtp["mtp"]):
            gr.insertVertex(grafo, mtp["mtp"])
    
    
    addRouteConnections_PS_newgraph(data_structs, grafo,  puntos_seguimiento_lista)
    addRouteConnections_MTP_newgraph(grafo, mtps)
    
    #cfc
    search = scc.KosarajuSCC(grafo)  

    cantidad = scc.connectedComponents(search)  
     
    llave_ref= lt.getElement(mtps, 1)["mtp"] 
    cfc= scc.sccCount(grafo, search, llave_ref)   

    mapa_cfc = mp.newMap(numelements= cantidad//4 , maptype= "CHAINING", loadfactor= 4 )  
    vertices = mp.keySet(cfc["idscc"])   

    
    #reversar 
    for vertice in lt.iterator(vertices):  
        value = mp.get(cfc["idscc"], vertice)  
        id=value["value"]  
        entry = mp.get(mapa_cfc, id)  
        if entry == None:  
            lista = lt.newList(datastructure="ARRAY_LIST")  
            mp.put(mapa_cfc, id, lista)  
        else:  
            lista= mp.get(mapa_cfc, id )["value"]  
        lt.addLast(lista, vertice)  

    # encontrar 3 grandes y 3 pequeños
    
    keyset_cfc= mp.keySet(mapa_cfc)   
    mapa_grande_pequeño = mp.newMap(numelements= 13, maptype="PROBING")
    mayor_cfc= mp.newMap(numelements= 7, maptype="PROBING" )
    menor_cfc= mp.newMap(numelements=7, maptype= "PROBING")  
    lista_mayores = lt.newList("ARRAY_LIST")
    lista_menores = lt.newList("ARRAY_LIST")
    lista_grande_pequeño = lt.newList("ARRAY_LIST")

    while mp.size(mayor_cfc) < 3:   
        mayor=0  
        for llave in lt.iterator(keyset_cfc):  
            value= mp.get(mapa_cfc, llave)["value"]  
            tamanio= lt.size(value) 
            if tamanio> mayor and mp.contains(mayor_cfc, llave) == False:  
                mayor= tamanio  
                mayor_values = value  
                llave_mayor = llave  
        mp.put(mayor_cfc, llave_mayor, mayor_values)
        mp.put(mapa_grande_pequeño, llave_mayor, mayor_values)  
        lt.addLast(lista_mayores, llave_mayor)
        lt.addLast(lista_grande_pequeño, llave_mayor)
    
    while mp.size(menor_cfc) < 3: 
        llave_ref= lt.getElement(lista_mayores, 1) 
        value_ref= mp.get(mapa_cfc, llave_ref)["value"]
        menor =  lt.size(value_ref)  
        for llave in lt.iterator(keyset_cfc):  
            value= mp.get(mapa_cfc, llave)["value"]  
            tamanio= lt.size(value) 
            if tamanio <= menor and mp.contains(menor_cfc, llave) == False:  
                menor= tamanio  
                menor_values = value  
                llave_menor = llave  
        mp.put(menor_cfc, llave_menor, menor_values) 
        mp.put(mapa_grande_pequeño, llave_menor, menor_values) 
        lt.addLast(lista_menores, llave_menor)
        lt.addLast(lista_grande_pequeño, llave_menor)

    keyset_grande_pequeño = mp.keySet(mapa_grande_pequeño)

    mapa = mp.newMap(numelements= 13, maptype="PROBING", loadfactor=0.5) 
     

    for llave in lt.iterator(keyset_grande_pequeño):  

        diccionario = {} 
        mp.put(mapa, llave, diccionario) 
        
    #encontrar 3 primeros y 3 ultimos
    
    for llave in lt.iterator(keyset_grande_pequeño): 
        primeros_ultimos = lt.newList("ARRAY_LIST") 
        value= mp.get(mapa_grande_pequeño, llave)["value"] 
        if lt.size(value)<=6: 
            for dato in lt.iterator(value):
                lt.addLast(primeros_ultimos, dato) 

        else: 
            for i in range (1,4): 
                fila= lt.getElement(value, i) 
                lt.addLast(primeros_ultimos,  fila) 
            for i in range (lt.size(value)-2, lt.size(value)+1): 
                fila= lt.getElement(value, i) 
                lt.addLast(primeros_ultimos,  fila) 

         
        dicc=mp.get(mapa, llave)["value"] 
        dicc["primeros_ultimos"]= primeros_ultimos
        
    #tamaño
    
    for llave in lt.iterator(keyset_grande_pequeño):
        dicc = mp.get(mapa, llave)["value"] 
        value= mp.get(mapa_grande_pequeño, llave)["value"]
        dicc["tamaño"]= lt.size(value)
        

    #encontrar lat y long  

    for llave in lt.iterator(keyset_grande_pequeño):  

        value= mp.get(mapa_grande_pequeño, llave)["value"]  
        mayor = buscar_mayor_long_lat_lista(value)  
        menor = buscar_menor_long_lat_lista (value)  
        lat_max  = lt.getElement(mayor, 2)  
        long_max = lt.getElement(mayor, 1)  
        lat_min = lt.getElement(menor, 2)  
        long_min = lt.getElement(menor, 1)  

        dicc = mp.get(mapa, llave)["value"] 
        dicc["min_lat"] = lat_min 
        dicc["max_lat"] = lat_max 
        dicc["min_lon"] = long_min 
        dicc["max_lon"] = long_max     
    
    
    #encontrar lobos
    for llave in lt.iterator(keyset_grande_pequeño): 
        
        lista_lobos = lt.newList(datastructure= "ARRAY_LIST") 
        value= mp.get(mapa_grande_pequeño, llave)["value"] 
        lobos = dar_lobos_en_adyacencias_lista(value) 
        cantidad_lobos = lt.size(lobos) 

        
        if cantidad_lobos <=6: 
            for lobo in lt.iterator(lobos): 
                fila= mp.get(data_structs["lobos"], lobo)["value"] 
                lt.addLast(lista_lobos,fila ) 

        else: 
            for i in range (1,4): 
                lobo= lt.getElement(lobos, i) 
                fila= mp.get(data_structs["lobos"], lobo)["value"] 
                lt.addLast(lista_lobos, fila ) 

            for i in range (lt.size(lobos)-2, lt.size(lobos)+1): 
                lobo= lt.getElement(lobos, i) 
                fila= mp.get(data_structs["lobos"], lobo)["value"] 
                lt.addLast(lista_lobos, fila ) 

 
        dicc=mp.get(mapa, llave)["value"] 
        dicc["cantidad_lobos"] = cantidad_lobos 
        dicc["informacion_lobos"]= lista_lobos
        
        
    #Ruta más larga
        
    mapa_arcos = mp.newMap(numelements = 13, maptype="PROBING")
        
    for llave in lt.iterator(keyset_grande_pequeño):
            value = {"arcos": lt.newList("ARRAY_LIST"), "distancia": 0, "cantidad_lobos": 0, "cantidad_vertices": 0, "cantidad_arcos":0, "primeros_ultimos": lt.newList("ARRAY_LIST"), "lobos": lt.newList("ARRAY_LIST")}
            mp.put(mapa_arcos, llave, value)         
        
        
    edges = gr.edges(grafo)
    
    
    for arco in lt.iterator(edges):
        for llave in  lt.iterator(keyset_grande_pequeño):
            lista= mp.get(mapa_grande_pequeño, llave)["value"]
            if lt.isPresent(lista, arco["vertexA"] ) != 0 and lt.isPresent(lista, arco["vertexB"] ) != 0  :
                arcos = mp.get(mapa_arcos, llave)["value"]
                lt.addLast(arcos["arcos"], arco)
              
    for llave in lt.iterator(keyset_grande_pequeño):
        arcos = mp.get(mapa_arcos, llave)["value"]
        for arco in lt.iterator(arcos["arcos"]):
            arcos["distancia"]+= e.weight(arco)
    
        arcos["cantidad_arcos"] = lt.size(arcos["arcos"])
        dicc=mp.get(mapa_grande_pequeño, llave)["value"] 
        arcos["cantidad_vertices"] = lt.size(dicc)
        arcos["cantidad_lobos"] = lt.size(dar_lobos_en_adyacencias_lista(dicc))
        arcos["primeros_ultimos"] = darTresPrimeros_Ultimos(dicc)
    
        if arcos["cantidad_lobos"] <= 6:
            arcos["lobos"]= dar_lobos_en_adyacencias_lista(dicc)
        else:
            lobos = dar_lobos_en_adyacencias_lista(dicc)
            for i in range(1,4):
                lt.addLast(arcos["lobos"], lt.getElement(lobos, i))
            for i in range (lt.size(lobos)-2, lt.size(lobos)+1):
                lt.addLast(arcos["lobos"], lt.getElement(lobos, i))
        
        
        
    #folium cfc
    mapa_folium = crear_mapa_folium()
    lista_color = ["red", "purple", "pink", "darkgreen", 'cadetblue', "orange"]
    contador = 0 
        
    for llave in lt.iterator(keyset_grande_pequeño):
        puntos = mp.get(mapa_grande_pequeño, llave)["value"]
        entry= mp.get(mapa, llave)["value"]
        
        crear_circulo(mapa_folium, entry["min_lon"], entry["max_lon"], entry["min_lat"], entry["max_lat"], llave, lista_color[contador] )
        contador+= 1
        for punto in lt.iterator(puntos):
            crear_marcador(mapa_folium, punto)
        
    #folium ruta mas larga
     
    
    for llave in lt.iterator(keyset_grande_pequeño):
        trail=[]
        nodos=mp.get(mapa_grande_pequeño, llave)["value"] 
        for nodo in lt.iterator(nodos):
            crear_ruta(trail, nodo)
            
        agregar_ruta(mapa_folium, trail)
        
        

    return cantidad, mapa, lista_grande_pequeño, mapa_arcos, mapa_folium
    
            

    

def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass



# Funciones utilizadas para comparar elementos dentro de una lista

def compareID(id1, vertice):
    """
    Compara dos estaciones
    """
    
    dato1=devolver_formato(id1)
    info1=separar_id(dato1)
    
    id2 = vertice['key']
    dato2=devolver_formato(id2)
    
    info2=separar_id(dato2)
    
    
    if float(info1[0])> float(info2[0]):
        return 1
    
    elif float(info1[0])< float(info2[0]):
        return -1
    
    else:
        if float(info1[1])> float(info2[1]):
            return 1
    
        elif float(info1[1])< float(info2[1]):
            return -1
        
        else:
            return 0
    
    
def compareID2(id1, id2):
    """
    Compara dos estaciones
    """
    
    dato1=devolver_formato(id1)
    info1=separar_id(dato1)
    
    dato2=devolver_formato(id2)
    info2=separar_id(dato2)
    
    
    if float(info1[0])> float(info2[0]):
        return 1
    
    elif float(info1[0])< float(info2[0]):
        return -1
    
    else:
        if float(info1[1])> float(info2[1]):
            return 1
    
        elif float(info1[1])< float(info2[1]):
            return -1
        
        else:
            return 0

def compareID3(id1, id2):
    """
    Compara dos estaciones
    """
    for llave in id1.keys():
        key1=llave
        
    for llave in id2.keys():
        key2=llave
    
    if key1 > key2:
        return 1
    
    elif key1 < key2:
        return -1  
    else:
        return 0
    
def compareID4(id1, id2):
    """
    Compara dos estaciones
    """
    
    dato1=devolver_formato(id1)
    info1=separar_id(dato1)
    
    dato2=devolver_formato(id2)
    info2=separar_id(dato2)
    
    
    if info1[0]> info2[0]:
        return 1
    
    elif info1[0]< info2[0]:
        return -1
    
    else:
        if info1[1]> info2[1]:
            return 1
    
        elif info1[1]< info2[1]:
            return -1
        
        else:
            return 0

def compareID5(id1, id2):
    """
    Compara dos estaciones
    """
    key1=id1["ps"]
    key2=id2["ps"]
    
    if key1 > key2:
        return 1
    
    elif key1 < key2:
        return -1  
    else:
        return 0

def cmp_by_fecha_hora (id1, id2):
    
    for llave in id1.keys():
        id1_fc= id1[llave]["timestamp"]
        id1_fcc= dt.strptime(id1_fc, "%Y-%m-%d %H:%M")
    
    for llave in id2.keys():
        id2_fc= id2[llave]["timestamp"]
        id2_fcc= dt.strptime(id2_fc, "%Y-%m-%d %H:%M")
    
    if id1_fcc < id2_fcc:
        return True
    else:
        return False
    
   
   
def cmp_by_hora(id1, id2):
    
  
    id1_fcc= dt.strptime(id1, "%Y-%m-%d %H:%M")
    
    id2_fcc= dt.strptime(id2, "%Y-%m-%d %H:%M")
    
    if id1_fcc > id2_fcc:
        return 1
    
    elif id1_fcc < id2_fcc:
        return -1
    
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


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass

#folium

def crear_mapa_folium():
    mapa=folium.Map(location=[58.096, -113.248], zoom_start=8)
    return mapa
    
    
def crear_marcador(mapa, vertice):
    
    ubicacion_vertice=dar_lat_long_nodo(vertice)
    longitud=float(lt.getElement(ubicacion_vertice,1))
    latitud=float(lt.getElement(ubicacion_vertice,2))
    etiqueta=vertice
    
    if verificar_mtp_o_ps(vertice)=="mtp":
        color="darkgreen"
    else:
        color="darkblue"
    
    folium.Marker(location=[latitud, longitud],popup=etiqueta,icon=folium.Icon(color=color)).add_to(mapa)
    
def crear_punto(mapa, longitud, latitud):
    color="purple"
    etiqueta="("+longitud+ ", "+latitud+")"
    longitud=float(longitud)
    latitud=float(latitud)
    
    folium.Marker(location=[latitud, longitud],popup=etiqueta,icon=folium.Icon(color=color)).add_to(mapa)
    
    
    
def crear_ruta(trail, vertice):
    ubicacion=dar_lat_long_nodo(vertice)
    lat_long=(float(lt.getElement(ubicacion, 2)), float(lt.getElement(ubicacion, 1)))
    trail.append(lat_long)
        
    
def agregar_ruta(mapa, trail):
    folium.PolyLine(trail).add_to(mapa)
    
    
def crear_circulo (mapa, lon_min, lon_max, lat_min, lat_max, llave_manada, color):
    
    lat= (float(lat_max)+float(lat_min))/2
    lon = (float(lon_max)+float(lon_min))/2
    
    if float(lat_max)-lat >= float(lon_max)-lon:
        radio = lat_max-lat
    else:
        radio = lon_max-lon   
    
    folium.CircleMarker(location=[lat, lon], radius= radio*1000, popup= llave_manada, color=color, fill=True, fill_color=color,).add_to(mapa)

 