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
from DISClib.ADT import graph as gr

sys.setrecursionlimit(2 ** 20)
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
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    return controller.new_controller()


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Planear una posible ruta entre dos puntos de encuentro (1)")
    print("3- Planear una ruta con menos paradas entre dos puntos de encuentro (2)")
    print("4- Reconocer los territorios habitados por distintas manadas (3)")
    print("5- Identificar el camino más corto entre dos puntos del hábitat (4)")
    print("6- Reconocer el corredor migratorio más extenso (5)")
    print("7- Identificar diferencias en los corredores migratorios según el tipo de individuo (6)")
    print("8- Identificar cambios en el territorio de las manadas según condiciones climáticas (7)")
    print("9- Graficar resultados para cada uno de los requerimientos (8)")
    print("0- Salir")

control = new_controller()

def load_data(control, filename):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    return controller.load_data(control, filename)
def load_data2(control,filename):
    return controller.load_data_2(control, filename)
def auxiliar_v(control):
    return controller.auxiliar_c(control)
def puntos_enc_v(control):
    return controller.puntos_enc(control)
def conectar_pe_v(control):
    return controller.conectar_pe(control)
def tabla_v(control):
    return controller.tabla(control)

def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control, vertexA, vertexB):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    #tiempo = f"{controller.req_1(control,vertexA, vertexB)[1]:.3f}"
    return controller.req_1(control,vertexA, vertexB)


def print_req_2(control, vertex_i, vertex_f):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    return controller.req_2(control, vertex_i, vertex_f)


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    #tiempo = f"{controller.req_3(control)[1]:.3f}"
    return controller.req_3(control)


def print_req_4(control, pos_i, pos_f):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    return controller.req_4(control, pos_i, pos_f)


def print_req_5(control, origen, distancia_max, puntos_min):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    return controller.req_5(control, origen, distancia_max, puntos_min)


def print_req_6(control, fecha1, fecha2, sexo):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    #tiempo = f"{controller.req_6(control, fecha1, fecha2, sexo)[1]:.3f}"
    return controller.req_6(control, fecha1, fecha2, sexo)#[0], #tiempo


def print_req_7(control, fecha1, fecha2, temp1, temp2):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    return controller.req_7(control, fecha1, fecha2, temp1, temp2)


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass

def tabular(data, header, maxcolwidths=16, imprimir=True):
    arr=[]
    for dato in lt.iterator(data):
        forr = dict((k,dato[k]) for k in (header)if k in dato)
        arr.append(forr)
    rows = [x.values() for x in arr]
    if imprimir:
        print(tabulate(rows, header, tablefmt="grid", maxcolwidths=maxcolwidths)) 
    else:
        return rows
def sexo_fn(sexo):
    if sexo in ("f", "Femenino","Femenino","Hembra","hembra"):
        return "f"
    elif sexo in ("m","Masculino","masculino","Macho","macho"):
        return "m"
    else:
        return ""
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
                print("Cargando información de los archivos ....\n")
                filename = str(input("Elija el tamaño de la muestra que desea: (-5pct, -10pct, -20pct, -30pct, -50pct, -80pct, -large o -small)\n"))
                print("")
                load = load_data(control, filename)
                data = load[0]
                tiempo1 = load[1]
                load2 = load_data2(control, filename)
                datos_lobos = load2[0]
                tiempo2 = load2[1]
                print("---- Caracteristicas de lobos y eventos ----")
                num_lobos = mp.size(data["mp_lobos"])
                print("Número de lobos: "+str(num_lobos)) 
                
                num_lobos2 = lt.size(datos_lobos["lt_lobos_a2"])
                print("Número de lobos con datos: "+str(num_lobos2))
                
                num_eventos = lt.size(data["lt_todos"])
                print("Número de eventos cargados: "+str(num_eventos))
                print("")
                print("---- Caracteristicas nodos ----")
                num_vertices = gr.numVertices(data["dirigido"])
                #print(gr.numEdges(auxiliar_v(control)["dirigido"]))
                pto_enc = puntos_enc_v(control)
                datos_pto_enc = pto_enc[0]
                tiempo3 = pto_enc[1]
                datos_pto_enc_2 = lt.size(datos_pto_enc)
                print("Número de puntos de encuentro: "+str(datos_pto_enc_2))
                
                print("Número de puntos de seguimiento: "+str(num_vertices))
                
                d_puntos = conectar_pe_v(control)
                datos_puntos = d_puntos[0]
                tiempo4 = d_puntos[1]
                num_total_vertice = gr.numVertices(datos_puntos["dirigido"])
                print("Número total de vertices: "+str(num_total_vertice))
                print("")
                print("---- Caracteristicas arcos ----")
                num_arcos_ptos = gr.numEdges(datos_puntos["dirigido"])
                
                print("Número de arcos en los puntos de encuentro: "+str(num_arcos_ptos))
                
                d_aux = auxiliar_v(control)
                datos_aux = d_aux[0]
                tiempo5 = d_aux[1]
                num_arcos = gr.numEdges(datos_aux["dirigido"])-num_arcos_ptos
                print("Número de arcos de los puntos de seguimiento: "+str(num_arcos))
                
                num_total_arco = gr.numEdges(data["dirigido"])
                print("Número total de arcos: "+str(num_total_arco))
                print("")
                print("---- Caracteristicas grafo dirigido ----")
                num_total_ver_di = gr.numVertices(data["dirigido"])
                print("Número total de vertices: "+str(num_total_ver_di))
                num_total_arc_di = gr.numEdges(data["dirigido"])
                print("Número total de arcos: "+str(num_total_arc_di))
                print("")
                
                print("---- Caracteristicas grafo no dirigido ----")
                num_total_ver_nodi = gr.numVertices(data["no_dirigido"])
                print("Número total de vertices: "+str(num_total_ver_nodi))
                num_total_arc_nodi = gr.numEdges(data["no_dirigido"])
                print("Número total de arcos: "+str(num_total_arc_nodi))
                print("")
                das = tabla_v(control)
                datas = das[0]
                tiempo6= das[1]
                max_lat = datas[1]
                min_lat = datas[2]
                max_lon = datas[3]
                min_lon = datas[4]
                print("----- Area del grafo -----")
                print("Min & Max latitud: "+str(min_lat)+" and "+str(max_lat))
                print("Min & Max longitud: "+str(min_lon)+" and "+str(max_lon))
                print("")
                
                print("Primeros y ultimos 5 nodos cargados en el digrafo")
                header = ["LON_APROX","LAT_APROX","NODE_ID","INDIVIDUAL_ID","ADJACENT_NODES"]
                maxcolwidths = [16,16,35,35,16]
                tabular(datas[0], header, maxcolwidths)
                
                print("")
                #tiempo = round(load_data(control, filename)[1]+load_data2(control, filename)[1]+puntos_enc_v(control)[1]+conectar_pe_v(control)[1]+auxiliar_v(control)[1],3)#+tabla_v(control)[1],3)
                tiempo = round(tiempo1+tiempo2+tiempo3+tiempo4+tiempo5+tiempo6,4)
                print("Tiempo total [ms]: "+str(tiempo))

                print("")
            elif int(inputs) == 2:
                vertexA = str(input("Punto de encuentro de partida: "))
                vertexB = str(input("Punto de encuentro de llegada: "))
                data = print_req_1(control, vertexA, vertexB)
                if data[0] != False:
                    print("Esta el vertice "+str(vertexB)+" en el arbol DFS? "+data[0])
                    if data[0] == "False":
                        print("El vertice "+str(vertexB)+" no está en el arbol")
                    else:
                        print("")
                        print("Total de nodos en el camino: " + str((data[1])))
                        print("Número total de puntos de encuentro: "+str(data[2]))
                        print("Número total de puntos de seguimiento: "+str(data[3]))
                        print("Distancia total en el camino [km]: "+str(data[5]))
                        if (data[1]) > 10:
                            print("El camino contiene mas de 10 nodos")
                            print("")
                            print("Los primeros y ultimos 5 nodos cargados en el camino DFS son: ")
                            tabular_lt = data[4]
                            primeros = lt.subList(tabular_lt, 1, 5)
                            ultimos = lt.subList(tabular_lt, lt.size(tabular_lt)-4,5)
                            lt_tabular = lt.newList()
                            for eleme in lt.iterator(primeros):
                                lt.addLast(lt_tabular,eleme)
                            for dato in lt.iterator(ultimos):
                                lt.addLast(lt_tabular,dato)
                            header = ["LON_APROX","LAT_APROX","NODE_ID","INDIVIDUAL_ID","INDIVIDUAL_COUNT","EDGE_TO","EDGE_DISTANCE[km]"]
                            tabular(lt_tabular, header)
                        else:
                            print("Hay menos de 10 nodos en el camino, estos son: ")
                            tabular_lt = data[4]
                            header = ["LON_APROX","LAT_APROX","NODE_ID","INDIVIDUAL_ID","INDIVIDUAL_COUNT","EDGE_TO","EDGE_DISTANCE[km]"]
                            tabular(tabular_lt, header)
                    print("Tiempo total [ms]: ", f"{data[6]:.3f}")
                else:
                    print("Alguno de los vertices ingresados no estan en el grafo")
                    print("Tiempo total [ms]: ", f"{data[6]:.3f}")

                
            elif int(inputs) == 3:
                vertexA = str(input("Punto de encuentro de partida: "))
                vertexB = str(input("Punto de encuentro de llegada: "))
                data = print_req_2(control, vertexA, vertexB)
                if data[0] != False:
                    print("Esta el vertice "+str(vertexB)+" en el arbol BFS? "+data[0])
                    if data[0] == "False":
                        print("El vertice "+str(vertexB)+" no está en el arbol")
                    else:
                        print("")
                        print("Total de nodos en el camino: " + str((data[1])))
                        print("Número total de puntos de encuentro: "+str(data[2]))
                        print("Número total de puntos de seguimiento: "+str(data[3]))
                        print("Distancia total en el camino [km]: "+str(data[5]))
                        if (data[1]) > 10:
                            print("El camino contiene mas de 10 nodos")
                            print("")
                            print("Los primeros y ultimos 5 nodos cargados en el camino BFS son: ")
                            tabular_lt = data[4]
                            primeros = lt.subList(tabular_lt, 1, 5)
                            ultimos = lt.subList(tabular_lt, lt.size(tabular_lt)-4,5)
                            lt_tabular = lt.newList()
                            for eleme in lt.iterator(primeros):
                                lt.addLast(lt_tabular,eleme)
                            for dato in lt.iterator(ultimos):
                                lt.addLast(lt_tabular,dato)
                            header = ["LON_APROX","LAT_APROX","NODE_ID","INDIVIDUAL_ID","INDIVIDUAL_COUNT","EDGE_TO","EDGE_DISTANCE[km]"]
                            tabular(lt_tabular, header)
                        else:
                            print("Hay menos de 10 nodos en el camino, estos son: ")
                            tabular_lt = data[4]
                            header = ["LON_APROX","LAT_APROX","NODE_ID","INDIVIDUAL_ID","INDIVIDUAL_COUNT","EDGE_TO","EDGE_DISTANCE[km]"]
                            tabular(tabular_lt, header)
                    print("Tiempo total [ms]: ", f"{data[6]:.3f}")
                else:
                    print("Alguno de los vertices ingresados no estan en el grafo")
                    print("Tiempo total [ms]: ", f"{data[6]:.3f}")
            
            
            elif int(inputs) == 4:
                data = print_req_3(control)
                print("Existen "+str(data[0])+" componentes fuertemente conectados en el grafo")
                print("")
                lt_tabular = data[1]
                header = ["SCCID","NODE_IDs","SCC\nSIZE","MIN-LAT","MAX-LAT","MIN-LON","MAX-LON","WOLF\nCOUNT","WOLF_DETAILS"]
                maxcolwidths = [8,32,8,8,8,8,8,8,68]
                print("El top 5 de SCC en el grafo son: ")
                arr = []
                for dato in lt.iterator(data[1]):
                    encabezado = ["id_individual","animal_sex","life_stage","study_site","deployment_comments"]
                    tabla_adentro = tabular(dato["WOLF_DETAILS"], encabezado, imprimir=False)
                    forr = dict((k,dato[k]) for k in ("SCCID","NODE_IDs","SCC_SIZE","MIN-LAT","MAX-LAT","MIN-LON","MAX-LON","WOLF_COUNT","WOLF_DETAILS")if k in dato)
                    encabezado = ["id_ind\nividual","animal\nsex","life\nstage","study\nsite","deployment\ncomments"]
                    forr["WOLF_DETAILS"] = tabulate(tabla_adentro, encabezado, tablefmt="grid", maxcolwidths=[6,6,4,8,10])
                    arr.append(forr)
                rows = [x.values() for x in arr]
                print(tabulate(rows, header, tablefmt="grid", maxcolwidths=maxcolwidths))
                print("Tiempo total [ms]: ", f"{data[2]:.3f}")
                
            elif int(inputs) == 5:
                posicion_incial = input("Ingrese coordenada 1: ")
                posicion_incial = tuple(posicion_incial.split(','))
                posicion_final = input("Ingrese coordenada 2: ")
                posicion_final = tuple(posicion_final.split(','))
                datos = print_req_4(control, posicion_incial, posicion_final)
                data = datos[0]
                tiempo = datos[1]
                if data:
                    header = ["node_id","long_aprox","lat_aprox","individual_id"]
                    print("La distancia desde la coordenada 1 hasta el nodo mas cercano es [km]: "+str(data[1]))
                    tabular(data[3], header)
                    print(" ")
                    print("La distancia desde la coordenada 2 hasta el nodo mas cercano es [km]: "+str(data[2]))
                    tabular(data[4], header)
                    print(" ")
                    print("Número de nodos visitados: "+str(data[5]))
                    print("Número de arcos visitados: "+str(data[5]-1))
                    print("Distancia total del recorrido [km]: "+str(data[0]))
                    print("")
                    encabezado = ["src_node_id","lat_src","lon_src","tgt_node_id","lat_tgt","lon_tgt","individual_id","distance[km]"]
                    if lt.size(data[6]) > 6:
                        print("Hay "+str(lt.size(data[6]))+" nodos en la ruta")
                        print("Los 3 primeros y 3 ultimos nodos que estan en el camino:")
                        primeros = lt.subList(data[6], 1, 3)
                        ultimos = lt.subList(data[6], lt.size(data[6])-2, 3)
                        todos =lt.newList()
                        for a in lt.iterator(primeros):
                            lt.addLast(todos,a)
                        for i in lt.iterator(ultimos):
                            lt.addLast(todos,i)
                        tabular(todos,encabezado,maxcolwidths=[30,16,16,30,16,16,16,16])
                    else:
                        print("Hay "+str(lt.size(data[6]))+" nodos en la ruta")
                        tabular(data[6],encabezado,maxcolwidths=[30,16,16,30,16,16,16,16])
                else:
                    print("No existe una ruta desde el vertice mas cercano a la coordenada 1 y el vertice mas cercano a la coordenada 2")
                print("Tiempo total [ms]: ", f"{tiempo:.3f}")

            elif int(inputs) == 6:
                origen = input("Ingrese el id del vertice de origen: ")#"m112p039_56p612"
                distancia_max = input("Ingrese la distancia máxima: ") #24.5
                puntos_min = input("Ingrese los puntos minimo del camino: ") #2
                data = print_req_5(control, origen, distancia_max, puntos_min)
                print(data)

            elif int(inputs) == 7:
                fecha1 = input("Ingrese fecha inicial (YYYY/MM/DD HH:MM): ")#"2013-02-16 00:00"
                fecha2 = input("Ingrese fecha final (YYYY/MM/DD HH:MM): ")#2014-10-23 23:59
                sexo = input("Ingrese sexo del animal (f/m):")#"f"
                sexo = sexo_fn(sexo)
                if sexo in ("f","m"):
                    fin = print_req_6(control, fecha1, fecha2, sexo)
                    datos = fin[0]
                    tiempo = fin[1]
                    header = ["individual_id","animal_taxon","animal_life_stage","animal_sex","study_site","travel_dist","deployment_comments"]
                    encabezado = ["node_id","long_aprox","lat_aprox","individual_id","individual_count"]
                    print("-------- Parte 1 --------")
                    tabular(datos[0], header)
                    tabla = datos[6]
                    nodos = datos[7]
                    arcos = nodos-1
                    print(" ")
                    print("Cantidad de nodos: "+str(nodos))
                    print("Cantidad de arcos: "+str(arcos))
                    print("Distancia total: "+str(datos[2]))
                    print(" ")
                    print("Hay "+str(nodos)+" nodos en la ruta")
                    if nodos > 6:
                        print("Estos son los 3 primeros y ultimos del camino: ")
                    else:
                        print("Estos son todos los nodos del camino: ")
                    tabular(tabla, encabezado)
                    print("\n")
                    print("-------- Parte 2 --------")
                    tabular(datos[1], header)
                    tabla2 = datos[4]
                    nodos2 = datos[5]
                    arcos2 = nodos2-1
                    print(" ")
                    print("Cantidad de nodos: "+str(nodos2))
                    print("Cantidad de arcos: "+str(arcos2))
                    print("Distancia total: "+str(datos[3]))
                    print(" ")
                    print("Hay "+str(nodos2)+" nodos en la ruta")
                    if nodos2 > 6:
                        print("Estos son los 3 primeros y ultimos del camino: ")
                    else:
                        print("Estos son todos los nodos del camino: ")
                    tabular(tabla2, encabezado)
                    print("Tiempo total [ms]: ", f"{tiempo:.3f}")
                else:
                    print("El sexo ingresado no existe, debe ser 'f' o 'm'")

            elif int(inputs) == 8:
                fecha1 = input("Ingrese fecha inicial (YYYY/MM/DD HH:MM): ")#"2012-11-28 00:00"
                fecha2 = input("Ingrese fecha final (YYYY/MM/DD HH:MM): ")#"2014-05-17 23:59"
                temp_max = float(input("Ingrese la temperatura máxima"))#9.7
                temp_min = float(input("Ingrese la temperatura mínima")) #-17.3
                req7 = print_req_7(control, fecha1, fecha2, temp_max, temp_min)
                datos = req7[0]
                tiempo = req7[1]
                print("Total de nodos",datos[0])
                print("Total de arcos",datos[1])
                print("Hay "+str(datos[2])+" SCC en el grafo")
                lt_tabular = datos[3]
                header = ["SCCID","NODE_IDs","SCC\nSIZE","MIN-LAT","MAX-LAT","MIN-LON","MAX-LON","WOLF\nCOUNT","WOLF_DETAILS"]
                maxcolwidths = [8,32,8,8,8,8,8,8,68]
                print("Los 3 primero y ultimos SCC son: ")
                arr = []
                for dato in lt.iterator(lt_tabular):
                    encabezado = ["id_individual","animal_sex","life_stage","study_site","deployment_comments"]
                    tabla_adentro = tabular(dato["WOLF_DETAILS"], encabezado, imprimir=False)
                    forr = dict((k,dato[k]) for k in ("SCCID","NODE_IDs","SCC_SIZE","MIN-LAT","MAX-LAT","MIN-LON","MAX-LON","WOLF_COUNT","WOLF_DETAILS")if k in dato)
                    encabezado = ["id_ind\nividual","animal\nsex","life\nstage","study\nsite","deployment\ncomments"]
                    forr["WOLF_DETAILS"] = tabulate(tabla_adentro, encabezado, tablefmt="grid", maxcolwidths=[6,6,4,8,10])
                    arr.append(forr)
                rows = [x.values() for x in arr]
                print(tabulate(rows, header, tablefmt="grid", maxcolwidths=maxcolwidths))
                print("Tiempo total [ms]: ", f"{tiempo:.3f}")

            elif int(inputs) == 9:
                print_req_8(control)

            elif int(inputs) == 0:
                working = False
                print("\nGracias por utilizar el programa")
                
            else:
                print("Opción errónea, vuelva a elegir.\n")
        except Exception as exp:
            print("ERR:", exp)
            traceback.print_exc()
    sys.exit(0)
