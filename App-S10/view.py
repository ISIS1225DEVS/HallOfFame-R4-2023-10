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
#from tabulate import tabulate
import traceback
from DISClib.ADT import map as mp

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
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    filename=""
    print("""ingrese el archivo que quiere cargar:
    1.0.05%
    2.5%
    3.10%
    4.20%
    5.30%
    6.50%
    7.80%
    8.100%
    """)
    x=int(input())
    filename=""
    if x==1:
        filename="BA-Grey-Wolf-tracks-utf8-small.csv"
        filename2="BA-Grey-Wolf-individuals-utf8-small.csv"
    elif x==2:
        filename="BA-Grey-Wolf-tracks-utf8-5pct.csv"
        filename2="BA-Grey-Wolf-individuals-utf8-5pct.csv"
    elif x==3:
        filename="BA-Grey-Wolf-tracks-utf8-10pct.csv"
        filename2="BA-Grey-Wolf-individuals-utf8-10pct.csv"
    elif x==4:
        filename="BA-Grey-Wolf-tracks-utf8-20pct.csv"
        filename2="BA-Grey-Wolf-individuals-utf8-20pct.csv"
    elif x==5:
        filename="BA-Grey-Wolf-tracks-utf8-30pct.csv"
        filename2="BA-Grey-Wolf-individuals-utf8-30pct.csv"
    elif x==6:
        filename="BA-Grey-Wolf-tracks-utf8-50pct.csv"
        filename2="BA-Grey-Wolf-individuals-utf8-50pct.csv"
    elif x==7:
        filename="BA-Grey-Wolf-tracks-utf8-80pct.csv"
        filename2="BA-Grey-Wolf-individuals-utf8-80pct.csv"
    elif x==8:
        filename="BA-Grey-Wolf-tracks-utf8-large.csv"
        filename2="BA-Grey-Wolf-individuals-utf8-large.csv"
    t1=controller.get_time()
    print("Cargando información...")
    controller.load_data(control, filename,filename2)
    lobos=controller.size(control["lobos"])
    puntos_encuentro=controller.size(control["puntos_encuentro"])
    eventos=controller.size(control["eventos"])
    numedges=controller.numedges(control["puntos_seguimiento"])
    lobos_encuentro=0
    numvertices=controller.numvertices(control["puntos_seguimiento"])
    for punto in controller.iterador(control["puntos_encuentro"]):
        lobos_encuentro+=controller.degree(control["puntos_seguimiento"], punto)
        #print(str(controller.degree(control["puntos_seguimiento"], punto)))
    edges_lobo=numedges-lobos_encuentro
    
    
    
    
    #print(control["posiciones"])
    #for llave in controller.iterador(control["puntos_encuentro"]):
        #x=mp.get(control["posiciones"], llave)
        #print(x)
    print("Total de lobos reconocidos en el estudio: "+str(lobos))
    print("Total de puntos de encuentro reconocidos: "+str(puntos_encuentro))
    print("Total de lobos presentes en los puntos de encuentro o nodos de seguimiento: "+str(numvertices))
    print("Total de eventos cargados durante el estudio "+str(eventos))
    print("Total de arcos creados para unir los nodos de encuentro y los puntos de seguimiento: "+str(lobos_encuentro))
    print("Total de arcos creados para representar el movimiento de los individuos: "+str(edges_lobo))
    print("Rango latitud: "+str(control["minlat"])+", "+str(control["maxlat"]))
    print("Rango longitud: "+str(control["minlong"])+", "+str(control["maxlong"]))
    t2=controller.get_time()
    deltat=controller.delta_time(t1,t2)
    print("Tiempo: "+str(round(deltat,2))+ " ms")

    #llaves=mp.keySet(control["info_lobos"])
    #for llave in controller.iterador(llaves):
        #print(str(llave))
    
    
    
    
    

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
    
    # TODO: Imprimir el resultado del requerimiento 1
    origen=input("Introduzca el punto de origen: ")
    destino=input("Introduzca el punto final: ")
    t1=controller.get_time()
    resp=controller.req_1(control, origen, destino)
    if resp[0]==True:
        print("Si existe un camino")
        print("La distancia total es: "+str(round(resp[1],3))+" km")
        print("Total de nodos: "+str(resp[2]))
        print("Puntos de encuentro: "+str(resp[3]))
        print("Puntos de seguimiento: "+str(resp[4]))
        print("Primeros 5  y últimos 5 puntos del camino: ")
        for dato in controller.iterador(resp[5]):
            print(str(dato))

        print(str(controller.size(resp[5])))
    else:
        print("No existe camino")  

    t2=controller.get_time()
    delta=controller.delta_time(t1,t2)
    print("Tiempo total: "+str(round(delta,2))+" ms")

    


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    
    origen=input("Introduzca el punto de origen: ")
    destino=input("Introduzca el punto final: ")
    t1=controller.get_time()
    resp=controller.req_2(control, origen, destino)
    if resp[0]==True:
        print("Si existe un camino")
        print("La distancia total es: "+str(round(resp[1],3))+" km")
        print("Total de nodos: "+str(resp[2]))
        print("Puntos de encuentro: "+str(resp[3]))
        print("Puntos de seguimiento: "+str(resp[4]))
        print("Primeros 5  y últimos 5 puntos del camino: ")
        for dato in controller.iterador(resp[5]):
            print(str(dato))

        print(str(controller.size(resp[5])))
    else:
        print("No existe camino")

    t2=controller.get_time()
    delta=controller.delta_time(t1,t2)
    print("Tiempo total: "+str(round(delta,2))+" ms")


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    t1=controller.get_time()
    print("Cargando requerimiento...")
    resp=controller.req_3(control)
    print("Total de manadas: "+str(resp[0]))
    for dato in controller.iterador(resp[1]):
        print("\n")
        print(str(dato))

    t2=controller.get_time()
    delta=controller.delta_time(t1,t2)
    print("Tiempo de ejecucion: "+str(round(delta,2))+" ms")
    


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    lat1=input("Ingrese la primera latitud: ")
    long1=input("Ingrese la primera longitud: ")
    lat2=input("Ingrese la segunda latitud: ")
    long2=input("Ingrese la segunda longitud: ")
    t1=controller.get_time()
    resp=controller.req_4(control, lat1, long1, lat2, long2)
    print("Cargando requerimiento...")
    print("\n")
    print("Punto inicial: "+str(resp[5]))
    print("Punto final: "+str(resp[6]))
    print("Distancia al punto inicial: "+str(round(resp[0],2)))
    print("Distancia al punto final: "+str(round(resp[1],2)))
    print("Distancia del camino: "+str(round(resp[2],2)))
    print("Total puntos de encuentro: "+str(resp[3]))
    print("Total puntos reconocidos: "+ str(resp[4]+1))
    print("\n")
    print("Total de arcos: "+str(resp[4]))
    for x in controller.iterador(resp[7]):
        print(str(x))

    
    print("\n")
    for x in controller.iterador(resp[8]):
        print(str(x))

    t2=controller.get_time()
    delta=controller.delta_time(t1,t2)
    print(str(round(delta,2)+" ms"))


    
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    origen=input("Introduzca el punto de origen: ")
    distancia=input("Ingrese la distancia que el guardabosques puede recorrer: ")
    min_pe=input("Ingrese el numero minimo de puntos de encuentro que el guardabosuqes desea inspeccionar: ")
    
    t1=controller.get_time()
    resp=controller.req_5(control, origen, distancia, min_pe)
    print("Cargando requerimiento...")
    print("\n")
    
    
    
    
    
    
    t2=controller.get_time()
    delta=controller.delta_time(t1,t2)
    print(str(round(delta,2)+" ms"))
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    f1=input("Ingrese la fecha de inicio: ")
    f2=input("Ingrese la fecha final: ")
    sexo=input("Ingrese el sexo: ")
    print("Cargando primera parte del requerimiento... ")
    t1=controller.get_time()
    resp=controller.req_6(control, f1, f2, sexo)
    print("\n")
    print("Lobo que recorrio mayor distancia: ")
    print("Info lobo: "+str(resp[0]))
    print("Distancia: "+str(round(resp[1],2))+ " km")
    print("Total de nodos: "+str(resp[2]))
    print("Total de arcos: "+str(resp[3]))
    print("Los 3 primeros y 3 ultimos nodos son: ")
    for x in controller.iterador(resp[4]):
        print(str(x))
    
    t2=controller.get_time()
    delta=controller.delta_time(t1,t2)
    print("\n")
    print("Tiempo de ejecucion primera parte: "+str(round(delta,2))+" ms")
    print("\n")
    print("Cargando segunda parte del requerimiento... ")
    resp=controller.req_6b(control, f1, f2, sexo)
    print("\n")
    print("Lobo que recorrio menor distancia: ")
    print("Info lobo: "+str(resp[0]))
    print("Distancia: "+str(round(resp[1],2))+ " km")
    print("Total de nodos: "+str(resp[2]))
    print("Total de arcos: "+str(resp[3]))
    print("Los 3 primeros y 3 ultimos nodos son: ")
    for x in controller.iterador(resp[4]):
        print(str(x))

    t3=controller.get_time()
    deltax=controller.delta_time(t1,t3)
    print("Tiempo total de ejecucion : "+str(round(deltax,2))+" ms")
    
    pass


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    t1=input("Ingrese la fecha 1: ")
    t2=input("Ingrese la fecha 2: ")
    temp1=input("Ingrese la temperatura 1: ")
    temp2=input("Ingrese la temperatura 2: ")
    
    tt1=controller.get_time()
    resp=controller.req_7(control,t1,t2,temp1,temp2)
    print("Total numero de manadas: "+str(resp[0]))
    print("3 manadas con mas y menos dominio de territorio: ")
    print("\n")
    for x in controller.iterador(resp[1]):
        print(x)
        print("\n")
    tt2=controller.get_time()
    delta=controller.delta_time(tt1,tt2)
    print("Tiempo total: "+str(round(delta,2))+" ms")
    # TODO: Imprimir el resultado del requerimiento 7
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


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
                data = load_data(control)
            elif int(inputs) == 2:
                print_req_1(control)

            elif int(inputs) == 3:
                print_req_2(control)

            elif int(inputs) == 4:
                print_req_3(control)

            elif int(inputs) == 5:
                print_req_4(control)

            elif int(inputs) == 6:
                print_req_5(control)

            elif int(inputs) == 7:
                print_req_6(control)

            elif int(inputs) == 8:
                print_req_7(control)

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
