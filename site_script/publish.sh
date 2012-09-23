#!/bin/bash
# Lists the posts to publish, then updates them and sends them live
# by Nat Welch 2010

# TODO: Write a regex to pull the name out of the file and update the published
# post's name and date.

POSTS=`ls _drafts/ | grep '-' && echo 'exit'`;

select opt in $POSTS; do
   if [ $opt == 'exit' ]; then 
      exit 0; 
   fi;

   NEWT=`grep -P '^title: ([\w ]+)$' _drafts/$opt`
   NEWT=`echo $NEWT | sed 's/^title: //'  | sed 's/ /-/g' | sed 's/[^A-Za-z0-9\-]//g' | tr "[:upper:]" "[:lower:]"`
   NEWT=`date +%Y-%m-%d`-$NEWT.textile;

   echo "Enter the Chinese title of your article:";
   read title;

   echo "Publishing: $opt.";
   #echo "git mv _drafts/$opt _posts/$NEWT"
   #git mv _drafts/$opt _posts/$NEWT
   echo "cp _drafts/$opt _posts/$NEWT";
   cp _drafts/$opt _posts/$NEWT;

   sed -i "/title/c\\title: $title" _posts/$NEWT;
   #echo "rm _drafts/$opt _posts/$NEWT";
   #rm _drafts/$opt _posts/$NEWT;

   #echo "git commit _drafts/$opt _posts/$NEWT -m \"Publishing $NEWT\"";
   echo "git commit _posts/$NEWT -m \"Publishing $NEWT\"";
   #git commit -a _drafts/$opt _posts/$NEWT -m "Publishing $NEWT."
   git add _posts/$NEWT
   git commit _posts/$NEWT -m "Publishing $NEWT."
   echo "git push origin master."
   git push origin master
   exit 0;
done;
