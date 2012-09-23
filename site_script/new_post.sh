#!/bin/bash
# Creates a new post in the Jekyll format.

echo -n "Post title? ";
read -e TITLE;
DTITLE=`echo -n $TITLE | sed 's/ /-/g' | sed 's/[^A-Za-z0-9\-]//g' | tr "[:upper:]" "[:lower:]"`;
DATE=`date +%Y-%m-%d`;
TIME=`date +%H:%M:%S`;
FILENAME=_drafts/$DATE-$DTITLE.md

if [ -f $FILENAME ]; then
   echo "Editing \"" $TITLE "\"";
else
#  category="notes project thinking interesting movie_music life exit";
   echo "category?(input number below): ";
   echo "1)notes; 2)project; 3)thinking; 4)interesting; 5)movie_music; 6)life; 7)exit";
   read -e NUM;
   case $NUM in
	1)
		CAT="notes"
	;;
	2)
		CAT="project"
	;;
	3)
		CAT="thinking"
	;;
	4)
		CAT="interesting"
	;;
	5)
		CAT="movie_music"
	;;
	6)
		CAT="life"
	;;
	7 | exit)
		exit;
	;;
   esac
#   echo "category? ";
#   select CAT in $category; do
#      if [ $CAT == 'exit' ]; then
#         exit 0;
#	done

#   read -e CAT;
   echo "---" > $FILENAME
   echo "layout: post" >> $FILENAME
   echo "title:" $TITLE >> $FILENAME
   echo "category:" $CAT >> $FILENAME
   echo "time:" $TIME >> $FILENAME
   echo "---" >> $FILENAME
fi

vim $FILENAME;
