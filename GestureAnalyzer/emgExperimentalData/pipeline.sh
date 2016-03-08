#!/bin/bash

if (( $# != 1 ))
then
	echo "Wrong number of parameters!"
	exit
fi

LABEL=$(basename $1 .spfmt)
cp $1 tmpFiles/.
mkdir $HOME/public_html/$LABEL 2>/dev/null


cat "tmpFiles/""$LABEL"".spfmt" |\
	./relativeTimestamps.py |\
	./addTotal.py |\
	./movingAvg.py totalPower avgTotalPower 40 |\
	./movingAvg.py avgTotalPower avgTotalPower 20 |\
	./movingAvg.py timestamp timestamp 10 |\
	./firstDerivitive.py avgTotalPower pwrDerivitive 100000 |\
	./movingAvg.py pwrDerivitive pwrDerivitive 30 |\
	./cast2int.py pwrDerivitive |\
	./firstDerivitive.py pwrDerivitive pwr2ndDerivitive 1000000 |\
	./movingAvg.py pwr2ndDerivitive pwr2ndDerivitive 60 |\
	./zeroCross.py pwr2ndDerivitive |\
	./intervalAverage.py > "tmpFiles/""$LABEL""_postProcessed.spfmt"

./spfmt2dat.py < "tmpFiles/""$LABEL""_postProcessed.spfmt" > "tmpFiles/""$LABEL"".dat"

FINAL_TIMESTAMP=$(tail -n1 < "tmpFiles/""$LABEL"".dat" | cut -f1)

cp emg.gnu tmpFiles/tmp.gnu

./interval2shadedRegion.py $FINAL_TIMESTAMP < "tmpFiles/""$LABEL""_postProcessed.spfmt"  > tmpFiles/rects


echo > $HOME/public_html/$LABEL/index.html
COLUMN=1
head -n1 < "tmpFiles/""$LABEL"".dat" |\
	cut -f2- |\
	sed 's/\t$//' |\
	tr '\t' '\n' |\
	while read CHANNEL
	do
		COLUMN=$(($COLUMN+1))
		cp emg.gnu tmpFiles/tmp.gnu
		cat tmpFiles/rects >> tmpFiles/tmp.gnu
		echo "plot 'tmpFiles/INPUT_FILENAME.dat' using 1:OUTPUT_COLUMN notitle with lines" >> tmpFiles/tmp.gnu
		sed 's/TITLE/'$CHANNEL'/g' -i tmpFiles/tmp.gnu
		sed 's/INPUT_FILENAME/'$LABEL'/g' -i tmpFiles/tmp.gnu
		sed 's/OUTPUT_FILENAME/'"$LABEL""\\/""$CHANNEL"'/g' -i tmpFiles/tmp.gnu
		sed 's/OUTPUT_COLUMN/'"$COLUMN"'/g' -i tmpFiles/tmp.gnu
		sed 's/XRANGE/'$FINAL_TIMESTAMP'/g' -i tmpFiles/tmp.gnu
		gnuplot tmpFiles/tmp.gnu
		echo "<img src="'"'"$CHANNEL"".svg"'"'"><br>" >> $HOME/public_html/$LABEL/index.html
	done

echo "<code>" >> $HOME/public_html/$LABEL/index.html
grep interval < "tmpFiles/""$LABEL""_postProcessed.spfmt" >> $HOME/public_html/$LABEL/index.html
echo "</code>" >> $HOME/public_html/$LABEL/index.html

rm tmpFiles/*

chmod -R a+r $HOME/public_html/*
