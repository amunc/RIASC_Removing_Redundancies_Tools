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

import os.path
import numpy as np
import pandas as pd
import sys
import utilities_phase_I as uf1
import utilities_redundancy_t1 as ur1
import utilities_redundancy_t2 as ur2
import utilities_redundancy_t3 as ur3

#Funcion que permite eliminar redundancias segun la secuencia introducida por el usuario
def eliminar_redundancias_segun_secuencia(secuencia_eliminacion,ruta_fichero,ruta_fichero_var_individuales,ruta_fichero_var_vectoriales,ruta_fichero_variables_eliminadas,ruta_fichero_variables_modificadas,ruta_fichero_volcado_datos_test,separador,separador_ficheros_variables,separador_apellidos,tipo_fichero,modo_operacion,pasada_actual,idioma):
    uf1.cargar_paquetes_idioma('paquete_idiomas',idioma)        
    lista_posibles_permutaciones = []
    ruta_fichero_resumen = ""
    numero_unos_matriz_A = 0
    numero_final_unos = 0
    ruta_fichero_original = ruta_fichero
    while(len(secuencia_eliminacion) > 1):
        numero = int(secuencia_eliminacion) % 10
        secuencia_eliminacion = str(int(secuencia_eliminacion) / 10)
        lista_posibles_permutaciones.append(numero)
    lista_posibles_permutaciones.append(int(secuencia_eliminacion))
    lista_posibles_permutaciones.reverse()
    lista_posibles_permutaciones = [tuple(lista_posibles_permutaciones)]

    posicion_grafo ="undefined"
    A_original = []
    diccionario_original = {}
    etiquetas_grafo = []
    indice_max_nombres=0
    indice_max_apellidos=0
    for indice in range(len(lista_posibles_permutaciones)):        
        primera_pasada = True
        lista_variables_eliminadas_por_pasada = []
        uf1.colored_print(_("Eliminacion a realizar: ") + str(lista_posibles_permutaciones[indice]),'green')
        for indice_redundancia in range(len(lista_posibles_permutaciones[indice])):
            print _("Fichero usado "),ruta_fichero
            redundancia_eliminar = int(lista_posibles_permutaciones[indice][indice_redundancia])
            if(primera_pasada == True):# si es la eliminacion de la primera redundancia de la permutacion, se hace sobre el csv original
                uf1.eliminar_contenido_fichero(ruta_fichero_variables_eliminadas)
                ruta_fichero = ruta_fichero_original
                salida_funcion = eliminar_redundancia(ruta_fichero,ruta_fichero_var_individuales,ruta_fichero_var_vectoriales,ruta_fichero_variables_eliminadas,ruta_fichero_variables_modificadas,redundancia_eliminar,separador,separador_ficheros_variables,separador_apellidos,tipo_fichero,modo_operacion,ruta_fichero_resumen,numero_unos_matriz_A,pasada_actual,posicion_grafo,A_original,diccionario_original,etiquetas_grafo,indice_max_nombres,indice_max_apellidos)
                ruta_csv_salida = salida_funcion[0]
                if(modo_operacion != _('individualizado')):
                    primera_pasada = False
                    ruta_fichero = ruta_csv_salida
                    tipo_fichero = salida_funcion[2]                                        
                    pasada_actual = indice_redundancia
                ruta_fichero_resumen = salida_funcion[3]                                        
                numero_unos_matriz_A = salida_funcion[4]
                numero_final_unos = salida_funcion[5]
                posicion_grafo = salida_funcion[6] #actualizamos la plantilla del grafo
                A_original = salida_funcion[7] #guardamos la martiz de adyacencia original
                diccionario_original = salida_funcion[8] #guardamos el diccionario de la base de datos original
                etiquetas_grafo = salida_funcion[9]
                indice_max_nombres = salida_funcion[10]
                indice_max_apellidos = salida_funcion[11]
                lista_variables_eliminadas_por_pasada = salida_funcion[1]                
                uf1.actualizar_fichero_variables(ruta_fichero_variables_eliminadas,lista_variables_eliminadas_por_pasada,separador_ficheros_variables)
                
            else:# si es la eliminacion de una redundancia de la permutacion distinta de la primera, sobre el csv resultado de la eliminacion anterior            
                pasada_actual = indice_redundancia
                salida_funcion = eliminar_redundancia(ruta_fichero,ruta_fichero_var_individuales,ruta_fichero_var_vectoriales,ruta_fichero_variables_eliminadas,ruta_fichero_variables_modificadas,redundancia_eliminar,separador,separador_ficheros_variables,separador_apellidos,tipo_fichero,modo_operacion,ruta_fichero_resumen,numero_unos_matriz_A,pasada_actual,posicion_grafo,A_original,diccionario_original,etiquetas_grafo,indice_max_nombres,indice_max_apellidos)
                ruta_csv_salida = salida_funcion[0]
                ruta_fichero = ruta_csv_salida
                lista_variables_eliminadas_por_pasada = salida_funcion[1]
                ruta_fichero_resumen = salida_funcion[3]
                numero_final_unos = salida_funcion[5]
                posicion_grafo = salida_funcion[6]
                A_original = salida_funcion[7]
                diccionario_original = salida_funcion[8]
                etiquetas_grafo = salida_funcion[9]
                indice_max_nombres = salida_funcion[10]
                indice_max_apellidos = salida_funcion[11]
                uf1.actualizar_fichero_variables(ruta_fichero_variables_eliminadas,lista_variables_eliminadas_por_pasada,separador_ficheros_variables)
            
            if(modo_operacion == _('individualizado')):
                uf1.imprimir_porcentaje_resumen(numero_unos_matriz_A,numero_final_unos,ruta_fichero_resumen)
        
        if(modo_operacion != _('individualizado')):
            uf1.imprimir_porcentaje_resumen(numero_unos_matriz_A,numero_final_unos,ruta_fichero_resumen)
        print "\n"
        if (tipo_fichero == 'csv' or tipo_fichero == _('base datos')):
            base = pd.read_csv(ruta_csv_salida,delimiter=separador)
        elif(tipo_fichero == 'excel'):
            xl = pd.ExcelFile(ruta_csv_salida)
            base = xl.parse('Csv_sin_redundancias')
    
#funcion que recibe un fichero y un nuemro de redundancia y elimina las variables que presentan ese tipo de redundancia
#devuelve un fichero como el original pero sin las variables redundantes
#Se divide en dos fase, primero se calcula la matriz de pesos y en la segunda fase el csv sin la redundancia especificada
def eliminar_redundancia(ruta_fichero,ruta_fichero_var_individuales,ruta_fichero_var_vectoriales,ruta_fichero_variables_eliminadas,ruta_fichero_variables_modificadas,redundancia_eliminar,separador,separador_ficheros_variables,separador_apellidos,tipo_fichero,modo_operacion,ruta_fichero_resumen,numero_unos_matriz_A,pasada_actual,posicion_grafo,A_original,diccionario_original,etiquetas_grafo,indice_max_nombres,indice_max_apellidos):
#----------------------------------------------------------Fase I. Obtencion de la matriz de pesos-------------------------------------------------------
    ruta_directorio_ficheros_generados = '../generated_files/'
    ruta_directorio_resumenes = '../summary_files/'
    ruta_directorio_grafos = '../graphs/'

    if (tipo_fichero == 'csv'):
        base = pd.read_csv(ruta_fichero,delimiter=separador,low_memory=False)
    
    elif(tipo_fichero == 'excel'):
        excel_path = ruta_fichero
        # Load spreadsheet
        fichero_excel = pd.ExcelFile(excel_path)
        # Print the sheet names
        if len(fichero_excel.sheet_names) > 1:             
            hoja_seleccionada = ''
            lista_hojas = fichero_excel.sheet_names
            while hoja_seleccionada not in lista_hojas:
                print _('El fichero proporcionado contiene mas de una hoja.Por favor, seleccione la hoja con la que trabajar')
                print lista_hojas
                hoja_seleccionada = raw_input(_('Seleccione una hoja valida con la que trabajar: '))
               
        else:
            hoja_seleccionada = fichero_excel.sheet_names[0]            
        # Load a sheet into a DataFrame by name    
        base = fichero_excel.parse(hoja_seleccionada)      
    
    #almacenamos en lista_variables_csv la lista con los nombres de las columnas
    lista_variables_csv = list(base)
    base.columns = lista_variables_csv
       
    #relacionamos la posicion de la variable en el csv original con el nombre de la variable, creando un diccionario    
    diccionario_variables = uf1.generar_diccionario_variables_indices_csv(lista_variables_csv)
    
    #obtenemos las lista de variables si las hay
    lista_variables_individuales = uf1.leer_variables_fichero(ruta_fichero_var_individuales,separador_ficheros_variables)
    lista_variables_vectoriales = uf1.leer_variables_fichero(ruta_fichero_var_vectoriales,separador_ficheros_variables)    
    variables_eliminadas = uf1.obtener_lista_variables_eliminadas_csv_original(ruta_fichero_variables_eliminadas) #variables_eliminadas 
    
    if(lista_variables_vectoriales != [] and lista_variables_individuales != []): # el programa toma de los ficheros las vriables individuales y vectoriales
        uf1.colored_print(_('El usuario hace distincion entre variables individuales y vectoriales'),'green')
        lista_individuales = [] #lista_variables_individuales
        for elemento in lista_variables_individuales:
            if(elemento in lista_variables_csv):
                lista_individuales.append(elemento)
                
        lista_variables_individuales = lista_individuales
        #obtenemos las variables vectoriales que pueden dar lugar a conflictos porque tienen nombres contenidos unos dentro de otros
        lista_vectores_variables_relacionadas = uf1.obtener_vectores_variables_relacionadas(lista_variables_vectoriales)       
        #obtenemos los variables vectoriales y sus apellidos
        diccionario_variables_vectoriales_apellidos = uf1.obtener_apellidos_variables_listas(lista_variables_vectoriales,lista_vectores_variables_relacionadas,lista_variables_csv,variables_eliminadas,separador_apellidos)       
    
    else:
        uf1.colored_print( _('No se han proporcionado variables individuales y vectoriales. Se obtendran directamente.'),'green')
        #obtenemos los apellidos de las variables
        lista_individuales_diccionario_vectoriales = uf1.obtener_apellidos_variables_fichero(lista_variables_csv,variables_eliminadas,separador_apellidos)
        lista_variables_individuales = lista_individuales_diccionario_vectoriales[0]
        diccionario_variables_vectoriales_apellidos = lista_individuales_diccionario_vectoriales[1]
    
 
    
    if(lista_variables_individuales == [] and diccionario_variables_vectoriales_apellidos == {}):
        uf1.colored_print("Error de reconocimiento de variables ",'red')
        return sys.exit(0)
        
    
    for elemento in variables_eliminadas:
        if elemento in base:
            base = base.drop(labels=[elemento],axis=1)
           
    #generamos las matrices de adyacencia y asociada
    matrices_adyacencia_asociada = uf1.generar_matriz_adyacencia_y_asociada(lista_variables_individuales,diccionario_variables_vectoriales_apellidos,separador_apellidos) #devuelve una lista con dos listas.La matriz de adyacencia y la matriz asociada        
    matriz_adyacencia = matrices_adyacencia_asociada[0] #matriz de aydacencia    
    matriz_asociada = matrices_adyacencia_asociada[1] #matriz nombres_apellidos asociada a matriz de ayacencia
      
    #creamos un diccionario que permita obtener la posición de una variable(nombre o nombre con apellido) en la matriz de adyacencia
    diccionario_variables_posicion_matriz = uf1.generar_diccionario_relacion_madyacencia_masociada(matriz_asociada)
    #Generamos el grafo con las variables del csv original
    if(pasada_actual == 0):
        matriz_adyacencia_np = np.array(matriz_adyacencia)
        etiquetas_grafo = matrices_adyacencia_asociada[2][0]
        indice_max_nombres=matrices_adyacencia_asociada[2][1]
        indice_max_apellidos = matrices_adyacencia_asociada[2][2]
        posicion_grafo = uf1.generar_grafo_no_dirigido(matriz_adyacencia_np,etiquetas_grafo,indice_max_nombres,indice_max_apellidos,ruta_directorio_grafos + 'original_graph.png',posicion_grafo)
        A_original = uf1.copiar_matriz_por_valor(matriz_adyacencia)
        diccionario_original = {}
        for key in diccionario_variables_posicion_matriz:
            diccionario_original[key] = diccionario_variables_posicion_matriz[key]      
        
      
    #obtenemos la matriz de pesos
    matriz_general_pesos = uf1.generar_matriz_pesos(base,variables_eliminadas,diccionario_variables,matriz_adyacencia,diccionario_variables_posicion_matriz,separador)
    
    #-----------------------------------------------------------Fin fase I. Obtencion de la matriz de pesos------------------------------------------------------

    #-----------------------------------------------------------Fase 2. Eliminacion de Redundancias-----------------------------------------------------
    variables_redundantes = []
    #-----------------------------------------------------------Fase 2. Eliminacion de redundancias de Tipo 1-------------------------------------------------
    #creamos un nuevo diccionario de la forma key-(fila,columna): value-variables
    diccionario_posicion_matriz_variables = ur1.generar_diccionario_posicion_variables(diccionario_variables_posicion_matriz)
    extension = os.path.splitext(ruta_fichero)[1]
    nombre_fichero = os.path.basename(ruta_fichero).split('.')[0]
    flag_matriz_adyacencia_creada = ruta_fichero_resumen
    if(redundancia_eliminar == 1):
        uf1.colored_print(_("=>Eliminacion de la redundancia de tipo 1"),'green')
        ruta_fichero_csv_generado= ruta_directorio_ficheros_generados + nombre_fichero + _('_sin_rT1') + extension
        ruta_fichero_volcado_datos =ruta_directorio_resumenes + _('resumen_') + nombre_fichero + _('_sin_rT1') + '.txt'
        #Comparamos todas las instancias de la matriz de pesos y nos quedamos con una en la que los valores serán 'nan' o cualquier otro valor
        instancia_resultado = ur1.comparar_instancias(matriz_general_pesos)
        #obtenemos la lista con las variables que se eliminaran por ser redundantes
        variables_redundantes = ur1.obtener_lista_variables_redundantes(instancia_resultado,diccionario_posicion_matriz_variables)        
        #registramos en un fichero las variables redundantes y el porcentaje de redundancia respecto al fichero original
        if(modo_operacion != _('individualizado')):
            variables_redundantes_totales = variables_redundantes + variables_eliminadas
        else:
            variables_redundantes_totales = variables_redundantes
        matriz_adyacencia_prima = uf1.calcular_matriz_adyacencia_prima(A_original,diccionario_original,variables_redundantes_totales)
        
        if(modo_operacion == _('individualizado')):
            uf1.imprimir_variables_redundantes(_("tipo 1"),variables_redundantes,ruta_fichero_volcado_datos)
            uf1.imprimir_porcentajes_redundancia(matriz_adyacencia,matriz_adyacencia_prima,variables_redundantes,ruta_fichero_volcado_datos,0,0,modo_operacion)
        elif(modo_operacion == _('acumulativo')):
            if(flag_matriz_adyacencia_creada != ""):# no es la primera pasada, se crea actualiza el fichero resumen              
                with open(ruta_fichero_resumen,'r') as fichero_anterior:
                    with open(ruta_fichero_volcado_datos, 'w') as fichero_volcado:
                        for line in fichero_anterior:                            
                            fichero_volcado.write(line) 
            uf1.imprimir_variables_redundantes(_("tipo 1"),variables_redundantes,ruta_fichero_volcado_datos)            
            uf1.imprimir_porcentajes_redundancia(matriz_adyacencia,matriz_adyacencia_prima,variables_redundantes,ruta_fichero_volcado_datos,numero_unos_matriz_A,pasada_actual,modo_operacion)
#-----------------------------------------------------------Fase 2.1 Eliminacion de redundancias de Tipo 2-------------------------------------------------
    elif(redundancia_eliminar == 2):
        uf1.colored_print(_("=>Eliminacion de la redundancia de tipo 2"),'green')
        ruta_fichero_csv_generado= ruta_directorio_ficheros_generados + nombre_fichero + _('_sin_rT2') + extension
        ruta_fichero_volcado_datos = ruta_directorio_resumenes +_('resumen_') + nombre_fichero + _('_sin_rT2') + '.txt'
        
        #Comparamos todas las instancias de la matriz de pesos y nos quedamos con una en la que los valores serán 'no redundante' o cualquier otro valor
        instancia_resultado = ur2.comparar_instancias(matriz_general_pesos)
    
        #obtenemos la lista con las variables que se eliminaran por ser redundantes
        variables_redundantes = ur2.obtener_lista_variables_redundantes(instancia_resultado,diccionario_posicion_matriz_variables)
        variables_redundantes_t2 = variables_redundantes[1]        
        
        if(modo_operacion != _('individualizado')):
            variables_redundantes_totales = variables_redundantes_t2 + variables_eliminadas
        else:
            variables_redundantes_totales = variables_redundantes_t2
        #registramos en un fichero las variables redundantes y el porcentaje de redundancia respecto al fichero original
        matriz_adyacencia_prima = uf1.calcular_matriz_adyacencia_prima(A_original,diccionario_original,variables_redundantes_totales)
        if(modo_operacion == _('individualizado')):
            uf1.imprimir_variables_redundantes(_("tipo 2"),variables_redundantes_t2,ruta_fichero_volcado_datos)
            uf1.imprimir_porcentajes_redundancia(matriz_adyacencia,matriz_adyacencia_prima,variables_redundantes_t2,ruta_fichero_volcado_datos,0,0,modo_operacion)
        elif(modo_operacion == _('acumulativo')):
            if(flag_matriz_adyacencia_creada != ""):# es la primera pasada, se crea un archivo de resumen
                with open(ruta_fichero_resumen,'r') as fichero_anterior:
                    with open(ruta_fichero_volcado_datos, 'w') as fichero_volcado:
                        for line in fichero_anterior:                            
                            fichero_volcado.write(line) 
            uf1.imprimir_variables_redundantes(_("tipo 2"),variables_redundantes_t2,ruta_fichero_volcado_datos)
            uf1.imprimir_porcentajes_redundancia(matriz_adyacencia,matriz_adyacencia_prima,variables_redundantes_t2,ruta_fichero_volcado_datos,numero_unos_matriz_A,pasada_actual,modo_operacion)
                
        variables_redundantes = variables_redundantes_t2

 #-----------------------------------------------------------Fase 3.1 Eliminacion de redundancias de Tipo 3-------------------------------------------------
    elif(redundancia_eliminar == 3):
        uf1.colored_print(_("=>Eliminacion de la redundancia de tipo 3"),'green') #Vamos a trabajar con la identidad y con la matriz de pesos C
        separador_nombre_apellido_original = separador_apellidos
        ruta_fichero_csv_generado= ruta_directorio_ficheros_generados + nombre_fichero + _('_sin_rT3') + extension
        ruta_fichero_volcado_datos = ruta_directorio_resumenes+ _('resumen_') + nombre_fichero + _('_sin_rT3') + '.txt'
        
        #creamos un nuevo diccionario en el que se agrupan los nombres con los mismos apellidos para las variables vectoriales
        diccionario_apellidos_nombres = ur3.obtener_diccionario_nombres_segun_apellidos(diccionario_variables_vectoriales_apellidos)        
        lista_listas_nombres_redundantes= ur3.obtener_lista_vectores_variables_redundantes_t3(diccionario_apellidos_nombres,diccionario_variables_vectoriales_apellidos,diccionario_variables_posicion_matriz,matriz_general_pesos,lista_variables_individuales,variables_eliminadas,separador_nombre_apellido_original)        
        lista_listas_nombres_redundantes_individuales = lista_listas_nombres_redundantes[0]
        lista_listas_nombres_redundantes_vectoriales = lista_listas_nombres_redundantes [1]
        #print lista_listas_nombres_redundantes_vectoriales
        variables_redundantes_t3 = ur3.obtener_lista_variables_redundantes(lista_listas_nombres_redundantes_individuales,lista_listas_nombres_redundantes_vectoriales,diccionario_variables_vectoriales_apellidos,separador_nombre_apellido_original)                
        #registramos en un fichero las variables redundantes y el porcentaje de redundancia respecto al fichero original
        if(modo_operacion != _('individualizado')):
            variables_redundantes_totales = variables_redundantes_t3 + variables_eliminadas
        else:
            variables_redundantes_totales = variables_redundantes_t3
        matriz_adyacencia_prima = uf1.calcular_matriz_adyacencia_prima(A_original,diccionario_original,variables_redundantes_totales)
        if(modo_operacion == _('individualizado')):
            uf1.imprimir_variables_redundantes("tipo 3",variables_redundantes_t3,ruta_fichero_volcado_datos)
            uf1.imprimir_porcentajes_redundancia(matriz_adyacencia,matriz_adyacencia_prima,variables_redundantes_t3,ruta_fichero_volcado_datos,0,0,modo_operacion)
        elif(modo_operacion == _('acumulativo')):
            if(flag_matriz_adyacencia_creada != ""):# es la primera pasada, se crea un archivo de resumen
                with open(ruta_fichero_resumen,'r') as fichero_anterior:
                    with open(ruta_fichero_volcado_datos, 'w') as fichero_volcado:
                        for line in fichero_anterior:                            
                            fichero_volcado.write(line) 
            uf1.imprimir_variables_redundantes(_("tipo 3"),variables_redundantes_t3,ruta_fichero_volcado_datos)
            uf1.imprimir_porcentajes_redundancia(matriz_adyacencia,matriz_adyacencia_prima,variables_redundantes_t3,ruta_fichero_volcado_datos,numero_unos_matriz_A,pasada_actual,modo_operacion)
            
        variables_redundantes = variables_redundantes_t3
               
    #actualizamos la lista inicial de variables eliminadas anadiendo las redundantes
    variables_eliminadas = ur1.actualizar_lista_variables_eliminadas(variables_eliminadas,variables_redundantes)
    
    uf1.colored_print("Total number of variables with this type of redundancy: " + str(len(variables_redundantes)),'cyan')
    
    #actualizamos el diccionario eliminando las variables que no se recogeran en el csv por ser redundante
    diccionario_variables_posicion_matriz = ur1.actualizar_diccionario(variables_redundantes,diccionario_variables_posicion_matriz)
    
    #generamos el nuevo csv sin redundancias( y sin las variables eliminadas)
    matriz_csv_final = ur1.generar_csv_sin_redundancia(matriz_general_pesos,diccionario_variables_posicion_matriz,lista_variables_csv,ruta_fichero_csv_generado,separador,tipo_fichero)
    
    #Generamos el grafo correspondiente a la eliminacion de la redundancia actual   
    matriz_adyacencia_prima = np.array(matriz_adyacencia_prima)
    archivo = os.path.basename(ruta_fichero_volcado_datos).split('.')[0]
    archivo = ruta_directorio_grafos + _('grafo_') + archivo     
    pos_graf = uf1.generar_grafo_no_dirigido(matriz_adyacencia_prima,etiquetas_grafo,indice_max_nombres,indice_max_apellidos,archivo +'.png',posicion_grafo)
    #uf1.generar_grafo_dirigido(matriz_adyacencia_prima,etiquetas_grafo,indice_max_nombres,indice_max_apellidos,archivo+ '.dot')
        
    if(numero_unos_matriz_A == 0):
        numero_unos_matriz_A = np.count_nonzero(matriz_adyacencia)
   
    numero_final_unos = float(np.count_nonzero(matriz_adyacencia_prima))
    return [ruta_fichero_csv_generado,variables_redundantes,tipo_fichero,ruta_fichero_volcado_datos,numero_unos_matriz_A,numero_final_unos,pos_graf,A_original,diccionario_original,etiquetas_grafo,indice_max_nombres,indice_max_apellidos]

#==============================================================Inicio de Ejecucion del programa============================================