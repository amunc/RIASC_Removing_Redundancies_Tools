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

separador_elementos = sys.argv[1]+sys.argv[1]
separador_ficheros_auxiliares = "\n"
separador_nombre_apellido_original = sys.argv[7]
separador_nombre_apellido = "___"

def actualizar_diccionario(lista_variables_eliminadas,diccionario,separador_apellidos):
    variables_completas_eliminadas = []
    diccionario_devuelto = {}
	
    for key in diccionario:
	diccionario_devuelto[key] = diccionario[key]

    for variable_eliminada in lista_variables_eliminadas:
	for variable in diccionario:
	    apellidos_eliminar = []
	    apellidos = diccionario[variable]
	    for apellido in apellidos:
		if(apellido == variable):
		    variable_completa = apellido
		else:
	            variable_completa = variable+separador_apellidos+apellido

		if(variable_completa == variable_eliminada):
		    apellidos_eliminar.append(apellido)

	    #eliminamos los apellidos que ya no existan
   	    for elemento in apellidos_eliminar:
		valores = diccionario_devuelto[variable]
		valores.remove(elemento)
		diccionario_devuelto[variable] = valores
		if(valores == []):	   
		    variables_completas_eliminadas.append(variable)
	    #eliminamos las variables que ya no tengan apellidos
    for variable_eliminada in variables_completas_eliminadas:
        del diccionario_devuelto[variable_eliminada]

    return diccionario_devuelto


lista_variables_eliminadas = uf1.obtener_lista_variables_fichero(sys.argv[2],separador_ficheros_auxiliares) #'variables_muestra_eliminadas'

#obtenemos el diccionario inicial porque lo vamos a necesitar
diccionario_variables_vectoriales_original = uf1.generar_diccionario_fichero(sys.argv[3]) #'diccionario_vectoriales'
diccionario_variables_vectoriales_original = actualizar_diccionario(lista_variables_eliminadas,diccionario_variables_vectoriales_original,separador_nombre_apellido_original) #diccionario original desde el que partimos

lista_variables_individuales = uf1.obtener_lista_variables_fichero(sys.argv[4],separador_ficheros_auxiliares)
lista_variables_individuales = uf2.actualizar_lista_variables_individuales(lista_variables_individuales,lista_variables_eliminadas)

#primero creamos los diccionarios que necesitamos para obtener las variables redundantes y otro para crear el csv final
matrices_adyacencia_asociada = uf1.generar_matriz_adyacencia_y_asociada(sys.argv[5]) #devuelve una lista con dos listas.La matriz de adyacencia y la matriz asociada
matriz_asociada = matrices_adyacencia_asociada[1] #matriz nombres_apellidos asociada a matriz de ayacencia

#creamos un diccionario que permita obtener la posicion de una variable(nombre o nombre con apellido) en la matriz de adyacencia
diccionario_variables_posicion_matriz = uf1.generar_diccionario_relacion_madyacencia_masociada(matriz_asociada)

diccionario_apellidos_nombres = uf2.generar_diccionario_apellidos_nombres_fichero(sys.argv[6]) #diccionario_apellidos_nombres

diccionario_final = {}
diccionario_cluster_apellidos_codificacion = {}
contador = 1
for key in diccionario_apellidos_nombres:
    nombres = diccionario_apellidos_nombres[key]
    if (len(nombres) > 1):
        nueva_clave = tuple(nombres)
	if(key == ()): # son las variables individuales
  	    nuevo_valor = 0	    
	else: 
	    nuevo_valor = contador
	    contador+=1
        diccionario_cluster_apellidos_codificacion[nuevo_valor] = key
	diccionario_final[nueva_clave] = nuevo_valor

lista_vectores_variables_redundantes = []
for linea in sys.stdin: 
    linea = linea.strip()
    linea = linea.split("\t") #separamos numero de linea respecto de la matriz de pesos de la instancia [0 w0], [1 w1]
    linea[1] = linea[1].replace('[[','[').replace(']]',']')
    instancia_actual_mpesos = uf2.reconvertir_instancia(linea[1],separador_elementos,[])
    diccionario_final = uf2.obtener_diccionario_variables_redundantes_t3(diccionario_final,diccionario_variables_vectoriales_original,diccionario_variables_posicion_matriz,instancia_actual_mpesos,lista_variables_individuales,lista_variables_eliminadas,separador_nombre_apellido_original,separador_nombre_apellido,separador_elementos)
    #print diccionario_final

diccionario_resultante = {}
for key in diccionario_final:
    codificacion = diccionario_final[key] # devuelve la clave que tiene asociada la tupla inicial
    tupla_inicial = diccionario_cluster_apellidos_codificacion[codificacion]
    if(tupla_inicial not in diccionario_resultante):
        valores = list(key)
        diccionario_resultante[tupla_inicial] = [valores]
    else:
	valores_actuales = diccionario_resultante[tupla_inicial]
        valores = list(key)
	valores_actuales.append(valores)	
        diccionario_resultante[tupla_inicial] = valores_actuales

for key in diccionario_resultante:
    valor = diccionario_resultante[key]
    if(len(valor) == 1):
	valor = valor[0]
	diccionario_resultante[key] = valor

for key in diccionario_resultante:
    print key,"\t",diccionario_resultante[key]
    
    
