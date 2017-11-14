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
import os
import zipimport
import json
import numpy as np

importer = zipimport.zipimporter('utilities.zip')
uf1 = importer.load_module('utilidades_fase_I')
uf2 = importer.load_module('utilidades_fase_II')
ug = importer.load_module('utilidades_generales')

#generacion del grafo
separador_ficheros_auxiliares = "\n"
fichero_matriz_asociada= sys.argv[1] #'matriz_asociada'

matrices_adyacencia_asociada = uf1.generar_matriz_adyacencia_y_asociada(fichero_matriz_asociada)
matriz_adyacencia = matrices_adyacencia_asociada[0] #matriz de aydacencia
matriz_asociada = matrices_adyacencia_asociada[1] #matriz nombres_apellidos asociada a matriz de ayacencia

ruta_fichero_variables_individuales = sys.argv[2] #'variables_individuales'
ruta_fichero_variables_vectoriales = sys.argv[3] #'variables_vectoriales'
ruta_fichero_apellidos = sys.argv[4] #'fichero_apellidos'
ruta_plantilla_grafo = sys.argv[6]
plantilla_grafo = {}
with open(ruta_plantilla_grafo,"r") as rpg:
    for line in rpg:
	valor = []
        line = line.split("\t")
        valores = line[1].replace("]","").replace("[","").split(",")
        for elemento in valores:
	    valor.append(float(elemento))
        plantilla_grafo[int(line[0])] = np.array(valor)

#obtenemos las 3 listas de variables de la matriz de adyacencia
variables_matriz_adyacencia = uf1.obtener_listas_variables(ruta_fichero_variables_individuales,ruta_fichero_variables_vectoriales,ruta_fichero_apellidos)
lista_nombres = variables_matriz_adyacencia[0]
lista_nombres_apellidos = variables_matriz_adyacencia[1]
lista_apellidos = variables_matriz_adyacencia[2]

variables_matriz_adyacencia = lista_nombres+lista_nombres_apellidos + lista_apellidos
diccionario_cabeceras_matriz_adyacencia = {}   
for indice in range(len(variables_matriz_adyacencia)):
    diccionario_cabeceras_matriz_adyacencia[indice] = variables_matriz_adyacencia[indice]

indice_max_nombres=len(lista_nombres+lista_nombres_apellidos)
indice_max_apellidos = len(lista_nombres+lista_nombres_apellidos+lista_apellidos)

#Esta parte del codigo de tiene influencia se hay variables eliminadas
variables_eliminadas = uf1.obtener_lista_variables_fichero(sys.argv[5],separador_ficheros_auxiliares) # alias_eliminadas
diccionario_variables_posicion_matriz = uf1.generar_diccionario_relacion_madyacencia_masociada(matriz_asociada)
matriz_adyacencia = uf2.calcular_matriz_adyacencia_prima(matriz_adyacencia,diccionario_variables_posicion_matriz,variables_eliminadas)

grafo_estructura = ug.generar_grafo_no_dirigido(matriz_adyacencia,diccionario_cabeceras_matriz_adyacencia,indice_max_nombres,indice_max_apellidos,plantilla_grafo)
grafo = grafo_estructura[0].split("\n")
for line in grafo:
    print line

