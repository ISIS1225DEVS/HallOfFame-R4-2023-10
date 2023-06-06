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
from DISClib.ADT import graph as gr
assert cf
from tabulate import tabulate
import traceback
import folium
import os
import webbrowser

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
    control = {'control': controller.new_model()}
    return control


def print_menu():
    print("*******************************************")
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
    print("*******************************************")


def load_data(control, file_size):
    """
    Carga los datos
    """
    
    data_by_size = {
        '1': {'individuals': 'Data/BA-Grey-Wolf-individuals-utf8-small.csv', 'tracks': 'Data/BA-Grey-Wolf-tracks-utf8-small.csv'},
        '2': {'individuals': 'Data/BA-Grey-Wolf-individuals-utf8-5pct.csv', 'tracks': 'Data/BA-Grey-Wolf-tracks-utf8-5pct.csv'},
        '3': {'individuals': 'Data/BA-Grey-Wolf-individuals-utf8-10pct.csv', 'tracks': 'Data/BA-Grey-Wolf-tracks-utf8-10pct.csv'},
        '4': {'individuals': 'Data/BA-Grey-Wolf-individuals-utf8-20pct.csv', 'tracks': 'Data/BA-Grey-Wolf-tracks-utf8-20pct.csv'},
        '5': {'individuals': 'Data/BA-Grey-Wolf-individuals-utf8-30pct.csv', 'tracks': 'Data/BA-Grey-Wolf-tracks-utf8-30pct.csv'},
        '6': {'individuals': 'Data/BA-Grey-Wolf-individuals-utf8-50pct.csv', 'tracks': 'Data/BA-Grey-Wolf-tracks-utf8-50pct.csv'},
        '7': {'individuals': 'Data/BA-Grey-Wolf-individuals-utf8-80pct.csv', 'tracks': 'Data/BA-Grey-Wolf-tracks-utf8-80pct.csv'},
        '8': {'individuals': 'Data/BA-Grey-Wolf-individuals-utf8-large.csv', 'tracks': 'Data/BA-Grey-Wolf-tracks-utf8-large.csv'}
    }
    load_data_return = controller.load_data(control['control'], data_by_size[file_size])
    
    lobos_reconocidos =  load_data_return['lobos_reconocidos']
    num_eventos_cargados = load_data_return['eventos_cargados']
    numero_lobos_en_puntos_encuentro = load_data_return['lobos_asociados_MTPs']
    numero_puntos_encuentro = load_data_return['num_puntos_encuentro']
    num_arcos_seguimiento = load_data_return['arcos_seguimiento']
    latitud_min = load_data_return['latitud_min']
    latitud_max = load_data_return['latitud_max']
    longitud_min = load_data_return['longitud_min']
    longitud_max = load_data_return['longitud_max']
    lista_first_last = load_data_return['list_mtps']
    time = load_data_return['time']
    vertices = load_data_return['total_vertices']
    aristas = load_data_return['total_aristas']

    print('Hay ', lobos_reconocidos, ' lobos reconocidos en el estudio')
    print('Se cargaron ', num_eventos_cargados, ' eventos')
    print('Hay ', numero_puntos_encuentro, ' puntos de encuentro reconocidos en el estudio')
    print('Hay ', numero_lobos_en_puntos_encuentro, ' puntos de seguimiento en el grafo')
    print('Hay ', num_arcos_seguimiento, ' arcos creados entre los puntos de seguimiento de los lobos')
    print('Hay ', vertices, ' vertices en el grafo')
    print('Hay ', aristas, ' aristas en el grafo')
    print('Los lobos ocupan un área entre las latitudes', latitud_min, ' y ', latitud_max, ' y las longitudes', longitud_min, ' y ', longitud_max)
    print(tabulate_disclib_list(lista_first_last))
    print('Este requerimiento tomó ', time, ' ms')
    print('\n')
    
def tabulate_disclib_list(list, columns = None, widths = 15):
    list_python = []
    if columns != None:
        for elem in lt.iterator(list):
            dict_result = {}
            for column in columns:
                 dict_result[column] = elem[column]
            list_python.append(dict_result)
    else:
        for elem in lt.iterator(list):
            list_python.append(elem)
    return tabulate(list_python, headers = 'keys', tablefmt='heavy_grid', maxcolwidths=widths, maxheadercolwidths=widths)



def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    

def print_req_1(control, punto_partida, punto_llegada):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    result = controller.req_1(control['control'], punto_partida, punto_llegada)[0]
    time = controller.req_1(control['control'], punto_partida, punto_llegada)[1]
    print(tabulate_disclib_list(result[0]))
    print('La distancia entre los puntos es de', result[1],'km si se viaja por el camino encontrado')
    print('En esta ruta, hay ', result[2], ' puntos de seguimiento entre estos dos puntos en esta ruta')
    print('Este requerimiento tomó ', time, ' ms')
    
    path = result[3]
    
    map = folium.Map(location=[57.5, -112.5], zoom_start=8)
    size = lt.size(path)
    count = 0
    for vertex in lt.iterator(path):
        count += 1
        vertex_latitude = controller.model.id_to_coords(vertex)[0]
        vertex_longitude = controller.model.id_to_coords(vertex)[1]
        
        if controller.model.is_MTP(vertex):
            folium.Marker(location = [vertex_latitude, vertex_longitude], icon=folium.Icon(color = 'blue'), popup = vertex).add_to(map)
        else:
            folium.Marker(location = [vertex_latitude, vertex_longitude], icon=folium.Icon(color = 'red'), popup = vertex).add_to(map)
        if count != size:
            next_vertex = lt.getElement(path, count+1)
            next_vertex_latitude = controller.model.id_to_coords(next_vertex)[0]
            next_vertex_longitude = controller.model.id_to_coords(next_vertex)[1]
            folium.PolyLine([(vertex_latitude, vertex_longitude),(next_vertex_latitude, next_vertex_longitude)], color='black').add_to(map)
        
    map.save('mapa_lobos.html')
    
    webbrowser.open_new_tab('file:///' + os.getcwd()+'/'+'mapa_lobos.html')
    
    os.remove('mapa_lobos.html')
    


def print_req_2(control, punto_partida, punto_llegada):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    result = controller.req_2(control['control'], punto_partida, punto_llegada)[0]
    time = controller.req_2(control['control'], punto_partida, punto_llegada)[1]
    print(tabulate_disclib_list(result[0]))
    print('La distancia entre los puntos es de', result[1],'km si se viaja por el camino encontrado')
    print('En esta ruta, hay ', result[2], ' puntos de seguimiento entre estos dos puntos en esta ruta')
    print('Este requerimiento tomó ', time, ' ms')
    
    path = result[3]
    
    map = folium.Map(location=[57.5, -112.5], zoom_start=8)
    size = lt.size(path)
    count = 0
    for vertex in lt.iterator(path):
        count += 1
        vertex_latitude = controller.model.id_to_coords(vertex)[0]
        vertex_longitude = controller.model.id_to_coords(vertex)[1]
        
        if controller.model.is_MTP(vertex):
            folium.Marker(location = [vertex_latitude, vertex_longitude], icon=folium.Icon(color = 'blue'), popup = vertex).add_to(map)
        else:
            folium.Marker(location = [vertex_latitude, vertex_longitude], icon=folium.Icon(color = 'red'), popup = vertex).add_to(map)
        if count != size:
            next_vertex = lt.getElement(path, count+1)
            next_vertex_latitude = controller.model.id_to_coords(next_vertex)[0]
            next_vertex_longitude = controller.model.id_to_coords(next_vertex)[1]
            folium.PolyLine([(vertex_latitude, vertex_longitude),(next_vertex_latitude, next_vertex_longitude)], color='black').add_to(map)
        
    map.save('mapa_lobos.html')
    
    webbrowser.open_new_tab('file:///' + os.getcwd()+'/'+'mapa_lobos.html')
    
    os.remove('mapa_lobos.html')

def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    result = controller.req_3(control['control'])[0]
    time = controller.req_3(control['control'])[1]
    num_manadas = result[0]

    print('Se encontraron ', num_manadas, ' manadas')
    
    datos_manadas = controller.model.first_last_n_elems_list(result[1],5)
    for manada in lt.iterator(datos_manadas):
        lista_lobos = manada['Primeros y últimos tres lobos en la manada']
        manada['Primeros y últimos tres lobos en la manada'] = tabulate_disclib_list(lista_lobos, widths = [])
        
    print(tabulate_disclib_list(datos_manadas,widths=[7,7,20,7,7,7,7,7]))
    
    print('Este requerimiento tomó ', time, ' ms')
    
    colors = {1:'red', 2:'blue',  3:'green', 4:'purple', 5:'orange', 6:'darkred',6:'lightred', 7:'beige', 8:'darkblue',9: 'darkgreen',10: 'cadetblue', 11:'darkpurple', 12:'white', 13:'pink', 14:'lightblue', 15:'lightgreen', 16:'gray', 17:'black', 18:'lightgray'}
    
    mapa_manadas = result[2]
    map = folium.Map(location=[57.5, -112.5], zoom_start=8)
    
    for num_manada in lt.iterator(mp.keySet(mapa_manadas)):
        color_manada = colors[num_manada%18 + 1]
        tracks_manada = me.getValue(mp.get(me.getValue(mp.get(mapa_manadas, num_manada)),'todos'))
        for vertex in lt.iterator(tracks_manada):
            vertex_latitude = controller.model.id_to_coords(vertex)[0]
            vertex_longitude = controller.model.id_to_coords(vertex)[1]
            folium.Marker(location = [vertex_latitude, vertex_longitude], icon=folium.Icon(color = color_manada), popup = vertex).add_to(map)
            
    map.save('mapa_lobos.html')
    
    webbrowser.open_new_tab('file:///' + os.getcwd()+'/'+'mapa_lobos.html')
    
    os.remove('mapa_lobos.html')
        
        

def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control,punto_partida, distancia, num_puntos):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    result = controller.req_5(control['control'], punto_partida, distancia, num_puntos)
    time = result[1]
    result = result[0]
    
    print('La maxima distancia recorrida es de', input_distancia_req5 ,'km')
    print('El minimo de puntos que el guardabosques desea recorrer ', input_puntos)
    print('hay  ', result[0], ' posibles caminos desde el punto de origen  ', input_punto_inicial_req5)
    
    info = result[0]
    print(tabulate_disclib_list(list = info, columns=['points count', 'path distance km', 'point list', 'animal count']))
    print('Este requerimiento tomó ', time, ' ms')


def print_req_6(control, initial_date, final_date, animal_sex):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    cont_result = controller.req_6(control['control'], initial_date, final_date, animal_sex)
    time = cont_result[1]
    result = cont_result[0]
    
    print('El lobo que menos distancia recorrió fue: ')
    min_info = result[0]
    print(tabulate_disclib_list(list = min_info, columns=['individual-id', 'animal-taxon', 'animal-life-stage', 'animal-sex', 'study-site', 'deployment-comments']))
    
    print('El lobo que más disancia recorrió fue: ')
    max_info = result[1]
    print(tabulate_disclib_list(list =max_info, columns=['individual-id', 'animal-taxon', 'animal-life-stage', 'animal-sex', 'study-site', 'deployment-comments']))
    
    print('Información camino más largo lobo que menos recorrió')
    print('Distancia recorrida: ', result[4])
    print('Número de aristas: ',result[5])
    print('Número de vértices: ', result[6])
    
    print(tabulate_disclib_list(result[2]))
    
    print('Información camino más largo lobo que más recorrió')
    print('Distancia recorrida: ', result[7])
    print('Número de aristas: ',result[8])
    print('Número de vértices: ', result[9])
    
    print(tabulate_disclib_list(result[3]))
    
    print('Este requerimiento tomó: ', time, 'ms')
    
    
    

def print_req_7(control, fecha_inic, fecha_fin, temp_min, temp_max):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    result = controller.req_7(control['control'], fecha_inic, fecha_fin, temp_min, temp_max)[0]
    time = controller.req_7(control['control'], fecha_inic, fecha_fin, temp_min, temp_max)[1]
    num_manadas = result[0]
    
    print('Se encontraron ', num_manadas, ' manadas')
    print('El grafo tiene ', result[4], ' vertices')
    print('El grafo tiene ', result[5], ' aristas')
    datos_manadas = controller.model.first_last_n_elems_list(result[1],3)
    for manada in lt.iterator(datos_manadas):
        lista_lobos = manada['Primeros y últimos tres lobos en la manada']
        manada['Primeros y últimos tres lobos en la manada'] = tabulate_disclib_list(lista_lobos, widths = [])
        
    print(tabulate_disclib_list(datos_manadas,widths=[7,7,20,7,7,7,7,7]))
    print(tabulate_disclib_list(result[3]))
    print('Este requerimiento tomó ', time, ' ms')
    
    colors = {1:'red', 2:'blue',  3:'green', 4:'purple', 5:'orange', 6:'darkred',6:'lightred', 7:'beige', 8:'darkblue',9: 'darkgreen',10: 'cadetblue', 11:'darkpurple', 12:'white', 13:'pink', 14:'lightblue', 15:'lightgreen', 16:'gray', 17:'black', 18:'lightgray'}
    
    mapa_manadas = result[2]
    map = folium.Map(location=[57.5, -112.5], zoom_start=8)
    
    for num_manada in lt.iterator(mp.keySet(mapa_manadas)):
        color_manada = colors[num_manada%18 + 1]
        tracks_manada = me.getValue(mp.get(me.getValue(mp.get(mapa_manadas, num_manada)),'todos'))
        for vertex in lt.iterator(tracks_manada):
            vertex_latitude = controller.model.id_to_coords(vertex)[0]
            vertex_longitude = controller.model.id_to_coords(vertex)[1]
            folium.Marker(location = [vertex_latitude, vertex_longitude], icon=folium.Icon(color = color_manada), popup = vertex).add_to(map)
            
    map.save('mapa_lobos.html')
    
    webbrowser.open_new_tab('file:///' + os.getcwd()+'/'+'mapa_lobos.html')
    
    os.remove('mapa_lobos.html')


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    result = controller.req_8(control['control'])[0]
    map_tracks = result[0]
    mtps = result[1]
    

    map = folium.Map(location=[57.5, -112.5], zoom_start=8)
    


    
    for wolf in lt.iterator(mp.keySet(map_tracks)):
        list_tracks = me.getValue(mp.get(map_tracks, wolf))
        size = lt.size(list_tracks)
        count = 0
        

        for track in lt.iterator(list_tracks):
            count += 1
            vertex = track['animal-seg-id']
            vertex_latitude = controller.model.id_to_coords(vertex)[0]
            vertex_longitude = controller.model.id_to_coords(vertex)[1]
            
            folium.Marker([vertex_latitude, vertex_longitude], color='blue', popup=vertex).add_to(map)
            
            if count != size:
                next_track = lt.getElement(list_tracks, count + 1)
                next_vertex = next_track['animal-seg-id']
                next_vertex_latitude = controller.model.id_to_coords(next_vertex)[0]
                next_vertex_longitude = controller.model.id_to_coords(next_vertex)[1]
                folium.PolyLine([(vertex_latitude,vertex_longitude),(next_vertex_latitude,next_vertex_longitude)], color='black').add_to(map)
    
    for MTP_ in lt.iterator(mtps):
        vertex_latitude = controller.model.id_to_coords(MTP_)[0]
        vertex_longitude = controller.model.id_to_coords(MTP_)[1]
        folium.Marker([vertex_latitude, vertex_longitude], color='red', popup=MTP_).add_to(map)     
    
    map.save('mapa_lobos.html')
    
    webbrowser.open_new_tab('file:///' + os.getcwd()+'/'+'mapa_lobos.html')
    
    os.remove('mapa_lobos.html')


# Se crea el controlador asociado a la vista

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
                control = new_controller()
                print('1- 1%')
                print('2- 5%')
                print('3- 10%')
                print('4- 20%')
                print('5- 30%')
                print('6- 50%')
                print('7- 80%')
                print('8- 100%')
                input_file_size = input('Seleccione un tamaño de datos: ')
                try:
                    if int(input_file_size) <= 8 and int(input_file_size) >= 1:
                        input_file_size = input_file_size
                except Exception as exp:
                    print("ERR:", exp)
                    traceback.print_exc()
                print("Cargando información de los archivos ....\n")
                load_data(control = control, file_size = input_file_size)
                
            elif int(inputs) == 2:
                input_punto_inicial_req1 = input('Ingrese un punto de partida: ')
                input_punto_final_req1 = input('Ingrese un punto de llegada: ')
                print_req_1(control, input_punto_inicial_req1, input_punto_final_req1)

            elif int(inputs) == 3:
                input_punto_inicial_req2 = input('Ingrese un punto de partida: ')
                input_punto_final_req2 = input('Ingrese un punto de llegada: ')
                print_req_2(control, input_punto_inicial_req2, input_punto_final_req2)

            elif int(inputs) == 4:
                print_req_3(control)

            elif int(inputs) == 5:
                print_req_4(control)

            elif int(inputs) == 6:
                input_punto_inicial_req5 = input('Ingrese un punto de partida: ')
                input_distancia_req5 = input('Ingrese un Distancia que puede recorrer el guardabosques desde el punto de origen: ')
                input_puntos=input("número mínimo de puntos de encuentros que el guardabosques desea inspeccionar: ")
                print_req_5(control, input_punto_inicial_req5,input_distancia_req5,input_puntos)

            elif int(inputs) == 7:
                input_fecha_incial_req_6 = input('Ingrese una fecha inicial: ')
                input_fecha_final_req_6 = input('Ingrese una fecha final: ')
                input_sexo_req_6 = input('Ingrese un sexo a consultar: ')
                print_req_6(control, input_fecha_incial_req_6, input_fecha_final_req_6, input_sexo_req_6)


            elif int(inputs) == 8:
                input_fecha_incial_req_7 = input('Ingrese una fecha inicial: ')
                input_fecha_final_req_7 = input('Ingrese una fecha final: ')
                input_temp_min_req_7 = float(input('Ingrese una temperatura mínima: '))
                input_temp_max_req_7 = float(input('Ingrese una temperatura máxima: '))
                print_req_7(control, input_fecha_incial_req_7, input_fecha_final_req_7, input_temp_min_req_7, input_temp_max_req_7)

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
