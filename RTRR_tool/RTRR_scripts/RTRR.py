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

import utilities_phase_I as uf1
import removing_redundancies_t1_t2_t3 as remred
import time
import warnings
warnings.filterwarnings("ignore")

separador_ficheros_variables = "\n"
ruta_fichero_volcado_datos_test = ''
ruta_fichero_variables_eliminadas = '../generated_files/variables_muestra_eliminadas.txt'
ruta_directorio_ficheros_entrada = '../input_files/'
uf1.mostrar_aviso_licencia_incial()
accion=raw_input()
if(accion == "show w"):
    uf1.mostrar_no_garantia()
elif(accion == "show c"):
    uf1.mostrar_condiciones()

parametros = uf1.definir_parametros_iniciales(ruta_fichero_variables_eliminadas,ruta_directorio_ficheros_entrada)
permutacion_redundancias = parametros[0]
ruta_fichero = parametros[1]
ruta_fichero_var_individuales = parametros[2]
ruta_fichero_var_vectoriales = parametros[3]
ruta_fichero_variables_eliminadas = parametros[4]
ruta_fichero_variables_modificadas= parametros[5]
separador_original = parametros[6]
extension_fichero = parametros[7]
modo_operacion = parametros[8]
separador_apellidos = parametros[9]
idioma = parametros[10]
pasada_actual = 0


start_time = time.time()
remred.eliminar_redundancias_segun_secuencia(permutacion_redundancias,ruta_fichero,ruta_fichero_var_individuales,ruta_fichero_var_vectoriales,ruta_fichero_variables_eliminadas,ruta_fichero_variables_modificadas,ruta_fichero_volcado_datos_test,separador_original,separador_ficheros_variables,separador_apellidos,extension_fichero,modo_operacion,pasada_actual,idioma)
var_eliminadas = uf1.leer_variables_fichero(ruta_fichero_variables_eliminadas,"\n")
uf1.eliminar_contenido_fichero(ruta_fichero_variables_eliminadas)
uf1.actualizar_fichero_variables(ruta_fichero_variables_eliminadas,var_eliminadas,separador_ficheros_variables)
print (time.time() - start_time)