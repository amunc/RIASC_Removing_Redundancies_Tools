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

import gettext
import getpass
import csv
import sys
import math
import os.path
from db import DB
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from colorama import init,Fore,Style
init()

def cargar_paquetes_idioma(dominio,idioma):
    paquete = ""
    if(idioma == 'EN'):
        paquete = 'en_US'
    elif(idioma == 'ES'):
        paquete = 'es_ES'
    idioma_cargado = gettext.translation(dominio, localedir='../Locale', languages=[paquete])                 
    idioma_cargado.install()

#Funcion que permite establecer los paramteros con los que trabajara el script (idioma, origen de datos, separadores...)
def definir_parametros_iniciales(ruta_fichero_variables_eliminadas,ruta_directorio_ficheros_entrada):
    #Paquete de idioma
    idioma = ""
    idiomas_posibles = ['ES','EN']
    while (idioma not in idiomas_posibles):
        idioma = raw_input("Por favor, seleccione idioma / Please, select language"+str(idiomas_posibles) + ": ")
    cargar_paquetes_idioma('paquete_idiomas',idioma)
    
    extensiones_validas_fichero = ['csv','excel',_('base datos'),_('salir')]    
    bases_datos = ['mysql','postgres']
    
    #Elegir un origen de datos
    extension_fichero = ""
    while (extension_fichero not in extensiones_validas_fichero):
        extension_fichero = raw_input(_("Por favor, seleccione el origen de la muestra ") + str(extensiones_validas_fichero) + ": ")
        
    if(extension_fichero == _('salir')):
        sys.exit()
    elif(extension_fichero == _('base datos')): #conexion con base de datos
        base_datos = ""    
        while (base_datos not in bases_datos):
            base_datos = raw_input(_('Seleccione el tipo de base de datos ')+ str(bases_datos) +" :" )
        if(base_datos == 'mysql'):
            databasebtype = 'mysql'                    
        elif(base_datos == 'postgres'):
            databasebtype = 'postgres'
        parametros_correctos = False
        while(parametros_correctos == False):
            host = raw_input(_('Introduzca el host de la base de datos: '))
            nombre_usuario = raw_input(_('Introduzca el nombre de usuario: '))
            pass_usuario = getpass.getpass(_('Introduzca clave acceso: '))
            databasename = raw_input(_('Introduza el nombre de la base de datos: '))
            tabla = raw_input(_('Introduzca el nombre de la tabla a la que desea acceder: '))
            try:
                database = DB(username=nombre_usuario, password=pass_usuario, hostname=host, dbtype=databasebtype,dbname=databasename)
                dataframe = database.query("select * from " + tabla + ";")
                ruta_nuevo_fichero = ruta_directorio_ficheros_entrada + tabla +".csv"
                dataframe.to_csv(ruta_nuevo_fichero,sep=';',index=False)
                ruta_fichero = ruta_nuevo_fichero
                extension_fichero = 'csv'
                parametros_correctos = True
            except:
                print _("\nAlguno de los parametros introducidos es incorrecto. Intentalo de nuevo")
            
    else:            
        fichero_encontrado = False
        extension_correcta = False
        while (fichero_encontrado == False or extension_correcta == False):            
            ruta_fichero = raw_input(_('Por favor, seleccione la muestra con la que trabajara: '))
            fichero_encontrado = os.path.exists(ruta_fichero)
            if(fichero_encontrado == True):
                ext = os.path.splitext(ruta_fichero)[1]
                if(extension_fichero == 'csv' and ext =='.csv'):
                    extension_correcta = True
                elif(extension_fichero == 'excel' and (ext == '.xls' or ext == '.xlsx')):
                    extension_correcta = True
                else:
                    print(_("La extension de la muestra seleccionada no se corresponde con la del tipo de fichero elegido ") + '('+extension_fichero+')')
                    
    #Elegir ficheros de variables auxiliares y variables vectoriales  
    respuesta = ""
    while(respuesta != _('S') and respuesta != 'N'):
        respuesta = raw_input(_("Va a utilizar un fichero para las variables individuales y otro para las vectoriales?['S','N']: "))
        if(respuesta == 'N'):
            ruta_fichero_var_individuales ='' 
            ruta_fichero_var_vectoriales ='' 
        elif(respuesta == _('S')):
            fich_individuales_encontrado = False
            fich_vectoriales_encontrado = False
            while(fich_individuales_encontrado == False):
                ruta_fichero_var_individuales = raw_input(_('Indique la ruta al fichero variables individuales: '))
                fich_individuales_encontrado = os.path.exists(ruta_fichero_var_individuales)
            while(fich_vectoriales_encontrado == False):
                ruta_fichero_var_vectoriales = raw_input(_('Indique la ruta al fichero variables vectoriales: '))
                fich_vectoriales_encontrado = os.path.exists(ruta_fichero_var_vectoriales)
    
    #Creacion del fichero vacio para las variables eliminadas    
    fichero_encontrado = os.path.exists(ruta_fichero_variables_eliminadas)
    open(ruta_fichero_variables_eliminadas, 'w').close()
    
    ruta_fichero_variables_modificadas = ''
    
    #Pretratamiento de datos procedentes de ficheros csv, separador de apellidos y separador de campos        
    if(extension_fichero == 'csv'):
        separador_original = detectar_separador_campos(ruta_fichero)
        print 
        detector_correcto = ""
        detector_correcto = raw_input(_("Se ha detectado ") + separador_original + _(" como separador de campos. Es correcto? ['S','N']: "))
        while(detector_correcto != _('S') and detector_correcto != 'N'):
            detector_correcto = raw_input(_("Es correcto ['S','N']: "))
        if(detector_correcto == 'N'):
            separador_original = ""
            while (len(separador_original) != 1):
                separador_original = raw_input(_("Introduzca separador de campos: "))
                separador_original = separador_original.strip()                
                try:
                    if(ord(separador_original) not in range(0,128)):
                        separador_original = ""
                except:
                    separador_original = ""
                                                         
        if(comprobar_si_caracter_csv(ruta_fichero,separador_original,separador_original) == 0): # es correcto de inicio
            separador_contenido_csv = False
        else: #hay que modificarlo por estar contenido en los campos                 
            nombre_nuevo_fichero= raw_input(_('El separador del fichero (') +separador_original+ _(') esta contenido en los campos. Es necesario modificarlo para poder trabajar con el fichero.\nDebe introducir un nombre para el nuevo fichero que se creara: '))
            while(nombre_nuevo_fichero==""):
                if(nombre_nuevo_fichero.strip() == ""):
                    nombre_nuevo_fichero = ""
            ruta_nuevo_fichero= ruta_directorio_ficheros_entrada + nombre_nuevo_fichero + '.csv'            
            ruta_separador = crear_nuevo_fichero_separador(ruta_fichero,ruta_nuevo_fichero,separador_original)
            ruta_fichero = ruta_separador[0]
            separador_original = ruta_separador[1]
    else:
        separador_original = '' #vale cualquiera puesto que no va a influir en la ejecucion del programa
    
    separador_apellidos= ""        
    while(separador_apellidos == ""):
        separador_apellidos = raw_input(_("Por favor, introduzca el separador de nombres y apellidos de variables: "))
        if(len(separador_apellidos) == 1):
            if(ord(separador_apellidos) not in range(0,128)):
                separador_apellidos = ""
        else:
            separador_apellidos = ""
        

    #Seleccion del modo de funcionamiento
    lista_modos_operacion = [_('individualizado'),_('acumulativo')]
    modo_operacion = ""
    while (modo_operacion not in lista_modos_operacion):
        modo_operacion = raw_input(_('Por favor, seleccione el modo de operacion ') + str(lista_modos_operacion) + ': ' )
    permutacion_redundancias = ''      
    permutaciones_validas = ['1','2','3','12','21','13','31','23','32','123','132','213','231','312','321']    
    while (permutacion_redundancias not in permutaciones_validas):
        permutacion_redundancias = raw_input(_('Por favor, introduzca el orden de eliminacion de redundancias (p.e 123) : '))
        if (permutacion_redundancias not in permutaciones_validas):
            print _('El orden introducido no es correcto. Los ordenes posibles de eliminacion son: ') + str(permutaciones_validas)
    parametros = [permutacion_redundancias,ruta_fichero,ruta_fichero_var_individuales,ruta_fichero_var_vectoriales,ruta_fichero_variables_eliminadas,ruta_fichero_variables_modificadas,separador_original,extension_fichero,modo_operacion,separador_apellidos,idioma]
    return parametros

#Funcion que obtiene, sin intervencion del usuario, el separador de campos de la muestra en formato csv
def detectar_separador_campos(ruta_csv):
    diccionario = {}
    rango_numeros = []
    rango_mayusculas = []
    rango_minusculas = []
    for i in range (48,58):
        rango_numeros.append(i)
    for i in range (65,91):
        rango_mayusculas.append(i)
    for i in range (97,123):
        rango_minusculas.append(i)
    especiales = [32,34,39,46] #espacio, comilla simple, comilla doble, asterisco, punto se decartan como separadores por ser muy frecuentes y no usados como tal
    with open(ruta_csv, 'r') as archivo_csv:
        lector_archivo = csv.reader(archivo_csv,delimiter='\n')                       
        cabecera = str(next(lector_archivo))
        for caracter in cabecera:
            valor_ascii = ord(caracter)
            if (valor_ascii not in especiales) and (valor_ascii not in rango_numeros) and (valor_ascii not in rango_mayusculas) and (valor_ascii not in rango_minusculas):
                if caracter not in diccionario:
                    diccionario[caracter] = 1
                else:
                    valor=diccionario[caracter]
                    valor+=1
                    diccionario[caracter] = valor
    frecuencia_max = 0
    caracter_frec_max = ''
    for elemento in diccionario:
        if(frecuencia_max == 0): # es el primer elemento
            frecuencia_max = diccionario[elemento]
            caracter_frec_max = elemento
        else:
            caracter = elemento
            if diccionario[elemento] > frecuencia_max:
                frecuencia_max = diccionario[elemento]
                caracter_frec_max = elemento
    return caracter_frec_max

#funcion que permite determinar si el separador de campos forma parte de los campos de la muestra
def comprobar_si_caracter_csv(ruta_csv,separador,caracter_buscado):
    contador = 0
    with open(ruta_csv, 'r') as archivo_csv:
        lector_archivo = csv.reader(archivo_csv,delimiter=separador)                       
        for linea in lector_archivo:
            for elemento in linea:
                if(caracter_buscado in elemento):
                    contador+=1

    return contador

#Funcion que comprueba que caracteres no se encuentran actualmente en la muestra (son separadores validos)
def buscar_caracteres_no_contenidos_csv(ruta_csv,separador):
    lista_separadores_validos = []
    for indice in range(32,127):
        no_encontrado = True
        with open(ruta_csv, 'r') as archivo_csv:
            lector_archivo = csv.reader(archivo_csv,delimiter=separador)                       
            for linea in lector_archivo:
                for ind_elemento in range(len(linea)):
                    if(no_encontrado == True ):
                        if(chr(indice) in linea[ind_elemento]):
                            no_encontrado = False
        if(no_encontrado == True and len(chr(indice)) == 1):
            lista_separadores_validos.append(chr(indice))
    return lista_separadores_validos

#Funcion que permite crear un fichero con un nuevo separador, si el actual no es valido por estar contenido en los campos
def crear_nuevo_fichero_separador(ruta_fichero_csv,ruta_fichero_csv_variables_formateadas,separador_original):
    print _('Comprobando separadores validos para la muestra...')
    caracteres_no_contenidos_csv = buscar_caracteres_no_contenidos_csv(ruta_fichero_csv,separador_original)
    print _('Lista valida de separadores: ')
    print caracteres_no_contenidos_csv
    separador = raw_input(_("Introduzca el nuevo separador de campos de entre los de la lista: "))
    while (separador not in caracteres_no_contenidos_csv):
        separador = raw_input(_("Introduzca el nuevo separador de campos de entre los de la lista: "))
    base = pd.read_csv(ruta_fichero_csv,delimiter=separador_original,low_memory=False)
    base.to_csv(ruta_fichero_csv_variables_formateadas,index= False,sep=separador)
    return [ruta_fichero_csv_variables_formateadas,separador]


#Obtenemos un diccionario que relaciona la variable del fichero csv con el numero de columna (es decir, la posicion en la primera linea del csv)
def generar_diccionario_variables_indices_csv(lista_variables):
    diccionario_variables = {}
    for indice in range(len(lista_variables)):
        diccionario_variables[indice] = lista_variables[indice]
    return diccionario_variables


#==================================================================================================================================================================
#==========================================================Funciones para la creacion de la matriz de adyacencia===================================================
#==================================================================================================================================================================
def eliminar_contenido_fichero(fName):
    with open(fName, "w"):
        pass    

def leer_variables_fichero(ruta_fichero_csv,separador):
    lista_variables = []
    if(ruta_fichero_csv != ''):        
        with open(ruta_fichero_csv, 'r') as archivo_csv:
            lector_archivo = csv.reader(archivo_csv,delimiter=separador)
            for elemento in lector_archivo:
                lista_variables.append(elemento[0])
    return sorted(lista_variables)

#acutalizamos el fichero con las variables eliminadas
def actualizar_fichero_variables(ruta_fichero_variables,lista_variables_eliminadas,separador_variables):
    fichero_volcado_datos = open(ruta_fichero_variables,'a')
    for elemento in lista_variables_eliminadas:
        informacion = elemento + separador_variables
        fichero_volcado_datos.write(informacion)
    fichero_volcado_datos.close()
    
#obtenemos clusters con grupos de variables que a nivel sintactico forman parte de otras y puede haber problemas en la obtencion de los apellidos
def obtener_vectores_variables_relacionadas(lista_variables_vectoriales):
    lista_control = [] # se mantiene un control de las que ya se han ido insertando
    lista_vectores_variables_relacionadas = []
    for indice in range(len(lista_variables_vectoriales)):
        variable1 = lista_variables_vectoriales[indice]#obtenemos la variable a comparar
        indice_actual = indice+1
        lista_parcial = []
        if (variable1 not in lista_control):
            for indice2 in range(indice_actual,len(lista_variables_vectoriales)):
                variable2 = lista_variables_vectoriales[indice2]
                if (variable2 not in lista_control):
                    if (variable2.find(variable1) == 0) and (variable2.index(variable1) == 0): #estan relacionadas
                        if(variable1 not in lista_parcial):
                            lista_parcial.append(variable1)
                        if(variable1 not in lista_control):
                            lista_control.append(variable1)
                        if(variable2 not in lista_parcial):
                            lista_parcial.append(variable2)
                        if(variable2 not in lista_control):
                            lista_control.append(variable2)
        if(lista_parcial != []):
            lista_vectores_variables_relacionadas.append(lista_parcial)   
    return lista_vectores_variables_relacionadas

#
def obtener_apellidos_variables_listas(lista_variables_vectoriales,lista_vectores_variables_relaciondas,lista_variables_csv,lista_variables_eliminadas,separador_apellidos):
    diccionario_variables_apellidos = {}
    lista_variables_relacionadas = []
    for elemento in lista_vectores_variables_relaciondas:      
        lista_variables_relacionadas+= elemento
    
    #Creamos un diccionario con las variables vectoriales no relacionadas y sus apellidos
    for variable_vectorial in lista_variables_vectoriales:
        if (variable_vectorial not in lista_variables_relacionadas): # las que dan problemas porque tomaran mas apellidos de los correspondientes, se tratan despues
            for variable_csv in lista_variables_csv:
                if (variable_csv.find(variable_vectorial) == 0) and (variable_csv.index(variable_vectorial) == 0): # comprobamos que la contiene y forma parte del nombre de la variable del csv
                    apellido = variable_csv.replace(variable_vectorial+separador_apellidos,'')
                    if(apellido == ''): # es decir, es una variable sin apellido pero no es individual
                        if (variable_vectorial) not in lista_variables_eliminadas:
                            apellido = variable_vectorial
                    if(variable_vectorial not in diccionario_variables_apellidos): #insertamos el primer apellido                    
                        if (variable_vectorial +separador_apellidos+ apellido) not in lista_variables_eliminadas:
                            diccionario_variables_apellidos[variable_vectorial] = [apellido]
                    else: #insertamos el n-esimo apellido                    
                        if (variable_vectorial +separador_apellidos+ apellido) not in lista_variables_eliminadas:
                            valores = diccionario_variables_apellidos[variable_vectorial]
                            valores.append(apellido)
                            diccionario_variables_apellidos[variable_vectorial] = valores                    
            #ordenamos la lista de valores            
            if (variable_vectorial) in diccionario_variables_apellidos:
                valores = diccionario_variables_apellidos[variable_vectorial]
                valores = sorted (valores)
                diccionario_variables_apellidos[variable_vectorial] = valores
        
    #Creamos las lista de apellidos para las variables realacionadas
    lista_variables_apellidos = []
    for vector_variables in lista_vectores_variables_relaciondas:
        vector_variables_apellidos = []        
        for variable_vectorial in vector_variables:            
            lista_apellidos = []
            for variable_csv in lista_variables_csv:
                if (variable_csv.find(variable_vectorial) == 0) and (variable_csv.index(variable_vectorial) == 0): # comprobamos que la contiene y forma parte del nombre de la variable del csv
                    apellido = variable_csv.replace(variable_vectorial+separador_apellidos,'')
                    if(apellido == ''): # es decir, es una variable sin apellido pero no es individual
                        if (variable_vectorial) not in lista_variables_eliminadas:
                            apellido = variable_vectorial
                            lista_apellidos.append(apellido)
                    elif (variable_vectorial +separador_apellidos+ apellido) not in lista_variables_eliminadas:
                        lista_apellidos.append(apellido)
            if(lista_apellidos != []):
                vector_variables_apellidos.append([variable_vectorial,lista_apellidos])                      
        if(vector_variables_apellidos != []):
            lista_variables_apellidos.append(vector_variables_apellidos)
    
    #en este punto tenemos las listas de nombres relacionados entre si con los apellidos
    #[[[nombre,[apellido1,apellido2,apellidoN]],[nombre segundo,[apellido2,apellido3]]]
    #el siguiente paso es elminar aquellos apellidos de las variables realcionadas que no les corresponden
    lista_listas_relacionadas = []
    diccionario_elementos_relacionados = {}
    for indice in range(len(lista_variables_apellidos)):
        lista_vectores_concatenacion_nombres_apellidos = []
        for indice_vector_relacionado in range(len(lista_variables_apellidos[indice])): #recorremos los nombres relacionados
            nombre_lista_apellidos = lista_variables_apellidos[indice][indice_vector_relacionado]
            nombre = nombre_lista_apellidos[0]
            diccionario_elementos_relacionados[nombre] = []
            vector_concatenaciones = [nombre]
            nombre = nombre_lista_apellidos[0] + separador_apellidos
            for apellido in nombre_lista_apellidos[1]:
                vector_concatenaciones.append(nombre + apellido)
            lista_vectores_concatenacion_nombres_apellidos.append(vector_concatenaciones)
        lista_listas_relacionadas.append(lista_vectores_concatenacion_nombres_apellidos)
        
    #tenemos la lista con las listas de vectores relacionados
    for lista_vectores_relacionados in lista_listas_relacionadas:
        for indice in range(len(lista_vectores_relacionados)):
            nombre = lista_vectores_relacionados[indice][0]
            indice_siguiente_lista = indice+1
            for indice_elemento_primero in range(1,len(lista_vectores_relacionados[indice])):
                variable1 = lista_vectores_relacionados[indice][indice_elemento_primero]
                encontrado = False
                for indice2 in range(indice_siguiente_lista,len(lista_vectores_relacionados)):
                    indice_elemento_segundo = 1 #empezamos en el segundo porque el primero marca que nombre es
                    while(encontrado == False) and (indice_elemento_segundo <= len(lista_vectores_relacionados[indice2])-1):
                        variable2 = lista_vectores_relacionados[indice2][indice_elemento_segundo]
                        if variable1 == variable2:
                            encontrado = True
                        indice_elemento_segundo+=1
                if(encontrado == False): #si al final de las comparaciones no se ha encontrado
                    #comprobamos conta la lista de variables_vectoriales
                    if(variable1 not in lista_variables_vectoriales):
                        variable1 = variable1.replace(nombre+separador_apellidos,"")
                        if nombre not in diccionario_elementos_relacionados:
                            diccionario_elementos_relacionados[nombre] = [variable1]
                        else:
                            valor = diccionario_elementos_relacionados[nombre]
                            valor.append(variable1)
                            diccionario_elementos_relacionados[nombre] = valor
                        
    #Combinamos los dos diccionarios( el de las variables vectoriales no relacionadas y el de las relacionadas)
    for key in diccionario_elementos_relacionados:
        diccionario_variables_apellidos[key] = diccionario_elementos_relacionados[key]
    
    for key in diccionario_variables_apellidos:
        diccionario_variables_apellidos[key] = sorted(diccionario_variables_apellidos[key])
    return diccionario_variables_apellidos

#Fucion que permite obtener los apellidos de cada variable del fichero csv descartando las eliminadas
def obtener_apellidos_variables_fichero(lista_variables_csv,lista_variables_eliminadas,separador_apellidos):
    diccionario_variables_apellidos = {}    
    lista_variables_individuales = []
    for variable_csv in lista_variables_csv:
        variable_csv = variable_csv.split(separador_apellidos)
        apellido = ""
        variable = variable_csv[0]
        #determinamos si es individual o nombre con apellidos
        if(len(variable_csv) > 1): #tiene un apellido por lo menos
            for indice in range(1,len(variable_csv)):
                if(indice < len(variable_csv) -1 ):
                    apellido += variable_csv[indice]+ separador_apellidos
                else:
                    apellido += variable_csv[indice]
            if(variable not in diccionario_variables_apellidos):
                diccionario_variables_apellidos[variable] = [apellido]
            else:
                valores = diccionario_variables_apellidos[variable]
                valores.append(apellido)
                diccionario_variables_apellidos[variable] = valores                        
        else:
            lista_variables_individuales.append(variable)           
    
    for key in diccionario_variables_apellidos:
        diccionario_variables_apellidos[key] = sorted(diccionario_variables_apellidos[key])
    return [lista_variables_individuales,diccionario_variables_apellidos]


#funcion que crea la matriz de adyacencia y la asociada(nombres, nombres con apellidos)
#recibe como parametro un diccionario en el que se recogen todos los nombres, apellidos y nombres con apellidos
def generar_matriz_adyacencia_y_asociada(lista_variables_individuales,diccionario_variables_vectoriales_apellidos,separador_apellidos): # se le pasaba el diccionario originalmente
   
    #obtenemos tres listas con los nombres, nombres con apellidos y nombres para poder construir la matriz de adyacencia     
    lista_nombres = lista_variables_individuales   
    lista_nombres_apellidos = [] 
    lista_apellidos = [] 
    for variable_vectorial in diccionario_variables_vectoriales_apellidos:
        lista_nombres_apellidos.append(variable_vectorial)
        for apellido in diccionario_variables_vectoriales_apellidos[variable_vectorial]:
            if(apellido not in lista_apellidos):
                lista_apellidos.append(apellido)
           
    #--------------generacion de la matriz de adyacencia-----------------------------------------
    #Primero se genera la fila que se recorrera posteriormente y que se corresponde con las variables (nombres de columnas) de la matriz
    variables_matriz_adyacencia = lista_nombres + lista_nombres_apellidos + lista_apellidos   
 
    #-----------------------------------generacion de "submatrices de la matriz de adyacencia------------------------
    matriz_adyacencia = [] # matriz de 1s y 0s
    matriz_asociada_matriz_adyacencia = [] # matriz en la que aparece el nombre/nombre con apellidos (si en la de adyacencia hay un 1) o 0s
    
    #---------------generacion de "submatriz nombres sin apellidos"----------------------------
    #primeras filas de la matriz de ayacencia, de la fila 0 a la numero total_nombres -1
    matriz_nombres = [] # con la identidad al principio
    for nombre in lista_nombres:
        matriz_parcial_nombres = []
        matriz_parcial_nombres_asociada = []
        for indice in range(len(variables_matriz_adyacencia)):
            if(indice<=len(lista_nombres)-1):
                if(nombre == variables_matriz_adyacencia[indice]):
                    matriz_parcial_nombres.append(1)
                    matriz_parcial_nombres_asociada.append(nombre)
                else:
                    matriz_parcial_nombres.append(0)
                    matriz_parcial_nombres_asociada.append(0)
            else:
                matriz_parcial_nombres.append(0)
                matriz_parcial_nombres_asociada.append(0)
        matriz_nombres.append(matriz_parcial_nombres)
        
        matriz_adyacencia.append(matriz_parcial_nombres)
        matriz_asociada_matriz_adyacencia.append(matriz_parcial_nombres_asociada)
    
        #---------------generacion de "submatriz nombres con apellidos----------------------------
    matriz_nombres_con_apellidos = []
    inicio_matriz_C = len(lista_nombres) + len(lista_nombres_apellidos)
    for nombre_con_apellido in lista_nombres_apellidos:
        matriz_parcial_nombres_apellidos = []
        matriz_parcial_nombres_con_apellidos_asociada = []
        for indice in range(len(variables_matriz_adyacencia)):
            if(indice>=inicio_matriz_C):
                if (variables_matriz_adyacencia[indice] in diccionario_variables_vectoriales_apellidos[nombre_con_apellido]):
                    if(nombre_con_apellido == variables_matriz_adyacencia[indice]):
                        elemento = nombre_con_apellido
                    else:
                        elemento = nombre_con_apellido + separador_apellidos + variables_matriz_adyacencia[indice]
                    matriz_parcial_nombres_apellidos.append(1)                    
                    matriz_parcial_nombres_con_apellidos_asociada.append(elemento)
                else:
                    matriz_parcial_nombres_apellidos.append(0)
                    matriz_parcial_nombres_con_apellidos_asociada.append(0)
            else:
                matriz_parcial_nombres_apellidos.append(0)
                matriz_parcial_nombres_con_apellidos_asociada.append(0)
        matriz_nombres_con_apellidos.append(matriz_parcial_nombres_apellidos)
        
        matriz_adyacencia.append(matriz_parcial_nombres_apellidos)
        matriz_asociada_matriz_adyacencia.append(matriz_parcial_nombres_con_apellidos_asociada)
        
    #---------------------------------    Dentro de esta suzmatriz tenemos C--------------
    #---------------generacion de "submatriz apellidos ----------------------------
    matriz_apellidos = [] # con la identidad al principio
    for apellido in lista_apellidos:
        matriz_parcial_apellidos = []
        matriz_parcial_apellidos_asociada = []
        for indice in range(len(variables_matriz_adyacencia)):
            matriz_parcial_apellidos_asociada.append(0)
            matriz_parcial_apellidos.append(0)
        matriz_apellidos.append(matriz_parcial_apellidos)
        
        matriz_adyacencia.append(matriz_parcial_apellidos)
        matriz_asociada_matriz_adyacencia.append(matriz_parcial_apellidos_asociada)

    diccionario_cabeceras_matriz_adyacencia = {}
    
    for indice in range(len(variables_matriz_adyacencia)):
        diccionario_cabeceras_matriz_adyacencia[indice] = variables_matriz_adyacencia[indice]
    #se duelven las matrices de 1's y 0's, la de nombres con apellidos asociada, un diccionario con las cabeceras para constuir el grafo y unos indices que determinan las posiciones maximas de las variables y los apellidos
    return [matriz_adyacencia,matriz_asociada_matriz_adyacencia,[diccionario_cabeceras_matriz_adyacencia,len(lista_nombres+lista_nombres_apellidos),len(variables_matriz_adyacencia)]]


#Diccionario que permite asociar los 1's de la matriz de asociada a las correspondientes posiciones en la matriz de adyacencia
def generar_diccionario_relacion_madyacencia_masociada(matriz_asociada):
    diccionario_matriz_asociada = {}
    for fila in range(len(matriz_asociada)):
        for columna in range(len(matriz_asociada[fila])):
            elemento = matriz_asociada[fila][columna]
            if(elemento != 0):
                    diccionario_matriz_asociada[elemento] = [fila,columna]
    return diccionario_matriz_asociada

#Funcion que permite generar una copia de la matriz original de adyacencia/asociada
def copiar_matriz_por_valor(matriz_original):
    copia = []
    for fila in matriz_original:
        copia.append(list(fila))
    return copia

#Funcion que permite obtener la matriz en la que cada fila es una matriz de pesos para cada instancia [[w1][w2]...[wn]] dond [wn] = [[nombre][nombre_apelllido]...[apellidos]]
def generar_matriz_pesos(dataframe_fichero,variables_elim,dic_var_indices_csv,mat_adya,dic_var_pos_matriz_ad,separador):
    matriz_pesos = [] #aqui vamos a guardar las listas con los pesos de cada fila
    lector_archivo = dataframe_fichero.as_matrix()
    for linea in lector_archivo:
        indice = 0
        matriz_wn = []
        matriz_wn = copiar_matriz_por_valor(mat_adya) # matriz de pesos de la fila n
        for elemento in linea:
            if(dic_var_indices_csv[indice] not in variables_elim):
                variable = dic_var_indices_csv[indice]
                if variable in dic_var_pos_matriz_ad:
                    posicion = dic_var_pos_matriz_ad[variable] # [fila,,columna]
                    es_numero = check_number(elemento)
                    if(es_numero == True):
                        if(math.isnan(float(elemento))):
                            elemento = "'nan'"
                        else:
                            elemento = float(elemento)
                    else:
                        if isinstance(elemento, unicode):                        
                            elemento_sin_espacios = u' '.join(elemento).encode('utf-8').strip()
                            if(elemento_sin_espacios == '' or elemento_sin_espacios == ""):
                                elemento = "'nan'"               
                    matriz_wn[posicion[0]][posicion[1]] = elemento
            indice+=1
        matriz_pesos.append(matriz_wn)
    return matriz_pesos

#Funcion que comprueba si el elemento leido es un numero o no
def check_number(number):    
    try:
        float(number)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

#Funcion que permite obtener una lista con las variables eliminadas
def obtener_lista_variables_eliminadas_csv_original(ruta_fichero_variables_eliminadas):
    lista_variables_eliminadas=[]
    with open(ruta_fichero_variables_eliminadas, 'r') as archivo_csv:
        lector_archivo = csv.reader(archivo_csv,delimiter="\n")
        for variable in lector_archivo:
            lista_variables_eliminadas.append(variable[0].strip())
    return lista_variables_eliminadas

#funcion que vuelca a un fichero la informacion relativa a las variables redundantes (tipo de redundancia, numero de variables redundantes y dichas variables)
def imprimir_variables_redundantes(informacion_descriptiva,lista_variables_redundantes,fichero_salida):    
    lista_variables_redundantes = sorted(lista_variables_redundantes)
    fichero_volcado_datos = open(fichero_salida,'a')
    informacion = _("||Eliminacion de redundancia de ") + informacion_descriptiva + _(" ||  \n\nSe han eliminado un total de ") + str(len(lista_variables_redundantes)) + _(" variables redundantes de ") + informacion_descriptiva + _(". Son: \n")
    fichero_volcado_datos.write(informacion)
    informacion = "\n".join(lista_variables_redundantes)
    informacion+="\n\n"
    fichero_volcado_datos.write(informacion)
    fichero_volcado_datos.close()

#Funcion que calcula la matriz de adyacencia prima dependiendo de la lista de variables redundantes que se han eliminado
def calcular_matriz_adyacencia_prima(matriz_adyacencia,diccionario_variables_posicion_matriz,variables_redundantes):
    matriz_adyacencia_prima = copiar_matriz_por_valor(matriz_adyacencia)
    for elemento in variables_redundantes:
        posicion_matriz_asociada = diccionario_variables_posicion_matriz[elemento]
        matriz_adyacencia_prima[posicion_matriz_asociada[0]][posicion_matriz_asociada[1]] = 0
    return matriz_adyacencia_prima

#Funcion que calcula el procentaje de redundancia de la matriz de adyacencia original con respecto a la matriz de adyacencia prima
def imprimir_porcentajes_redundancia(matriz_adyacencia,matriz_adyacencia_prima,variables_redundantes,fichero_salida,numero_unos_matriz_A,pasada_actual,modo_operacion):
    if(numero_unos_matriz_A == 0): # modo individual
        A_original = float(np.count_nonzero(matriz_adyacencia))
        A_entrada = A_original
    else:
        A_original = numero_unos_matriz_A
        A_entrada = float(np.count_nonzero(matriz_adyacencia)) #es modo acumulativo, la original es la matriz input actual
        
    A_prima = float(np.count_nonzero(matriz_adyacencia_prima))
    
    porcentaje_redundancia_variables_tipo_actual = len(variables_redundantes) / float(A_original)
    fichero_volcado_datos = open(fichero_salida,'a')
    informacion = _("||Porcentajes de redundancia ||\n")
    informacion+= _(" % de redundancia de este tipo sobre el total de variables: ") + str(porcentaje_redundancia_variables_tipo_actual)+ "\n"
    if(modo_operacion == _('acumulativo')): # si es moodo acumulativo        
        porcentaje_redundancia_parcial = len(variables_redundantes) / float(A_entrada)
        nomenclatura_matriz_entrada = generar_nomeclatura(pasada_actual-1)
        nomenclatura_matriz_salida = generar_nomeclatura(pasada_actual)
        informacion+= _("\n % de redundancia parcial -de la matriz ") + nomenclatura_matriz_entrada + _(" a la matriz ") + nomenclatura_matriz_salida + "-: " + str(porcentaje_redundancia_parcial)     
        porcentaje_redundancia_acumulativo = (A_original - A_prima) / A_original
        informacion+= _("\n\n % de redundancia acumulativa -de la matriz A a la matriz ") + nomenclatura_matriz_salida + "-: " + str(porcentaje_redundancia_acumulativo)
    informacion+="\n\n"
    informacion+="--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
    informacion+="\n\n"
    fichero_volcado_datos.write(informacion)
    fichero_volcado_datos.close()
    
def imprimir_porcentaje_resumen(A_original,A_prima,fichero_salida):
    porcentaje_redundancia = (A_original - A_prima) / A_original
    fichero_volcado_datos = open(fichero_salida,'a')
    informacion = _("||Porcentaje de redundancia total ") + _("||\nSe ha pasado de ") + str(float(A_original)) + _(" variables a una cantidad final de ") + str(A_prima) + " variables "+ "\n"
    informacion+= _("% de redundancia total: ") + str(porcentaje_redundancia)+ "\n"
    informacion+="\n\n"
    informacion+="--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
    informacion+="\n\n"
    fichero_volcado_datos.write(informacion)
    fichero_volcado_datos.close()
    
#Funcion que genera un grafo no dirigido donde se distinguen por colores los nombres de los apellidos
def generar_grafo_no_dirigido(adjacency_matrix,mylabels,indice_max_nombres,indice_max_apellidos,ruta_guardado,posicion_grafo):
    color_nombres = 'green'
    color_apellidos = 'yellow'
     #Grafo de colores
    etiquetas = {}
    for elemento in  mylabels:
        etiquetas[elemento] = mylabels[elemento]
    gr = nx.Graph()
    gr.clear()
    gr = nx.Graph()
    
    #flechas
    rows, cols = np.where(adjacency_matrix == 1)
    edges = zip(rows.tolist(), cols.tolist())      
    gr.add_edges_from(edges)
      
    # nodos y colores
    nodos_nombres = []
    nodos_apellidos = []
    for indice in range(0,indice_max_nombres):
        nodos_nombres.append(indice)
    
    for indice in range(indice_max_nombres,indice_max_apellidos):
        nodos_apellidos.append(indice)
    
    gr.add_nodes_from(nodos_nombres)
    gr.add_nodes_from(nodos_apellidos) 
    
    color_map = []
    for node in gr:
        if node in range(0,indice_max_nombres):
            color_map.append(color_nombres)
        else:
            color_map.append(color_apellidos)
            
    #generacion del grafo
    if (posicion_grafo == "undefined"):
        position=nx.spring_layout(gr)
    else:        
        position=posicion_grafo
        
    f = plt.figure(figsize=(25,25))
    for indice in nx.isolates(gr):
        etiquetas.pop(indice)
        color_map[indice] = 'deleted'
    
    while 'deleted' in color_map: color_map.remove('deleted')
    graph_copy = gr.copy()
    gr.remove_nodes_from(nx.isolates(graph_copy))
    nx.draw(gr,pos=position,labels=etiquetas,node_color=color_map,font_size=6,font_weight='bold',node_size=500,linewidths=0.1)    
    f.savefig(ruta_guardado)
    return position

def generar_nomeclatura(pasada_actual):    
    nomenclatura_matriz_secundaria = "A"
    if(pasada_actual == 0):
        nomenclatura_matriz_secundaria = "A'"
    if(pasada_actual == 1):
        nomenclatura_matriz_secundaria = "A''"
    if(pasada_actual == 2):
        nomenclatura_matriz_secundaria = "A'''"
    return nomenclatura_matriz_secundaria

def colored_print(texto,color):
    if color == 'cyan':
        print (Fore.CYAN + texto + Style.RESET_ALL)
    elif color == 'yellow':
        print (Fore.YELLOW + texto + Style.RESET_ALL)
    elif color == 'green':
        print (Fore.GREEN + texto + Style.RESET_ALL)

def mostrar_aviso_licencia_incial():
    colored_print("RIASC Tool For Removing Redundancies(RTRR) Copyright (C) 2017  Miguel Carriegos Vieira, Noemi de Castro, Angel Muñoz, Mario Fernandez\n\
                  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.This is free software, and you are welcome to redistribute it under certain conditions; type 'show c' for details. If you agree, press enter to continue.",'yellow')    
    
def mostrar_no_garantia():
    colored_print("15. Disclaimer of Warranty\nTHERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY \
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT \
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM \"AS IS\" WITHOUT WARRANTY \
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, \
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR \
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM \
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF \
ALL NECESSARY SERVICING, REPAIR OR CORRECTION\n 16. Limitation of Liability.\n\
IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING \
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS \
THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY \
GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE \
USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF \
DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD \
PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), \
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF \
SUCH DAMAGES.\n\
  17. Interpretation of Sections 15 and 16.\n\
  If the disclaimer of warranty and limitation of liability provided \
above cannot be given local legal effect according to their terms,\
reviewing courts shall apply local law that most closely approximates \
an absolute waiver of all civil liability in connection with the \
Program, unless a warranty or assumption of liability accompanies a \
copy of the Program in return for a fee.\n",'yellow')

def mostrar_condiciones():  
    colored_print("Please, visit https://www.gnu.org/licenses/gpl-3.0.en.html to check the GPLv3 conditions",'yellow')
    
    