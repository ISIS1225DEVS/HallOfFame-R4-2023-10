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
import datetime
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback
from DISClib.ADT import graph as gr
default_limit = 1000
sys.setrecursionlimit(default_limit*10)
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    control = controller.new_controller()
    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Planear una posible ruta entre dos puntos de encuentro")
    print("3- Planear una ruta con menos paradas entre dos puntos de encuentro")
    print("4- Reconocer los territorios habitados por distintas manadas")
    print("5- Identificar el camino más corto entre dos puntos del hábitat")
    print("6- Reconocer el corredor migratorio mas extenso")
    print("7- Identificar diferencias en los corredores migratorios según el tipo de individuo")
    print("8- Identificar cambios en el territorio de las manadas según condiciones climáticas")
    print("0- Salir")


def load_data(control, filename):
    
    datastructs = controller.load_data(control, filename)
    print("***********************************")
    print("** WOLF TRANKING & GATERING AREA **")
    print("***********************************")
    
    headers = ["location-long-aprox", "location-lat-aprox", "node-id", "individual-id","adjacent_nodes" ]
    location_long_aprox=[]
    location_lat_aprox=[]
    node_id=[]
    individual_id=[]
    adjacent_nodes=[]
    #print(datastructs["puntos_s_valor"])
    #print(datastructs["lobos_puntos_s"])
    #print(datastructs["lobos_puntos_s"])
    
    
    for data in datastructs["lobos_puntos_s"]["table"]["elements"]:
        for element in lt.iterator(data):
            for valor in element["value"]["lista_puntos_s"]["elements"]:
                location_long_aprox.append(valor["location-long"])
                location_lat_aprox.append(valor["location-lat"])
                node_id.append(valor["identificador_s"])
                individual_id.append(valor["identificador_e"])
                adjacent_nodes.append(valor["gps:dop"])
                #print(valor)
    location_long_aprox_min=location_long_aprox.copy()[:5]
    location_long_aprox_max=location_long_aprox.copy()[len(location_long_aprox)-6:len(location_long_aprox)-1]
    
    location_lat_aprox_min=location_lat_aprox.copy()[:5]
    location_lat_aprox_max=location_lat_aprox.copy()[len(location_lat_aprox)-6:len(location_lat_aprox)-1]
    
    node_id_min=node_id.copy()[:5]
    node_id_max=node_id.copy()[len(node_id)-6:len(node_id)-1]
    
    individual_id_min=individual_id.copy()[:5]
    individual_id_max=individual_id.copy()[len(individual_id)-6:len(individual_id)-1]
    
    adjacent_nodes_min=adjacent_nodes.copy()[:5]
    adjacent_nodes_max=adjacent_nodes.copy()[len(adjacent_nodes)-6:len(adjacent_nodes)-1]
    
    
    location_long_aprox_sum=location_long_aprox_min + location_long_aprox_max
    location_lat_aprox_sum=location_lat_aprox_min +location_lat_aprox_max
    node_id_sum=node_id_min + node_id_max
    individual_id_sum=individual_id_min + individual_id_max
    adjacent_nodes_sum=adjacent_nodes_min + adjacent_nodes_max
    
    
    
    table = zip(location_long_aprox_sum, location_lat_aprox_sum, node_id_sum, individual_id_sum, adjacent_nodes_sum)
    print(tabulate(table, headers=headers,  tablefmt="grid" ,floatfmt=".4f"))

def print_req_1(control, origen, destino):
    print ("######### REQ No 1. Answer ###################")
    headers = ["location-long-aprox", "location-lat-aprox", "node-id", "individual-id", "individual-count","edge-to", "edge-to", "edge-distance-km"]
    
    camino= controller.req_1(control, origen, destino)
    
    print(camino)
    
    
    return None


def print_req_2(control, origen, destino):
    print ("######### REQ No 2. Answer ###################")
    headers = ["location-long-aprox", "location-lat-aprox", "node-id", "individual-id", "individual-count","edge-to", "edge-to", "edge-distance-km"]
    
   
        
    camino, answer = controller.req_2(control, origen, destino)
    print(answer)
    return None


def print_req_3(control):
    
    respuesta, answer= controller.req_3(control)
    
    print ("######### REQ No 3. Answer ###################")
   #print(respuesta)
   
    headers = ["SCCID", "Node IDs", "SCC size", "min-lat", "max-lat","min-lon", "Wolf Count", "Wolf Details"]
   
    lista_act_economicas=[]
    anio=0
        
    
        
    
   
    lista_tabulate=[lista_act_economicas]
   
   
   
    print("Mayores descuentos tributarios en: ", anio)
    print(tabulate(lista_tabulate, headers,  tablefmt="grid", maxcolwidths=12))
    #printLoadDataAnswer(answer)

    
    return None



def print_req_4(control, origen, destino):
    print ("######### REQ No 4. Answer ###################")
    headers1 = ["node-id", "location-long-aprox", "location-long-aprox", "individual-id"]
    
    
    headers2= ["src-node-id","location-last-src","location-long-src","tgt-node-id","location-long-tgt","individual-id","distance-km"]
    
    headers3=["node-id","location-long-aprox","location-lat-aprox","individual-id","individual-count"]
    camino = controller.req_4(control, origen, destino)
    
    print("++ Source gatering point ++")
    
    print("++ Target gatering point ++")
    
    print("++ Wolf route details ++")
    
    print("++ Route details ++ ")
    
    print("++ Gathering Points details ++ ")
    
    
    
    return None



def print_req_5(control, origen, distancia, num_min):
    print ("######### REQ No 5. Answer ###################")  
    headers = ["Points Count", "Path distance [km]", "Point List", "Animal Count"]
    best, dato_mejor = controller.req_5(control, origen, distancia, num_min)
    print(best, dato_mejor)
    return None

def print_req_6(control, fecha_inicial, fecha_final, sexo):
    
    cosas = controller.req_6(control, fecha_inicial, fecha_final, sexo)
    
    
    print ("######### REQ No 6. Answer ###################")
    
   
    
    print("Considering the tracking data between the following dates:")
    
    print("- - - - - Part 1 - - - - -")
    
    print("The individual with the longest travel distance is :")
    
    headers1=["Individual-id","animal-taxon","animal-sex","study-site","travel-dist","deployment-comments"]
    
    id=0
    print("The longest path for the wolf"+id+" has: ")
    
    print("---Longest path details---")
    
    headers2=["node-id","location-long-aprox","location-lat-aprox","individual-id","individual-count"]
    
    print("- - - - - Part 2 - - - - -")
    
    print("The individual with the shortest travel distance is :")
    
    #headers=["Individual-id","animal-taxon","animal-sex","study-site","travel-dist","deployment-comments"]
    print("The longest path for the wolf"+id+"has:")
    print("Longest path details")
    #headers=["Individual-id","animal-taxon","animal-sex","study-site","travel-dist","deployment-comments"]
    print("Considering the tracking data between the following dates:")
    
    
    return None


def print_req_7(control):
    print ("######### REQ No 7. Answer ###################")
    headers = ["SCCID", "Node IDs", "SCC size", "min-lat", "max-lat","min-lon", "Wolf Count", "Wolf Details"]
    print("There a "+ +" Strongly Connected Components (SCC) in the graph")
    
    print("+++ The SCC details are: +++")
    
    
    return None


def print_req_8(control):
    
    camino= controller.req_7(control, fecha_inicial, fecha_final, tem_min, tem_max)
    
    return None


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
                print("1 - small")
                print("2 - 5pct")
                print("3 - 10pct")
                print("4 - 20pct")
                print("5 - 30pct")
                print("6 - 50pct")
                print("7 - 80pct")
                print("8 - large")
                filename = int(input("Escoja el tamaño de la muestra:"))
                if filename<1 and filename>8:
                    print("Ingreso un tamaño no permitido")   
                control = new_controller()   
                print("Adecuando el sistema a la representación necesaria")
                print("Cargando información de los archivos ....\n")
                data = load_data(control, filename)
            elif int(inputs) == 2:
                origen = input("Diligencie el punto de encuentro inicial del cual quiere partir:")
                destino = input("Diligencie el punto de encuentro final al cual quiere llegar:")
                print_req_1(control, origen, destino)
            elif int(inputs) == 3:
                origen = input("Diligencie el punto de encuentro inicial del cual quiere partir:")
                destino = input("Diligencie el punto de encuentro final al cual quiere llegar:")
                print_req_2(control, origen, destino)
            elif int(inputs) == 4:
                print_req_3(control)
            elif int(inputs) == 5:
                origen = input("Diligencie el punto de encuentro inicial del cual quiere partir:")
                destino = input("Diligencie el punto de encuentro final al cual quiere llegar:") 
                print_req_4(control, origen, destino)
            elif int(inputs) == 6:
                origen = input("Diligencie el punto de encuentro inicial del cual quiere partir:")
                distancia =  input("Diligencie la distancia que puede recorrer el guardabosques del punto de origen:")
                num_min = input("Diligencie el número mínimo de puntos de encuentro:")
                print_req_5(control, origen, distancia, num_min)
            elif int(inputs) == 7:
                fecha_inicial = input("Diligencie la fecha inicial del análisis:")
                fecha_final = input("Diligencia la fecha final del análisis:")
                fecha_inicial = datetime.datetime.strptime(fecha_inicial, "%Y-%m-%d %H:%M")
                fecha_final = datetime.datetime.strptime(fecha_final, "%Y-%m-%d %H:%M")
                sexo = input("Comente el sexo del animal:")
                print_req_6(control, fecha_inicial, fecha_final, sexo)

            elif int(inputs) == 8:
                fecha_inicial = input("Diligencie la fecha inicial del análisis: ")
                fecha_final = input("Diligencia la fecha final del análisis: ")
                tem_min= input("Diligencie la temperatura mínima: ")
                tem_max= input("Diligencie la temperatura máxima: ")
                print_req_7(control, fecha_inicial, fecha_final, tem_min,tem_max)
                
            elif int(inputs) == 0:
                working = False
                print("\nGracias por utilizar el programa")
                
            else:
                print("Opción errónea, vuelva a elegir.\n")
        except Exception as exp:
            print("ERR:", exp)
            traceback.print_exc()
    sys.exit(0)
