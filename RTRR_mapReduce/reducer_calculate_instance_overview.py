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
uf2 = importer.load_module('utilidades_fase_II')

separador_elementos = sys.argv[2] +sys.argv[2]
instancia_resultado = []
for linea in sys.stdin:
    linea = linea.strip()
    linea = linea.split("\t") #separamos numero de linea respecto de la matriz de pesos de la instancia [0 w0], [1 w1]
    linea[1] = linea[1].replace('[[','[').replace(']]',']')
    instancia_iesima = uf2.reconvertir_instancia(linea[1],separador_elementos,[])
    if(sys.argv[1] == "t1"):
        instancia_resultado = uf2.comparar_instancia_iesima_t1(instancia_resultado, instancia_iesima)
    elif(sys.argv[1] == "t2"):
        instancia_resultado = uf2.comparar_instancia_iesima_t2(instancia_resultado, instancia_iesima)
instancia = "["
for fila in range(len(instancia_resultado)):
    instancia+="["
    for columna in range(len(instancia_resultado[fila])):
        if (columna <= len(instancia_resultado[fila])-2):
            instancia+= str(instancia_resultado[fila][columna])+separador_elementos
        else: # es el ultimo elemento, hay que poner el corchete de cierre
            if(fila <= len(instancia_resultado)-2):
                instancia+= str(instancia_resultado[fila][columna])+"], "
            else:
                instancia+= str(instancia_resultado[fila][columna])+"]]"
print instancia

