#!/bin/bash
#Usage: ./display_execute_file.sh
directories=`echo $PATH | column -s ':' -t`

function display_execute_file {
	for directory in $directories
	do
		[[ -d $directory ]] || continue
		cd $directory
		for file in *
		do 
			[[ -x $file && ! -d $file ]] || continue
			echo $file
		done
		cd -
	done | sort | uniq
}

display_execute_file
