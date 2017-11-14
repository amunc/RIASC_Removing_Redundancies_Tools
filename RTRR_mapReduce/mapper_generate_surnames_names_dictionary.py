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

separador_ficheros_auxiliares = '\n'
separador_apellidos = sys.argv[2]

#obtenemos la lista de variables eliminadas
variables_eliminadas = uf1.obtener_lista_variables_fichero(sys.argv[1],separador_ficheros_auxiliares) #'variables_muestra_eliminadas'
diccionario_apellidos_nombres = {}

for linea in sys.stdin: #la entrada pueden ser variables individuales o vectoriales
    linea = linea.strip()
    linea = linea.split('\t')
    clave_valor = []
    if(len(linea) == 1): #es variable individual
        variable_individual = linea[0]
	if(variable_individual not in variables_eliminadas):
	    clave_valor=[variable_individual,[]]
    else:#es vectorial
	variable_vectorial = linea[0]
        lista_apellidos =uf1.formatear_cadena_valor_diccionario(linea[1])
        lista_apellidos_no_eliminados = []
        for apellido in lista_apellidos:
	    if(apellido == variable_vectorial):
	        variable_comprobar = variable_vectorial
	    else:
	        variable_comprobar = variable_vectorial + separador_apellidos + apellido
	    #si no esta en las variables eliminadas, mantenemos el apellido	
      	    if(variable_comprobar not in variables_eliminadas):
	        lista_apellidos_no_eliminados.append(apellido)
	    if(lista_apellidos_no_eliminados != []):
	        clave_valor = [variable_vectorial,lista_apellidos_no_eliminados]
    if(clave_valor != []):
        diccionario_apellidos_nombres=uf2.obtener_diccionario_nombres_segun_apellidos(clave_valor,diccionario_apellidos_nombres)

#El diccionario contiene tanto variables individuales como variables vectoriales
for key in diccionario_apellidos_nombres:
    print key,"\t",diccionario_apellidos_nombres[key]
