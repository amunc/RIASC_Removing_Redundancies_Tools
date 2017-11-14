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

#----------------------------------Funciones realtivas a la Fase Eliminacion Redundancias de tipo 2------------------------------

#funcion que permite comparar una instancia de la matriz de pesos con la siguiente hasta llegar a la ultima y que devuelve una unica instancia
#a modo de resumen, de forma que el resultado es una instancia en la que los valores son 'no_redundante' (si alguna de las instancias presenta un valor distinto al acumulado para esa variable)
#o un valor distinto de 'no_redundante' lo que supondría que todos los valores para esa variable son el mismo
#la funcion recibe como parametro la matriz general de pesos:
#matriz_general pesos = [[matriz_pesos_instancia_1][matriz_pesos_instancia_2]...[matriz_pesos_instancia_n]]
#matriz_pesos_instancia_1 = [[nombres][nombres_apellidos][apellidos]]


def comparar_instancias(matriz_general_pesos):
    palabra_reservada = 'no_redundante'
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
                    if(instancia_resultado[fila_instancia][columna_instancia] != palabra_reservada):
                        if(matriz_general_pesos[instancias][fila_instancia][columna_instancia] != instancia_resultado[fila_instancia][columna_instancia]):
                            instancia_resultado[fila_instancia][columna_instancia] = palabra_reservada
                            
    return instancia_resultado

#funcion que permite obtener la lista con las variables que resultan ser redundantes, devuelve una matriz de listas
def obtener_lista_variables_redundantes(instancia_final,diccionario_posiciones_variables_matriz):
    palabra_reservada = 'no_redundante'
    lista_variables_redundantes = []
    variables_redundantes_t1 = [] #si son vacias
    variables_redundantes_t2 = [] # si son constantes
    for fila in range(len(instancia_final)):
        for columna in range(len(instancia_final)):
            elemento = instancia_final[fila][columna]
            if(str(elemento) != "0" and elemento != palabra_reservada):
                lista_variables_redundantes.append(diccionario_posiciones_variables_matriz[fila,columna])
                if(str(elemento).strip() == "'nan'" ):
                    variables_redundantes_t1.append(diccionario_posiciones_variables_matriz[fila,columna])
                else:
                    variables_redundantes_t2.append(diccionario_posiciones_variables_matriz[fila,columna])
    return [sorted(variables_redundantes_t1),sorted(variables_redundantes_t2)]
