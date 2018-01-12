#!/bin/bash

cd ../resource/
for f in pdf/new/*.pdf;
do
	b=$(basename $f)
	filename="${b%.*}"
	echo "Extracting $b..."
	pdf2txt.py -o "xml/new/$filename.xml" $f
done
