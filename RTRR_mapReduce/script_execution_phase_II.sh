#!/bin/bash

operative_mode=$1 #single|accumulative
field_delimiter=$2 
name_surname_delimiter=$3

./script_erasing_T3_redundancy.sh $operative_mode $field_delimiter $name_surname_delimiter
./script_erasing_T1_redundancy.sh $operative_mode $field_delimiter
./script_erasing_T2_redundancy.sh $operative_mode $field_delimiter



