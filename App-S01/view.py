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
from DISClib.ADT import graph as gr
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback
import threading
import folium

default_limit = 10000
sys.setrecursionlimit(default_limit*1000)



"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller(data_type):
    """
        Se crea una instancia del controlador
    """
    control = controller.new_controller(data_type)
    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Planear una posible ruta entre dos puntos de encuentro ")
    print("3- Planear una ruta con menos paradas entre dos puntos de encuentro")
    print("4- Reconocer los territorios habitados por distintas manadas")
    print("5- Identificar el camino más corto entre dos puntos del hábitat")
    print("6- Reconocer el corredor migratorio más extenso")
    print("7- Identificar diferencias en los corredores migratorios según el tipo de individuo")
    print("8- Identificar cambios en el territorio de las manadas según condiciones climáticas ")
    print("9- Graficar requerimiento 1")
    print("10- Graficar requerimiento 2")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    filename_tabla_1 = "BA-Grey-Wolf-tracks-utf8-small.csv"
    filename_tabla_2 = "BA-Grey-Wolf-individuals-utf8-small.csv"
    data, arcos_encuentro , arcos_seguimiento= controller.load_data(control, filename_tabla_1, filename_tabla_2)
    return data,arcos_encuentro , arcos_seguimiento

def load_carga(control):

    grafo = control["model"]["grafoDirigido"]
    mapa_encuentro = control['model']['encuentro']
    vertices = gr.vertices(grafo)
    sublist1 = lt.subList(vertices, 1, 5)
    sublist2 = lt.subList(vertices, lt.size(vertices)-5, 5)
    tabla_grande = []

    for node_id in lt.iterator(sublist1):
        tabla_puntos = []
        tabla = []
        adyacent_nodes = lt.size(gr.adjacents(grafo, node_id))
        entry = mp.get(mapa_encuentro, node_id)
        if entry is not None:
            info = me.getValue(entry)
            for element in lt.iterator(info):
                element = element.split("_")
                if len(element) == 3:
                    element = element[2]
                elif len(element) == 4:
                    element = element[2] + "_" + element[3]

                elif len(element) == 5:
                    element = element[2] + "_" + element[3] + "_" + element[4]
        
                tabla_puntos.append(element)

        else:
            element = node_id.split("_")
            if len(element) == 3:
                    element = element[2]
            elif len(element) == 4:
                    element = element[2] + "_" + element[3]
            elif len(element) == 5:
                    element = element[2] + "_" + element[3] + "_" + element[4]
        
            tabla_puntos.append(element)

        posicion = node_id.split("_")
        if 'm' in posicion[0]:
                longitud = posicion[0].replace("m", "-")
        if 'p' in longitud:
                longitud = longitud.replace("p", ".")
        
        if 'p' in posicion[1]:
                latitud = posicion[1].replace("p", ".")
        if 'm' in latitud:
                latitud = latitud.replace("m", "-")
            
        tabla = [longitud, latitud, node_id, tabla_puntos, adyacent_nodes]

        tabla_grande.append(tabla)


    for node_id in lt.iterator(sublist2):
        tabla_puntos = []
        tabla = []
        adyacent_nodes = lt.size(gr.adjacents(grafo, node_id))
        entry = mp.get(mapa_encuentro, node_id)
        if entry is not None:
            info = me.getValue(entry)
            for element in lt.iterator(info):
                element = element.split("_")
                if len(element) == 3:
                    element = element[2]
                elif len(element) == 4:
                    element = element[2] + "_" + element[3]
                elif len(element) == 5:
                    element = element[2] + "_" + element[3] + "_" + element[4]
        
                tabla_puntos.append(element)

        else:
            element = node_id.split("_")
            if len(element) == 3:
                    element = element[2]
            elif len(element) == 4:
                    element = element[2] + "_" + element[3]

            elif len(element) == 5:
                    element = element[2] + "_" + element[3] + "_" + element[4]
        
            tabla_puntos.append(element)

        posicion = node_id.split("_")
        if 'm' in posicion[0]:
                longitud = posicion[0].replace("m", "-")
        if 'p' in longitud:
                longitud = longitud.replace("p", ".")
        
        if 'p' in posicion[1]:
                latitud = posicion[1].replace("p", ".")
        if 'm' in latitud:
                latitud = latitud.replace("m", "-")
            
        tabla = [longitud, latitud, node_id, tabla_puntos, adyacent_nodes]

        tabla_grande.append(tabla)

    print(tabulate(tabla_grande, headers=["location-long-aprox", 
                                          "location-lat-aprox", "node_id", 
                                          "individual_id", "adjected_nodes"], 
                                          tablefmt="fancy_grid",maxcolwidths=28, maxheadercolwidths=20,
                                          numalign="right"), "\n")
    

def print_req_1(control, initial, destination, modo):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    print("====================== Req No. 1 Answer ======================")
    headers = ["location-long-aprox", 
                "location-lat-aprox", 
                "node-id", 
                "individual-id", 
                "individual-count",
                "edge-to",
                "edge-distance-km"]
    info, t = controller.req_1(control, initial, destination, modo)
    if info == None:
        print("No existe camino entre " + initial + " y " + destination)
    else:
        path = info[0] 
        nG = info[1] 
        nT = info[2] 
        w = info[3] 
        size = lt.size(path)
        
        print("Total of nodes in the path:", size)
        print("Total of gathering points in the path:", nG)
        print("Total of tracking points in the path:", nT)
        print("Total distance in the path:", w, "km")
        print("\nFirst 5 & Last 5 nodes loaded in the DFS path are:")
        table = []
        
        if size > 10:
            first = lt.subList(path, 1, 6)
            last = lt.subList(path, size - 4, 5)
            first5 = controller.generateListPath(first, control, True)
            last5 = controller.generateListPath(last, control)
            for felement in first5:
                table.append(felement)
            for lelement in last5:
                table.append(lelement)
        else:
            table = controller.generateListPath(path, control)
            
        print(tabulate(table, 
                       headers, 
                       tablefmt="fancy_grid",
                       maxcolwidths=28, 
                       maxheadercolwidths=20,
                       numalign="right"), "\n")
        
    print(t)


def print_req_2(control, initial, destination):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    print("====================== Req No. 2 Answer ======================")
    headers = ["location-long-aprox", 
                "location-lat-aprox", 
                "node-id", 
                "individual-id", 
                "individual-count",
                "edge-to",
                "edge-distance-km"]
    info, t = controller.req_2(control, initial, destination)
    if info == None:
        print("No existe camino entre " + initial + " y " + destination)
    else:
        path = info[0] 
        nG = info[1] 
        nT = info[2] 
        w = info[3] 
        size = lt.size(path)
        
        print("Total of nodes in the path:", size)
        print("Total of gathering points in the path:", nG)
        print("Total of tracking points in the path:", nT)
        print("Total distance in the path:", w, "km")
        print("\nFirst 5 & Last 5 nodes loaded in the BFS path are:")
        table = []
        
        if size > 10:
            first = lt.subList(path, 1, 6)
            last = lt.subList(path, size - 4, 5)
            first5 = controller.generateListPath(first, control, True)
            last5 = controller.generateListPath(last, control)
            table = first5 + last5
        else:
            table = controller.generateListPath(path, control)
            
        print(tabulate(table, 
                       headers, 
                       tablefmt="fancy_grid",
                       maxcolwidths=28, 
                       maxheadercolwidths=20,
                       numalign="right"), "\n")
        
    print(t)


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control, origen_lon, origen_lat, destino_lon, destino_lat):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    porigen, pdestino, dissource, distgt, trips_edges, nodes, distTo, first_3, last_3, t = controller.req_4(control, origen_lon, origen_lat, 
                                                                   destino_lon, destino_lat)
    
    print('++ Finding the nearest gathring points to src and tgt locations ++\n')
    print('The nearest gathering point to the source location is: ' + porigen)
    print('The nearest gathering point to the target location is: ' + pdestino)

    print("\n")
    print("------------------- Req No.4 Answer ---------------------\n")
    print("+++ Source gathering point +++")
    print("             Distance from the source point: " + str(dissource) + "[km]")

    lon1, lat1 = controller.noFormat(porigen)
    lon2, lat2 = controller.noFormat(pdestino)

    mapa_encuentro = control['model']['encuentro']
    entry = mp.get(mapa_encuentro, porigen)
    tabla_puntos = []

    if entry is not None:
        info = me.getValue(entry)
        for element in lt.iterator(info):
            element = element.split("_")
            if len(element) == 3:
                element = element[2]
            elif len(element) == 4:
                element = element[2] + "_" + element[3]
            elif len(element) == 5:
                element = element[2] + "_" + element[3] + "_" + element[4]

            tabla_puntos.append(element)

    tabla_grande = []
    tabla = [porigen, lon1, lat1, tabla_puntos]
    tabla_grande.append(tabla)
    print(tabulate(tabla_grande, headers=["node_id", "location-long-aprox", 'location-lat-aprox', "individual_id"],
                     tablefmt="fancy_grid", maxcolwidths=14, maxheadercolwidths=14, numalign="right"), "\n")
    
    print("\n")
    print("+++ Target gathering point +++")
    print("             Distance from the target point: " + str(distgt) + "[km]")

    entry = mp.get(mapa_encuentro, pdestino)
    tabla_puntos = []

    if entry is not None:
        info = me.getValue(entry)
        for element in lt.iterator(info):
            element = element.split("_")
            if len(element) == 3:
                element = element[2]
            elif len(element) == 4:
                element = element[2] + "_" + element[3]
            elif len(element) == 5:
                element = element[2] + "_" + element[3] + "_" + element[4]
        
            tabla_puntos.append(element)

    tabla = []
    tabla = [pdestino, lon2, lat2, tabla_puntos]
    tabla_grande = []
    tabla_grande.append(tabla)
    print(tabulate(tabla_grande, headers=["node_id", "location-long-aprox", 'location-lat-aprox', "individual_id"],
                  tablefmt="fancy_grid", maxcolwidths=14, maxheadercolwidths=14, numalign="right"), "\n")
    

    print("\n")
    if trips_edges is not None:
        print("++++++++ Wolf route details ++++++++")
        print(" - Number of nodes (gathering and tracking points): " + str(nodes))
        print(" - Number of trips (edges): " + str(trips_edges))
        print(" - Total distance from source to target: " + str(distTo) + "[km]")

        print("\n")
        print("----- Route details -----")
        print("       There are " + str(trips_edges) + " edges in the route")
        print("       The first 3  and last 3 in range area are:")
        print("       - Distance from source location with LON: " + lon1 + " and LAT: " + lat1 + " to the gathering point " + porigen + " is: " + str(dissource) +  " [km]")
    
        first = None
        table = []

        for element in lt.iterator(first_3):
            if first == None:
                individual = element['vertexB'].split("_")
                if len(element) >= 3:
                    for i in range(2, len(individual)):
                        if i == 2:
                            individual_new = individual[2]
                        else:
                            individual_new = individual_new + "_" + individual[i]
                    
                    first = 'Ya se encontro el id'
                
            lonA, latA = controller.noFormat(element['vertexA'])
            lonB, latB = controller.noFormat(element['vertexB'])
            row = [element['vertexA'], lonA, latA, element['vertexB'], lonB, latB, individual_new, element['weight']]

            
            table.append(row)

        for element in lt.iterator(last_3):
            if first == None:
                individual = element['vertexB'].split("_")
                if len(element) >= 3:
                    for i in range(2, len(individual)):
                        if i == 2:
                            individual_new = individual[2]
                        else:
                            individual_new = individual_new + "_" + individual[i]
                    
                    first = 'Ya se encontro el id'
                
            lonA, latA = controller.noFormat(element['vertexA'])
            lonB, latB = controller.noFormat(element['vertexB'])
            row = [element['vertexA'], lonA, latA, element['vertexB'], lonB, latB, individual_new, element['weight']]

            
            table.append(row)

        headers = ['src-node-id', 'src-location-long-aprox', 'src-location-lat-aprox', 'tgt-node-id', 
                'tgt-location-long-aprox', 'tgt-location-lat-aprox', 'individual_id', 'distance - km']

        print(tabulate(table, headers=headers, tablefmt="fancy_grid", maxcolwidths=14, maxheadercolwidths=14, numalign="right"), "\n")
        print("       - Distance from target location with LON: " + lon2 + " and LAT: " + lat2 + " to the gathering point " + pdestino + " is: " + str(distgt) +  " [km]")
        total = distTo + dissource + distgt
        print("       TOTAL DISTANCE: " + str(total) +  "[km]")

        print("\n")
        print("----- Gathering Points details -----")
        print("There are " + str(nodes) + " gathering points in the route")
        print("The first 3 and last 3 gathering points are:")

        table = []

        for element in lt.iterator(first_3):
            vertex = element['vertexA']
            lonA, latA = controller.noFormat(vertex)

            entry = mp.get(mapa_encuentro, vertex)
            if entry is not None:
                tabla_puntos = []
                info = me.getValue(entry)
                for element in lt.iterator(info):
                    element = element.split("_")
                    if len(element) == 3:
                        element = element[2]
                    elif len(element) == 4:
                        element = element[2] + "_" + element[3]
                    elif len(element) == 5:
                        element = element[2] + "_" + element[3] + "_" + element[4]
            
                    tabla_puntos.append(element)

                row = [vertex, lonA, latA, tabla_puntos, len(tabla_puntos)]

            else:
                element = vertex.split("_")
                if len(element) >= 3:
                    for i in range(2, len(individual)):
                        if i == 2:
                            individual_new = individual[2]
                        else:
                            individual_new = individual_new + "_" + individual[i]
                row = [vertex, lonA, latA, individual_new, 1]

            table.append(row)

        for element in lt.iterator(last_3):
            vertex = element['vertexB']
            lonA, latA = controller.noFormat(vertex)

            entry = mp.get(mapa_encuentro, vertex)
            if entry is not None:
                tabla_puntos = []
                info = me.getValue(entry)
                for element in lt.iterator(info):
                    element = element.split("_")
                    if len(element) == 3:
                        element = element[2]
                    elif len(element) == 4:
                        element = element[2] + "_" + element[3]
                    elif len(element) == 5:
                        element = element[2] + "_" + element[3] + "_" + element[4]
            
                    tabla_puntos.append(element)

                row = [vertex, lonA, latA, tabla_puntos, len(tabla_puntos)]

            else:
                element = vertex.split("_")
                if len(element) >= 3:
                    for i in range(2, len(individual)):
                        if i == 2:
                            individual_new = individual[2]
                        else:
                            individual_new = individual_new + "_" + individual[i]
                row = [vertex, lonA, latA, individual_new, 1]

            table.append(row)
        
        print(tabulate(table, headers=["node_id", "location-long-aprox", 'location-lat-aprox', "individual_id", "individual-count"],
                        tablefmt="fancy_grid", maxcolwidths=14, maxheadercolwidths=14, numalign="right"), "\n")
    else:
        print('No existe camino entre ' + origen_lon + ' y ' + destino_lon)

    print(t)
    

def print_req_5(control, minGathering, maxdistance, origin):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    print(controller.req_5(control, minGathering, maxdistance, origin))


def print_req_6(control, fecha_inicial, fecha_final, sex):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6

    id_menor, distancia_menor, nodos_menor, arcos_menor, first_3_menor, last_3_menor, id_mayor, distancia_mayor, nodos_mayor, arcos_mayor, first_3_mayor, last_3_mayor, contador,t1,t2, t = controller.req_6(control, fecha_inicial, fecha_final, sex)

    mapa_wolfs = control['model']['wolfs']
    print("\n")
    print("------------------------- Important data -------------------------\n")
    print("                         - Total of unique individuals: " + str(contador))
    
    print("\n")
    print("========================= Req No.6 Answer ===========================")
    print("Details for the longest and closest traveling wolf")
    print("\n")
    print("------------------------- Part 1-------------------------\n")
    print("The longest traveling wolf is: ")
    print("              - Individual ID: " + id_mayor)

    entry = mp.get(mapa_wolfs, id_mayor)
    wolfs_info = me.getValue(entry)
    info = wolfs_info['info']

    headers = ['individual-id', 'animal-taxon', 'animal-life-stage', 'animal-sex',
               'study-site', 'travel-dist', 'deployment-comments']
    
    info = info['elements'][0]

    tabla = [id_mayor, info['animal-taxon'], info['animal-life-stage'], info['animal-sex'],
             info['study-site'], t1, info['deployment-comments']]
    
    tabla_grande = []
    tabla_grande.append(tabla)

    print(tabulate(tabla_grande, headers=headers, tablefmt="fancy_grid", maxcolwidths=14, maxheadercolwidths=14, numalign="right"), "\n")
    print("The longest path for the wolf " + id_mayor + " has:")
    print("              - Node count: " + str(nodos_mayor))
    print("              - Edge count: " + str(arcos_mayor))
    print("              - TOTAL DISTANCE: " + str(distancia_mayor) + "[km]")

    print("\n")
    print("----- Longest path details -----")
    print("       There are " + str(arcos_mayor) + " edges in the route")
    print("       The first 3  and last 3 in range are:")

    if last_3_mayor is not None:
        tabla_grande = []
        for ps in lt.iterator(first_3_mayor):
            lon1, lat1 = controller.noFormat(ps)
            tabla = []
            tabla = [ps, lon1, lat1, id_mayor, '1']
            tabla_grande.append(tabla)

        for ps in lt.iterator(last_3_mayor):
            lon1, lat1 = controller.noFormat(ps)
            tabla = []
            tabla = [ps, lon1, lat1, id_mayor, '1']
            tabla_grande.append(tabla)
    
    else:
        tabla_grande = []
        for ps in lt.iterator(first_3_mayor):
            lon1, lat1 = controller.noFormat(ps)
            tabla = []
            tabla = [ps, lon1, lat1, id_mayor, '1']
            tabla_grande.append(tabla)

    print(tabulate(tabla_grande, headers=["node_id", "location-long-aprox", 'location-lat-aprox', "individual_id", "individual-count"],
                     tablefmt="fancy_grid", maxcolwidths=14, maxheadercolwidths=14, numalign="right"), "\n")
        
    print("------------------------- Part 2-------------------------\n")

    print("The closest traveling wolf is: " + id_menor)
    print("              - Individual ID: " + id_menor)

    entry = mp.get(mapa_wolfs, id_menor)
    wolfs_info = me.getValue(entry)
    info = wolfs_info['info']
    
    info = info['elements'][0]

    tabla = [id_menor, info['animal-taxon'], info['animal-life-stage'], info['animal-sex'],
             info['study-site'], t2, info['deployment-comments']]
    
    tabla_grande = []
    tabla_grande.append(tabla)

    print(tabulate(tabla_grande, headers=headers, tablefmt="fancy_grid", maxcolwidths=14, maxheadercolwidths=14, numalign="right"), "\n")
    print("The longest path for the wolf " + id_menor + " has:")
    print("              - Node count: " + str(nodos_menor))
    print("              - Edge count: " + str(arcos_menor))
    print("              - TOTAL DISTANCE: " + str(distancia_menor) + "[km]")

    print("\n")
    print("----- Shortest path details -----")
    print("       There are " + str(arcos_menor) + " edges in the route")
    print("       The first 3  and last 3 in range are:")

    if last_3_menor is not None:
        tabla_grande = []
        for ps in lt.iterator(first_3_menor):
            lon1, lat1 = controller.noFormat(ps)
            tabla = []
            tabla = [ps, lon1, lat1, id_mayor, '1']
            tabla_grande.append(tabla)

        for ps in lt.iterator(last_3_menor):
            lon1, lat1 = controller.noFormat(ps)
            tabla = []
            tabla = [ps, lon1, lat1, id_mayor, '1']
            tabla_grande.append(tabla)
    
    else:
        tabla_grande = []
        for ps in lt.iterator(first_3_menor):
            lon1, lat1 = controller.noFormat(ps)
            tabla = []
            tabla = [ps, lon1, lat1, id_mayor, '1']
            tabla_grande.append(tabla)

    print(tabulate(tabla_grande, headers=["node_id", "location-long-aprox", 'location-lat-aprox', "individual_id", "individual-count"],
                     tablefmt="fancy_grid", maxcolwidths=14, maxheadercolwidths=14, numalign="right"), "\n")
        
    print(t)

def print_req_7(control, lowtime, hightime, lowtemp, hightemp):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    ksrj, cmpnnts, lngst = controller.req_7(control, lowtime, hightime, lowtemp, hightemp)
    print("========================= Req No.7 Answer ===========================")
    headers1 = ["SCCID", 
                "Disp Node IDs", 
                "SSC size", 
                "min-lat", 
                "max-lat",
                "min-lon",
                "max-lon",
                "W-Count",
                "Wolf Details"]
    headers2 = ["SCCID", 
                "SSC size", 
                "min-lat", 
                "max-lat",
                "min-lon",
                "max-lon",
                "LP Node count",
                "LP Edges count",
                "LP distance [km]",
                "LP Disp details"]
    print("There are", ksrj["components"], "Strongly Connected Components (SCC) in the graph")
    print("++ The SCC details are: ++")
    print("     There are", ksrj["components"], "SCC in the graph")
    print("     The first 3 and last 3 in the range are:")
    table1 = []
    size1 = lt.size(cmpnnts)
    if size1 > 6:
        firstC = lt.subList(cmpnnts, 1, 3)
        lastC = lt.subList(cmpnnts, lt.size(cmpnnts) - 2, 3)
        firstList, wolflist1 = controller.generateListSCC(firstC, control)
        lastList, wolflist2 = controller.generateListSCC(lastC, control)
        table1 = firstList + lastList
    else:
        table1 = controller.generateListSCC(cmpnnts, control)
    wolflist = wolflist1 + wolflist2
    print("\n")
    print(tabulate(table1, 
                       headers1, 
                       tablefmt="grid",maxcolwidths=[4,20,4,4,4,4,4,4,None], numalign="right"), "\n")
    
    print("++ The Longest Paths (LP) possible in the SCC are: ++")
    print("     There are", ksrj["components"], "SCC in the graph")
    print("     The first 3 and last 3 in the range are:")
    table2 = []
    size2 = lt.size(lngst)
    if size2 > 6:
        firstC = lt.subList(lngst, 1, 3)
        lastC = lt.subList(lngst, lt.size(lngst) - 4, 3)
        firstList = controller.createListLongest(firstC)
        lastList = controller.createListLongest(lastC)
        table2 = firstList + lastList
    else:
        table2 = controller.createListLongest(lngst)
    print(tabulate(table2, 
                       headers2, 
                       tablefmt="fancy_grid",
                       maxcolwidths=28, 
                       maxheadercolwidths=20,
                       numalign="right"), "\n")


def print_req_8_1(control, initial, destination, modo):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    mapa = controller.req_8_1(control, initial, destination, modo)
    mapa.show_in_browser()

def print_req_8_2(control, initial, destination):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    mapa = controller.req_8_2(control, initial, destination)
    mapa.show_in_browser()


# Se crea el controlador asociado a la vista
control = new_controller(data_type = "CHAINING")

# main del reto
#if __name__ == "__main__":


if __name__ == "__main__":
    working = True
    #ciclo del menu
    data = None
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        try:
            if int(inputs) == 1:
                print("Cargando información de los archivos ....\n")
                data, arcos_encuentro, arcos_seguimiento = load_data(control)
                latitudes, longitudes = controller.organizarL(data)
                minlat = lt.firstElement(latitudes)
                minlong = lt.firstElement(longitudes)
                maxlat = lt.lastElement(latitudes)
                maxlong = lt.lastElement(longitudes)
                puntos_encuentro = lt.size(data['model']['lista_encuentros'])
                puntos_seguimiento = lt.size(data['model']['lista_seguimientos'])
                number_wolfs, wolfs_with_data, events = controller.wolfs_size(data)

                print("-----------------------------------------")
                print("WOLF TRACKING AND GATHERING DATA")
                print("-----------------------------------------")

                print("------Wold and event features------")
                print("Number of wolfs", number_wolfs)
                print("Number of wolfs with data", wolfs_with_data)
                print("Number of tracking events", events)

                print("\n")
                print('------Nodes features------')
                print("Number of gathering points", puntos_encuentro)
                print("Number of tracking points", puntos_seguimiento)
                print("Number of identified points", puntos_encuentro + puntos_seguimiento)

                print("\n")
                print('------Edges features------')
                print("Number of gathering edges", arcos_encuentro)
                print("Number of tracking edges", arcos_seguimiento)
                print("Number of identified edges", arcos_encuentro + arcos_seguimiento)

                print("\n")
                print("+++++ WOLF TRACKING AND GATHERING DIGRAPH +++++")
                print('Total number of nodes', puntos_encuentro + puntos_seguimiento)
                print('Total number of edges', arcos_encuentro + arcos_seguimiento)

                print("\n")
                print("----- Graph Area -----")
                print("Minimum and maximum latitude: " + str(minlat) + " and " + str(maxlat))
                print("Minimun and maximum longitude: " + str(minlong) + " and " + str(maxlong))
                
                print("\n")
                load_carga(data)


            elif int(inputs) == 2:
                initial = input("Start Gathering Point: ")
                destination = input("End Gathering Point: ")
                modo = input("Ingrese el modo de búsqueda (DFS/BFS): ")
                print_req_1(control, initial, destination, modo)

            elif int(inputs) == 3:
                initial = input("Start Gathering Point: ")
                destination = input("End Gathering Point: ")
                print_req_2(control, initial, destination)

            elif int(inputs) == 4:
                print_req_3(control)

            elif int(inputs) == 5:
                print('-------------------------Req No.4 Inputs-------------------------\n')
                origen_lon = input("Ingrese la longitud del punto de origen: ")
                origen_lat = input("Ingrese la latitud del punto de origen: ")
                destino_lon = input("Ingrese la longitud del punto de destino:: ")
                destino_lat = input("Ingrese la latitud del punto de destino: ")
                print_req_4(control, origen_lon, origen_lat, destino_lon, destino_lat)

            elif int(inputs) == 6:
                minGathering = input("Min of Gathering Points to visit: ")
                maxdistance = float(input("Max roundtrip traveling distance [km]: ")) / 2
                origin = input("Origin gathering point: ")
                print_req_5(control, minGathering, maxdistance, origin)

            elif int(inputs) == 7:
                print('-------------------------Req No.6 Inputs-------------------------\n')
                fecha_inicial = input("Ingrese la fecha inicial (YYYY-MM-DD H:M): ")
                fecha_final = input("Ingrese la fecha final (YYYY-MM-DD H:M): ")
                sex = input("Ingrese el sexo del lobo (m/f): ")
                print_req_6(control, fecha_inicial, fecha_final, sex)

            elif int(inputs) == 8:
                lowtime = '2012-11-28'
                hightime = '2014-05-17'
                lowtemp = -17.300
                hightemp = 9.700
                # lowtime = input(" - Start Date(YYYY-MM-DD): ")
                # hightime = input(" - End Date(YYYY-MM-DD): ")
                # lowtemp = input(" - Low Temperature: ")
                # hightemp = input(" - High Temperature: ")
                print_req_7(control, lowtime, hightime, lowtemp, hightemp)

            elif int(inputs) == 9:
                initial = input("Start Gathering Point: ")
                destination = input("End Gathering Point: ")
                modo = input("Ingrese el modo de búsqueda (DFS/BFS): ")
                print_req_8_1(control, initial, destination, modo)

            elif int(inputs) == 10:
                initial = input("Start Gathering Point: ")
                destination = input("End Gathering Point: ")
                print_req_8_2(control, initial, destination)

            elif int(inputs) == 0:
                working = False
                print("\nGracias por utilizar el programa")
                
            else:
                print("Opción errónea, vuelva a elegir.\n")
        except Exception as exp:
            print("ERR:", exp)
            traceback.print_exc()
    sys.exit(0)


