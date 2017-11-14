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
uf2 = importer.load_module('utilidades_fase_II')

separador_elementos = sys.argv[2]+sys.argv[2]
separador_ficheros_auxiliares = '\n'

#obtenemos la lista con las variables cuya nomenclatura se modifico
variables_modificadas = [] #ut.obtener_lista_variables_modificadas('variables_muestra_modificadas')

#1 - Creacion de los diccionarios para poder obtener posteriormente los valores de las variables de la matriz de pesos
#primero creamos los diccionarios que necesitamos para obtener las variables redundantes y otro para crear el csv final
matrices_adyacencia_asociada = uf1.generar_matriz_adyacencia_y_asociada(sys.argv[3]) #devuelve una lista con dos listas.La matriz de adyacencia y la matriz asociada
matriz_asociada = matrices_adyacencia_asociada[1] #matriz nombres_apellidos asociada a matriz de ayacencia

#creamos un diccionario que permita obtener la posicion de una variable(nombre o nombre con apellido) en la matriz de adyacencia
diccionario_variables_posicion_matriz = uf1.generar_diccionario_relacion_madyacencia_masociada(matriz_asociada)

#diccionario_variables_posicion_matriz = ut.recodificar_diccionario(diccionario_variables_posicion_matriz,variables_modificadas)
diccionario_posicion_matriz_variables = uf2.generar_diccionario_posicion_variables(diccionario_variables_posicion_matriz)

#2 - Obtencion de las variables que se han eliminado
#obtenemos la lista de variables eliminadas en pasadas anteriores(si las ha habido)
variables_eliminadas = uf1.obtener_lista_variables_fichero(sys.argv[4],separador_ficheros_auxiliares) #'variables_muestra_eliminadas'

#obtenemos la lista de variables eliminadas por presentar la redundancia actual
if(sys.argv[1] == "t1"):
    instancia_resultado = uf2.obtener_instancia_resumen(sys.argv[5],separador_elementos) #'instancia_resumen'
    variables_redundantes = uf2.obtener_lista_variables_redundantes_t1(instancia_resultado,diccionario_posicion_matriz_variables)
elif(sys.argv[1] == "t2"):
    instancia_resultado = uf2.obtener_instancia_resumen(sys.argv[5],separador_elementos) #'instancia_resumen
    variables_redundantes = uf2.obtener_lista_variables_redundantes_t2(instancia_resultado,diccionario_posicion_matriz_variables)
elif(sys.argv[1] == "t3"):
    variables_redundantes = uf2.obtener_lista_variables_redundantes_t3_fichero(sys.argv[5]) #'variables_redundantes_t3'


#variables_redundantes = ut.recodificar_lista_variables_redundantes(variables_redundantes,variables_modificadas)
lista_completa_variables_eliminadas = variables_eliminadas + variables_redundantes
lista_completa_variables_csv_original = uf1.obtener_lista_variables_fichero(sys.argv[6],separador_ficheros_auxiliares)  #'variables_csv'


#3 - Actualizacion del diccionario que es el que determina si una variable aparecera en el csv final o no
diccionario_variables_posicion_matriz = uf2.actualizar_diccionario(lista_completa_variables_eliminadas,diccionario_variables_posicion_matriz)


#4 - Eliminamos de la lista original las variables redundantes
lista_final_variables_csv_original = []

for indice in range(len(lista_completa_variables_csv_original)):
    elemento = lista_completa_variables_csv_original[indice]
    if(elemento in diccionario_variables_posicion_matriz):
        lista_final_variables_csv_original.append(elemento)
instancia = "["
for indice in range(len(lista_final_variables_csv_original)):
    if(indice <= len(lista_final_variables_csv_original)-2):
        instancia+=lista_final_variables_csv_original[indice] + separador_elementos
    else:
        instancia+=lista_final_variables_csv_original[indice] + "]"
print 0,"\t",instancia

for linea in sys.stdin:
    linea = linea.strip()
    linea = linea.split("\t") # separa numero de linea y matriz wN
    instancia = uf2.reconvertir_instancia(linea[1],separador_elementos,[])
    instancia_generada = uf2.generar_instancia_csv_sin_redundancia(instancia,diccionario_variables_posicion_matriz,lista_completa_variables_csv_original)
    linea[0] = int(linea[0])+1
    instancia = "["
    for indice in range(len(instancia_generada)):
        if(indice <= len(instancia_generada)-2):
            instancia+=str(instancia_generada[indice]) + separador_elementos
        else:
            instancia+=str(instancia_generada[indice]) + "]"
    print linea[0],"\t",instancia
