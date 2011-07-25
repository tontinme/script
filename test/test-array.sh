#!/bin/bash
ARRAY=('debian linux' 'redhat linux' 'ubuntu linux')
ELEMENTS=${#ARRAY[@]}
for (( i=0; i < $ELEMENTS; i++ ))
do
	echo ${ARRAY[${i}]}
done 

args=("$@")
len_args=${#args[@]}
len_args_2=$#
echo $len_args
echo $len_args_2
