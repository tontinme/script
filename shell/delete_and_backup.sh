#!/bin/bash
Backup_Dir=$HOME/.rm_back
Systemrm=/bin/rm

if [ -z "$1" -o "$1" -eq "--help" ]
then
	exec $Systemrm 
fi

if [ ! -d $Backup_Dir ]
then
	mkdir -m 0700 $Backup_Dir || echo "$0: Cannot create $Backup_Dir"
	exit
fi

args=$( getopt dfrPRivw $* ) || exec $Systemrm

count=0
flags=""
for argument in $args
do
	case $argument in 
		--) break;
			;;
		*) flags="$flags $argument";
			#((count++));
			count=`expr $count + 1`;
			;;
	esac
done
shift $count

for file
do
	[ -e $file ] || continue
	copyfile=$Backup_Dir/$(basename $file).$(date "+%m.%d.%y.%H.%M.%S")
	/bin/cp -R $file $copyfile
done

exec $Systemrm $flags "$@"
