#!/bin/bash
USAGE: ./bash_for_loop.sh
#bash for loop
for f in $( ls /var/ ); do
	echo $f
done 
