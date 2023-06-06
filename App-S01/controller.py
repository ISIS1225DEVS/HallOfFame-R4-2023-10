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
import datetime

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller(data_type):
    """
    Crea una instancia del modelo
    """
    control = {
        "model": None
    }

    control["model"] = model.new_data_structs(data_type)
    return control

def load_data(control, filename_1, filename_2):
    filename_1 = cf.data_dir + filename_1
    filename_2 = cf.data_dir + filename_2
    input_file_1 = csv.DictReader(open(filename_1, encoding = 'utf-8'))
    input_file_2 = csv.DictReader(open(filename_2, encoding = 'utf-8'))
    
    for carga_1 in input_file_1:
        load_data_wolfs_tracks(control, carga_1)
        #load_data_timestamp(control, carga_1)
        
    for carga_2 in input_file_2:
        load_data_wolfs_info(control, carga_2)
    
    arcos_encuentro = model.crearGrafoEncuentro(control["model"])
    arcos_seguimiento = model.crearGrafoSeguimiento(control["model"])

    return control, arcos_encuentro, arcos_seguimiento

def load_data_wolfs_tracks(control, carga):

    return model.add_wolfs_tracks(control["model"], carga)

def load_data_wolfs_info(control,carga):

    return model.add_wolfs_info(control["model"], carga)

def load_data_timestamp(control, carga):

    return model.add_timestamp(control["model"], carga)

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

def wolfs_size(control):

    total_wolfs, events, data_wolfs = model.wolfs_size(control["model"])

    return total_wolfs, events, data_wolfs

def wolfs_data_size(control):

    return model.wolfs_data_size(control["model"])

def organizarL(control):

    latitudes, longitudes =  model.organizarL(control['model'])
    return latitudes, longitudes

def req_1(control, initial, destination, modo):
    """
    Retorna el resultado del requerimiento 1
    """
    info = model.req_1(control["model"], initial, destination, modo)
    start_time = get_time()
    model.req_1(control["model"], initial, destination, modo)
    end_time = get_time()
    delta_t = delta_time(start_time, end_time)
    return info, delta_t


def req_2(control, initial, destination):
    """
    Retorna el resultado del requerimiento 2
    """
    q = model.req_2(control["model"], initial, destination)
    start_time = get_time()
    model.req_2(control["model"], initial, destination)
    end_time = get_time()
    delta_t = delta_time(start_time, end_time)
    return q, delta_t

def generateListPath(path, control, remove = False):
    l = model.generateListPath(path, control["model"], remove)
    return l

def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(control, origen_lon, origen_lat, destino_lon, destino_lat):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    p1, p2, d1, d2, trips_edges, nodes, distTo, first_3, last_3 = model.req_4(control["model"],origen_lon, origen_lat, destino_lon, destino_lat)
    start_time = get_time()
    model.req_4(control["model"],origen_lon, origen_lat, destino_lon, destino_lat)
    end_time = get_time()
    delta_t = delta_time(start_time, end_time)
    return p1, p2, d1, d2, trips_edges, nodes, distTo, first_3, last_3, delta_t


def req_5(control, minGathering, maxdistance, origin):
    """
    Retorna el resultado del requerimiento 5
    """
    y = model.req_5(control["model"], minGathering, maxdistance, origin)
    return y

def req_6(control, fecha_inicial, fecha_final, sex):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    fecha_inicial = datetime.datetime.strptime(fecha_inicial, '%Y-%m-%d %H:%M')
    fecha_final = datetime.datetime.strptime(fecha_final, '%Y-%m-%d %H:%M')
    id_menor, distancia_menor, nodos_menor, arcos_menor, first_3_menor, last_3_menor, id_mayor, distancia_mayor, nodos_mayor, arcos_mayor, first_3_mayor, last_3_mayor, contador,t1,t2 =  model.req_6(control['model'], fecha_inicial, fecha_final, sex)
    start_time = get_time()
    model.req_6(control['model'], fecha_inicial, fecha_final, sex)
    end_time = get_time()
    delta_t = delta_time(start_time, end_time)
    return id_menor, distancia_menor, nodos_menor, arcos_menor, first_3_menor, last_3_menor, id_mayor, distancia_mayor, nodos_mayor, arcos_mayor, first_3_mayor, last_3_mayor, contador,t1,t2, delta_t

def req_7(control, lowtime, hightime, lowtemp, hightemp):
    """
    Retorna el resultado del requerimiento 7
    """
    l = model.req_7(control["model"], lowtime, hightime, lowtemp, hightemp)
    return l

def generateListSCC(l, control):
    w1, w2 = model.generateListSCC(l, control["model"])
    return w1, w2

def createListLongest(k):
    o = model.createListLongest(k)
    return o

def req_8_1(control, initial, destination, modo):
    """
    Retorna el resultado del requerimiento 8
    """
    data = model.req_8_1(control["model"], initial, destination, modo)
    return data

def req_8_2(control, initial, destination):
    """
    Retorna el resultado del requerimiento 8
    """
    data = model.req_8_2(control["model"], initial, destination)
    return data

def noFormat(str):
    str1, str2 = model.noFormat(str)
    return str1, str2


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
