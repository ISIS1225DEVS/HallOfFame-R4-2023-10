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
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback
import time
import webbrowser

default_limit = 10000
sys.setrecursionlimit(default_limit*100)

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
    #Llamar la función del controlador donde se crean las estructuras de datos
    control = controller.new_controller()
    return control

def loadDataSteps():
    print("\n¿Qué archivos de datos desea cargar?")
    print("   BA-Grey-Wolf-tracks-utf8-[#]")
    print("   BA-Grey-Wolf-individuals-utf8-[#]")
    print("   [1] small.csv")
    print("   [2] 5%.csv")
    print("   [3] 10%.csv")
    print("   [4] 20%.csv")
    print("   [5] 30%.csv")
    print("   [6] 50%.csv")
    print("   [7] 80%.csv")
    print("   [8] large.csv\n")
    op = int(input())
    if op == 1:
        arch = "small.csv"
    elif op == 2:
        arch = "5pct.csv"
    elif op == 3:
        arch = "10pct.csv"
    elif op == 4:
        arch = "20pct.csv"
    elif op == 5:
        arch = "30pct.csv"
    elif op == 6:
        arch = "50pct.csv"
    elif op == 7:
        arch = "80pct.csv"
    else:
        arch = "large.csv"
    print("Usted eligió cargar el archivo" + arch)
    return ("BA-Grey-Wolf-tracks-utf8-" + arch)


def print_menu():
    print("\n{} Bienvenido Al Reto #4 del Grupo 1 {}\n".format("·"*15, "·"*15))
    print("» 1 « Elegir Tamaño de datos")
    print("» 2 « Cargar datos")
    print("» 3 « (REQ. 1) Planear una posible ruta entre dos puntos de encuentro")
    print("» 4 « (REQ. 2) Planear una ruta con menos paradas entre dos puntos de encuentro")
    print("» 5 « (REQ. 3) Reconocer los territorios habitados por distintas manadas")
    print("» 6 « (REQ. 4) Identificar el camino más corto entre dos puntos del hábitat")
    print("» 7 « (REQ. 5) Reconocer el corredor migratorio más extenso")
    print("» 8 « (REQ. 6) Identificar diferencias de movilidad entre tipos de miembros de la manada")
    print("» 9 « (REQ. 7) Identificar cambios en el territorio de las manadas según condiciones climáticas")
    print("» 0 « Salir ")


def load_data(control, filename):
    """
    Carga los datos
    """
    # Realizar la carga de datos
    x = float(time.perf_counter())
    catalog,eventos_analizados,lamax, lamin, lomax, lomin = controller.load_data(control, filename)
    catalog = control['model']
    numpe = 0
    events = 0
    arcos_unir = 0
    final_pedict = {}
    for pe in catalog['pedict']:
        n = len(catalog['pedict'][pe])
        if n != 1:
            numpe += 1
            arcos_unir += 2*n
            final_pedict[pe] = catalog['pedict'][pe]
        events += n
    catalog['pedict'] = final_pedict
    arcos_total = gr.numEdges(catalog['grafo_d'])
    arcos_movimiento = arcos_total - arcos_unir
    
    catalog = control['model']
    print("{:·^80s}".format("REPORTE DE LA CARGA DE DATOS"))
    print('· El total de lobos reconocidos en el estudio es: {}'.format(mp.size(catalog['map'])))
    print('· El total de eventos cargados durante el estudio es: {}'.format(eventos_analizados))
    print('\n· El total de puntos de encuentro reconocidos es: {}'.format(numpe))
    print('· El total de puntos de seguimiento reconocidos es: {}'.format(events))
    print('· El total de nodos en el digraph es: {}'.format(gr.numVertices(catalog['grafo_d'])))
    print('\n· El total de arcos creados para unir los nodos de encuentro y los puntos de seguimiento es: {}'.format(arcos_unir))
    print('· El total de arcos creados para representar el movimiento de los individuos es: {}'.format(arcos_movimiento))
    print('· El total de arcos en el digraph es: {}'.format(arcos_total))
    print('\n· El total de nodos en el graph es: {}'.format(gr.numVertices(catalog['grafo'])))
    print('· El total de arcos en el graph es: {}'.format(gr.numEdges(catalog['grafo'])))
    print('\n· Latitud mínima y máxima: {} y {}'.format(lamin,lamax))
    print('· Longitud mínima y máxima: {} y {}'.format(lomin,lomax))    
    print('\n· Los primeros cinco y últimos cinco nodos de la lista de adyacencia dentro del grafo dirijido son: ')
    vertices = gr.vertices(catalog['grafo_d'])
    vlist = []
    for vertice in lt.iterator(vertices):
        vlist += [vertice]
    vlist = vlist[:5] + vlist[-5:]
    ltab = []
    for vertice in vlist:
        dtab = {}
        dtab['Identificador'] = vertice
        coord = vertice.replace('p','.').replace('m','-').split('_')
        dtab['Geolocalizacón'] = '({},{})'.format(coord[1],coord[0])
        adj = gr.adjacents(catalog['grafo_d'],vertice)
        if len(vertice.split('_')) == 2:
            lad = []
            for ad in lt.iterator(adj):
                lad += ['_'.join(ad.split('_')[2:])]
            dtab['Lobos en el punto de encuentro / nodo de seguimiento'] = ', '.join(lad)
        else:
            dtab['Lobos en el punto de encuentro / nodo de seguimiento'] = '_'.join(vertice.split('_')[2:])
        dtab['Número de nodos adyacentes'] = lt.size(adj)
        ltab += [dtab]
    print(tabulate(ltab, headers="keys", tablefmt="grid", maxcolwidths=30, maxheadercolwidths=30))
    y = float(time.perf_counter())
    print('==⇒ El tiempo de ejecución es: {} s'.format(round(float(y-x),2)))

def print_req_1(control, identificador_origen, identificador_destino):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # Imprimir el resultado del requerimiento 1
    x = float(time.perf_counter())
    dist, total_pe, total_ps, lista_tab, mapa = controller.req_1(control, identificador_origen, identificador_destino)
    mapa.save("map1.html")
    print("La distancia total recorrida es: " + str(round(dist, 0)) + " km")
    print("El numero de puntos de encuentro en el camino son: " + str(total_pe))
    print("El numero de puntos de seguimiento en el camino son: " + str(total_ps))
    print("El numero total de puntos es: " + str(total_pe+total_ps))
    headers = ["location-long-aprox",
               "location-lat-aprox",
               "node-id",
               "individual-id",
               "individual-count",
               "edge-to",
               "edge-distance-km"]
    print("Los primeros 5 y los ultimos 5 nodos cargados son" )
    print(tabulate(lista_tab, headers, tablefmt="grid", maxcolwidths=14, maxheadercolwidths=12))
    y = float(time.perf_counter())
    print('==⇒ El tiempo de ejecución es: {} s'.format(round(float(y-x),2)))
    webbrowser.open("map1.html")    

def print_req_2(control, identificador_origen, identificador_destino):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # Imprimir el resultado del requerimiento 2
    x = float(time.perf_counter())
    dist, total_pe, total_ps, lista_tab, mapa = controller.req_2(control, identificador_origen, identificador_destino)
    mapa.save("map2.html")
    print("El numero de vertices reconocidos es: " + str(total_pe+total_ps))
    print("La distancia total recorrida es: " + str(round(dist, 4)) + " km")
    print("El numero de puntos de encuentro en el camino son: " + str(total_pe))
    print("El numero de puntos de seguimiento en el camino son: " + str(total_ps))
    headers = ["location-long-aprox",
               "location-lat-aprox",
               "node-id",
               "individual-id",
               "individual-count",
               "edge-to",
               "edge-distance-km"]
    print("Los primeros 5 y los ultimos 5 nodos cargados son" )
    print(tabulate(lista_tab, headers, tablefmt="grid", maxcolwidths=16, maxheadercolwidths=16))
    y = float(time.perf_counter())
    print('==⇒ El tiempo de ejecución es: {} s'.format(round(float(y-x),2)))
    webbrowser.open("map2.html")

def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # Imprimir el resultado del requerimiento 3
    x = float(time.perf_counter())
    tabla, cc, mapa = controller.req_3(control)
    mapa.save("map3.html")
    headers = ["SCCID",
               "Nodes ID's",
               "SCC size",
               "Min-lat",
               "Max-lat",
               "Min-lon",
               "Max-lon",
               "Wolf Count",
               "Wolf Details"]
    print("El numero de componentes conectados (manadas) son: " + str(cc))
    print(tabulate(tabla, headers, tablefmt="grid"))
    y = float(time.perf_counter())
    webbrowser.open("map3.html")
    print('==⇒ El tiempo de ejecución es: {} s'.format(round(float(y-x),2)))



def print_req_4(control, punto_origen, punto_destino):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    x = float(time.perf_counter())
    dist, total_pe, total_ps, lista_tab, mapa = controller.req_4(control, punto_origen, punto_destino)
    mapa.save("map4.html")
    print("La distancia total recorrida es: " + str(round(dist, 0)))
    print("El numero de puntos de encuentro en el camino son: " + str(total_pe))
    print("El numero de puntos de seguimiento en el camino son: " + str(total_ps))
    headers = ["location-long-aprox",
               "location-lat-aprox",
               "node-id",
               "individual-id",
               "individual-count",
               "edge-to",
               "edge-distance-km"]
    print("Los primeros 5 y los ultimos 5 nodos cargados son" )
    print(tabulate(lista_tab, headers, tablefmt="grid", maxcolwidths=14))
    y = float(time.perf_counter())
    print('==⇒ El tiempo de ejecución es: {} s'.format(round(float(y-x),2)))
    webbrowser.open("map4.html")


def print_req_5(control,o,d,m):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    x = float(time.perf_counter())
    r, mapa = controller.req_5(control,o,d,m)
    mapa.save("map5.html")
    print('\nHay {} posibles caminos desde el punto \'{}\'\n'.format(lt.size(r),o))
    if lt.size(r) != 0:
        print(tabulate([r['elements'][0]], headers="keys", tablefmt="grid", maxcolwidths=28, maxheadercolwidths=28))
    y = float(time.perf_counter())
    print('==⇒ El tiempo de ejecución es: {} s'.format(round(float(y-x),2)))
    webbrowser.open("map5.html")

def print_req_6(control,fi,ff,g):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    x = float(time.perf_counter())
    list, mapa, mapa2 = controller.req_6(control,fi,ff,g)
    mapa.save("mapa6.html")
    mapa2.save("mapa62.html")
    lma = list['elements'][0]
    lme = list['elements'][-1]
    print('·····PARTE 1·····')
    print('Lobo que recorrio la mayor distancia: {}'.format(lma['info']['individual-id']))
    print(tabulate([lma['info']],headers="keys", tablefmt="grid", maxcolwidths=28, maxheadercolwidths=28))
    print('El camino mas largo tiene {} nodos y {} arcos. La distancia máxima entre el primer y ultimo nodo es: {}.'.format(lma['path_details']['num_nodos'],lma['path_details']['num_arcos'],lma['path_details']['max_dist']))
    if len(lma['path_details']['path']) > 6:
        print('Los primeros 3 y ultimos 3 puntos de los {} son: '.format(len(lma['path_details']['path'])))
        newlist = lma['path_details']['path'][:3] + lma['path_details']['path'][-3:]
        print(tabulate(newlist,headers="keys", tablefmt="grid", maxcolwidths=28, maxheadercolwidths=28))
    else:
        print('Los {} puntos son: '.format(len(lma['path_details']['path'])))
        print(tabulate(lma['path_details']['path'],headers="keys", tablefmt="grid", maxcolwidths=28, maxheadercolwidths=28))
    print('·····PARTE 2·····') 
    print('Lobo que recorrio la menor distancia: {}'.format(lme['info']['individual-id']))
    print(tabulate([lme['info']],headers="keys", tablefmt="grid", maxcolwidths=28, maxheadercolwidths=28))
    print('El camino mas largo tiene {} nodos y {} arcos. La distancia máxima entre el primer y ultimo nodo es: {}.'.format(lme['path_details']['num_nodos'],lme['path_details']['num_arcos'],lme['path_details']['max_dist']))
    if len(lme['path_details']['path']) > 6:
        print('Los primeros 3 y ultimos 3 puntos de los {} son: '.format(len(lme['path_details']['path'])))
        newlist = lme['path_details']['path'][:3] + lme['path_details']['path'][-3:]
        print(tabulate(newlist,headers="keys", tablefmt="grid", maxcolwidths=28, maxheadercolwidths=28))
    else:
        print('Los {} puntos son: '.format(len(lme['path_details']['path'])))
        print(tabulate(lme['path_details']['path'],headers="keys", tablefmt="grid", maxcolwidths=28, maxheadercolwidths=28))
    y = float(time.perf_counter())
    print('==⇒ El tiempo de ejecución es: {} s'.format(round(float(y-x),2)))
        
    webbrowser.open("mapa6.html")
    webbrowser.open("mapa62.html")

def print_req_7(control, fi, ff, ti, tf):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    x = float(time.perf_counter())
    tabla, cc, mapa = controller.req_7(control, fi, ff, ti, tf)
    mapa.save("map7.html")
    headers = ["SCCID",
               "Nodes ID's",
               "SCC size",
               "Min-lat",
               "Max-lat",
               "Min-lon",
               "Max-lon",
               "Wolf Count",
               "Wolf Details"]
    print("El numero de componentes conectados (manadas) son: " + str(cc))
    print(tabulate(tabla, headers, tablefmt="grid"))
    y = float(time.perf_counter())
    webbrowser.open("map7.html")
    print('==⇒ El tiempo de ejecución es: {} s'.format(round(float(y-x),2)))


# Se crea el controlador asociado a la vista
control = new_controller()

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
                filename = loadDataSteps()
                
            elif int(inputs) == 2:
                print("Cargando información de los archivos ....\n")
                data = load_data(control, filename)
                
            elif int(inputs) == 3:
                ident_origen = input("Identificador de origen: ")
                ident_destino = input("Identificador de destino: ")
                print_req_1(control, ident_origen, ident_destino)

            elif int(inputs) == 4:
                ident_origen = input("Identificador de origen: ")
                ident_destino = input("Identificador de destino: ")
                print_req_2(control, ident_origen, ident_destino)

            elif int(inputs) == 5:
                print_req_3(control)
                
            elif int(inputs) == 6:
                punto_origen = input("Punto de origen: ")
                punto_destino = input("Punto de destino: ")
                print_req_4(control, punto_origen, punto_destino)
            
            elif int(inputs) == 7:
                o = input('Identificador del punto de encuentro de origen: ')
                d = float(input('Distancia que puede recorrer el guardabosques desde el punto de origen [km]: '))
                m = int(input('El número mínimo de puntos de encuentros que el guardabosques desea inspeccionar: '))
                print_req_5(control,o,d,m)

            elif int(inputs) == 8:
                print("Porfavor ingrese la fecha inicial: ")
                fi = input("")
                print("Porfavor ingrese la fecha final: ")
                ff = input("")
                print("Porfavor ingrese el genero [f/m]: ")
                g = input("")
                print_req_6(control,fi,ff,g)

            elif int(inputs) == 9:
                print("Porfavor ingrese la fecha inicial: ")
                fi = input("")
                print("Porfavor ingrese la fecha final: ")
                ff = input("")
                print("Porfavor ingrese la temperatura incial: ")
                ti = input("")
                print("Porfavor ingrese la temperatura final: ")
                tf = input("")
                print_req_7(control, fi, ff, ti, tf)

            elif int(inputs) == 0:
                working = False
                print("\nGracias por utilizar el programa")
                
            else:
                print("Opción errónea, vuelva a elegir.\n")
        except Exception as exp:
            print("ERR:", exp)
            traceback.print_exc()
    sys.exit(0)
