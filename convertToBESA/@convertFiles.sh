#!/bin/bash

current=`pwd`

cd text
for aS in *.txt
do
	python ${current}/convertToBESA.py \
	--input ${aS} \
	--output ${aS%.txt}.avr \
	--baseline 2000.00 \
	--srate 1000
done

