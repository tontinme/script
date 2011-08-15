#!/usr/bin/env python # -*- coding: utf-8 -*-
import sys
from ConfigParser import ConfigParser
import paramiko

# 读取配置文件，并存储
def readConfig():
	config = ConfigParser()
	config.read("./check-config.cfg")
	program_List = config.sections()
	count = 0
	#for program in range(len(program_List)):
	for program in program_List:
		#print program_List
		path_attr = config.get(program_List[count], "PATH")
		path_List = path_attr.split(",")
		path_Dict[program] = path_List
		#print path_List
		config_attr = config.get(program_List[count], "CONFIG_TYPE")
		config_List = config_attr.split(",")
		config_Dict[program] = config_List
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

def getConfigFilePath(machine,program_path,config_type,auth_method,auth_fileORpass,port=22,username='supertool'):
	hostname = machine
        #com_mand = 'cat %s' % config
        com_mand = 'find %s -name *.%s' % (program_path,config_type)
        paramiko.util.log_to_file('check-ssh.log')
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        if auth_method == 1:
                key = paramiko.RSAKey.from_private_key_file(auth_fileORpass)
                s.connect(hostname,port,username,pkey=key)
        elif auth_method == 0:
                s.connect(hostname,port,username,auth_fileORpass)
        else:
                print "Wrong authorized method"
                sys.exit(1)
        stdin, stdout, stderr = s.exec_command(com_mand)
        fileContent = stdout.read()
        fileError = stderr.read()
        s.close
        if fileError != '':
                return fileError
        else:
                return fileContent

#按程序分类存储各个配置文件的具体路径
def findConfigFile(auth_method,auth_fileORpass):
	configFile_Path_Dict = {}
	for program in program_List:
		configSet_List = config_Dict[program]
		pathSet_List = path_Dict[program]
		machineSet_List = machine_Dict[program]
		#configFilePath_List = catConfigFile(machineSet)
		#configFile_Path_Dict[program] = configFilePath(pathSet_List,configSet_List)

		machine_Number = machineSet_List[0]
		config_Content_List = []
		for config_Path in pathSet_List:
			for config_Type in configSet_List:
        			config_Content = getConfigFilePath(machine_Number,config_Path,config_Type,auth_method,auth_fileORpass)
        			#print config_Content
        			config_Content_List_Tmp = config_Content.split('\n')
        			config_Content_List.extend(config_Content_List_Tmp[0:(len(config_Content_List_Tmp)-1)])

		configFile_Path_Dict[program] = config_Content_List
	return configFile_Path_Dict

#显示配置文件内容
def catConfigFile(machine,config,auth_method,auth_fileORpass,port=22,username='supertool'):
	hostname = machine
        #com_mand = 'cat %s' % config
	#这里只寻找含有=的行，但是需要注意，有些配置文件不含=，比如abstractor的logserver.conf
        com_mand = 'grep = %s' % config
        paramiko.util.log_to_file('check-ssh.log')
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        if auth_method == 1:
		key = paramiko.RSAKey.from_private_key_file(auth_fileORpass)
                s.connect(hostname,port,username,pkey=key)
        elif auth_method == 0:
		s.connect(hostname,port,username,auth_fileORpass)
        else:
		print "Wrong authorized method"
                sys.exit(1)
        stdin, stdout, stderr = s.exec_command(com_mand)
        fileContent = stdout.read()
        fileError = stderr.read()
        s.close
        if fileError != '':
	        return fileError
        else:
                return fileContent

def displayConfigFile(auth_method,auth_fileORpass):
	#print file_log
	f = open("show_ConfigFile_Content_log.txt",'a')
	for program in program_List:
		for configFile in configFilePathDict[program]:
			for machine in machine_Dict[program]:
				config_Content = catConfigFile(machine,configFile,auth_method,auth_fileORpass)
				print "== %s :: %s ==" % (program,machine)
				configFileName = configFile.split('/')[len(configFile.split('/'))-1]
				f.write('\n== %s : %s : %s ==\n' % (program,configFileName,machine))
			        #print config_Content
				f.write(config_Content)
	f.close()

if __name__ == '__main__':
	path_Dict  = {}
	config_Dict = {}
	machine_Dict = {}
	program_List = readConfig()	
	print program_List
	print path_Dict
	print config_Dict
	print machine_Dict

        #1-rsa key auth, 0-password auth
        authorizedMethod = 1
	#keyORpass = '123456'
	keyORpass = '/home/debug/myproject/python/check-config/id_rsa'
	#file_log = 'show_ConfigFile_Content.log'

	#取得所有配置文件的内容
        configFilePathDict = findConfigFile(authorizedMethod,keyORpass)
	print configFilePathDict
	displayConfigFile(authorizedMethod,keyORpass)

	#在所有文件中查看某个关键词的所有具体配置
