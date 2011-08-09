#!/usr/bin/env python # -*- coding: utf-8 -*-
import os
from ConfigParser import ConfigParser

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
def isTargetFile(file_name,config_file_set):
	split_List = file_name.split('.')
        file_suffix = split_List[len(split_List) - 1]
        if file_suffix in config_file_set:
        	return True
        return False

#查找给出的配置文件的具体路径
def configFilePath(pathList,config_file_set,file_callback=None, topdown=True):
	num_Index = 0
	configFile_Path_List = []
	for dir in pathList:
		for root, dirs, files in os.walk(dir, topdown):
			for f in files:
				if isTargetFile(f,config_file_set):
					#配置文件名称
					#print f
					#配置文件绝对路径
					#print os.path.join(root,f)
					configFile_Path_List.append(os.path.join(root,f))
					#print configFile_Path_List[num_Index]
					num_Index += 1
				file_path = os.path.join(f)
				if file_callback: file_callback(file_path)
	return configFile_Path_List

def findConfigFile():
	configFile_Path_Dict = {}
	for program in program_List:
		configSet_List = config_Dict[program]
		pathSet_List = path_Dict[program]
		configFile_Path_Dict[program] = configFilePath(pathSet_List,configSet_List)
	return configFile_Path_Dict

if __name__ == '__main__':
	path_Dict  = {}
	config_Dict = {}
	machine_Dict = {}
	program_List = readConfig()	
	print program_List
	print path_Dict
	print config_Dict
	print machine_Dict
	target_file_suffixes = ['conf','ini']
        path = "/home/workspace/"
        configFilePathDict = findConfigFile()
	print configFilePathDict
