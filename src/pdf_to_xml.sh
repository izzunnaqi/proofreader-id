#!/bin/bash

cd ../resource/
for f in pdf/firs10/*.pdf;
do
	b=$(basename $f)
	filename="${b%.*}"
	echo "Extracting $b..."
	pdf2txt.py -o "xml/first10/$filename.xml" $f
done
