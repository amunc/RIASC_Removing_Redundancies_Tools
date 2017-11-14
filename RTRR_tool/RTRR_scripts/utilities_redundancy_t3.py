# -*- coding: utf-8 -*-
'''RIASC Tool For Removing Redundancies(RTRR), a tool for erasing variables of type 1, type 2 and type 3.
Copyright (C) 2017  by RIASC Universidad de Leon(Miguel Carriegos Vieira, Noemi De Castro García, Angel Luis Muñoz, Mario Fernandez Rodriguez)
This file is part of RIASC Tool for Removing Redundancies (RTRR)

RTRR is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RTRR is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.'''

#funcion que permite agrupar nombres en funcion de los apellidos que tengan, es decir, si dos nombres tienen
#exactamente los mismos apellidos, estaran agrupados bajo la misma clave de apellidos {(apellido1,apellido2,aplleido3):[nombre1,nombre2]}
#se descartan las variables del diccionario original que son solo nombre o apellido
def obtener_diccionario_nombres_segun_apellidos(diccionario_variables_vectoriales):
    diccionario_apellidos_nombres = {}
    for key in diccionario_variables_vectoriales:
        if (diccionario_variables_vectoriales[key] != []):
            tupla_apellidos = tuple(diccionario_variables_vectoriales[key])
            if tupla_apellidos not in diccionario_apellidos_nombres:
                diccionario_apellidos_nombres[tupla_apellidos] = [key]
            else:
                valores = diccionario_apellidos_nombres[tupla_apellidos]
                valores.append(key)
                diccionario_apellidos_nombres[tupla_apellidos] = valores
    
    #en este punto tenemos agrupados los nombres segun los apellidos, nos quedamos sólo con los grupos en los que haya 2 o más nombres con
    #los mismos apellidos    
    diccionario_cribado = {}
    for key in diccionario_apellidos_nombres:
        if len(diccionario_apellidos_nombres[key]) > 1:
            diccionario_cribado[key] = diccionario_apellidos_nombres[key]    
    return diccionario_cribado

#funcion que permite obtener la lista con las listas de nombres que son redundantes entre si
#se recorre cada uno de los nombres que se corresponden con el mismo grupo de apellidos y se concatena con los apellidos para obtener la lista completa nombre_apellido y se genera una lista de listas
#una vez que tenemos las listas completas se van comparando entre si hasta que se obtienen las listas de los nombres que pueden ser redundantes entre si
#si un nombre ya se ha determinado que es redundante no se vuelve a comparar de modo que el primero se compara con n-1, el segundo con n-2 ... en el peor de los casos
#se devuelven las listas que se han formado con los nombres redundantes entre si
def obtener_lista_vectores_variables_redundantes_t3(diccionario_apellidos_nombres,diccionario_nombres_apellidos_inicial,diccionario_variables_posicion_matriz,matriz_general_pesos,lista_variables_individuales,lista_variables_eliminadas,separador_nombre_apellido_original):
    separador_nombre_apellido_interno = "___"
    lista_listas_variables_semejantes_vectoriales=[]
    for key in diccionario_apellidos_nombres:
        lista_listas_nombres_apellidos = []
        for nombre in diccionario_apellidos_nombres[key]: # cogemos los nombres
            lista_apellidos = diccionario_nombres_apellidos_inicial[nombre]
            lista_concatenacion_nombre_apellidos = []
            for apellido in lista_apellidos:
                lista_concatenacion_nombre_apellidos.append(nombre+ separador_nombre_apellido_interno +apellido)
            lista_listas_nombres_apellidos.append(lista_concatenacion_nombre_apellidos)            
            #vamos generando las listas de listas de nombres que pueden ser redundantes entre si y porcedemos a determinar si son redundantes
            #o no en el siguiente tramo de codigo
        lista_completa_variables_semejantes = []
        for indice in range(len(lista_listas_nombres_apellidos)):
            lista_uno = lista_listas_nombres_apellidos[indice]
            nombre = lista_uno[0].split(separador_nombre_apellido_interno)
            nombre = nombre[0]
            lista_parcial_variables_semejantes = []
            if(nombre not in lista_completa_variables_semejantes):
                for indice_lista2 in range(indice+1,len(lista_listas_nombres_apellidos)):#bucle para desplazarse por la lista de apellidos
                    lista_dos = lista_listas_nombres_apellidos[indice_lista2]
                    #comparamos los valores de las variables:
                    ind_nombre_apellido = 0
                    seguir_comprobando = True #centinela que permite sber si hay que seguir comprobando o si ya se ha encontrado un valor que difiera entre las dos variables
                    while (ind_nombre_apellido <= len(lista_uno)-1) and (seguir_comprobando == True): # bucle para desplazarse por la lista de nombre_apellido dentro del mismo nombre
                        variable1 = lista_uno[ind_nombre_apellido]
                        variable1_original = variable1.replace(separador_nombre_apellido_interno,separador_nombre_apellido_original)
                        posicion_var1 = diccionario_variables_posicion_matriz[variable1_original]
                        
                        variable2 = lista_dos[ind_nombre_apellido]
                        variable2_original = variable2.replace(separador_nombre_apellido_interno,separador_nombre_apellido_original)
                        posicion_var2 = diccionario_variables_posicion_matriz[variable2_original]
                        
                        for instancia in range(len(matriz_general_pesos)):
                            valor1 = matriz_general_pesos[instancia][posicion_var1[0]][posicion_var1[1]]
                            valor2 = matriz_general_pesos[instancia][posicion_var2[0]][posicion_var2[1]]
                            if(valor1 != valor2):
                                seguir_comprobando = False
                        ind_nombre_apellido+=1
                #aqui se ha comparado los nombres con  los apellidos
                    if(seguir_comprobando == True): # significa que todas las variables tienen los mismos valores                        
                        nombre1 = variable1.split(separador_nombre_apellido_interno)                    
                        nombre2 = variable2.split(separador_nombre_apellido_interno)
                        if nombre1[0] not in lista_parcial_variables_semejantes:
                            lista_parcial_variables_semejantes.append(nombre1[0])
                        if nombre1[0] not in lista_completa_variables_semejantes:
                            lista_completa_variables_semejantes.append(nombre1[0])
                        if nombre2[0] not in lista_parcial_variables_semejantes:
                            lista_parcial_variables_semejantes.append(nombre2[0])
                        if nombre2[0] not in lista_completa_variables_semejantes:
                            lista_completa_variables_semejantes.append(nombre2[0])
                if(lista_parcial_variables_semejantes):
                    lista_listas_variables_semejantes_vectoriales.append(lista_parcial_variables_semejantes) # insertamos en la lista que vamos a devolver finalmente las listas de elementos semejantes
    #ahora seguimos el mismo procedimiento con las variables individuales
    #lista_listas_variables_semejantes=[]
    lista_completa_variables_semejantes = []
    lista_listas_variables_semejantes_individual = []
    for indice in range(len(lista_variables_individuales)):
        nombre1 = lista_variables_individuales[indice]        
        lista_parcial_variables_semejantes = []
        if(nombre1 not in lista_variables_eliminadas) and (nombre1 not in lista_completa_variables_semejantes):
            for indice_lista2 in range(indice+1,len(lista_variables_individuales)):#bucle para desplazarse por la lista de apellidos
                nombre2 = lista_variables_individuales[indice_lista2]
                if(nombre2 not in lista_variables_eliminadas) and (nombre2 not in lista_completa_variables_semejantes):
                    #comparamos los valores de las variables:
                    seguir_comprobando = True #centinela que permite sber si hay que seguir comprobando o si ya se ha encontrado un valor que difiera entre las dos variables
                    posicion_var1 = diccionario_variables_posicion_matriz[nombre1]
                    posicion_var2 = diccionario_variables_posicion_matriz[nombre2]
                    for instancia in range(len(matriz_general_pesos)):
                        valor1 = matriz_general_pesos[instancia][posicion_var1[0]][posicion_var1[1]]
                        valor2 = matriz_general_pesos[instancia][posicion_var2[0]][posicion_var2[1]]
                        if(valor1 != valor2):
                            seguir_comprobando = False                    
                    #aqui se ha comparado los nombres con  los apellidos
                    if(seguir_comprobando == True): # significa que todas las variables tienen los mismos valores                        
                        if nombre1 not in lista_parcial_variables_semejantes:
                            lista_parcial_variables_semejantes.append(nombre1)
                        if nombre1 not in lista_completa_variables_semejantes:
                            lista_completa_variables_semejantes.append(nombre1)
                        if nombre2 not in lista_parcial_variables_semejantes:
                            lista_parcial_variables_semejantes.append(nombre2)
                        if nombre2 not in lista_completa_variables_semejantes:
                            lista_completa_variables_semejantes.append(nombre2)
            if(lista_parcial_variables_semejantes):
                lista_listas_variables_semejantes_individual.append(lista_parcial_variables_semejantes) # insertamos en la lista que vamos a devolver finalmente las listas de elementos semejantes    
    return [lista_listas_variables_semejantes_individual,lista_listas_variables_semejantes_vectoriales]

#funcion que devuelve una lista con los nombres con cada uno de los apellidos que son redundantes
def obtener_lista_variables_redundantes(lista_listas_nombres_redundantes_individuales,lista_listas_nombres_redundantes_vectoriales,diccionario_nombres_apellidos_inicial,separador_nombre_apellido_original):
    lista_variables_redundantes = []
    
    for lista in lista_listas_nombres_redundantes_individuales:
        lista = sorted(lista)        
        for indice in range(1,len(lista)): # nos quedamos con el primero 
            nombre_completo = lista[indice]
            lista_variables_redundantes.append(nombre_completo)
            
    for lista in lista_listas_nombres_redundantes_vectoriales:
        lista = sorted(lista)        
        for indice in range(1,len(lista)): # nos quedamos con el primero            
            nombre_buscado = lista[indice]
            lista_completa_apellidos = diccionario_nombres_apellidos_inicial[nombre_buscado]            
            for apellido in lista_completa_apellidos:
                nombre_completo = nombre_buscado + separador_nombre_apellido_original + apellido
                lista_variables_redundantes.append(nombre_completo)
    
    return sorted(lista_variables_redundantes)
