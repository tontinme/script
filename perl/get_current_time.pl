#!/usr/bin/perl
use warnings;
use strict;
sub getTime
{
        my $time = shift || time();
        my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($time);
        $year += 1900;
        $mon ++;
        $min  = '0'.$min  if length($min)  < 2;
        $sec  = '0'.$sec  if length($sec)  < 2;
        $mon  = '0'.$mon  if length($mon)  < 2;
        $mday = '0'.$mday if length($mday) < 2;
        $hour = '0'.$hour if length($hour) < 2;
					   
        my $weekday = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat')[$wday];
							    
        return { 'second' => $sec,
	       'minute' => $min,
               'hour'   => $hour,
               'day'    => $mday,
               'month'  => $mon,
               'year'   => $year,
               'weekNo' => $wday,
               'wday'   => $weekday,
               'yday'   => $yday,
               'date'   => "$year-$mon-$mday",
               'all'    => "$year-$mon-$mday-$hour-$min-$sec"
        };
 }
my $date=&getTime();
print "$date->{all}\n";
print "$!\n";
