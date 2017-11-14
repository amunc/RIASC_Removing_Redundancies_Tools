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

separador_nombres_apellidos = sys.argv[2]


diccionario = uf1.generar_diccionario_fichero(sys.argv[1]) #'diccionario_apellidos_nombres'
diccionario_nombres_apellidos = {}
for key in diccionario:
    lista_nombres = diccionario[key]
    key = key.replace('\t','').replace('\'','')
    key = key[1:len(key)-3]
    if(key.strip() != ''):
	if(key[len(key)-1] == ","):
	    key = key[0:len(key)-1]
    key = key.split(', ')	    
    lista_apellidos = []    
    for apellido in key:
        lista_apellidos.append(apellido)
	for nombre in lista_nombres:
	    if(nombre not in diccionario_nombres_apellidos):
 		if apellido == "":
  		    diccionario_nombres_apellidos[nombre] = []
		else:
		    diccionario_nombres_apellidos[nombre] = [apellido]
	    else:
		valores = diccionario_nombres_apellidos[nombre]
		valores.append(apellido)
		diccionario_nombres_apellidos[nombre] = valores

variables_redundantes = []
tupla_actual = ""
tupla_anterior = ""
vector_listas_variables_redundantes = []
for linea in sys.stdin: 
    linea = linea.strip()
    linea = linea.split('\t')
    if(tupla_actual == ""): # es el primer elemento
        tupla_actual = linea[0]
  	vector_listas_variables_redundantes = uf2.reconvertir_lista_vectores_nombres(linea[1])

    else:
	if(tupla_actual == linea[0]): # es el n-esimo elemento
	    l1 = vector_listas_variables_redundantes
	    l2 = uf2.reconvertir_lista_vectores_nombres(linea[1])
	    vector_listas_variables_redundantes = [list(x) for x in set(tuple(x) for x in l1).intersection(set(tuple(x) for x in l2))]
	    
	else:
            if(vector_listas_variables_redundantes != []):# imprimimos el valor y continuamos
		uf2.obtener_lista_variables_redundantes_t3(vector_listas_variables_redundantes,diccionario_nombres_apellidos,separador_nombres_apellidos)
	    tupla_actual = linea[0]
            vector_listas_variables_redundantes = uf2.reconvertir_lista_vectores_nombres(linea[1])
		
if(vector_listas_variables_redundantes != []):# imprimimos el ultimo valor
    uf2.obtener_lista_variables_redundantes_t3(vector_listas_variables_redundantes,diccionario_nombres_apellidos,separador_nombres_apellidos)

