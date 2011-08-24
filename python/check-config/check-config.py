#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#USAGE EXAMPLE: python check-config.py -f ./check-config.cfg -i ./id_rsa [-o 654321] -c SK -k kfs_host [-u supertool -p 22]

'''
#=============================================================================
#     FileName: check-config.py
#         Desc: check program configure file 
#       Author: tontinme
#        Email: tontinme@gmail.com
#     HomePage: http://www.tontin.me
#      Version: 0.2.0
#   LastChange: 2011-08-25 00:30:04
#      History:
#=============================================================================
'''

from sys import argv
from ConfigParser import ConfigParser
import paramiko
#from fabric.api import env,run
from os import path

def input_argument():
	global USER,PORT,CONFIGURE_FILE,PRI_KEY,PASSOFAUTH,PASSWORD,CMD,SPECIFYKEYWORD
	for i in range(1,len(argv)+1):
	        if argv[i-1] == '-h' or len(argv) == 1:
	                print """
	                USAGE:
	                        -u [user]       	use this argument to specify the user, default is 'supertool'
	                        -f [file]       	The config file path, default is './check-config.cfg'
	                        -p [port]       	The ssh port, default is 22
	                        -i [pwd|file]   	You can specify password or a private key file to connect the host
				-o [pass of id_rsa]	If your private key is encrypted,you should specify this pass, default is 'NULL'
	                        -c [command]    	The command you want to run
	                                        	Command List:
	                                        	CF|catConfigFile
	                                        	SK|specifyKeyword
	                        -k [keyword]    	The keyword you want to displayKeyword
	                                        	If you specify '-k', you must specify '-c displayKeyword'
	                        -h              	Print this help screen

			EXAMPLE:
				python check-config.py  [-f ./check-config.cfg] -i /home/cinder/id_rsa [-o 654321] -c [SK -k kfs_host]|[CF]
							[-u supertool] [-p 22]
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
		if argv[i-1] == '-o':
			PASSOFAUTH = argv[i]
	        if argv[i-1] == '-c':
	                CMD = argv[i]
	        if argv[i-1] == '-k':
	                SPECIFYKEYWORD = argv[i]
	if SPECIFYKEYWORD != '' and CMD != 'SK' and CMD != 'specifyKeyword':
	        exit("If you specify '-k', you must specify '-c SK|specifyKeyword' as same!")
	#if CONFIGURE_FILE == '':
	#        exit("You must specify a configure file!")
	if PRI_KEY == '':
		if PASSWORD == '':
	        	exit("You must specify a authorized method!")
		if PASSOFAUTH != '':
			exit("-o option could be used when you specify the private key authorized")
	elif PRI_KEY != '' and PASSWORD != '':
	        exit("You should only specify one authorized method!")
	if CMD == '':
	        exit("You must run a command!")
	if CMD == 'SK' or CMD == 'SPECIFYKEYWORD':
	        if SPECIFYKEYWORD == '':
	                exit("You must specify '-k keyword' when you want to run '-c SK|SPECIFYKEYWORD'")
	#print "-u|user:%s, -p|port:%d, -f|config_File:%s, -i|private_Key:%s, -i|password:%s, -c|comand:%s, -k|keyword:%s" % (USER,PORT,CONFIGURE_FILE,PRI_KEY,PASSWORD,CMD,SPECIFYKEYWORD)

# 读取配置文件，并存储
def readConfig():
	config = ConfigParser()
	#config.read("./check-config.cfg")
	config.read(CONFIGURE_FILE)
	program_List = config.sections()
	count = 0
	#for program in range(len(program_List)):
	for program in program_List:
		#print program_List
		path_attr = config.get(program_List[count], "PATH")
		path_List = path_attr.split(",")
		programPath_Dict[program] = path_List
		#print path_List
		config_attr = config.get(program_List[count], "CONFIG_TYPE")
		config_List = config_attr.split(",")
		configType_Dict[program] = config_List
		#print config_List
		machine_attr = config.get(program_List[count], "MACHINE")
		machine_List = machine_attr.split(",")
		machine_Dict[program] = machine_List
		#print machine_List
		count += 1
	return program_List

#判断文件是否符否是要求的类型
#def isTargetFile(file_name,config_file_set):
#	split_List = file_name.split('.')
#        file_suffix = split_List[len(split_List) - 1]
#        if file_suffix in config_file_set:
#        	return True
#        return False

#查找给出的配置文件的具体路径
#这里要更改为ssh连接,即从远程机器上判断具体路径
#def configFilePath(pathList,config_file_set,file_callback=None, topdown=True):
#	num_Index = 0
#	configFile_Path_List = []
#	for dir in pathList:
#		for root, dirs, files in os.walk(dir, topdown):
#			for f in files:
#				if isTargetFile(f,config_file_set):
#					#配置文件名称
#					#print f
#					#配置文件绝对路径
#					#print os.path.join(root,f)
#					configFile_Path_List.append(os.path.join(root,f))
#					#print configFile_Path_List[num_Index]
#					num_Index += 1
#				file_path = os.path.join(f)
#				if file_callback: file_callback(file_path)
#	return configFile_Path_List

def getConfigFilePath(machine,program_path,config_type,auth_fileORpass,PASSOFAUTH,PORT,USER):
	hostname = machine
        #com_mand = 'cat %s' % config
        com_mand = 'find %s -name *.%s' % (program_path,config_type)
        paramiko.util.log_to_file('check-ssh.log')
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        if path.isfile(auth_fileORpass) == True:
		try:
                	key = paramiko.RSAKey.from_private_key_file(auth_fileORpass)
		except paramiko.PasswordRequiredException:
			key = paramiko.RSAKey.from_private_key_file(auth_fileORpass, PASSOFAUTH)
                s.connect(hostname,PORT,USER,pkey=key)
        else:
                s.connect(hostname,PORT,USER,auth_fileORpass)
        #else:
        #        print "Wrong authorized method"
        #        sys.exit(1)
        stdin, stdout, stderr = s.exec_command(com_mand)
        fileContent = stdout.read()
        fileError = stderr.read()
        s.close
        if fileError != '':
                return fileError
        else:
                return fileContent

#按程序分类存储各个配置文件的具体路径
def findConfigFile(auth_fileORpass):
	configFile_Path_Dict = {}
	for program in program_List:
		configSet_List = configType_Dict[program]
		pathSet_List = programPath_Dict[program]
		machineSet_List = machine_Dict[program]
		#configFilePath_List = catConfigFile(machineSet)
		#configFile_Path_Dict[program] = configFilePath(pathSet_List,configSet_List)

		machine_Number = machineSet_List[0]
		config_Content_List = []
		for config_Path in pathSet_List:
			for config_Type in configSet_List:
        			config_Content = getConfigFilePath(machine_Number,config_Path,config_Type,auth_fileORpass,PASSOFAUTH,PORT,USER)
        			#print config_Content
        			config_Content_List_Tmp = config_Content.split('\n')
        			config_Content_List.extend(config_Content_List_Tmp[0:(len(config_Content_List_Tmp)-1)])

		configFile_Path_Dict[program] = config_Content_List
	return configFile_Path_Dict

#对给定文件执行grep操作(显示配置文件内容，显示配置文件中的keyword值)
def catConfigFile(machine,configFile_Path,grep_key_word,auth_fileORpass,PASSOFAUTH,PORT,USER):
	hostname = machine
        #com_mand = 'cat %s' % config
	#这里只寻找含有=的行，但是需要注意，有些配置文件不含=，比如abstractor的logserver.conf
        com_mand = 'grep %s %s' % (grep_key_word,configFile_Path)
        paramiko.util.log_to_file('check-ssh.log')
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        if path.isfile(auth_fileORpass) == True:
		try:
			key = paramiko.RSAKey.from_private_key_file(auth_fileORpass)
		except paramiko.PasswordRequiredException:
			key = paramiko.RSAKey.from_private_key_file(auth_fileORpass, PASSOFAUTH)
                s.connect(hostname,PORT,USER,pkey=key)
	else:
		s.connect(hostname,PORT,USER,auth_fileORpass)
        #else:
	#	print "Wrong authorized method"
        #        sys.exit(1)
        stdin, stdout, stderr = s.exec_command(com_mand)
        fileContent = stdout.read()
        fileError = stderr.read()
        s.close
        if fileError != '':
	        return fileError
        else:
                return fileContent

def displayConfigFile(auth_fileORpass):
	#print file_log
	grepKeyword = '='
	f = open("show_ConfigFile_Content_log.txt",'a')
	for program in program_List:
		for configFile in configFilePath_Dict[program]:
			for machine in machine_Dict[program]:
				config_Content = catConfigFile(machine,configFile,grepKeyword,auth_fileORpass,PASSOFAUTH,PORT,USER)
				print "== %s :: %s ==" % (program,machine)
				configFileName = configFile.split('/')[len(configFile.split('/'))-1]
				f.write('\n== %s : %s : %s ==\n' % (program,configFileName,machine))
			        #print config_Content
				f.write(config_Content)
	f.close()
	print "The Content of configFiles have been appended to show_ConfigFile_Content_log.txt"

def getKeywordValue(auth_fileORpass,grepKeyword):
	f = open("show_specify_keyword_log.txt",'a')
	for program in program_List:
		for configFile in configFilePath_Dict[program]:
			for machine in machine_Dict[program]:
				specifyKeyword_Content = catConfigFile(machine,configFile,grepKeyword,auth_fileORpass,PASSOFAUTH,PORT,USER)
				print "== %s :: %s ==" % (program,machine)
				configFileName = configFile.split('/')[len(configFile.split('/'))-1]
				if specifyKeyword_Content != '':
					f.write('\n== %s : %s : %s < %s > ==\n' % (program,machine,configFileName,configFile))
					f.write(specifyKeyword_Content)
	f.close()
	print "The result of %s has been appended to show_specify_keyword_log.txt" % (grepKeyword)

if __name__ == '__main__':
	USER = 'supertool'
	PORT = 22
	CONFIGURE_FILE = './check-config.cfg'
	PRI_KEY,PASSOFAUTH,PASSWORD,CMD,SPECIFYKEYWORD = '','','','',''
	input_argument()
	print "-u|user:%s, -p|port:%d, -f|config_File:%s, -i|private_Key:%s, -o|passofauth:%s, -i|password:%s, -c|comand:%s, -k|keyword:%s" % (USER,PORT,CONFIGURE_FILE,PRI_KEY,PASSOFAUTH,PASSWORD,CMD,SPECIFYKEYWORD)

	programPath_Dict  = {}
	configType_Dict = {}
	machine_Dict = {}
	program_List = readConfig()	
	print program_List
	print programPath_Dict
	print configType_Dict
	print machine_Dict

        #1-rsa key auth, 0-password auth
        #authorizedMethod = 1
	#keyORpass = '123456'
	#keyORpass = '/home/debug/myproject/python/check-config/id_rsa'
	#file_log = 'show_ConfigFile_Content.log'
	if PRI_KEY != '' and PASSWORD == '':
		keyORpass = PRI_KEY
	elif PASSWORD != '' and PRI_KEY == '':
		keyORpass = PASSWORD
	else:
		exit(1)

	#取得所有配置文件的内容
        configFilePath_Dict = findConfigFile(keyORpass)
	print configFilePath_Dict
	if CMD == 'CF' or CMD == 'catConfigFile':
		displayConfigFile(keyORpass)

	#在所有文件中查看某个关键词的所有具体配置
	elif CMD == 'SK' or CMD == 'specifyKeyword':
		specifyKeyword = SPECIFYKEYWORD
		getKeywordValue(keyORpass,specifyKeyword)
	else:
		exit("UNKOWN COMMAND!")
