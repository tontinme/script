#!/bin/bash
USAGE: ./bash_until_loop.sh
COUNT=0
# bash until loop
until [ $COUNT -gt 5 ]; do
        echo Value of count is: $COUNT
        let COUNT=COUNT+1
done 

Bash until loop
