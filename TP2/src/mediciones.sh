#!/bin/bash

host_src=$1
mask_src=$2
host_dst=$3
mask_dst=$4
host_final=$5
dump_file=$6

if [ -z "$host_dst" -o -z "$mask_dst" -o -z "$host_src" -o -z "$mask_src" -o -z "$host_final" -o -z "$dump_file" ]
then
	echo "Usar ./mediciones.sh <host_src> <mask_src> <host_dst> <mask_dst> <host_final> <dump_file>"
	exit 0
fi

tr_file=traceroute_dump.txt

traceroute $host_final > $tr_file
hops=$(python rangoDeIPs.py $host_src $mask_src $host_dst $mask_dst)

first=`echo $hops | awk '{print $1}'`
max=`echo $hops | awk '{print $2}'`

touch $dump_file

rtt_sum=0

for i in $(seq 1 100)
do
	echo TR $i Hop inicial: $first  Hop final: $max

	traceroute -f $first -m $max -q 5 $host_final > $tr_file
	hops=$(python rangoDeIPs.py $host_src $mask_src $host_dst $mask_dst $tr_file)
	
	#si el python devuelve un -1, bash lo ve como un 255 (alta saturacion xD)
	if [ $? = 255 ]; then
		echo "Cambio el enlace.. TODO MAL!!! chau.."
		break
	fi

	first=`echo $hops | awk '{print $1}'`
	max=`echo $hops | awk '{print $2}'`
	rtt=`echo $hops | awk '{print $3}' | tee -a $dump_file`

	rtt_sum=`echo "$rtt_sum+$rtt" | bc -l`
	rtt_prom=`echo "$rtt_sum/$i" | bc -l`

	echo "RTT = $rtt, RTT PROMEDIO = $rtt_prom"
done

rm -f $tr_file

exit 0
