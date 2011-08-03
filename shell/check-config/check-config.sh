#!/bin/bash
#Need check-config.cfg
#Usage:./check-config.sh display|diff|modify

. ./check-config.cfg

#echo $CHECK_PATH
#echo $CONF_NAME

case "$1" in
display)
	for key_name in $KEY_NAME; do
		echo "===================================="
		echo "you specify the keyword: $key_name"
		echo "------------------------------------"
		for conf_name in $CONF_NAME; do
			for check_path in $CHECK_PATH; do
				grep $key_name $check_path/$conf_name || echo "no $key_name found in $check_path/$conf_name"
			done
		done
		echo "===================================="
		echo ""
		echo ""
	done
	;;
diff)
	echo "diff option coming soon!"
	;;
modify)
	echo "modify option coming soon!"
	;;
*)
	echo "Usage:./check-config.sh display|diff|modify"
	exit 1
	;;
esac

exit 0
