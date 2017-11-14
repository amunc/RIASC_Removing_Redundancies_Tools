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
import csv
import zipimport

importer = zipimport.zipimporter('utilities.zip')
uf1 = importer.load_module('utilidades_fase_I')
uf2 = importer.load_module('utilidades_fase_II')
ug = importer.load_module('utilidades_generales')

separador_fichero = sys.argv[2]
separador_elementos = sys.argv[2]+sys.argv[2]
separador_ficheros_auxiliares = '\n'
matriz_instancias = []
directorio_salida_csv = 'csv_without_r' + sys.argv[1]
directorio_salida_porcentajes = 'redundancy_' + sys.argv[1] +'_summary'
directorio_salida_eliminadas = 'erased_variables'

#obtenemos la lista con las variables cuya nomenclatura se modifico
variables_modificadas = [] #ut.obtener_lista_variables_modificadas('variables_muestra_modificadas')

#primero creamos los diccionarios que necesitamos para obtener las variables redundantes y otro para crear el csv final
matrices_adyacencia_asociada = uf1.generar_matriz_adyacencia_y_asociada(sys.argv[3]) #devuelve una lista con dos listas.La matriz de adyacencia y la matriz asociada
matriz_adyacencia = matrices_adyacencia_asociada[0]
matriz_asociada = matrices_adyacencia_asociada[1] #matriz nombres_apellidos asociada a matriz de ayacencia

#creamos un diccionario que permita obtener la posicion de una variable(nombre o nombre con apellido) en la matriz de adyacencia
diccionario_variables_posicion_matriz = uf1.generar_diccionario_relacion_madyacencia_masociada(matriz_asociada)

#diccionario_variables_posicion_matriz = ut.recodificar_diccionario(diccionario_variables_posicion_matriz,variables_modificadas)
diccionario_posicion_matriz_variables = uf2.generar_diccionario_posicion_variables(diccionario_variables_posicion_matriz)

#Ambos diccionarios contienen todas las variables, dado que se esta trabajando sobre la matriz de adyacencia original

#2 - Obtencion de las variables que se han eliminado
#obtenemos la lista de variables eliminadas en pasadas anteriores(si las ha habido)
variables_eliminadas = uf1.obtener_lista_variables_fichero(sys.argv[4],separador_ficheros_auxiliares) #alias_eliminadas

if(sys.argv[1] == "t1"):
    instancia_resultado = uf2.obtener_instancia_resumen(sys.argv[5],separador_elementos) #alias_instancia_resumen
    variables_redundantes = uf2.obtener_lista_variables_redundantes_t1(instancia_resultado,diccionario_posicion_matriz_variables)
elif(sys.argv[1] == "t2"):
    instancia_resultado = uf2.obtener_instancia_resumen(sys.argv[5],separador_elementos) #alias_instancia_resumen
    variables_redundantes = uf2.obtener_lista_variables_redundantes_t2(instancia_resultado,diccionario_posicion_matriz_variables)
elif(sys.argv[1] == "t3"):
    variables_redundantes = uf2.obtener_lista_variables_redundantes_t3_fichero(sys.argv[5]) #alias_redundantes_t3

#variables_redundantes = ut.recodificar_lista_variables_redundantes(variables_redundantes,variables_modificadas)
lista_completa_variables_eliminadas = variables_eliminadas + variables_redundantes
for variable_eliminada in lista_completa_variables_eliminadas:
    print("%s\t%s" %(directorio_salida_eliminadas,variable_eliminada))
if(len(lista_completa_variables_eliminadas) == 0):
    print("%s\t%s" %(directorio_salida_eliminadas,''))

#3.1 Calculamos la matriz de adyancencia (en el caso acumulativo, teniendo en cuenta las eliminadas hasta el momento)

#matriz_adyacencia = uf2.calcular_matriz_adyacencia_prima(matriz_adyacencia,diccionario_variables_posicion_matriz,variables_eliminadas)

#3.2 - Calculamos la matriz de adyacencia prima
matriz_adyacencia_input = uf2.calcular_matriz_adyacencia_prima(matriz_adyacencia,diccionario_variables_posicion_matriz,variables_eliminadas)
matriz_adyacencia_output = uf2.calcular_matriz_adyacencia_prima(matriz_adyacencia,diccionario_variables_posicion_matriz,lista_completa_variables_eliminadas)

#4 - Actualizacion del diccionario que es el que determina si una variable aparecera en el csv final o no
diccionario_variables_posicion_matriz = uf2.actualizar_diccionario(lista_completa_variables_eliminadas,diccionario_variables_posicion_matriz)

variables_modificadas = uf1.crear_diccionario_variables_modificadas(variables_modificadas)


cabecera_encontrada = False
for linea in sys.stdin:
    linea = linea.strip()
    linea = linea.split("\t") # separa numero de linea y matriz wN
    clave = linea[0]
    cabecera_encontrada = uf2.imprimir_instancia(clave,cabecera_encontrada,variables_modificadas,linea[1],directorio_salida_csv,separador_fichero)
ug.imprimir_variables_redundantes(variables_redundantes,directorio_salida_porcentajes,sys.argv[1])
ug.imprimir_porcentajes_redundancia(matriz_adyacencia,matriz_adyacencia_input,matriz_adyacencia_output,variables_redundantes,directorio_salida_porcentajes)
#ug.generar_estadisticas_matrices(matriz_asociada,matriz_adyacencia,variables_eliminadas,variables_redundantes,directorio_salida_porcentajes,diccionario_variables_posicion_matriz)

