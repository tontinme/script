#! /usr/bin/env ruby
#

#EXAMPLE 1
puts "EXAMPLE 1"
def call_back
  puts "test line 1"
  yield
  yield("hello", "tian")
  puts "test line 2"
end
call_back { puts "In the block" }
call_back { |str1, str2| puts "#{str1}: #{str2}" }
puts ""

#EXAMPLE 2
puts "EXAMPLE 2"
def call_back
  animals = %w( ant bee cat dog el )
  animals.each { |animal| puts animal }
end
call_back { |animal| print "#{animal}" }
puts ""

#EXMAPLE 3
puts "EXAMPLE 3"
[ 'cat', 'dog', 'horse' ].each { |name| print name, " " }
5.times { print "*" }
3.upto(6) { |i| print i }
('a'...'e').each {|char| print char}
printf("\n\n")

#EXAMPLE 4
printf("Number: %5.2f,\nString: %s\n\n",1.23, "Hello" )

#EXAMPLE 5
line = gets
puts line
print
