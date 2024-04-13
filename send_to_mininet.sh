#!/bin/bash

if [ $# -lt 1 ] ; then
	echo "Script called without arguments"
	return 1
fi

for i; do 
	if ! [ -f $i ] ; then
		echo $i "does not exists"
	else
		echo $i "sent to mininet"
		sshpass -p "mininet" scp -P 2222 $i mininet@127.0.0.1:/home/mininet/LINFO2347/
	fi
done

echo "All files sent to mininet!"
