#!/bin/bash

declare -A UNIQUENAME
cd ../resource/pdf

for f in new/*.pdf
do
	b=$(basename $f)
	n="${b%.*}"
	a=${n:0:-1}
	UNIQUENAME[$a]=''
done
for i in ${!UNIQUENAME[@]}
do
	echo $i
done
echo 'Num of doc: ' ${#UNIQUENAME[@]}



