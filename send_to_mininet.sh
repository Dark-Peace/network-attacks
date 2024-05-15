#!/bin/bash

readdir() 
{
	echo "reading the directory" $i
	for i in $1*; do
		if [ -d $i ]; then
			readdir $i
		else
			echo $i "sent to mininet"
			sshpass -p "mininet" scp -P 2222 $i mininet@127.0.0.1:/home/mininet/LINFO2347/
		fi
	done
}

if [ $# -lt 1 ] ; then
	echo "Script called without arguments"
	return 1
fi
for i; do 
	if [ -d $i ]; then
		readdir $i
	elif ! [ -f $i ] ; then
		echo $i "does not exists"
	else
		echo $i "sent to mininet"
		sshpass -p "mininet" scp -P 2222 $i mininet@127.0.0.1:/home/mininet/LINFO2347/
	fi
done

echo "All files sent to mininet!"
