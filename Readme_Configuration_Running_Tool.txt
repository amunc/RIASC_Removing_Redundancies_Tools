###################################################################################################################
####RIASC Tool For Removing Redundancies(RTRR), a tool for erasing redundant variables from vectorial databases####
###################################################################################################################
Copyright (C) 2017  by RIASC Universidad de Leon(Miguel Carriegos Vieira, Noemi De Castro García, Angel Luis Muñoz, Mario Fernandez Rodriguez)


This tool was developed to run in Python 2.7 in a Hadoop ecosystem  using the library 


-------------------------------------------------
-----General Description-------------------------
-------------------------------------------------
The tool removes variables that have a redundancy of different types:
Type 1 - Empty variables
Type 2 - Constant variables
Type 3 - Equivalent variables

It generates cleaned databases
It generates graphs of the original state of the database and of the cleaned databases
It generates reports with the level of redundacy cleaned

-------------------------------------------------
-----Library dependencies------------------------
-------------------------------------------------
The next libraries are necessary for the tool to run:

-numpy
-pandas
-networkx
-matplotlib
-colorama



-------------------------------------------------
-----Directory structure-------------------------
-------------------------------------------------
The required directory structure is the next:

root_directory/
	      |_ input_files/ (it can contain the input samples when working with csv and the auxiliary files)
	      |_ jars (it must containt at least custom.jar, hadoop-streaming-2.7.3 and utilities.zip
	      |_ .py and .sh files
			  
		
---------------------------------------------------
-------------Input---------------------------------
---------------------------------------------------
The input sources that are allowed are:
	csv files
	
Auxiliary files:
	It can be used an auxiliary file for the single variables and another one for the vector variables. Both must be placed inside input_files folder
Auxiliary files must be .txt files, one for isolated names and another one for vector names (without surnames,surnames will be automatically extracted from csv)

**User must provide auxiliary files and let them empty in the case the user wants the program automatically between isolated names and names with columns.



---------------------------------------------------
-------------Ouput---------------------------------
---------------------------------------------------

-Cleaned database.
-Graphs in pdf format of the initial and final database (cleaned database).
-Summary files with the percentage of redundancy cleaned and the variables removed.

---------------------------------------------------
-------------How to run the tool-------------------
---------------------------------------------------

-Inside a folder create the structure described in Directory Structure with all the files included in the repository
-The execution is done in two steps:
	Pashe I - Getting the weighted matrix and the initial graph:
		./script_execution_phase_I.sh path_to_sample field_delimiter delimiter_names_surnames name_of_variable path_to_isolated_names_file path_to_names_columns_file		
		
	Example:
	
		./script_execution_phase_I.sh input_files/sample.csv ^ ' ' variable1 input_files/single.txt input_files/vector.txt
	
	Pashe II - Removing redundancies the outputs:
		./script_execution_phase_II.sh operative_mode field_delimiter name_surname_delimiter
	
		** This phase can be only executed afert computing successfully the phase I
		** the operative_mode parameter can be accumulative or individualize depending on the working mode selected
		** Inside the script_execution_phase_II.sh the default deleting order of redundancies is type 3, type 2, type 1. Modify the order when necessary.
	
	Example:
		If the user want to remove the three redundancies at once in the default order (III,II,I):
		./script_execution_phase_I.sh path_to_sample accumulative ^ ' ' 
	
	




		
