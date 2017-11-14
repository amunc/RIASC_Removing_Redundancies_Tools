#!/usr/bin/env python

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
ut = importer.load_module('utilidades_fase_I')

separador_apellidos= sys.argv[1]
separador_ficheros_auxiliares = '\n'

#directorios_generacion_ficheros

directorio_variables_csv = sys.argv[2] # csv_variables
directorio_variables_matriz_adyacencia_individuales = sys.argv[3] #adjacency_matrix_single_variables
directorio_variables_matriz_adyacencia_vectoriales =  sys.argv[4] #adjacency_matrix_vector_names_dictionary "variables_componer_madyacencia_vectoriales"
directorio_variables_matriz_adyacencia_apellidos = sys.argv[5] #adjacency_matrix_surnames "variables_componer_madyacencia_apellidos"
directorio_variables_matriz_adyacencia_todas= sys.argv[6] #adjacency_matrix_full_list "variables_componer_madyacencia_todas"

diccionario = {}
lista_variables_csv = []
lista_variables_sin_eliminadas = []
lista_apellidos = []
#directorio_diccionario = "diccionario"

lista_variables_eliminadas = ut.obtener_lista_variables_fichero(sys.argv[7],separador_ficheros_auxiliares) #alias_fichero_eliminadas
lista_variables_individuales = ut.obtener_lista_variables_fichero(sys.argv[8],separador_ficheros_auxiliares) #alias_fichero_individuales
lista_variables_vectoriales = ut.obtener_lista_variables_fichero(sys.argv[9],separador_ficheros_auxiliares) #alias_fichero_vectoriales

for linea in sys.stdin:    
    linea = linea.strip()
    linea = linea.split("\t")
    linea = linea[1] # nos quedamos con la lista de variables
    for elemento in linea.split(","):
        elemento = elemento.replace(']','').replace('[','').replace('\'','').strip()
        lista_variables_csv.append(elemento)

#aqui se determina si las variables se obtienen directamente del csv o si hay ficheros de individuales y vectoriales
if(lista_variables_vectoriales !=[] and lista_variables_individuales !=[]):
    lista_vectores_variables_relacionadas= ut.obtener_vectores_variables_relacionadas(lista_variables_vectoriales)
    diccionario_variables_vectoriales_apellidos = ut.obtener_apellidos_variables_listas(lista_variables_vectoriales,lista_vectores_variables_relacionadas,lista_variables_csv,lista_variables_eliminadas,separador_apellidos)

else:
    lista_individuales_diccionario_vectoriales = ut.obtener_apellidos_variables_fichero(lista_variables_csv,lista_variables_eliminadas,separador_apellidos)
    lista_variables_individuales = lista_individuales_diccionario_vectoriales[0]
    diccionario_variables_vectoriales_apellidos = lista_individuales_diccionario_vectoriales[1]

#limpiamos de eliminadas las listas que hemos obtenido
lista_variables_individuales_sin_eliminadas = []
for variable_individual in lista_variables_individuales:
    if variable_individual in lista_variables_csv:
	lista_variables_individuales_sin_eliminadas.append(variable_individual)
lista_variables_individuales = lista_variables_individuales_sin_eliminadas
	

#Imprimimos las variables del csv
for indice in range(len(lista_variables_csv)):
    actual = lista_variables_csv[indice]
    print("%s\t%s" %(directorio_variables_csv,actual))
    if(actual not in lista_variables_eliminadas):
        lista_variables_sin_eliminadas.append(actual)

#Para poder constuir la matriz de adyacencia imprimimos los nombres y posteriormente los nombres con apellidos
contador = 0
if (lista_variables_individuales == []):
    print("%s\t%s" %(directorio_variables_matriz_adyacencia_individuales,''))
else:
    for indice in range(len(lista_variables_individuales)):
        print("%s\t%s" %(directorio_variables_matriz_adyacencia_individuales,lista_variables_individuales[indice]))
        print("%s\t%s\t%s" %(directorio_variables_matriz_adyacencia_todas,contador,lista_variables_individuales[indice]))
        contador+=1

if (diccionario_variables_vectoriales_apellidos == {}):
    print("%s\t%s" %(directorio_variables_matriz_adyacencia_vectoriales,''))
    print("%s\t%s" %(directorio_variables_matriz_adyacencia_apellidos,''))
else:
    for key in diccionario_variables_vectoriales_apellidos:
        print("%s\t%s\t%s" %(directorio_variables_matriz_adyacencia_vectoriales,key,sorted(diccionario_variables_vectoriales_apellidos[key])))
        print("%s\t%s\t%s\t%s" %(directorio_variables_matriz_adyacencia_todas,contador,key,sorted(diccionario_variables_vectoriales_apellidos[key])))
        contador+=1
        for apellido in diccionario_variables_vectoriales_apellidos[key]:
	    if apellido not in lista_apellidos:
	        lista_apellidos.append(apellido)
    lista_apellidos = sorted(lista_apellidos)

    for apellido in lista_apellidos:
        print("%s\t%s" %(directorio_variables_matriz_adyacencia_apellidos,apellido))
        print("%s\t%s\t%s" %(directorio_variables_matriz_adyacencia_todas,contador,apellido))
        contador+=1

