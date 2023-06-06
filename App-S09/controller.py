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
 """

import config as cf
import model
import time
import csv
import tracemalloc
from DISClib.ADT import graph as gr
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    control = model.new_data_structs()
    
    return control


# Funciones para la carga de datos
def load_data (control, filename):
    start_time = get_time()
    data1= load_data1(control, filename)
    data2= load_data2(control, filename)
    size_lobos=mp.size(control["lobos"])
    size_mtp=mp.size(control["mtp"])
    stop_time = get_time()
    d_time = delta_time(start_time, stop_time)
    return size_lobos, data1[0], size_mtp, data1[5], data1[2], data1[3], data1[1], data1[4], round(d_time, 3)

def load_data1(control, filename):
    """
    Carga los datos del reto
    """
    booksfile=cf.data_dir + "BA-Grey-Wolf-tracks-utf8-"+filename
    input_file= csv.DictReader(open(booksfile, encoding='utf-8'))
    
    size=0
    pss=lt.newList(datastructure="ARRAY_LIST")
    for fila in input_file:
        ps=model.add_track(control, fila)
        if ps is not None:
            lt.addLast(pss, ps)
        size+=1    
        
    
    size_pss=lt.size(pss)
    
    arcos=model.add_arcos(control)
    
    
    return size, arcos[0], arcos[1], arcos[2], pss, size_pss

def load_data2 (control, filename):
    
    booksfile=cf.data_dir + "BA-Grey-Wolf-individuals-utf8-"+filename
    input_file= csv.DictReader(open(booksfile, encoding='utf-8'))
    
    size=0
    for fila in input_file:
        model.addLobo(control, fila)
        size+=1   
        
    
    return size
    
def buscar_menor(control, columna):
    return model.buscar_menor_columna(control,columna)
    
    
def buscar_mayor(control, columna):
    return model.buscar_mayor_columna(control,columna)

def dar_adyacencias(control, vertice):
    return model.dar_adyacencias(control, vertice)


def dar_lobos_en_adyancencias(control,vertice):
    return model.dar_lobos_en_adyacencias(control, vertice)

def dar_distancia(grafo, vertice1, vertice2):
    return model.dar_distancia(grafo, vertice1, vertice2)

def dar_lat_long_nodo(nodo):
    return model.dar_lat_long_nodo(nodo)

def dar_lobo_en_arco(arco):
    return model.dar_lobo_en_arco(arco)
    
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
    start_time = get_time()
    req_1 = model.req_1(control, origen, destino)
    end_time = get_time()
    delta_t = delta_time(start_time, end_time)
    return req_1, round(delta_t, 3)


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    start_time = get_time()
    req_3 = model.req_3(control)
    end_time = get_time()
    delta_t = delta_time(start_time, end_time)
    return req_3, round(delta_t, 3)


def req_4(control, origen, destino):
    """
    Retorna el resultado del requerimiento 4
    """
    start_time = get_time()
    req_4 = model.req_4(control, origen, destino)
    end_time = get_time()
    delta_t = delta_time(start_time, end_time)
    return req_4, round(delta_t, 3)




def req_6(control, fecha_inicial, fecha_final, sexo):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    start_time = get_time()
    req_6 = model.req_6(control, fecha_inicial, fecha_final, sexo )
    end_time = get_time()
    delta_t = delta_time(start_time, end_time)
    return req_6, round(delta_t, 3)


def req_7(control, fecha_inicial, fecha_final, temp_min, temp_max):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    start_time = get_time()
    req_7 = model.req_7(control, fecha_inicial, fecha_final, temp_min, temp_max )
    end_time = get_time()
    delta_t = delta_time(start_time, end_time)
    return req_7, round(delta_t, 3)



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
