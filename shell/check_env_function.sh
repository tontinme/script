#!/bin/bash

##check system env
SetString()
{
	PRE_LANG=$(expr substr $LANG 1 9)
	if [ $PRE_LANG = "zh_CN.UTF" ] | [ $PRE_LANG = "zh_CN.utf" ]
	then
		MESSAGE="显示中文消息"
	else
		MESSAGE="display in english"
	fi

	return 0
}

##check OS arch
INSTALL_LOG='./install.log'
CheckOS()
{
	echo $(date) ":" "Begin to CheckOS" >> $INSTALL_LOG
	case `uname -m` in
		i[3456789]86|x86|i86pc)
			sysinfo='x86'
			;;
		x86_64|amd64|AMD64)
			sysinfo='amd64'
			;;
		*)
			sysinfo='error'
			;;
	esac

	if [ "$sysinfo" = "error" ]
	then
		echo $(date) ":" "Not support OS --" $sysinfo >> $INSTALL_LOG
		return STATUS_ERR
	elif [ $sysinfo = 'x86' ]
	then
		pass
	elif [ $sysinfo = 'amd64' ]
	then
		pass
	fi
	echo $(date) ":" "OS--" $sysinfo >> $INSTALL_LOG

	return 0
}

##check user type
checkUsr()
{
	if [ `whoami` = "root" ] | [ `whoami` = "ROOT" ]
	then
		IS_ROOT=$TRUE
	else
		IS_ROOT=$FALSE
	fi

	return 0
}

#将二进制文件/打包文件追加到bash脚本中执行
TMP_DIR="$HOME/tmp_dir"
main()
{
	#提取文件并解压缩到TMP_DIR(这里以压缩包为例)
	ARCHIVE=`awk '/^__ARCHIVE_FOLLOW__/ { print NR+1; exit 0; }' $0`
	tail -n+$ARCHIVE "$0" | tar xzvm -C $TMP_DIR > /dev/null 2>&1 3>&1
	if [ $? -ne 0 ]
	then
		echo "error"
		exit 1
	fi

	cd $TMP_DIR
	#
	#对解压后的文件进行后续操作
	#
}
__ARCHIVE_FOLLOW__
#cat [a.out | xxx.tar.gz ] >> xxxxx.sh
