#!/bin/bash

for f in ../resource/xml/new/*.xml;
do
	b=$(basename $f)
	echo "Parsing $b..."
	python parser.py $f -o 'doc/new/'${b}
done
