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


clave_anterior = ''
diccionario_apellidos_nombres = {}
for linea in sys.stdin:
    linea = linea.strip()
    linea = linea.split("\t")
    clave_actual = linea[0]
    valor_actual = linea[1]
    valor_actual=uf1.formatear_cadena_valor_diccionario(valor_actual)
    if clave_anterior == '': # es el primer elemento
        clave_anterior = linea[0]
        valor_anterior = valor_actual

    elif clave_actual == clave_anterior: # si dos mappers han trabajado con la misma clave, actualizamos la lista de nombres            
            for indice in range(len(valor_actual)):
                if valor_actual[indice] not in valor_anterior:
                    valor_anterior = valor_anterior + valor_actual

    else: # aniadimos el anterior al diccionario
            diccionario_apellidos_nombres[clave_anterior] = valor_anterior
            print clave_anterior,"\t",valor_anterior
            clave_anterior = clave_actual
            valor_anterior = valor_actual

#el ultimo elemento hay que aniadirlo tambien
if clave_actual not in diccionario_apellidos_nombres:
    print clave_actual,"\t",valor_actual # imprimimos el ultimo elemento
else:
    for indice in range(len(valor_actual)):
        if valor_actual[indice] not in valor_anterior:
            valor_anterior = valor_anterior + valor_actual
    print clave_actual,"\t",valor_anterior
