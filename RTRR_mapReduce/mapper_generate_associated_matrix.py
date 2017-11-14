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
ut = importer.load_module('utilidades_fase_I')

ruta_fichero_variables_individuales = sys.argv[1] # alias_variables_individuales
ruta_fichero_variables_vectoriales = sys.argv[2] #alias_variables_vectoriales
ruta_fichero_apellidos = sys.argv[3] #alias_fichero_apellidos
separador_apellidos = sys.argv[4]

#obtenemos las 3 listas de variables de la matriz de adyacencia
variables_matriz_adyacencia = ut.obtener_listas_variables(ruta_fichero_variables_individuales,ruta_fichero_variables_vectoriales,ruta_fichero_apellidos)

#obtenemos los rangos para poder generar la matriz de adyacencia
rangos = ut.obtener_rangos_variables(variables_matriz_adyacencia[0],variables_matriz_adyacencia[1],variables_matriz_adyacencia[2])
variables_matriz_adyacencia = variables_matriz_adyacencia[0] + variables_matriz_adyacencia[1] + variables_matriz_adyacencia[2]
for linea in sys.stdin:
    linea = linea.strip()
    linea = linea.split('\t')
    elemento = []
    if(len(linea) == 3):
        apellidos = ut.formatear_apellidos(linea[2])
        elemento = [linea[1],apellidos]
    else:
        elemento = [linea[1]]
    ut.generar_matriz_asociada(int(linea[0]),elemento,rangos,variables_matriz_adyacencia,separador_apellidos)

