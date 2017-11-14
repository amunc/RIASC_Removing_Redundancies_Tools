###################################################################################################################
####RIASC Tool For Removing Redundancies(RTRR), a tool for erasing redundant variables from vectorial databases####
###################################################################################################################
Copyright (C) 2017  by RIASC Universidad de Leon(Miguel Carriegos Vieira, Noemi De Castro García, Angel Luis Muñoz, Mario Fernandez Rodriguez)


This tool was developed to run in Python 2.7


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

-gettext
-getpass
-db.py
-mysql.connector.python
-openpyxl
-pydotplus
-xlrd
-xlsxwriter
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
	      |_ input_files/ (it can contain the input samples when working with csv /excel and the auxiliary files)
	      |_ generated_files/ (it will contain the cleaned databases)
	      |_ graphs/ (it will contain the generated graphs)
	      |_ RTRR_scripts/ (it will contain the python scripts of the tool)
			     |_ RTRR.py
			     |_ removing_redundancies_t1_t2_t3.py
			     |_ utilities_phase_I.py
			     |_ utilities_redundancy_t1.py
			     |_ utilities_redundancy_t2.py
			     |_ utilities_redundancy_t3.py
	      |_ Locale/
		       |_ en_US/
		               |_ LC_MESSAGES/
			    	             |_ paquete_idiomas.mo
				             |_ paquete_idiomas.po
		       |_ en_ES/
		               |_ LC_MESSAGES/
			    	             |_ paquete_idiomas.mo
				             |_ paquete_idiomas.po
	      |_ summary_files (it will contain the files with the summaries of the redundancies removed)
			  

The names for the next directories must be exactly this:
		generated_files
		graphs
		Locale (with the internal estructure as defined)
		summary_files
		
		
---------------------------------------------------
-------------Input---------------------------------
---------------------------------------------------
The input sources that are allowed are:
	csv files
	excel files (.xls,.xlsx)
	a table from a database (postgre or MySql)
	
For the excel and csv files are allowed absolute and relative paths.

Auxiliary files:
It can be used an auxiliary file for the single variables and another one for the vector variables.
Auxiliary files must be .txt files, one for isolated names and another one for vector names (without surnames,surnames will be automatically extracted from csv)

If the user doesn't provide auxiliary files, the tool will distinguish between those kind of variables according to the names surnames delimiter.



---------------------------------------------------
-------------Ouput---------------------------------
---------------------------------------------------

-Cleaned database.
-Graphs in png format of the initial and final database (cleaned database).
-Summary files with the percentage of redundancy cleaned and the variables removed.

---------------------------------------------------
-------------How to run the tool-------------------
---------------------------------------------------

-Execute the script RTRR.py in an environment with the required library dependecies installed.
-Then follow the command line instrucions.



		
