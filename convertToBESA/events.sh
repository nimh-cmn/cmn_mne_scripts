#!/bin/bash

current=`pwd`

for aS in $@
do
	echo $aS
	cd $aS
	ct=1
	
	for aRun in *.mff
	do
		python ${current}/mffquery.py \
		--filter 'TR' 'OJFix' \
		--repeating Code 1 \
		--unq description \
		--to_csv events_run_${ct}.txt \
		${aRun} \
		Code description_unq description label
		
		let ct=ct+1
	done
	
	for aEvent in events_run_*
	do
		sed -i '' 's/relative_millis/Tms/g' $aEvent
		sed -i '' 's/description_unq/TriNo/g' $aEvent
		sed -i '' 's/label/Comnt/g' $aEvent
		sed -i '' 's/description/Comnt/g' $aEvent
		sed -i '' 's/,240/,2/g' $aEvent #nov
		sed -i '' 's/,241/,3/g' $aEvent #rep
	done
	
	
	cd $current
done