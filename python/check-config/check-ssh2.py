#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paramiko
import sys

def catConfigFile(machine,config_path,config_type,auth_method,auth_fileORpass,port=22,username='supertool'):
        hostname = machine
        #com_mand = 'cat %s' % config
        com_mand = 'find %s -name *.%s' % (config_path,config_type)
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
if __name__ == '__main__':
        machine_Number = '112.mzhen.cn'
        #1-rsa key auth, 0-password auth
        authorizedMethod = 1
        #keyORpass = '123456'
        #keyORpass = '/home/supertool/tian/id_rsa'
        keyORpass = '/home/debug/myproject/python/check-config/id_rsa'
        config_Path = '/home/workspace/monitor47/TA/release-1.0.7/bin/tracker/'
	#config_Type = 'conf,ini'
	config_Type = 'ini'
        #config_Path = '/home/workspace/monitor47/TA/release-1.0.7/bin/tracker/conf/tracker.ini'
        config_Content = catConfigFile(machine_Number,config_Path,config_Type,authorizedMethod,keyORpass)
        #print config_Content
	config_Content_List = config_Content.split('\n')
	print config_Content_List[0:(len(config_Content_List)-1)]
