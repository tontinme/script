#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from ConfigParser import ConfigParser

# 读取配置文件，并存储
def readConfig():
	config = ConfigParser()
	config.read("./check-config.cfg")
	program_List = config.sections()
	#program_Number = len(program_List)
	#print program_Number
	#for program in program_List:
	for program in range(len(program_List)):
		print program_List[program]
		path_attr = config.get(program_List[program], "PATH")
		path_list = path_attr.split(",")
		print path_list
		config_attr = config.get(program_List[program], "CONFIG_TYPE")
		config_list = config_attr.split(",")
		print config_list
		machine_attr = config.get(program_List[program], "MACHINE")
		machine_list = machine_attr.split(",")
		print machine_list

#判断文件是否符否是要求的类型
def isTargetFile(file_name):
	split_list = file_name.split('.')
        file_suffix = split_list[len(split_list) - 1]
        if file_suffix in target_file_suffixes:
        	return True
        return False

#查找给出的配置文件的具体路径
def findConfigFile(dir,file_callback=None, topdown=True):
	num_Index = 0
	configFile_Path_List = []
	for root, dirs, files in os.walk(dir, topdown):
		for f in files:
			if isTargetFile(f):
				#配置文件名称
				print f
				#配置文件绝对路径
				#print os.path.join(root,f)
				configFile_Path_List.append(os.path.join(root,f))
				#print configFile_Path_List[num_Index]
				num_Index += 1
			file_path = os.path.join(f)
			if file_callback: file_callback(file_path)
	return configFile_Path_List

if __name__ == '__main__':
	readConfig()	
	target_file_suffixes = ['conf','ini']
        path = "/home/workspace/"
        #findConfigFile(path)
        configFilePathList = findConfigFile(path)
	print configFilePathList
