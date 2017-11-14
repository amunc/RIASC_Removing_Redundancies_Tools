#!/bin/bash

#II - Eliminacion de redundancies
#creamos el directorio para ejecutar la tarea
#-D mapred.reduce.tasks=0 \
eliminar_redundancies=""
workspace_path=hdfs://quickstart.cloudera:8020/user/cloudera/task_removing_redundancies

operative_mode=$1
field_delimiter=$2
separador_nombre_apellidos=$3

#IV - Eliminar redundancia tipo 3
#Subtarea 4.1 Obtencion del diccionario de apellidos segun nombre
hdfs dfs -rm -r task_removing_redundancies/redundancies/type_3/surnames_names_dictionary
/usr/bin/hadoop jar ./jars/hadoop-streaming-2.7.3.jar \
-files mapper_generate_surnames_names_dictionary.py,reducer_generate_surnames_names_dictionary.py,./jars/utilities.zip,$workspace_path/input_files/erased_sample_variables.txt#erased_sample_variables \
-mapper "mapper_generate_surnames_names_dictionary.py erased_sample_variables '$separador_nombre_apellidos'" -reducer reducer_generate_surnames_names_dictionary.py \
-input task_removing_redundancies/auxiliary_files/adjacency_matrix_vector_names_dictionary/part-00000,task_removing_redundancies/auxiliary_files/adjacency_matrix_single_variables/part-00000 \
-output task_removing_redundancies/redundancies/type_3/surnames_names_dictionary

#Subtarea 4.2 Obtencion del vector de variables redundantes
hdfs dfs -rm -r task_removing_redundancies/redundancies/type_3/redundant_type_3_variables
/usr/bin/hadoop jar ./jars/hadoop-streaming-2.7.3.jar \
-D mapreduce.task.timeout=8000000 \
-files mapper_generate_list_vector_redundant_variables.py,reducer_generate_list_vector_redundant_variables.py,./jars/utilities.zip,$workspace_path/input_files/erased_sample_variables.txt#erased_sample_variables,$workspace_path/auxiliary_files/adjacency_matrix_vector_names_dictionary/part-00000#vector_variables,$workspace_path/auxiliary_files/adjacency_matrix_single_variables/part-00000#single_variables,$workspace_path/auxiliary_files/associated_matrix/part-00000#associated_matrix,$workspace_path/redundancies/type_3/surnames_names_dictionary/part-00000#surnames_names_dictionary \
-mapper "mapper_generate_list_vector_redundant_variables.py $field_delimiter erased_sample_variables vector_variables single_variables associated_matrix surnames_names_dictionary '$separador_nombre_apellidos'" -reducer "reducer_generate_list_vector_redundant_variables.py surnames_names_dictionary '$separador_nombre_apellidos'" \
-input task_removing_redundancies/output_files_phase_I/weight_matrix/part-00000 \
-output task_removing_redundancies/redundancies/type_3/redundant_type_3_variables

#Subtarea 4.3 Obtención del nuevo csv (continuar aqui viernes 20_09_2017)
hdfs dfs -rm -r task_removing_redundancies/redundancies/type_3/rt3_files
/usr/bin/hadoop jar ./jars/hadoop-streaming-2.7.3.jar \
-libjars ./jars/custom.jar \
-D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator -D mapreduce.partition.keycomparator.options=-n \
-files mapper_removing_variables_generate_csv.py,reducer_removing_variables_generate_csv.py,./jars/utilities.zip,$workspace_path/auxiliary_files/associated_matrix/part-00000#associated_matrix,$workspace_path/redundancies/type_3/redundant_type_3_variables/part-00000#redundant_type_3_variables,$workspace_path/auxiliary_files/csv_variables/part-00000#csv_variables,$workspace_path/input_files/erased_sample_variables.txt#erased_sample_variables \
-mapper "mapper_removing_variables_generate_csv.py t3 $field_delimiter associated_matrix erased_sample_variables redundant_type_3_variables csv_variables" -reducer "reducer_removing_variables_generate_csv.py t3 $field_delimiter associated_matrix erased_sample_variables redundant_type_3_variables csv_variables" \
-input task_removing_redundancies/output_files_phase_I/weight_matrix/part-00000 \
-outputformat com.custom.CustomMultiOutputFormat \
-output task_removing_redundancies/redundancies/type_3/rt3_files

if [ "$operative_mode" = "accumulative" ]; then

hdfs dfs -rm -r task_removing_redundancies/input_files/erased_sample_variables.txt 
hdfs dfs -mv task_removing_redundancies/redundancies/type_3/rt3_files/erased_variables/part-00000 task_removing_redundancies/input_files/erased_sample_variables.txt

./script_generating_graph.sh redundancies/type_3/rt3_files/grafo input_files/erased_sample_variables.txt output_files_phase_I/graph/graph_template

else

./script_generating_graph.sh redundancies/type_3/rt3_files/grafo redundancies/type_3/rt3_files/erased_variables/part-00000 output_files_phase_I/graph/graph_template 

fi
