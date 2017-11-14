#!/bin/bash

#II - Eliminacion de redundancies
#creamos el directorio para ejecutar la tarea
#-D mapred.reduce.tasks=0 \
eliminar_redundancies=""
workspace_path=hdfs://quickstart.cloudera:8020/user/cloudera/task_removing_redundancies
hadoop_execution_path=/usr/bin/hadoop

operative_mode=$1
field_delimiter=$2

#II - Eliminar redundancia tipo 2
#Subtarea 2.2 Obtención de la instancia resumen 
hdfs dfs -rm -r task_removing_redundancies/redundancies/type_2/instance_overview
$hadoop_execution_path jar ./jars/hadoop-streaming-2.7.3.jar \
-files mapper_calculate_instance_overview.py,reducer_calculate_instance_overview.py,./jars/utilities.zip,$workspace_path/input_files/erased_sample_variables.txt#erased_sample_variables,$workspace_path/auxiliary_files/associated_matrix/part-00000#associated_matrix \
-mapper "mapper_calculate_instance_overview.py t2 $field_delimiter erased_sample_variables associated_matrix" -reducer "reducer_calculate_instance_overview.py t2 $field_delimiter" \
-input task_removing_redundancies/output_files_phase_I/weight_matrix/part-00000 \
-output task_removing_redundancies/redundancies/type_2/instance_overview

#Subtarea 2.2 Obtención del nuevo csv
hdfs dfs -rm -r task_removing_redundancies/redundancies/type_2/rt2_files
$hadoop_execution_path jar ./jars/hadoop-streaming-2.7.3.jar \
-libjars ./jars/custom.jar \
-D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator -D mapreduce.partition.keycomparator.options=-n \
-files mapper_removing_variables_generate_csv.py,reducer_removing_variables_generate_csv.py,./jars/utilities.zip,$workspace_path/auxiliary_files/associated_matrix/part-00000#associated_matrix,$workspace_path/redundancies/type_2/instance_overview/part-00000#instance_overview,$workspace_path/auxiliary_files/csv_variables/part-00000#csv_variables,$workspace_path/input_files/erased_sample_variables.txt#erased_sample_variables \
-mapper "mapper_removing_variables_generate_csv.py t2 $field_delimiter associated_matrix erased_sample_variables instance_overview csv_variables" -reducer "reducer_removing_variables_generate_csv.py t2 $field_delimiter associated_matrix erased_sample_variables instance_overview csv_variables" \
-input task_removing_redundancies/output_files_phase_I/weight_matrix/part-00000 \
-outputformat com.custom.CustomMultiOutputFormat \
-output task_removing_redundancies/redundancies/type_2/rt2_files

if [ "$operative_mode" = "accumulative" ]; then

hdfs dfs -rm -r task_removing_redundancies/input_files/erased_sample_variables.txt 
hdfs dfs -mv task_removing_redundancies/redundancies/type_2/rt2_files/erased_variables/part-00000 task_removing_redundancies/input_files/erased_sample_variables.txt
#./script_generating_graph.sh redundancies/type_2/rt2_files/grafo input_files/erased_sample_variables.txt
./script_generating_graph.sh redundancies/type_2/rt2_files/grafo input_files/erased_sample_variables.txt output_files_phase_I/graph/graph_template

else

./script_generating_graph.sh redundancies/type_2/rt2_files/grafo redundancies/type_2/rt2_files/erased_variables/part-00000 output_files_phase_I/graph/graph_template 

fi
