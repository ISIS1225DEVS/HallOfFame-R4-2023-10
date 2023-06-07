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
    return controller.new_controller()

def new_controller2():
    """
        Se crea una instancia del controlador
    """
    return controller.new_controller2()



def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Planear una posible ruta entre dos puntos de encuentro")
    print("3- Planear una ruta con menos paradas entre dos puntos de encuentro ")
    print("4- Reconocer los territorios habitados por distintas manadas")
    print("5- Identificar el camino más corto entre dos puntos del hábitat")
    print("6- Reconocer el coredor migratorio mas extenso")
    print("7- Identificar diferencias de movilidad entre tipos de miembros la manada")
    print("8- Identificar cambios en el territorio de las manadas según condiciones climáticas ")
    print("9- Graficar resultados para cada uno de los requerimientos")
    print("0- Salir")

def load_data(analyzer):
    """
    Carga los datos
    """
    return controller.load_data(analyzer,'BA-Grey-Wolf-tracks-utf8-small.csv',"BA-Grey-Wolf-individuals-utf8-small.csv")


def load_data2(analyzer):
    """
    Carga los datos
    """
    return controller.load_data2(analyzer,'BA-Grey-Wolf-tracks-utf8-small.csv',"BA-Grey-Wolf-individuals-utf8-small.csv")


def print_req_1(analyzer):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    punto1=input("Digite el primer punto de encuentro: ")
    punto2=input("Digite el segundo punto de encuentro: ")
    pila=controller.req_1(analyzer,punto1,punto2)
    headers= ["location-long-aprox",
                         "location_lat_aprox", "node-id"]
    table = []
    for elemento in lt.iterator(pila):
        info=controller.buscarInfo(analyzer,elemento)
        if info != None:
          table.append([info["location-long"],info["location-lat"],elemento])
    print(tabulate(table,headers,tablefmt="grid",maxcolwidths=14))




def print_req_2(analyzer):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(analyzer):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    hashConectados=controller.req_3(analyzer)

    headers= ["SCC_ID",
                         "SCC size", "min-lat", "max-lat", "min-lon",
                          "max-lon", "wolf Count"]
    table = []
    for key in lt.iterator(mp.keySet(hashConectados)):
        elements=me.getValue(mp.get(hashConectados,key))
        cantidadPuntos=lt.size(me.getValue(mp.get(elements,"puntos")))
        hashLobos=me.getValue(mp.get(elements,"lobos"))
        tamañoLista=lt.size(mp.keySet(hashLobos))-4
        minLat=me.getValue(mp.get(hashLobos,"minLat"))
        maxLat=me.getValue(mp.get(hashLobos,"maxLat"))
        minLong=me.getValue(mp.get(hashLobos,"minLong"))
        maxLong=me.getValue(mp.get(hashLobos,"maxLong"))

        table.append([key,cantidadPuntos,minLat,maxLat,minLong,maxLong,
                     tamañoLista])
        
    print(tabulate(table,headers,tablefmt="grid",maxcolwidths=14))

    for key in lt.iterator(mp.keySet(hashConectados)):
        table = []
        headers= ["individual-id",
                            "animal-sex", "animal-life-stage", "study-site", "deployment-comments",
                            ]
        elements=me.getValue(mp.get(hashConectados,key))
        lobos=me.getValue(mp.get(elements,"lobos"))
        mp.remove(lobos,"minLat")
        mp.remove(lobos,"maxLat")
        mp.remove(lobos,"minLong")
        mp.remove(lobos,"maxLong")
        for lobo in lt.iterator(mp.keySet(lobos)):
            dictLobo=me.getValue(mp.get(lobos,lobo))
            table.append([dictLobo["ID"],
                            dictLobo["animal-sex"], dictLobo["animal-life-stage"], dictLobo["study-site"], dictLobo["deployment-comments"],
                            ])
        print("Lobos del componente fuertemente conectado número",key)
        print(tabulate(table,headers,tablefmt="grid",maxcolwidths=14),"\n"*2)





def print_req_4(analyzer):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    punto1=input("Digite el primer punto de encuentro: ")
    punto2=input("Digite el segundo punto de encuentro: ")
    pila=controller.req_1(analyzer,punto1,punto2)
    headers= ["location-long-aprox",
                         "location_lat_aprox", "node-id"]
    table = []
    for elemento in lt.iterator(pila):
        info=controller.buscarInfo(analyzer,elemento)
        if info != None:
          table.append([info["location-long"],info["location-lat"],elemento])
    print(tabulate(table,headers,tablefmt="grid",maxcolwidths=14))

    


def print_req_5(analyzer):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(analyzer):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    movimientos=controller.req_6(analyzer)
    headers= ["individual-id",
                         "animal-taxon", "animal-life-stage", "animal-sex", "dist",
                          "deployment-comments"]
    table = []
    for lobo in lt.iterator(mp.keySet(movimientos)):
        infolobo=me.getValue(mp.get(analyzer["infoLobos"],lobo))
        table.append([infolobo["ID"],infolobo["animal-taxon"],infolobo["animal-life-stage"],infolobo["animal-sex"],infolobo["dist"],infolobo["deployment-comments"]
                     ])
        
    print(tabulate(table,headers,tablefmt="grid",maxcolwidths=14))


def print_req_7(analyzer):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    hashConectados=controller.req_7(analyzer)

    headers= ["SCC_ID",
                         "SCC size", "min-lat", "max-lat", "min-lon",
                          "max-lon", "wolf Count"]
    table = []
    for key in lt.iterator(mp.keySet(hashConectados)):
        elements=me.getValue(mp.get(hashConectados,key))
        cantidadPuntos=lt.size(me.getValue(mp.get(elements,"puntos")))
        hashLobos=me.getValue(mp.get(elements,"lobos"))
        tamañoLista=lt.size(mp.keySet(hashLobos))-4
        minLat=me.getValue(mp.get(hashLobos,"minLat"))
        maxLat=me.getValue(mp.get(hashLobos,"maxLat"))
        minLong=me.getValue(mp.get(hashLobos,"minLong"))
        maxLong=me.getValue(mp.get(hashLobos,"maxLong"))

        table.append([key,cantidadPuntos,minLat,maxLat,minLong,maxLong,
                     tamañoLista])
        
    print(tabulate(table,headers,tablefmt="grid",maxcolwidths=14))

    for key in lt.iterator(mp.keySet(hashConectados)):
        table = []
        headers= ["individual-id",
                            "animal-sex", "animal-life-stage", "study-site", "deployment-comments",
                            ]
        elements=me.getValue(mp.get(hashConectados,key))
        lobos=me.getValue(mp.get(elements,"lobos"))
        mp.remove(lobos,"minLat")
        mp.remove(lobos,"maxLat")
        mp.remove(lobos,"minLong")
        mp.remove(lobos,"maxLong")
        for lobo in lt.iterator(mp.keySet(lobos)):
            dictLobo=me.getValue(mp.get(lobos,lobo))
            table.append([dictLobo["ID"],
                            dictLobo["animal-sex"], dictLobo["animal-life-stage"], dictLobo["study-site"], dictLobo["deployment-comments"],
                            ])
        print("Lobos del componente fuertemente conectado número",key)
        print(tabulate(table,headers,tablefmt="grid",maxcolwidths=14),"\n"*2)


def print_req_8(analyzer):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista
analyzer = new_controller()

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
                data = load_data(analyzer)
            elif int(inputs) == 2:
                print_req_1(analyzer)

            elif int(inputs) == 3:
                print_req_2(analyzer)

            elif int(inputs) == 4:
                print_req_3(analyzer)

            elif int(inputs) == 5:
                print_req_4(analyzer)

            elif int(inputs) == 6:
                print_req_5(analyzer)

            elif int(inputs) == 7:
                print_req_6(analyzer)

            elif int(inputs) == 8:
                analyzer2=new_controller2()
                load_data2(analyzer2)
                print_req_7(analyzer2)

            elif int(inputs) == 9:
                print_req_8(analyzer)

            elif int(inputs) == 0:
                working = False
                print("\nGracias por utilizar el programa")
                
            else:
                print("Opción errónea, vuelva a elegir.\n")
        except Exception as exp:
            print("ERR:", exp)
            traceback.print_exc()
    sys.exit(0)
