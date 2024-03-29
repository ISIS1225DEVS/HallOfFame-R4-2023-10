﻿"""
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
 """

import config as cf
import model
import time
import csv
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    return model.new_data_structs()


# Funciones para la carga de datos

def load_data(control, filename,filename2):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    data_file = cf.data_dir + filename
    input_file = csv.DictReader(open(data_file, encoding='utf-8'))
    datos=model.ord_data(input_file, control)
    control["eventos"]=datos
    last_dato=None
    
    for dato in iterador(control["eventos"]):
        if last_dato is not None:
            samelobo=dato["individual-local-identifier"]==last_dato["individual-local-identifier"]
            sameevent=dato["event-id"]==last_dato["event-id"]
            if samelobo and not sameevent: 
                model.add_data(control, last_dato, dato)
        last_dato=dato
    
    model.puntos_encuentro(control)
    model.conectar_puntos_encuentro(control)
    lobos_file=cf.data_dir+filename2
    input2_file = csv.DictReader(open(lobos_file, encoding='utf-8'))
    for lobo in input2_file:
        model.addlobo(control,lobo)
    
    
    model.mapa_lobos(control)

    return control


# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control, origen, destino):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    return model.req_1(control, origen, destino)


def req_2(control, origen, destino):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    return model.req_2(control, origen, destino)


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    return model.req_3(control)


def req_4(control, lat1, long1, lat2, long2):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    return model.req_4(control, lat1, long1, lat2, long2)


def req_5(control, origen, distancia, min_pe):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    return model.req_5(control, origen, distancia, min_pe)
    pass

def req_6(control, f1,f2, sexo):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    return model.req_6(control,f1,f2, sexo)

def req_6b(control, f1,f2, sexo):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    return model.req_6b(control,f1,f2, sexo)



def req_7(control, t1,t2,temp1,temp2):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    return model.req_7(control, t1,t2,temp1,temp2)


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory

def iterador(lista):
    return model.iterador(lista)

def size(lista):
    return model.size(lista)

def degree(grafo, punto):
    return model.degree(grafo, punto)

def numvertices(grafo):
    return model.numvertices(grafo)

def vertices(grafo):
    return model.vertices(grafo)

def numedges(grafo):
    return model.arcos(grafo)

def keyset(mapa):
    return model.keyset(mapa)

def numvertices(grafo):
    return model.numvertices(grafo)