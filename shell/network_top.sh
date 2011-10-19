#!/bin/bash
#=============================================================================
#     FileName: network_top.sh
#         Desc: monitor the network interface's flow
#	 Usage: sh network_top.sh --network-port=eth0 --interval-time=1 --repeat-total=10
#       Author: mysqlops.com
#     Modifyed: tontinme
#        Email: tontinme@gmail.com
#     HomePage: http://www.tontin.me
#      Version: 1.0
#   LastChange: 2011-10-19 14:26:53
#=============================================================================

Usage()
{
	cat <<EOF
	Usage: $0 [OPTIONS]
		--network-port=ethN	Show which network port, for example --network-port=eth0
		--interval-time=N	Every twice that networked interval time, for example --interval-time=1
		--repeat-total=N	We need to see a continuous flow of card number, for example --repeat-total=10

EOF
exit 1
}

if [ "$#" -ne 3 ]
then
	Usage
fi

for INPUT_DATA in $*
do 
	INPUT_DATA_1=$1
	Val=`echo "$INPUT_DATA_1" | sed -e "s:--[^=]*=::"`

	case "$INPUT_DATA_1" in
		--network-port=*)
			ETH_PORT="$Val"
			;;
		--interval-time=*)
			INTERVAL_TIME="$Val"
			;;
		--repeat-total=*)
			REPEAT_TOTAL="$Val"
			;;
		*)
			echo -e "\n ERROR VARIABLES: $INPUT_DATA_1 \n"
			Usage
			exit 1
			;;
	esac
	shift
done

infirst=$(cat /proc/net/dev | tr ':' ' ' | awk '/'$ETH_PORT'/{print $2}')
outfirst=$(cat /proc/net/dev | tr ':' ' ' | awk '/'$ETH_PORT'/{print $10}')
echo "$ETH_PORT" "in_bytes/sec" "out_bytes/sec" "total_bytes/sec" | awk '{printf("%10s %16s %16s %16s\n",$1,$2,$3,$4)}'
sleep $INTERVAL_TIME"s"

i=0
while [ "$i" -lt "$REPEAT_TOTAL" ]
do
	inend=$(cat /proc/net/dev | tr ':' ' ' | awk '/'$ETH_PORT'/{print $2}')
	outend=$(cat /proc/net/dev | tr ':' ' ' | awk '/'$ETH_PORT'/{print $10}')
	sumin=$((($inend-$infirst)/$INTERVAL_TIME))
	sumout=$((($outend-$outfirst)/$INTERVAL_TIME))
	sum=$(($sumin+$sumout))

	echo "$ETH_PORT" "$sumin" "$sumout" "$sum" | awk '{printf("%10s %16s %16s %16s\n",$1,$2,$3,$4)}'
	infirst=$inend
	outfirst=$outend
	i=$(($i+1))
	sleep $INTERVAL_TIME
done
	sleep $INTERVAL_TIME"s"
