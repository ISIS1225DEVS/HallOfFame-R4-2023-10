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


def new_model():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    mod = {'model': model.new_data_structs()}
    return mod


# Funciones para la carga de datos

def load_data(mod_, filenames):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    
    mod = mod_['model']
    
    filename_individuals = filenames['individuals']
    file_individuals = csv.DictReader(open(filename_individuals, encoding = 'utf-8'), delimiter = ',')
    
    filename_tracks = filenames['tracks']
    file_tracks = csv.DictReader(open(filename_tracks, encoding='utf-8'), delimiter = ',')
    
    latitudes = mod['latitudes']
    longitudes = mod['longitudes']
    
    start_time = get_time()
    rec_wolves = 0
    for wolf_individual in file_individuals:
        model.add_wolf_individual(mod, wolf_individual)
        rec_wolves += 1
    
    num_events = 0
    for wolf_track in file_tracks:
        num_events += 1
        model.add_wolf_track(mod, wolf_track)
    
    nums_vert1 = model.gr.numVertices(mod['wolf_tracks_graph'])
    nums_edg1 = model.gr.numEdges(mod['wolf_tracks_graph'])
    
    latitud_min = min(latitudes)
    latitud_max = max(latitudes)
    longitud_min = min(longitudes)
    longitud_max = max(longitudes)
    
    puntos_encuentro = mod['MTPs']

    
    
    
    model.trace_paths(mod)
    end_time = get_time()
    
    nums_edg2 = model.gr.numEdges(mod['wolf_tracks_graph'])
  
    list_first_last = model.first_last_n_elems_list(puntos_encuentro, 5)
    
    list_last_first_n_mtps = model.lt.newList('ARRAY_LIST')

    for elem in model.lt.iterator(list_first_last):
        dict_MTP = {}
        dict_MTP['Identificador'] = elem
        dict_MTP['Ubicación aprox'] = model.id_to_coords(elem)
        dict_MTP['Número de lobos en esa ubicación'] = model.gr.outdegree(mod['wolf_tracks_graph'], elem)
        dict_MTP['Lobos adyacientes'] = []
        for elem in model.lt.iterator(model.gr.adjacents(mod['wolf_tracks_graph'], elem)):
            dict_MTP['Lobos adyacientes'].append(elem)
        model.lt.addLast(list_last_first_n_mtps, dict_MTP)
        
    dict_result = {}
    dict_result['total_vertices'] = nums_vert1
    dict_result['total_aristas'] = nums_edg2
    dict_result['lobos_reconocidos'] = rec_wolves
    dict_result['eventos_cargados']= num_events
    dict_result['lobos_asociados_MTPs'] = int(nums_edg1/2)
    dict_result['num_puntos_encuentro'] = model.lt.size(puntos_encuentro)
    dict_result['arcos_seguimiento'] = nums_edg2-int(nums_edg1/2)
    dict_result['latitud_min'] = latitud_min
    dict_result['latitud_max'] = latitud_max
    dict_result['longitud_min'] = longitud_min
    dict_result['longitud_max'] = longitud_max
    dict_result['list_mtps'] = list_last_first_n_mtps
    dict_result['time'] = delta_time(start_time, end_time)
    

    return dict_result
    
    


# Funciones de consulta sobre el catálogo

def get_wolf_individual(model, animal_id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(mod_, punto_partida, punto_llegada):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    mod = mod_['model']
    start_time = get_time()
    result = model.req_1(mod, punto_partida, punto_llegada)
    end_time = get_time()
    time = delta_time(start_time, end_time)
    return result, time


def req_2(mod_, punto_partida, punto_llegada):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    mod = mod_['model']
    start_time = get_time()
    result = model.req_2(mod, punto_partida, punto_llegada)
    end_time = get_time()
    time = delta_time(start_time, end_time)
    return result, time


def req_3(mod_):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    mod = mod_['model']
    start_time = get_time()
    result = model.req_3(mod)
    end_time = get_time()
    time = delta_time(start_time, end_time)
    return result, time


def req_4(model):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(mod_,punto_partida, distancia, num_puntos):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    mod = mod_['model']
    start_time = get_time()
    result = model.req_5(mod,punto_partida, distancia, num_puntos)
    end_time = get_time()
    time = delta_time(start_time, end_time)
    return result, time

def req_6(mod_, initial_date, final_date, animal_sex):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    mod = mod_['model']
    start_time = get_time()
    result = model.req_6(mod, initial_date, final_date, animal_sex)
    end_time = get_time()
    time = delta_time(start_time, end_time)
    return result, time


def req_7(mod_, initial_date, final_date, minimum_temp, maximum_temp):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    mod = mod_['model']
    start_time = get_time()
    result = model.req_7(mod, initial_date, final_date, minimum_temp, maximum_temp)
    end_time = get_time()
    time = delta_time(start_time, end_time)
    return result, time


def req_8(mod_):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    mod = mod_['model']
    start_time = get_time()
    result = model.req_8(mod)
    end_time = get_time()
    time = delta_time(start_time, end_time)
    return result, time


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
