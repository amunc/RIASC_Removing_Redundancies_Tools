workspace_path=hdfs://quickstart.cloudera:8020/user/cloudera/task_removing_redundancies
hadoop_execution_path=/usr/bin/hadoop
output_directory=$1
erased_variables_path_file=$2
ruta_plantilla_grafo=$3

#Subtarea - Obtenemos el grafo (inicial si no hay variables eliminadas, o uno correspondiente a la eliminacion de variables redundante)
hdfs dfs -touchz task_removing_redundancies/input_files/empty_file
hdfs dfs -rm -r task_removing_redundancies/$output_directory
$hadoop_execution_path jar ./jars/hadoop-streaming-2.7.3.jar \
-D mapreduce.job.reduces=0 \
-D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator -D mapreduce.partition.keycomparator.options=-n \
-files mapper_generate_graph.py,./jars/utilities.zip,$workspace_path/auxiliary_files/associated_matrix/part-00000#associated_matrix,$workspace_path/$erased_variables_path_file#erased_sample_variables,$workspace_path/auxiliary_files/adjacency_matrix_single_variables/part-00000#single_variables,$workspace_path/auxiliary_files/adjacency_matrix_vector_names_dictionary/part-00000#vector_variables,$workspace_path/auxiliary_files/adjacency_matrix_surnames/part-00000#surnames_file,$workspace_path/$ruta_plantilla_grafo/part-00000#plantilla_grafo \
-mapper "mapper_generate_graph.py associated_matrix single_variables vector_variables surnames_file erased_sample_variables plantilla_grafo" \
-input task_removing_redundancies/input_files/empty_file \
-output task_removing_redundancies/$output_directory

