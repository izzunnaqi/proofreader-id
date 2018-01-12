# proofreader-id

Proofreader for Indonesian scientific writing.

### How-to-use:

1. Extract PDF to XML 
```
$ bash pdf_to_xml.sh
```

2. Extract new XML format
```
$ bash extract_xml.sh
```

3. Align document
```
$ bash align.sh
```

4. Classify errors
```
$ python classify.py pair/gold_standard.xml
```