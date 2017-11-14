#!/usr/bin/env python

# -*- coding: utf-8 -*-
#RIASC Tool For Removing Redundancies(RTRR), a tool for erasing variables of type 1, type 2 and type 3.
#Copyright (C) 2017  by RIASC Universidad de Leon(Miguel Carriegos Vieira, Noemi De Castro Garcia, Angel Luis Munoz, Mario Fernandez Rodriguez)
#This file is part of RIASC Tool for Removing Redundancies (RTRR)
#RTRR is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#RTRR is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.
import sys
import zipimport

importer = zipimport.zipimporter('utilities.zip')
uf1 = importer.load_module('utilidades_fase_I')

separador_fichero = sys.argv[2]
separador_elementos = sys.argv[2] +sys.argv[2]
separador_ficheros_auxiliares = '\n'
fichero_variables_csv= sys.argv[3] #'variables_csv'
fichero_variables_eliminadas= sys.argv[4] #'variables_muestra_eliminadas'
fichero_matriz_asociada= sys.argv[5] #'matriz_asociada'

#obtenemos la lista completa de variables del csv para crear un diccionario que asocie las posiciones en el csv con las variables
lista_variables_csv = uf1.obtener_lista_variables_fichero(fichero_variables_csv,separador_ficheros_auxiliares)
diccionario_variables = uf1.generar_diccionario_variables_indices_csv(lista_variables_csv)

#obtenemos la lista de variables eliminadas
variables_eliminadas = uf1.obtener_lista_variables_fichero(fichero_variables_eliminadas,separador_ficheros_auxiliares)

#generamos las matrices de adyacencia y asociada
matrices_adyacencia_asociada = uf1.generar_matriz_adyacencia_y_asociada(fichero_matriz_asociada) #devuelve una lista con dos listas.La matriz de adyacencia y la matriz asociada
matriz_adyacencia = matrices_adyacencia_asociada[0] #matriz de aydacencia
matriz_asociada = matrices_adyacencia_asociada[1] #matriz nombres_apellidos asociada a matriz de ayacencia

#creamos un diccionario que permita obtener la posicion de una variable(nombre o nombre con apellido) en la matriz de adyacencia
diccionario_variables_posicion_matriz = uf1.generar_diccionario_relacion_madyacencia_masociada(matriz_asociada)

for linea in sys.stdin:
    linea = linea.strip()
    linea = linea.split(separador_fichero)
    if (len(linea) > 1) and (sys.argv[1] not in linea): # si la linea no tiene nada raro (un salto de linea unicamente o similar) ni es la primera linea (la de las variables) entonces que la procese
        matriz_pesos = uf1.generar_matriz_pesos(linea,variables_eliminadas,diccionario_variables,matriz_adyacencia,diccionario_variables_posicion_matriz)
        instancia = "["
        for fila in range(len(matriz_pesos)):
            instancia+="["
            for columna in range(len(matriz_pesos[fila])):
                if (columna <= len(matriz_pesos[fila])-2):
                    instancia+= str(matriz_pesos[fila][columna])+separador_elementos
                else: # es el ultimo elemento, hay que poner el corchete de cierre
                    if(fila <= len(matriz_pesos)-2):
                        instancia+= str(matriz_pesos[fila][columna])+"], "
                    else:
                        instancia+= str(matriz_pesos[fila][columna])+"]]"
        print 0,"\t",instancia #print linea[len(linea)-1],"\t",matriz_pesos
