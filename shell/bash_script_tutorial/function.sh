#!/bin/bash
#USAGE: ./function.sh
# BASH FUNCTIONS CAN BE DECLARED IN ANY ORDER
myvar="hello"
function function_B {
        echo Function B.
	myvar="function_B"
	echo "$myvar"
}
function function_A {
        echo $1
}
function function_D {
        echo Function D.
}
function function_C {
        echo $1
	myvar="function_C"
	echo "$myvar"
}
#虽然在function_B和function_C中重新定义了myvar变量，但是该定义是对该脚本全局有效的
echo "test $myvar"
# FUNCTION CALLS
# Pass parameter to function A
function_A "Function A."
function_B
echo "test $myvar"
# Pass parameter to function C
function_C "Function C."
function_D 
echo "test $myvar"
