#!/bin/bash

for f in ../resource/xml/first10/*.xml;
do
	b=$(basename $f)
	echo "Parsing $b..."
	python parser.py $f -o 'doc/first10/'${b}
done
