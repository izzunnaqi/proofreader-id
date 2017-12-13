#!/bin/bash

declare -A UNIQUENAME

for f in doc/new2/*
do
	b=$(basename $f)
	n="${b%.*}"
	a=${n:0:-1}
	UNIQUENAME[$a]=''
done

for i in ${!UNIQUENAME[@]}
do
	echo "Aligning ${i}1 and ${i}2..."
	python alignment.py doc/new2/${i}1.xml doc/new2/${i}2.xml -o pair/unannotated_3.xml
done



