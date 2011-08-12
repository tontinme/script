#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paramiko
import sys

def catConfigFile(machine,config,auth_method,auth_fileORpass,port=22,username='supertool'):
        hostname = machine
        com_mand = 'cat %s' % config
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
        #machine_Number = '127.0.0.1'
        #1-rsa key auth, 0-password auth
        authorizedMethod = 1
        #keyORpass = '123456'
        keyORpass = '/home/supertool/tian/id_rsa'
        config_Path = '/home/workspace/monitor47/TA/release-1.0.7/bin/tracker/conf/tracker.conf'
        #config_Path = '/home/workspace/monitor47/TA/release-1.0.7/bin/tracker/conf/tracker.ini'
        config_Content = catConfigFile(machine_Number,config_Path,authorizedMethod,keyORpass)
        print config_Content


'''
为了避免如下错误，请务必保证执行该程序的机器的~/.ssh/known_hosts内含有要连接的机器信息
    raise SSHException('Unknown server %s' % hostname)

'''
