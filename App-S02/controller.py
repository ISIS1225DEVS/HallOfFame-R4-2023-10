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
    return model.new_data_structs()

def new_controller2():
    """
    Crea una instancia del modelo
    """
    return model.new_data_structs2()


# Funciones para la carga de datos

def load_data(analyzer, filename, filename2):
    """
    Carga los datos del reto
    """
    filename = cf.data_dir + filename
    input_file = csv.DictReader(open(filename, encoding="utf-8"),
                                delimiter=",")
    for event in input_file:
        event["ID"]=model.enFormatoID(event)
        event["formatoNodo"]=model.enFormato(event)
        event["latLong"]=model.enFormatoLatLong(event)
        model.add_data1(analyzer,event)
    model.sortListByTime(analyzer)
    model.addGraph(analyzer)
    model.addMeetingPoint(analyzer)

    filename2 = cf.data_dir + filename2
    input_file2 = csv.DictReader(open(filename2, encoding="utf-8"),
                                delimiter=",")
    for event in input_file2:
        event["ID"]=model.enFormatoID2(event)
        model.add_dataFile2(analyzer,event)
    return analyzer

def load_data2(analyzer, filename, filename2):
    """
    Carga los datos del reto
    """
    start=input("Digite la fecha inicial: ")
    end=input("Digite la fecha final: ")
    min=float(input("Digite la temperatura mínima: "))
    max=float(input("Digite la temperatura máxima: "))

    filename = cf.data_dir + filename
    input_file = csv.DictReader(open(filename, encoding="utf-8"),
                                delimiter=",")
    for event in input_file:
        event["ID"]=model.enFormatoID(event)
        event["formatoNodo"]=model.enFormato(event)
        event["latLong"]=model.enFormatoLatLong(event)
        if model.evaluarTiempoYClima(event,start,end,min,max)==True:
             model.add_data1(analyzer,event)
    model.sortListByTime(analyzer)
    model.addGraph(analyzer)
    model.addMeetingPoint(analyzer)

    filename2 = cf.data_dir + filename2
    input_file2 = csv.DictReader(open(filename2, encoding="utf-8"),
                                delimiter=",")
    for event in input_file2:
        event["ID"]=model.enFormatoID2(event)
        model.add_dataFile2(analyzer,event)

    return analyzer
        

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


def req_1(analyzer,punto1,punto2):
    """
    Retorna el resultado del requerimiento 1
    """
    return model.req_1(analyzer,punto1,punto2)


def req_2(control):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(analyzer):
    """
    Retorna el resultado del requerimiento 3
    """
    return model.req_3(analyzer)


def req_4(control, punto1, punto2):
    """
    Retorna el resultado del requerimiento 4
    """
    
    return model.req_4(control, punto1, punto2)
    


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(analyzer):
    """
    Retorna el resultado del requerimiento 6
    """
    sexo=input("Digite el sexo de interes: ")
    start=input("Digite la fecha inicial: ")
    end=input("Digite la fecha final: ")
    return model.req_6(analyzer,sexo,start,end)


def req_7(control):
    """
    Retorna el resultado del requerimiento 7
    """
    return model.req_7(control)


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

def buscarInfo(analyzer,nodo):
    return model.buscarInfo(analyzer,nodo)
