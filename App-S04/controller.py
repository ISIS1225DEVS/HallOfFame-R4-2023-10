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
import math

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
csv.field_size_limit(2147483647)

def new_controller():
    """
    Crea una instancia del modelo
    """
    # Llamar la función del modelo que crea las estructuras de datos
    control = {
        "model": None
    }
    control["model"] = model.new_catalog()
    return control

# Funciones para la carga de datos

def load_data(control, filename):
    """
    Carga los datos del reto
    """
    # Realizar la carga de datos
    catalog = control['model']
    # numero de eventos para print
    eventos_analizados = 0
    # cordenadas maximas y minimas para print (lat,lon)S
    lamax = -90
    lamin = 90
    lomax = -180
    lomin = 180
    csvfile = cf.data_dir + filename
    input_file = csv.DictReader(open(csvfile, encoding='utf-8'))
    for row in input_file:
        key = model.data_id_generator(row)
        model.add_data(catalog, key, row)
        if (float(row['location-lat']) > lamax):
            lamax = math.ceil(float(row['location-lat'])*1000)/1000
        if (float(row['location-long']) > lomax):
            lomax = math.ceil(float(row['location-long'])*1000)/1000
        if (float(row['location-lat']) < lamin):
            lamin = math.ceil(float(row['location-lat'])*1000)/1000
        if (float(row['location-long']) < lomin):
            lomin = math.ceil(float(row['location-long'])*1000)/1000
        eventos_analizados += 1
    catalog = model.agrupar_data(catalog)
    
    csvfile_spec = cf.data_dir + 'BA-Grey-Wolf-individuals-utf8-' + filename.split('-')[5]
    input_file_spec = csv.DictReader(open(csvfile_spec, encoding='utf-8'))
    for row in input_file_spec:
        for key in row:
            if row[key].isspace() or len(row[key]) == 0 or row[key].lower() == 'none':
                row[key] = None
        key = model.data_id_generator_spec(row)
        model.add_data_spec(catalog,key,row)
    return catalog,eventos_analizados, lamax, lamin, lomax, lomin

# Funciones de requerimientos

def req_1(control, identificador_origen, identificador_destino):
    """
    Retorna el resultado del requerimiento 1
    """
    # Modificar el requerimiento 1
    return model.req_1(control["model"], identificador_origen, identificador_destino)


def req_2(control, identificador_origen, identificador_destino):
    """
    Retorna el resultado del requerimiento 2
    """
    # Modificar el requerimiento 2
    return model.req_2(control["model"], identificador_origen, identificador_destino)



def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    return model.req_3(control["model"])


def req_4(control, punto_origen, punto_destino):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    return model.req_4(control["model"], punto_origen, punto_destino)


def req_5(control,o,d,m):
    """
    Retorna el resultado del requerimiento 5
    """
    # Modificar el requerimiento 5
    return model.req_5(control['model'],o,d,m)

def req_6(control,fi,ff,g):
    """
    Retorna el resultado del requerimiento 6
    """
    return model.req_6(control['model'],fi,ff,g)


def req_7(control, fi, ff, ti, tf):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    return model.req_7(control["model"], fi, ff, ti, tf)


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

"""
def get_memory():

    toma una muestra de la memoria alocada en instante de tiempo

    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):

    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)

    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
"""

