#! /usr/bin/env ruby
#

file = "dhcp.txt"
file.each {|line| print line if line =~ /pool/ }
printf("Or print like this:\n")
print file.grep(/pool/)
