!/usr/bin/perl
#######################################################
#author:luoxuan
#date:20110719
#purpose:check master and slave variables is consisit?
#version:0.1
#######################################################
use warnings;
use strict;
 
my $mysql="/usr/local/mysql/bin/mysql";
my $socket="/tmp/mysql.sock";
#my $master_ip=readpipe("hostname -i");
#get slave ips
my $get_sips="$mysql -uroot -S$socket -e \"show processlist\"|grep \"Binlog Dump\"|awk '{print \$3}'|awk -F \":\" '{print \$1}'";
my $slave_ips=readpipe($get_sips);
my @slave_ip=split(/\s+/,$slave_ips);
#get master variables
my $get_master_var="$mysql -uroot -S$socket -e \"show variables\"|awk -F \"|\" '{print \$1 \$2}'";
my $master_var=readpipe($get_master_var);
my %master_vars;
my %slave_var;
my %slave_ref;
my $key1;
my $value1;
my $kv;
 
#master variables init
sub master_init{
        print "now initialize the master\n";
        open(OUTFILE,">/tmp/master");
        print OUTFILE "$master_var";
        close(OUTFILE);
        open(INFILE,"</tmp/master");
        while(<INFILE>){
                chomp($_);
                my ($key,$value)=split(/\s+/,$_,2);
                $master_vars{$key}=$value;
        }
        close(INFILE);
        print "now initialize the master finished\n";
}
 
#all slave variables init
sub slave_init{
        print "now initialize the all slave\n";
        my @slaveip_var;
        my @slaveconn_var;
        my @slave_result;
        my $file;
        my $slave_ipnum=scalar @_;
        my $lkv;
        my $rkv;
        for(my $i=0;$i<$slave_ipnum;$i++){
                $file="/tmp/"."slave"."$i";
                $slave_var{$i}={};
                $slaveip_var[$i]=[];
                $slaveconn_var[$i]=[];
                $slave_result[$i]=[];
 
                $slaveip_var[$i]=shift @_;
                $slaveconn_var[$i]="$mysql -uluoxuan -pluoxuan -h$slaveip_var[$i] -e \"show variables\"|awk -F \"|\" '{print \$1 \$2}'";
                $slave_result[$i]=readpipe($slaveconn_var[$i]);
 
                open(SOUTFILE,">$file");
                print SOUTFILE "$slave_result[$i]";
                close(SOUTFILE);
                open(SINFILE,"$file");
                <SINFILE>;
                while(<SINFILE>){
                        chomp($_);
                        my ($key,$value)=split(/\s+/,$_,2);
                        $slave_var{$i}{$key}=$value; 
                }
                close(SINFILE);
                $slave_ref{$slaveip_var[$i]}=\%{$slave_var{$i}};
        }
        return \%slave_ref;
        print "now initialize the all slave finished\n\n";
}
 
sub ms_diff{
        my $slave_add=shift @_;
        while(my ($key,$value)=each %$slave_add){
                print "master and slave($key) variables different(just on side):\n";
                print "**************************************************************\n";
                while(($key1,$value1)=each %$value){
                        if(exists $master_vars{$key1}){
                                if($master_vars{$key1} ne $value1){
                                        print "$key1\'s value is different from master,please check!\n";
                                }
                        }
                }
                print "***************************************************************\n";
        }
}
 
sub main{
        &master_init;
        my $slaveinfo=&slave_init(@slave_ip);
        &ms_diff($slaveinfo);
}
eval{&main
};
