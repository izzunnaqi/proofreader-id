#!/bin/bash
# for f (pdf/new/*.pdf) {pdf2txt.py -o $f xml/new/$f.xml}

for f in pdf/new2/*.pdf;
do
	b=$(basename $f)
	filename="${b%.*}"
#	echo $filename
	pdf2txt.py -o "xml/new2/$filename.xml" $f
done
