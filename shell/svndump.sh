#!/bin/bash 
#=============================================================================
#     FileName: svndump.sh
#         Desc: this script is used for svn repository backup
#       Author: tontinme
#        Email: tontinme@gmail.com
#     HomePage: http://www.tontin.me
#      Version: 0.0.1
#   LastChange: 2011-07-28 21:32:15
#      History:
#=============================================================================
MAILADDR=tontinme@gmail.com

#backup directory
BACKUP_DIR=/svnroot/svnback

#svn repository directory
SVN_DIR=/svnroot/repository

#hostname and project list
Project_List=$BACKUP_DIR/projectlist.txt

#svn backup log path and date
LogFile=$BACKUP_DIR/svnback.log
DATE=`date + %Y%m%d-%T`

#svn command path
export PATH=$PATH:/bin:/usr/bin:/usr/local/bin

#our actual rsyncing function
do_accounting() {
	echo " " >> $LogFile
	echo " " >> $LogFile
	echo "#####################" >> $LogFile
	echo "$DATE" >> $LogFile
	echo "#####################" >> $LogFile
	cd $BACKUP_DIR
}

do_svndump() {
	PROJECT_LIST=`cat $Project_List`
	cd $SVN_DIR
	for project in $Project_List
	do
		echo "begin to dump $project databases" >> $LogFile
		if [ ! -f $BACKUP_DIR/$project.dump ]
		then
			YOUNGEST=`svnlook youngest $project`
			svnadmin dump $project > $BACKUP_DIR/$project.dump
			echo "OK, dump file $project successfully!" >> $LogFile
			echo "$YOUNGEST" >> $BACKUP_DIR/$project.dump
		else
			echo "$project.dump existed, will do increatment job" >> $LogFile
			if [ ! -f $BACKUP_DIR/$project.youngest ]
			then
				echo "$project:Error, no youngest check!" >> $LogFile
			else
				PREVYOUNGEST=`cat $BACKUP_DIR/$project.youngest`
				NEWYOUNGEST=`svnlook youngest $project`
				if [ $PREVYOUNGEST -eq $NEWYOUNGEST ]
				then
					echo "$project:no database updated!" >> $LogFile
				else
					LASTYOUNGEST=`expr $PREVYOUNGEST + 1`
					echo "last youngest is $LASTYOUNGEST" >> $LogFile
					svnadmin dump $project --revision $LASTYOUNGEST:$NEWYOUNGEST --increatment > $BACKUP_DIR/$project-$LASTYOUNGEST-$NEWYOUNGEST.$DATE
					echo "$NEWYOUNGEST" > $BACKUP_DIR/$project.youngest
				fi
			fi
		fi
	done
}

#our post rsync accounting function
do_mail() {
	mail $MAILADDR -s svn-back_log < $LogFile
}

#some error handling and/or run our backup and accounting
do_accounting && do_svndump && do_mail
