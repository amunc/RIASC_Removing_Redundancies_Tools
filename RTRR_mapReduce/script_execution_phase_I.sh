#!/bin/bash

#uso ./script_realizacion_fase_I p1:fichero_muestra p2:field_delimiter p3:separador_nombres_apellidos p4:variable_existente p5:ruta_fichero_individuales p6:ruta_fichero_vectoriales
#I - Obtencion de la matriz de pesos
#creamos el directorio para ejecutar la tarea
#-D mapred.reduce.tasks=0 \
workspace_path=hdfs://quickstart.cloudera:8020/user/cloudera/task_removing_redundancies
hadoop_execution_path=/usr/bin/hadoop
sample_path=$1
field_delimiter=$2
name_surname_delimiter=$3
existent_variable=$4
single_variables_file_path=$5
vector_variables_file_path=$6
hdfs dfs -rm -r task_removing_redundancies
hdfs dfs -mkdir task_removing_redundancies
hdfs dfs -mkdir task_removing_redundancies/input_files
hdfs dfs -put $sample_path task_removing_redundancies/input_files/sample.csv
hdfs dfs -touchz task_removing_redundancies/input_files/erased_sample_variables.txt
hdfs dfs -put $single_variables_file_path task_removing_redundancies/input_files/single_variables.txt
hdfs dfs -put $vector_variables_file_path task_removing_redundancies/input_files/vector_variables.txt


#Subtask 1.1 - Generarion of the base files
hdfs dfs -rm -r task_removing_redundancies/auxiliary_files
$hadoop_execution_path jar ./jars/hadoop-streaming-2.7.3.jar \
-libjars ./jars/custom.jar \
-files mapper_generate_initial_variable_lists.py,reducer_generate_initial_variable_lists.py,./jars/utilities.zip,$workspace_path/input_files/erased_sample_variables.txt#erased_sample_variables,$workspace_path/input_files/single_variables.txt#single_variables,$workspace_path/input_files/vector_variables.txt#vector_variables \
-mapper "mapper_generate_initial_variable_lists.py $existent_variable  $field_delimiter" -reducer "reducer_generate_initial_variable_lists.py '$name_surname_delimiter' csv_variables adjacency_matrix_single_variables adjacency_matrix_vector_names_dictionary adjacency_matrix_surnames adjacency_matrix_full_list erased_sample_variables single_variables vector_variables" \
-input task_removing_redundancies/input_files/sample.csv \
-outputformat com.custom.CustomMultiOutputFormat \
-output task_removing_redundancies/auxiliary_files

#Subtarea 1.2 - Generation of the names_surnames matriz asociated to the adjacency matrix
hdfs dfs -rm -r task_removing_redundancies/auxiliary_files/associated_matrix
$hadoop_execution_path jar ./jars/hadoop-streaming-2.7.3.jar \
-D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator -D mapreduce.partition.keycomparator.options=-n \
-files mapper_generate_associated_matrix.py,reducer_generate_associated_matrix.py,./jars/utilities.zip,$workspace_path/auxiliary_files/adjacency_matrix_single_variables/part-00000#single_variables,$workspace_path/auxiliary_files/adjacency_matrix_vector_names_dictionary/part-00000#vector_variables,$workspace_path/auxiliary_files/adjacency_matrix_surnames/part-00000#surnames_file \
-mapper "mapper_generate_associated_matrix.py single_variables vector_variables surnames_file '$name_surname_delimiter'" -reducer "reducer_generate_associated_matrix.py" \
-input task_removing_redundancies/auxiliary_files/adjacency_matrix_full_list/part-00000 \
-output task_removing_redundancies/auxiliary_files/associated_matrix

#Subtarea 1.3 - Generation of the weight matrix
hdfs dfs -rm -r task_removing_redundancies/output_files_phase_I/weight_matrix
$hadoop_execution_path jar ./jars/hadoop-streaming-2.7.3.jar \
-D mapreduce.job.reduces=1 \
-D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator -D mapreduce.partition.keycomparator.options=-n \
-files mapper_generate_weight_matrix.py,reducer_generate_weight_matrix.py,./jars/utilities.zip,$workspace_path/auxiliary_files/csv_variables/part-00000#csv_variables,$workspace_path/input_files/erased_sample_variables.txt#erased_sample_variables,$workspace_path/auxiliary_files/associated_matrix/part-00000#associated_matrix \
-mapper "mapper_generate_weight_matrix.py $existent_variable $field_delimiter csv_variables erased_sample_variables associated_matrix" -reducer reducer_generate_weight_matrix.py \
-input task_removing_redundancies/input_files/sample.csv \
-output task_removing_redundancies/output_files_phase_I/weight_matrix

#Subtarea 1.4- Obtenemos la plantilla del grafo para que se puedan comparar los otros obtenidos
hdfs dfs -touchz task_removing_redundancies/input_files/empty_file
hdfs dfs -rm -r task_removing_redundancies/output_files_phase_I/graph/graph_template
$hadoop_execution_path jar ./jars/hadoop-streaming-2.7.3.jar \
-D mapreduce.job.reduces=0 \
-D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator -D mapreduce.partition.keycomparator.options=-n \
-files mapper_generate_graph_template.py,./jars/utilities.zip,$workspace_path/auxiliary_files/associated_matrix/part-00000#associated_matrix,$workspace_path/auxiliary_files/adjacency_matrix_single_variables/part-00000#single_variables,$workspace_path/auxiliary_files/adjacency_matrix_vector_names_dictionary/part-00000#vector_variables,$workspace_path/auxiliary_files/adjacency_matrix_surnames/part-00000#surnames_file \
-mapper "mapper_generate_graph_template.py associated_matrix single_variables vector_variables surnames_file" \
-input task_removing_redundancies/input_files/empty_file \
-output task_removing_redundancies/output_files_phase_I/graph/graph_template

./script_generating_graph.sh output_files_phase_I/graph/original_graph input_files/erased_sample_variables.txt output_files_phase_I/graph/graph_template



