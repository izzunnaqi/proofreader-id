#!/bin/bash

for f in ../resource/xml/new2/*.xml;
do
	b=$(basename $f)
	python parser.py $f -o 'doc/new2/'${b}
done
