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

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = model.new_data_structs()
    return control


# Funciones para la carga de datos

def load_data(control, filename):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    start_time = get_time()
    filename = cf.data_dir + "wolfs/BA-Grey-Wolf-tracks-utf8"+filename+".csv"
    input_file = csv.DictReader(open(filename, encoding="utf-8"),
                                delimiter=",")
    data2 = None
    for Data in input_file:
        model.add_data(control, Data)
    stop_time = get_time()
    delta_Time = delta_time(start_time, stop_time)
    
    return control, delta_Time

def load_data_2(control,filename):
    start_time = get_time()
    filename = cf.data_dir + "wolfs/BA-Grey-Wolf-individuals-utf8"+filename+".csv"
    input_file = csv.DictReader(open(filename, encoding="utf-8"),
                                delimiter=",")
    data2 = None
    for Data in input_file:
        model.add_data2(control, Data)
    stop_time = get_time()
    delta_Time = delta_time(start_time, stop_time)
    return control, delta_Time

def auxiliar_c(control):
    start_time = get_time()
    controla = model.auxiliar(control)
    stop_time = get_time()
    delta_Time = delta_time(start_time, stop_time)
    return controla, delta_Time
def puntos_enc(control):
    start_time = get_time()
    controlar = model.puntos_enc_m(control)
    stop_time = get_time()
    delta_Time = delta_time(start_time, stop_time)
    return controlar, delta_Time
def conectar_pe(control):
    start_time = get_time()
    controlare = model.conectar_p_encu(control)
    stop_time = get_time()
    delta_Time = delta_time(start_time, stop_time)
    return controlare, delta_Time
def tabla(control):
    start_time = get_time()
    tabla = model.primeros_ultimos(control)
    stop_time = get_time()
    delta_Time = delta_time(start_time, stop_time)
    return tabla, delta_Time

"""def LOAD_DATA(control, filename):
    load_data(control, filename)
    load_data_2(control, filename)
    auxiliar_c(control)
    puntos_enc(control)
    conectar_pe(control)"""
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


def req_1(control, vertexA, vertexB):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    start_time = get_time()
    if model.req_1(control, vertexA, vertexB):
        existe, tama_cam, punto_encuentro, vertices_seg, tabular, distancia = model.req_1(control, vertexA, vertexB)
        stop_time = get_time()
        delta_Time = delta_time(start_time, stop_time)
        return existe, tama_cam, punto_encuentro, vertices_seg, tabular, distancia, delta_Time
    else:
        stop_time = get_time()
        delta_Time = delta_time(start_time, stop_time)
        return False, delta_Time


def req_2(control, vertex_i, vertex_f):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    start_time = get_time()
    if model.req_2(control, vertex_i, vertex_f):
        existe, nodes, puntos_encuentro, vertices_seguidos, tabla, distancia = model.req_2(control, vertex_i, vertex_f)
        stop_time = get_time()
        delta_Time = delta_time(start_time, stop_time)
        return existe, nodes, puntos_encuentro, vertices_seguidos, tabla, distancia, delta_Time
    else:
        stop_time = get_time()
        delta_Time = delta_time(start_time, stop_time)
        return False, delta_Time


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    start_time = get_time()
    conectados, tabular = model.req_3(control)
    stop_time = get_time()
    delta_Time = delta_time(start_time, stop_time)
    return conectados, tabular, delta_Time


def req_4(control, pos_1, pos_2):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    start_time = get_time()
    if model.req_4(control, pos_1, pos_2):
        r4= model.req_4(control, pos_1, pos_2)
        stop_time = get_time()
        delta_Time = delta_time(start_time, stop_time)
        return r4, delta_Time
    else:
        stop_time = get_time()
        delta_Time = delta_time(start_time, stop_time)
        return False, delta_Time
    


def req_5(control, origen, distancia_max, puntos_min):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    return model.req_5(control, origen, distancia_max, puntos_min)

def req_6(control, fecha1, fecha2, sexo):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    start_time = get_time()
    req6_fin = model.req_6(control, fecha1, fecha2, sexo)
    stop_time = get_time()
    delta_Time = delta_time(start_time, stop_time)
    return req6_fin, delta_Time


def req_7(control, fecha1, fecha2, temp1, temp2):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    start_time = get_time()
    req7_fin = model.req_7(control, fecha1, fecha2, temp1, temp2)
    stop_time = get_time()
    delta_Time = delta_time(start_time, stop_time)
    return req7_fin, delta_Time 


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
