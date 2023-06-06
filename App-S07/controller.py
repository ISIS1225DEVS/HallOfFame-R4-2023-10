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
import sys
default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    control = {"model": None}
    control["model"] = model.newdatastructs()
    return control



def load_data(control, filename):
    
    if filename == 1:
        tamano = "small"
    if filename == 2:
        tamano = "5pct"
    elif filename == 3:
        tamano = "10pct"
    elif filename == 4:
        tamano = "20pct"
    elif filename == 5:
        tamano = "30pct"
    elif filename == 6:
        tamano = "50pct"
    elif filename == 7:
        tamano = "80pct"
    elif filename == 8:
        tamano = "large"
        
    ruta_muestreo = "BA-Grey-Wolf-tracks-utf8-"+tamano+".csv"
    ruta_indv = "BA-Grey-Wolf-individuals-utf8-"+tamano+".csv"
    datastructs = control["model"]
    booksfile_m= cf.data_dir + ruta_muestreo
    booksfile_i= cf.data_dir + ruta_indv
    csvreader_m = open(booksfile_m, newline="", encoding="utf-8" )
    csvreader_i = open(booksfile_i, newline="", encoding="utf-8" )
    data_m = csv.DictReader(csvreader_m, delimiter=",")
    data_i = csv.DictReader(csvreader_i, delimiter=",")
    

    """Conexiones y puntos de muestreo"""

    for lobo in data_i:
        model.anadir_data(datastructs, lobo)
    
    for punto_m in data_m:
        model.anadir_data1(datastructs, punto_m)
        model.anadir_data2(datastructs, punto_m)
    model.anadir_grafo(datastructs)
    model.anadir_grafo_1(datastructs)
    
    
    return datastructs

def req_1(control, origen, destino):
   
    datastructs = control["model"]
    camino = model.req_1(datastructs, origen, destino)

    return camino, 

def req_2(control, origen, destino):
    start_time= get_time()
    datastructs = control["model"]
    camino = model.req_2(datastructs, origen, destino)
    stop_time = get_time()
    delta_time = delta_time(start_time, stop_time)
    answer= delta_time
    
    return camino, answer


def req_3(control):
    start_time= get_time()
    datastructs = control["model"]
    mapa_idscc, cantidad_componentes=model.req_3(datastructs, "1")
    stop_time = get_time()
    delta_time = delta_time(start_time, stop_time)
    answer= delta_time
    return mapa_idscc, cantidad_componentes, answer


def req_4(control, origen, destino):
    start_time= get_time()
    datastructs = control["model"]
    camino = model.req_4(datastructs, origen, destino)
    stop_time = get_time()
    delta_time = delta_time(start_time, stop_time)
    answer= delta_time
    return camino, answer


def req_5(control, origen, distancia, num_min):
    datastructs = control["model"]
    best, dato_mejor= model.req_5(datastructs, origen, distancia, num_min)

    return best, dato_mejor

def req_6(control, fecha_inicial, fecha_final, sexo):
    datastructs = control["model"]
    model.req_6(datastructs, fecha_inicial, fecha_final, sexo)
    
    return None


def req_7(control, fecha_inicial, fecha_final, tem_min, tem_max):
    datastructs = control["model"]
    model.req7(datastructs, fecha_inicial, fecha_final, tem_min, tem_max)
    return None

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
