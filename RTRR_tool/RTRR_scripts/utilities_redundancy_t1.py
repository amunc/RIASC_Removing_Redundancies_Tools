# -*- coding: utf-8 -*-
'''RIASC Tool For Removing Redundancies(RTRR), a tool for erasing variables of type 1, type 2 and type 3.
Copyright (C) 2017  by RIASC Universidad de Leon(Miguel Carriegos Vieira, Noemi De Castro García, Angel Luis Muñoz, Mario Fernandez Rodriguez)
This file is part of RIASC Tool for Removing Redundancies (RTRR)

RTRR is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RTRR is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.'''

import csv
import pandas as pd
#----------------------------------Funciones realtivas a la Fase Eliminacion Redundancias de tipo 1------------------------------

#funcion que permite comparar una instancia de la matriz de pesos con la siguiente hasta llegar a la ultima y que devuelve una unica instancia
#a modo de resumen, de forma que el resultado es una instancia en la que los valores son 'nan' (si todas las instancias presentan 'nan' como valor
#para esa variable) o un valor distinto de 'nan'
#la funcion recibe como parametro la matriz general de pesos:
#matriz_general pesos = [[matriz_pesos_instancia_1][matriz_pesos_instancia_2]...[matriz_pesos_instancia_n]]
#matriz_pesos_instancia_1 = [[nombres][nombres_apellidos][apellidos]]

#funcion que permite crear un diccionario, en base al inicial (variable:[fila,columna]) pero de forma inversa (fila,columna):variable
#permite obtener un diccionario que devuelve variables de la matriz de pesos en funcion de la fila y de la columna
def generar_diccionario_posicion_variables(diccionario):
    diccionario_inverso = {}
    for key in diccionario:
        fila = diccionario[key][0]
        columna = diccionario[key][1]
        diccionario_inverso[fila,columna] = key
    return diccionario_inverso

def comparar_instancias(matriz_general_pesos):
    palabra_reservada = "'nan'"
    instancia_resultado = []
    for instancias in range(len(matriz_general_pesos)):
        if instancias == 0 : # si la instancia es la primera, la igualamos a la instancia resultado
            for fila_instancia in range(len(matriz_general_pesos[0])):
                fila_instancia_resultado =[]
                for columna_instancia in range(len(matriz_general_pesos[0][fila_instancia])):
                    fila_instancia_resultado.append(matriz_general_pesos[0][fila_instancia][columna_instancia])
                instancia_resultado.append(fila_instancia_resultado)
                
        else:# tenemos una instancia completa, comparamos con la siguiente
            for fila_instancia in range(len(matriz_general_pesos[instancias])):
                for columna_instancia in range(len(matriz_general_pesos[instancias][fila_instancia])):
                    if(instancia_resultado[fila_instancia][columna_instancia] == palabra_reservada):
                        if(matriz_general_pesos[instancias][fila_instancia][columna_instancia] != palabra_reservada):
                            instancia_resultado[fila_instancia][columna_instancia] = matriz_general_pesos[instancias][fila_instancia][columna_instancia]
    return instancia_resultado

#funcion que permite obtener la lista con las variables que resultan ser redundantes
def obtener_lista_variables_redundantes(instancia_final,diccionario_posiciones_variables_matriz):
    palabra_reservada = "'nan'"
    lista_variables_redundantes = []
    for fila in range(len(instancia_final)):
        for columna in range(len(instancia_final[fila])):
            elemento = instancia_final[fila][columna]
            if(elemento == palabra_reservada):                
                lista_variables_redundantes.append(diccionario_posiciones_variables_matriz[fila,columna])
    return sorted(lista_variables_redundantes)

#funcion que une la lista de variables eliminadas inicialmente y las nuevas variables eliminadas por ser redundantes
def actualizar_lista_variables_eliminadas(lista_variables_eliminadas,lista_variables_redundantes):
    return lista_variables_eliminadas + lista_variables_redundantes

#funcion que elimina del diccionario las variables redundantes
def actualizar_diccionario(lista_variables_eliminadas,diccionario):
    for variable_eliminada in lista_variables_eliminadas:
        if(variable_eliminada in diccionario):
            del diccionario[variable_eliminada]
    return diccionario

#funcion que genera el csv sin redundancias de tipo 1 ni elementos eliminados
def generar_csv_sin_redundancia(matriz_pesos,diccionario_elemento_posicion,lista_variables_csv,ruta_destino,separador_campos,tipo_fichero):
    csv_final = []
    cabeceras = []
    for instancias in range(len(matriz_pesos)):
        registro_csv_final = []
        if(instancias == 0):
            for variable in lista_variables_csv:
                  if(variable in diccionario_elemento_posicion):
                      cabeceras.append(variable)
            csv_final.append(cabeceras)
        for variable in lista_variables_csv:
            if(variable in diccionario_elemento_posicion): # es decir, si la variable no se ha eliminado del original
                fila = diccionario_elemento_posicion[variable][0]
                columna = diccionario_elemento_posicion[variable][1]
                elemento = matriz_pesos[instancias][fila][columna]
                if (elemento == "'nan'"):
                    elemento = float('nan')
                registro_csv_final.append(elemento)
        csv_final.append(registro_csv_final)
        
    if(tipo_fichero == 'csv'):        
    #creamos el nuevo fichero sin los elementos redundantes
        with open(ruta_destino,'wb') as fichero_csv: 
            writer = csv.writer(fichero_csv,delimiter=separador_campos)
            writer.writerows(csv_final)
            
    elif(tipo_fichero == 'excel'):
        if('xlsx' in ruta_destino):

            writer = pd.ExcelWriter(ruta_destino,engine='xlsxwriter',options={'strings_to_urls': False})
        elif('xls' in ruta_destino):

            writer = pd.ExcelWriter(ruta_destino)
        # Write your DataFrame to a file
        dframe = pd.DataFrame(csv_final)  
        dframe = dframe[1:]
        dframe.columns = cabeceras
        dframe.to_excel(writer, sheet_name='Csv_sin_redundancias',index=False)    
        writer.save()
    return csv_final

def recodificar_lista_variables_redundantes(lista_variables_redundantes,lista_variables_modificadas):
    for fila in range(len(lista_variables_modificadas)):
        if(lista_variables_modificadas[fila][1] in lista_variables_redundantes):
            posicion = lista_variables_redundantes.index(lista_variables_modificadas[fila][1])
            lista_variables_redundantes[posicion] = lista_variables_modificadas[fila][0]
    return lista_variables_redundantes
