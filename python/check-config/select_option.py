#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv 
#from fabric.api import env,run
from os import path

USER = 'supertool'
PORT = 22
CONFIGURE_FILE,PRI_KEY,PASSWORD,CMD,SPECIFYKEYWORD = '','','','',''

for i in range(1,len(argv)+1):
	if argv[i-1] == '-h' or len(argv) == 1:
		print """
		USAGE:
			-u [user]	use this argument to specify the user, default is 'supertool'
			-f [file]	The config file path
			-p [port]	The ssh port, default is 22
			-i [pwd|file]	You can specify password or a private key file to connect the host
			-c [command]	The command you want to run
					Command List:
					CF|catConfigFile
					SK|specifyKeyword
			-k [keyword]	The keyword you want to displayKeyword
					If you specify '-k', you must specify '-c displayKeyword'
			-h		Print this help screen
		"""
		exit(1)
	if argv[i-1] == '-u':
		USER = argv[i]
	if argv[i-1] == '-f':
		if path.isfile('%s' % (argv[i])) == True:
			CONFIGURE_FILE = argv[i]
	if argv[i-1] == '-p':
		try:
			PORT = int(argv[i])
		except ValueError:
			exit ("port value must be int!")
	if argv[i-1] == '-i':
		if path.isfile(argv[i]) == True:
			PRI_KEY = argv[i]
		else:
			PASSWORD = argv[i]
	if argv[i-1] == '-c':
		CMD = argv[i]
	if argv[i-1] == '-k':
		SPECIFYKEYWORD = argv[i]
if SPECIFYKEYWORD != '' and CMD != 'SK' and CMD != 'specifyKeyword':
	exit("If you specify '-k', you must specify '-c SK|specifyKeyword' as same!")
if CONFIGURE_FILE == '':
	exit("You must specify a configure file!")
if PRI_KEY == '' and PASSWORD == '':
	exit("You must specify a authorized method!")
elif PRI_KEY != '' and PASSWORD != '':
	exit("You should only specify one authorized method!")
if CMD == '':
	exit("You must run a command!")
if CMD == 'SK' or CMD == 'SPECIFYKEYWORD':
	if SPECIFYKEYWORD == '':
		exit("You must specify '-k keyword' when you want to run '-c SK|SPECIFYKEYWORD'")

print "-u|user:%s, -p|port:%d, -f|config_File:%s, -i|private_Key:%s, -i|password:%s, -c|comand:%s, -k|keyword:%s" % (USER,PORT,CONFIGURE_FILE,PRI_KEY,PASSWORD,CMD,SPECIFYKEYWORD)
