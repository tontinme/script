#!/bin/bash
USAGE: ./bash_while_loop.sh
COUNT=6
# bash while loop
while [ $COUNT -gt 0 ]; do
	echo Value of count is: $COUNT
	let COUNT=COUNT-1
done 

