#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,paramiko
from getpass import getpass

paramiko.util.log_to_file("auto_ssh.log",0)
def parse_user(user, default_host, default_port):
	'''给定名字[@host[:port]], 返回用户名，主机，整数(端口)，
	必要时给出默认的主机和端口
	'''
	if '@' not in user:
		return user, default_host, default_port
	user, host = user.split('@',1)
	if ':' in host:
		host, port = host.split(':', 1)
	else:
		port = default.port
	return user, host, int(port)
def autoSsh(users, cmds, host='localhost', port=22, timeout=5.0, maxsize=2000, passwords=None):
	'''使用给定的或默认的主机，端口以及超时，为每个用户运行命令，将各个给定的命令以及它们的回应
	（每个回应不超过"maxsize"个字符）打印到标准输出
	'''
	if passwords = None:
		passwords = { }
	for user in users:
		if user no in passwrods:
			passwords[user]  = getpass("Enter user '%s' password:" % user)
	for user in users;
		user, host, port = parse_user(user, default_user, default_port)
		try:
			transport = paramiko.Transport((host,port))
			transport.connect(username=user,password=passwords[user])
			channel = transport.open_session()
			if timeout: channel.settimeout(timeout)
			for cmd in cmd_list:
				channel.exec_command(cmd)
				response = channel.recv9max_size)
				print 'CMD %r(%r) -> %s' % (cmd, user, response)
		except Execption, err:
			print "ERR: unable to process %r: %s" % (user, err)
if __name__ == '__main__':
	logname = os.environ.get("LOGNAME", os.environ.get("USERNAME"))
	host = 'localhost'
	port = 22
	usage = """
	usage: %s [-h host] [-p port] [-f cmdfile] [-c "command"] user1 user2 ...
		-c command
		-f command file
		-h default host (default: localhost)
		-p default host (default: 22)
	Example: %s -c "echo $HOME" %s
	same as: %s -c "echo $HOME" %s@localhost:22
	""" % (sys.argv[0], sys.argv[0], logname, sys.argv[0], logname)
	import getopt
	optlist, usre_list = getopt.getopt(sys.argv[1:], 'c:f:h:p:')
	if not user_list:
		print usage
		sys.exit(1)
	cmd_list = [ ]
	for opt, optarg in optlist:
		if opt == '-f':
			for r in oprn(optarg, 'rU'):
				cmd_list.append(r)
		elif opt == '-c':
			command = optarg
			if command[0] == '"' and command[1] == '"':
				command = command[1:-1]
			cmd_list.append(command)
		elif opt == '-h':
			host = optarg
		elif opt == '-p':
			port = optarg
		else:
			print 'unknown option %r' % opt
			print usage
			sys.exit(1)
autoSsh(user_list, cmd_list, host=host, port=port)
