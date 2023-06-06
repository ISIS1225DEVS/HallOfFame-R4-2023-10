"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback

default_limit = 10000
sys.setrecursionlimit(default_limit*1000)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """
    control=controller.new_controller()
    
    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Planear una posible ruta entre dos puntos de encuentro")
    print("3- Reconocer los territorios habitados por distintas manadas")
    print("4- Identificar el camino más corto entre dos puntos del hábitat")
    print("5- Identificar diferencias en los corredores migratorios según el tipo de individuo")
    print("6- Identificar cambios en el territorio de las manadas según condiciones climáticas")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    print("\nSeleccione cuántos datos desea cargar:")
    print("1: 1% de los datos")
    print("2: 5% de los datos")
    print("3: 10% de los datos")
    print("4: 20% de los datos")
    print("5: 30% de los datos")
    print("6: 50% de los datos")
    print("7: 80% de los datos")
    print("8: 100% de los datos")
    res=input()
    try:
        if int(res)==1:
            filename="small.csv"
        elif int(res)==2:
            filename='5pct.csv'
        elif int(res)==3:
            filename='10pct.csv'
        elif int(res)==4:
            filename='20pct.csv'
        elif int(res)==5:
            filename='30pct.csv'
        elif int(res)==6:
            filename='50pct.csv'
        elif int(res)==7:
            filename='80pct.csv'
        elif int(res)==8:
            filename='large.csv'
        else:
            print("Opción errónea, vuelva a elegir.\n")
    except ValueError:
            print("Ingrese una opción válida.\n")
            traceback.print_exc()
        
        
                    
    print("\nCargando información de los archivos ....\n")
    
    datas = controller.load_data(control,filename)
    
    tabla1=[]
    print("---Información del grafo---\n")
    
    tabla1.append(["Total de lobos reconocidos en el estudio", datas[0]])
    tabla1.append(["Total de eventos cargados durante el estudio", datas[1]])
    tabla1.append(["Total de puntos de encuentro reconocidos", datas[2]])
    tabla1.append(["Total de puntos de seguimiento reconocidos", datas[3]])
    tabla1.append(["Total de arcos creados para unir los nodos de encuentro y los puntos de seguimiento", datas[4]])
    tabla1.append(["Total de arcos creados entre puntos de seguimiento", datas[5]])
    
    menor_lat=controller.buscar_menor(control, "location-lat")
    mayor_lat=controller.buscar_mayor(control, "location-lat")
    
    menor_long=controller.buscar_menor(control, "location-long")
    mayor_long=controller.buscar_mayor(control, "location-long")
    
    tabla1.append(["Latitud mínima y máxima reconocida", menor_lat["location-lat"]+" y "+mayor_lat["location-lat"]])
    tabla1.append(["Longitud mínima y máxima reconocida", menor_long["location-long"]+" y "+mayor_long["location-long"]])
    
    print(tabulate(tabla1, tablefmt="fancy_grid", stralign="left"))
    print("\t-Total de nodos en el grafo:", datas[2]+datas[3])
    print("\t-Total de arcos en el grafo:", datas[4]+datas[5])
    
    tabla=[]
    titulos=["Longitud aproximada", "Latitud aproximada","Identificador del nodo", "Identificadores en el punto", "Número de nodos adyacentes"]
    
    mtps = datas[6]
    pss= datas[7]
    
    print("\n\nPrimeros y últimos cinco nodos cargados:\n")
    
    for i in range(1,6):
        linea=[]
        if lt.size(pss)>=i:
            fila_ref=lt.getElement(pss, i)
            linea.append(fila_ref["info"]["location-long"])
            linea.append(fila_ref["info"]["location-lat"])
            linea.append(fila_ref["id"])
            comp=fila_ref["id"].split("_")
            lobo=comp[2]+"_"+comp[3]
            linea.append(lobo)
            adyacencias=controller.dar_adyacencias(control,fila_ref["id"] )
            linea.append(lt.size(adyacencias))  
            tabla.append(linea)
        
    for i in range(lt.size(mtps)-4,lt.size(mtps)+1):
        linea=[]
        if lt.size(mtps)>=lt.size(mtps)-i:
            id=lt.getElement(mtps, i)
            fila_ref=lt.getElement(id["info"], 1)
            linea.append(fila_ref["fila"]["location-long"])
            linea.append(fila_ref["fila"]["location-lat"])
            linea.append(id["id"])
            lobos=controller.dar_lobos_en_adyancencias(control, id["id"])
            ids=[]
            for lobo in lt.iterator(lobos):
                ids.append(lobo)
                
            ids_str=", ".join(ids)
            linea.append(ids_str)
            adyacencias=controller.dar_adyacencias(control,id["id"] )
            linea.append(lt.size(adyacencias))  
            tabla.append(linea)
    
    print(tabulate(tabla, headers=titulos, tablefmt="fancy_grid", stralign="left", numalign="left"))
    print("\nTiempo de ejecución [ms]", datas[8])
    print("\n")


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    origen=input("Ingrese el punto de encuentro de inicio: ")
    destino=input("Ingrese el punto de encuentro de final: ")
    datas=controller.req_1(control, origen, destino)
    
    print('\n---------------Req No. 1-------------------\n')
    
    mapa=datas[0][4]
    mapa.show_in_browser()
    
    
    if datas is None:
        print("No existe un camino entre", origen, "y", destino)
        
    else:
        print("Total distancia en el camino",datas[0][0], "km")
        print("Total de nodos en el camino", datas[0][1]+datas[0][2])
        print("Total puntos de encuentro en el camino:", datas[0][1])
        print("Total puntos de seguimiento en el camino:", datas[0][2])
        print("\n")
        
        info_filas=datas[0][3]
        
        tabla=[]
        
        print("---Especificaciones del camino de DFS---")
        print("Primeros y últimos 5 nodos cargados en el camino:\n")
        for i in range(1,6):
            info=lt.getElement(info_filas, i)
            linea=[]
            ubicacion=lt.getElement(info,2)
            linea.append(ubicacion[0])
            linea.append(ubicacion[1])
            id=lt.getElement(info, 1)
            linea.append(id)
            linea.append(lt.getElement(info, 3))
            lobos=controller.dar_lobos_en_adyancencias(control, id)
            ids=[]
            if lt.size(lobos)<=6:
                for lobo in lt.iterator(lobos):
                    ids.append(lobo)
            else:
                for i in range(1,4):
                    ids.append(lt.getElement(lobos,i))
                for i in range(lt.size(lobos)-2,lt.size(lobos)+1):
                    ids.append(lt.getElement(lobos,i))             
            ids_str=", ".join(ids)
            linea.append(ids_str)
            info2=lt.getElement(info_filas, i+1)
            id2=lt.getElement(info2, 1)
            linea.append(id2)
            distancia=controller.dar_distancia(control["movimientos"], id, id2)
            linea.append(distancia)
            tabla.append(linea)
        
        for i in range(lt.size(info_filas)-4,lt.size(info_filas)+1):
            info=lt.getElement(info_filas, i)
            linea=[]
            ubicacion=lt.getElement(info,2)
            linea.append(ubicacion[0])
            linea.append(ubicacion[1])
            id=lt.getElement(info, 1)
            linea.append(id)
            linea.append(lt.getElement(info, 3))
            lobos=controller.dar_lobos_en_adyancencias(control, id)
            ids=[]
            if lt.size(lobos)<=6:
                for lobo in lt.iterator(lobos):
                    ids.append(lobo)
            else:
                for i in range(1,4):
                    ids.append(lt.getElement(lobos,i))
                for i in range(lt.size(lobos)-2,lt.size(lobos)+1):
                    ids.append(lt.getElement(lobos,i))             
            ids_str=", ".join(ids)
            linea.append(ids_str)
            if i!=lt.size(info_filas):
                info2=lt.getElement(info_filas, i+1)
                id2=lt.getElement(info2, 1)
                linea.append(id2)
                distancia=controller.dar_distancia(control["movimientos"], id, id2)
                linea.append(distancia)
                    
            else:
                linea.append("Desconocido")
                linea.append("Desconocido")
            tabla.append(linea)
        
        
            
    
            
    titulos=["long-aprox","lat-aprox","Identificador del nodo", "Cantidad de\nlobos en\nel nodo", "Identificadores de\nlobos en el punto", "Edge-to", "Edge-distance-to" ]    
    anchos=[4,4,None,5, 14, None, 10] 
        
    print(tabulate(tabla, headers=titulos, maxcolwidths=anchos, tablefmt="fancy_grid", stralign="left", numalign="left"))
    print("\nTiempo de ejecución [ms]:", datas[1])
    print("\n")
            
                
    
    



def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    datas=controller.req_3(control)
    
    print('\n---------------Req No. 3-------------------\n')
    
    cantidad = datas[0][0] 

    info = datas[0][1]
    
    orden = datas[0][2] 
    
    mapa=datas[0][3]
    mapa.show_in_browser()

    print("\n  Hay " , cantidad , "componentes fuertemente conectados en el grafo") 
    print ("\n Los TOP 5 componentes fuertemente conectados en el grafo son: ")

    titulos1= ["SCCID\n", "Nodos ID\n", "Tamaño\n", "min-lat\n" , "max-lat\n", "min-lon\n", "max-lon\n", "Cantidad\nlobos\n", "Información lobos"] 
    llaves1 = ["primeros_ultimos", "tamaño", "min_lat", "max_lat", "min_lon", "max_lon", "cantidad_lobos", "informacion_lobos" ] 
    anchos = [1, 15, 1, 1, 1, 1, 1, 1, None]
    tabla1=[]

    subtitulos= ["individual-id", "animal-sex", "animal-life-stage", "study-site", "deployment-comments"]
    subtitulos1= ["individual-id", "animal-sex", "animal-life-\nstage", "study-site", "deployment-\ncomments"]


    for dato in lt.iterator(orden): 
        fila=[] 
        fila.append(dato)
        value= mp.get(info, dato)["value"] 
        for llave in llaves1: 
            if llave== "primeros_ultimos":
                linea = []
                for nodo in lt.iterator(value["primeros_ultimos"]):
                    linea.append(nodo)
                fila_str=", ".join(linea)
                fila.append(fila_str)
            elif llave== "informacion_lobos":
                subtabla=[]
                for lobo in lt.iterator(value["informacion_lobos"]):
                    sublinea= []
                    for subllave in subtitulos:
                        if subllave == "individual-id":
                            id= lobo["animal-id"]+ "_" + lobo["tag-id"]
                            sublinea.append(id)
                        else:
                            if lobo[subllave]== "":
                                sublinea.append("Unknown")
                            else:
                                sublinea.append(lobo[subllave])
                    subanchos=[4, 4, 4, 7, 10]
                    subtabla.append(sublinea)
                tabulada=tabulate(subtabla, headers= subtitulos1, tablefmt="fancy_grid", maxcolwidths=subanchos, stralign="left", numalign="left")
                fila.append(tabulada)        
            else:
                fila.append(value[llave])
            
        tabla1.append(fila)
    
    print(tabulate(tabla1, headers=titulos1, tablefmt="fancy_grid", maxcolwidths=anchos, stralign="left", numalign="left"))
    
                    
        
    print("\nTiempo de ejecución [ms]:", datas[1]) 

    print("\n") 

     
    
 


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    origen_long=input("\nIngrese la longitud del origen: ")
    origen_lat=input("Ingrese la latitud del origen: ")
    destino_long=input("Ingrese la longitud del destino: ")
    destino_lat=input("Ingrese la latitud del destino: ")
    
    origen={"location-long":origen_long, "location-lat": origen_lat}
    destino={"location-long":destino_long, "location-lat": destino_lat}
    
    datas=controller.req_4(control, origen, destino)
    print('\n---------------Req No. 4-------------------\n')
    
    
    if datas[0] is None:
        return "No se encontró un camino desde (",origen_long, ",", origen_lat, ") hasta (",origen_long, ",", origen_lat, ")"
    
    info_origen=datas[0][0]
    info_destino=datas[0][1]
    
    mapa=datas[0][7]
    mapa.show_in_browser()
    
    titulos1=["Identificador del nodo", "location-long-aprox", "location-lat-aprox", "Identificadores de lobos en el punto"]
    llaves1=["id", "longitud", "latitud", "lobos"]
    
    
    print("---Punto de encuentro de origen---")
    print("\tDistancia desde el punto de origen",info_origen["distancia"],"km")

    tabla11=[]
    linea11=[]
    for llave in llaves1:
        if llave=="lobos":
            ids=[]
            for lobo in lt.iterator(info_origen[llave]):
                ids.append(lobo)
            ids_str=", ".join(ids)
            linea11.append(ids_str)
        else:
            linea11.append(info_origen[llave])
    tabla11.append(linea11)
            
    print(tabulate(tabla11, headers=titulos1, tablefmt="fancy_grid", stralign="left", numalign="left"))
    
    print("\n---Punto de encuentro de destino---")
    print("\tDistancia desde el punto de origen",info_destino["distancia"],"km")
    tabla12=[]
    linea12=[]
    for llave in llaves1:
        
        if llave=="lobos":
            ids=[]
            for lobo in lt.iterator(info_destino[llave]):
                ids.append(lobo)
            ids_str=", ".join(ids)
            linea12.append(ids_str)
        else:
            linea12.append(info_destino[llave])
    tabla12.append(linea12)
            
    print(tabulate(tabla12, headers=titulos1, tablefmt="fancy_grid", stralign="left", numalign="left"))
    
    lobos_en_camino=datas[0][3]
    arcos=datas[0][4]
    nodos=datas[0][5]
    mtps=datas[0][6]

    print("\n---Detalles de la ruta---")
    print("- Cantidad de nodos en la ruta:", lt.size(nodos))
    print("- Cantidad de viajes en la ruta:", lt.size(arcos))
    print("- Distancia total de la ruta:", datas[0][2])
    print("- Cantidad de lobos identificados en la ruta:", lt.size(lobos_en_camino))
    
    print("\n---Detalles del camino---")
    print("Hay",lt.size(arcos), "arcos en el camino")
    print("\n\tPrimeros y últimos 3 arcos en el camino")
    
    tabla2=[]
    titulos2=["ID del nodo\ndel origen", "location-long\norigen", "location-lat\norigen", "ID del nodo\ndel destino", "location-long\ndestino", "location-lat\ndestino", "individual-id", "Distancia"]
    
    if lt.size(arcos)<=6:
        for i in range(1, lt.size(arcos)+1):
            linea2=[]
            arco=lt.getElement(arcos, i)
            linea2.append(arco["vertexA"])
            ubicacionA=controller.dar_lat_long_nodo(arco["vertexA"])
            linea2.append(lt.getElement(ubicacionA,1))
            linea2.append(lt.getElement(ubicacionA,2))
            linea2.append(arco["vertexB"])
            ubicacionB=controller.dar_lat_long_nodo(arco["vertexB"])
            linea2.append(lt.getElement(ubicacionB,1))
            linea2.append(lt.getElement(ubicacionB,2))
            lobo=controller.dar_lobo_en_arco(arco)
            linea2.append(lobo)
            distancia=controller.dar_distancia(control["movimientos"], arco["vertexA"], arco["vertexB"])
            linea2.append(distancia)    
            
            tabla2.append(linea2)
    else:
        for i in range(1, 4):
            linea2=[]
            arco=lt.getElement(arcos, i)
            linea2.append(arco["vertexA"])
            ubicacionA=controller.dar_lat_long_nodo(arco["vertexA"])
            linea2.append(lt.getElement(ubicacionA,1))
            linea2.append(lt.getElement(ubicacionA,2))
            linea2.append(arco["vertexB"])
            ubicacionB=controller.dar_lat_long_nodo(arco["vertexB"])
            linea2.append(lt.getElement(ubicacionB,1))
            linea2.append(lt.getElement(ubicacionB,2))
            lobo=controller.dar_lobo_en_arco(arco)
            linea2.append(lobo)
            distancia=controller.dar_distancia(control["movimientos"], arco["vertexA"], arco["vertexB"])
            linea2.append(distancia)    
            
            tabla2.append(linea2)
            
        for i in range(lt.size(arcos)-2, lt.size(arcos)+1):
            linea2=[]
            arco=lt.getElement(arcos, i)
            linea2.append(arco["vertexA"])
            ubicacionA=controller.dar_lat_long_nodo(arco["vertexA"])
            linea2.append(lt.getElement(ubicacionA,1))
            linea2.append(lt.getElement(ubicacionA,2))
            linea2.append(arco["vertexB"])
            ubicacionB=controller.dar_lat_long_nodo(arco["vertexB"])
            linea2.append(lt.getElement(ubicacionB,1))
            linea2.append(lt.getElement(ubicacionB,2))
            lobo=controller.dar_lobo_en_arco(arco)
            linea2.append(lobo)
            distancia=controller.dar_distancia(control["movimientos"], arco["vertexA"], arco["vertexB"])
            linea2.append(distancia)    
            
            tabla2.append(linea2)
    
        
    print(tabulate(tabla2, headers=titulos2, tablefmt="fancy_grid", stralign="left", numalign="left"))
    print("\tDistancia total del recorrido:", round(float(datas[0][2])+float(info_origen["distancia"])+float(info_destino["distancia"]),3), "km")
                           
    
    
    print("\n---Detalles de los puntos en el camino---")
    print("Hay", lt.size(nodos),"vértices en el camino")
    print("\n\tPrimeros y últimos  3 vértices en el camino")

    titulos3=["ID del nodo", "location-long-aprox", "location-lat-aprox", "Identificadores en el nodo", "Cantidad de lobos en el nodo"]
    tabla3=[]
    
    if lt.size(nodos)<=6:
        for i in range(1,lt.size(nodos)+1):
            linea3=[]
            vertice=lt.getElement(nodos, i)
            linea3.append(vertice)
            ubicacion=controller.dar_lat_long_nodo(vertice)
            linea3.append(lt.getElement(ubicacion,1))
            linea3.append(lt.getElement(ubicacion,2))
            lobos=controller.dar_lobos_en_adyancencias(control, vertice)
            ids=[]
            for lobo in lt.iterator(lobos):
                ids.append(lobo)
            ids_str=", ".join(ids)
            linea3.append(ids_str)
            linea3.append(lt.size(lobos))
            tabla3.append(linea3)
            
    else:
        for i in range(1,4):
            linea3=[]
            vertice=lt.getElement(nodos, i)
            linea3.append(vertice)
            ubicacion=controller.dar_lat_long_nodo(vertice)
            linea3.append(lt.getElement(ubicacion,1))
            linea3.append(lt.getElement(ubicacion,2))
            lobos=controller.dar_lobos_en_adyancencias(control, vertice)
            ids=[]
            for lobo in lt.iterator(lobos):
                ids.append(lobo)
            ids_str=", ".join(ids)
            linea3.append(ids_str)
            linea3.append(lt.size(lobos))
            tabla3.append(linea3)
            
        for i in range(lt.size(nodos)-2,lt.size(nodos)+1):
            linea3=[]
            vertice=lt.getElement(nodos, i)
            linea3.append(vertice)
            ubicacion=controller.dar_lat_long_nodo(vertice)
            linea3.append(lt.getElement(ubicacion,1))
            linea3.append(lt.getElement(ubicacion,2))
            lobos=controller.dar_lobos_en_adyancencias(control, vertice)
            ids=[]
            for lobo in lt.iterator(lobos):
                ids.append(lobo)
            ids_str=", ".join(ids)
            linea3.append(ids_str)
            linea3.append(lt.size(lobos))
            tabla3.append(linea3)
        
    print(tabulate(tabla3, headers=titulos3, tablefmt="fancy_grid", stralign="left", numalign="left"))
    
    
    print("\nTiempo de ejecución [ms]:", datas[1])
    print("\n")

def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    fecha_inicial = input("\nIngrese la fecha inicial (%Y-%m-%d): ")
    fecha_final = input("\nIngrese la fecha final (%Y-%m-%d): ")
    sexo = input("\nIngrese sexo (f o m): ")
    datas = controller.req_6(control, fecha_inicial, fecha_final, sexo)
    
    print('\n---------------Req No. 6-------------------\n')
    info_mayor=datas[0][0]
    info_menor=datas[0][1] 
    
    mapa=datas[0][2]
    mapa.show_in_browser()
    
    print('---------------Parte 1-------------------')
    print("\tIndividuo que recorrió la mayor distancia:", info_mayor["id"])
    titulos1=["individual-id", "animal-taxon", "animal-life-stage", "animal-sex", "study-site", "travel-dist", "deployment-comments"]
    anchos1=[None,None,None,None,None,None,20]
    
    tabla11=[]
    linea11=[]
    linea11.append(info_mayor["id"])
    linea11.append(info_mayor["fila"]["animal-taxon"])
    linea11.append(info_mayor["fila"]["animal-life-stage"])
    linea11.append(info_mayor["fila"]["animal-sex"])
    linea11.append(info_mayor["fila"]["study-site"])
    linea11.append(info_mayor["distancia"])
    linea11.append(info_mayor["fila"]["deployment-comments"])
    tabla11.append(linea11)
    
    print(tabulate(tabla11, headers=titulos1, maxcolwidths=anchos1, tablefmt="fancy_grid", stralign="left", numalign="left"))
    
    print("\n---Detalles de la ruta más larga---")
    print("\t- Cantidad de nodos en la ruta:", info_mayor["nodos"])
    print("\t- Cantidad de arcos en la ruta:", info_mayor["arcos"])
    print("\t- Distancia total de la ruta:", info_mayor["distancia"], "km")
    
    titulos2=["node-id", "location-long-aprox", "location-lat-aprox", "individual-id", "individual-count"]
    
    tabla12=[]
    
    for punto in lt.iterator(info_mayor["ruta"]):
        linea12=[]
        linea12.append(punto)
        ubicacion=controller.dar_lat_long_nodo(punto)
        linea12.append(lt.getElement(ubicacion,1))
        linea12.append(lt.getElement(ubicacion,2))
        lobos=controller.dar_lobos_en_adyancencias(control, punto)
        ids=[]
        for lobo in lt.iterator(lobos):
            ids.append(lobo)
        ids_str=", ".join(ids)
        linea12.append(ids_str)
        linea12.append(lt.size(lobos))
        tabla12.append(linea12)
        
    print(tabulate(tabla12, headers=titulos2, tablefmt="fancy_grid", stralign="left", numalign="left"))
    

    
    print('\n---------------Parte 2-------------------')
    print("\tIndividuo que recorrió la menor distancia:", info_menor["id"])
    titulos1=["individual-id", "animal-taxon", "animal-life-stage", "animal-sex", "study-site", "travel-dist", "deployment-comments"]
    anchos1=[None,None,None,None,None,None,20]
    
    tabla21=[]
    linea21=[]
    linea21.append(info_menor["id"])
    linea21.append(info_menor["fila"]["animal-taxon"])
    linea21.append(info_menor["fila"]["animal-life-stage"])
    linea21.append(info_menor["fila"]["animal-sex"])
    linea21.append(info_menor["fila"]["study-site"])
    linea21.append(info_menor["distancia"])
    linea21.append(info_menor["fila"]["deployment-comments"])
    tabla21.append(linea21)
    
    print(tabulate(tabla21, headers=titulos1, maxcolwidths=anchos1, tablefmt="fancy_grid", stralign="left", numalign="left"))
    
    print("\n---Detalles de la ruta más larga---")
    print("\t- Cantidad de nodos en la ruta:", info_menor["nodos"])
    print("\t- Cantidad de arcos en la ruta:", info_menor["arcos"])
    print("\t- Distancia total de la ruta:", info_menor["distancia"], "km")
    
    titulos2=["node-id", "location-long-aprox", "location-lat-aprox", "individual-id", "individual-count"]
    
    tabla22=[]
    
    for punto in lt.iterator(info_menor["ruta"]):
        linea22=[]
        linea22.append(punto)
        ubicacion=controller.dar_lat_long_nodo(punto)
        linea22.append(lt.getElement(ubicacion,1))
        linea22.append(lt.getElement(ubicacion,2))
        lobos=controller.dar_lobos_en_adyancencias(control, punto)
        ids=[]
        for lobo in lt.iterator(lobos):
            ids.append(lobo)
        ids_str=", ".join(ids)
        linea22.append(ids_str)
        linea22.append(lt.size(lobos))
        tabla22.append(linea22)
        
    print(tabulate(tabla22, headers=titulos2, tablefmt="fancy_grid", stralign="left", numalign="left"))
    
    print("\nTiempo de ejecución [ms]:", datas[1])
    print("\n")
    



def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    fecha_inicial = input("\nIngrese la fecha inicial (%Y-%m-%d): ")
    fecha_final = input("\nIngrese la fecha final (%Y-%m-%d): ")
    temp_min = input("\nIngrese temperatura mínima: ")
    temp_max= input("\nIngrese temperatura máxima: ")
    datas = controller.req_7(control,fecha_inicial, fecha_final, temp_min, temp_max)
    
    
    print('\n---------------Req No. 7-------------------\n')
    
    cantidad = datas[0][0] 

    info = datas[0][1]
    
    orden = datas[0][2]
    info_ruta = datas[0][3]
    
    mapa=datas[0][4]
    mapa.show_in_browser() 

    print("\n  Hay " , cantidad , "componentes fuertemente conectados en el grafo") 
    print ("\n Los primeros y ultimos 3 componentes fuertemente conectados en el grafo son: ")

    titulos1= ["SCCID\n", "Nodos ID\n", "Tamaño\n", "min-lat\n" , "max-lat\n", "min-lon\n", "max-lon\n", "Cantidad\nlobos\n", "Información lobos"] 
    llaves1 = ["primeros_ultimos", "tamaño", "min_lat", "max_lat", "min_lon", "max_lon", "cantidad_lobos", "informacion_lobos" ] 
    anchos = [1, 15, 1, 1, 1, 1, 1, 1, None]
    tabla1=[]


    subtitulos1= ["individual-id", "animal-sex", "animal-life-\nstage", "study-site", "deployment-\ncomments"]
    subtitulos= ["individual-id", "animal-sex", "animal-life-stage", "study-site", "deployment-comments"]
    for dato in lt.iterator(orden): 
        fila=[] 
        fila.append(dato)
        value= mp.get(info, dato)["value"] 
        for llave in llaves1: 
            if llave== "primeros_ultimos":
                linea = []
                for nodo in lt.iterator(value["primeros_ultimos"]):
                    linea.append(nodo)
                if lt.size(value["primeros_ultimos"])>1:
                    fila_str=", ".join(linea)
                    fila.append(fila_str)
                else: 
                    fila.append(linea[0])
            elif llave== "informacion_lobos":
                subtabla=[]
                for lobo in lt.iterator(value["informacion_lobos"]):
                    sublinea= []
                    for subllave in subtitulos:
                        if subllave == "individual-id":
                            id= lobo["animal-id"]+ "_" + lobo["tag-id"]
                            sublinea.append(id)
                        else:
                            if lobo[subllave]== "":
                                sublinea.append("Unknown")
                            else:
                                sublinea.append(lobo[subllave])
                    subanchos=[4, 4, 4, 7, 7]
                    subtabla.append(sublinea)
                tabulada=tabulate(subtabla, headers= subtitulos1, tablefmt="fancy_grid", maxcolwidths=subanchos, stralign="left", numalign="left")
                fila.append(tabulada)        
            else:
                fila.append(value[llave])
            
        tabla1.append(fila)
    
    print(tabulate(tabla1, headers=titulos1, tablefmt="fancy_grid", maxcolwidths=anchos, stralign="left", numalign="left"))
    
    print("\n---Rutas más largas---")
    print ("\tRutas de los 3 primeros y últimos componentes fuertemente conectados en el grafo")
    
    tabla2=[]
    anchos2 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 22, 12]
    titulos2=["SCCIP", "SCC size", "min-lat", "max-lat", "min-lon", "max-lon", "LP distance [km]", "LP Node\ncount", "LP Edges\ncount", "LP Details", "LP indididual id"]
    
    llaves21 = ["tamaño", "min_lat", "max_lat", "min_lon", "max_lon"] 
    llaves22 = ["distancia", "cantidad_vertices", "cantidad_arcos", "primeros_ultimos" , "lobos" ]
    
    for dato in lt.iterator(orden):
        fila=[] 
        fila.append(dato)
        value= mp.get(info, dato)["value"]
        for llave in llaves21:
            fila.append(value[llave])
        
        value_ruta= mp.get(info_ruta, dato)["value"]

        
        for llave in llaves22:
            if llave == "primeros_ultimos" or llave == "lobos":
                linea=[]
                for nodo in lt.iterator(value_ruta[llave]):
                    linea.append(nodo)
                linea_str=", ".join(linea)
                fila.append(linea_str)
            else:
                fila.append(value_ruta[llave])
        tabla2.append(fila)
        
    print(tabulate(tabla2, headers=titulos2, tablefmt="fancy_grid", maxcolwidths=anchos2, stralign="left", numalign="left"))
   
    
    

def correr_pruebas(control):
    tabla=[]
    titulos=["Archivo","Carga de datos", "Req 1","Req 3", "Req 4", "Req 6","Req 7","Req 8"]
    
    
    for archivo in ["small.csv", '5pct.csv', '10pct.csv', '20pct.csv','30pct.csv','50pct.csv','80pct.csv', "large.csv"]:
            linea=[]
            linea.append(archivo)
            
            t0=controller.load_data(control, archivo)[2]
            linea.append(t0)
            
            t1=controller.req_1(control, "m111p862_57p449", "m111p908_57p427")[1]
            linea.append(t1)
            
            t3=controller.req_3(control)[1]
            linea.append(t3)
            
            t4=controller.req_4(control,{"location-long":"-111.911", "location-lat": "57.431"}, {"location-long":"-111.865", "location-lat": "57.435"})[1]
            linea.append(t4)
            
            t6=controller.req_6(control, "2013-02-16", "2013-03-23", "f")[1]
            linea.append(t6)
            
            t7=controller.req_7(control, "2012-11-28", "2013-01-31", "-17.3", "9.7")[1]
            linea.append(t7)
            
            tabla.append(linea)
            print(archivo, ":)")
            
    print(tabulate(tabla, headers=titulos, tablefmt="fancy_grid", maxcolwidths=10, stralign="left", numalign="left"))



# Se crea el controlador asociado a la vista


# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        try:
            if int(inputs) == 1:
                control = new_controller()
                data = load_data(control)
            elif int(inputs) == 2:
                print_req_1(control)

            elif int(inputs) == 3:
                print_req_3(control)

            elif int(inputs) == 4:
                print_req_4(control)

            elif int(inputs) == 5:
                print_req_6(control)

            elif int(inputs) == 6:
                print_req_7(control)
                
            elif int(inputs) == 0:
                working = False
                print("\nGracias por utilizar el programa")
            
            elif int(inputs) == 8:
                correr_pruebas(control)
                
            else:
                print("Opción errónea, vuelva a elegir.\n")
        except Exception as exp:
            print("ERR:", exp)
            traceback.print_exc()
    sys.exit(0)
