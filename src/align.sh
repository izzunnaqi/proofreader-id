#!/bin/bash

declare -A UNIQUENAME

for f in doc/first10/*
do
	b=$(basename $f)
	n="${b%.*}"
	a=${n:0:-1}
	UNIQUENAME[$a]=''
done

for i in ${!UNIQUENAME[@]}
do
	echo "Aligning ${i}a and ${i}b..."
	python alignment.py doc/first10/${i}a.xml doc/first10/${i}b.xml -o pair/first10_30.xml
done



