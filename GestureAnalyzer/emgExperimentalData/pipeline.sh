#!/bin/bash

if (( $# != 1 ))
then
	echo "Wrong number of parameters!"
	exit
fi

rm tmpFiles/*

LABEL=$(basename $1 .spfmt)
cp $1 tmpFiles/.
mkdir $HOME/public_html/$LABEL 2>/dev/null


cat "tmpFiles/""$LABEL"".spfmt" |\
	./addSequenceNum.py |\
	./relativeTimestamps.py |\
	./normalizeTimestamps.py |\
	./movingAvg.py timestamp timestamp 10 |\
	./addTotal.py |\
	./movingAvg.py totalPower avgTotalPower 35 |\
	./movingAvg.py avgTotalPower avgTotalPower 25 |\
	./firstDerivitive.py avgTotalPower pwrDerivitive 100000 |\
	./movingAvg.py pwrDerivitive pwrDerivitive 30 |\
	./firstDerivitive.py pwrDerivitive pwr2ndDerivitive 1000000 |\
	./movingAvg.py pwr2ndDerivitive pwr2ndDerivitive 30 |\
	./copyColumn.py |\
	./cast2float.py emg0 |\
	./movingAvg.py emg0 emg0 30 |\
	./movingAvg.py emg0 emg0 30 |\
#	./firstDerivitive.py emg0 emg0_derivitive 10000000 |\
#	./movingAvg.py emg0_derivitive emg0_derivitive 30 |\
#	./firstDerivitive.py emg0_derivitive emg0_derivitive2nd 10000000 |\
#	./movingAvg.py emg0_derivitive2nd emg0_derivitive2nd 30 |\
	./cast2float.py emg1 |\
	./movingAvg.py emg1 emg1 30 |\
	./movingAvg.py emg1 emg1 30 |\
#	./firstDerivitive.py emg1 emg1_derivitive 10000000 |\
#	./movingAvg.py emg1_derivitive emg1_derivitive 30 |\
#	./firstDerivitive.py emg1_derivitive emg1_derivitive2nd 10000000 |\
#	./movingAvg.py emg1_derivitive2nd emg1_derivitive2nd 30 |\
	./cast2float.py emg2 |\
	./movingAvg.py emg2 emg2 30 |\
	./movingAvg.py emg2 emg2 30 |\
#	./firstDerivitive.py emg2 emg2_derivitive 10000000 |\
#	./movingAvg.py emg2_derivitive emg2_derivitive 30 |\
#	./firstDerivitive.py emg2_derivitive emg2_derivitive2nd 10000000 |\
#	./movingAvg.py emg2_derivitive2nd emg2_derivitive2nd 30 |\
	./cast2float.py emg3 |\
	./movingAvg.py emg3 emg3 30 |\
	./movingAvg.py emg3 emg3 30 |\
#	./firstDerivitive.py emg3 emg3_derivitive 10000000 |\
#	./movingAvg.py emg3_derivitive emg3_derivitive 30 |\
#	./firstDerivitive.py emg3_derivitive emg3_derivitive2nd 10000000 |\
#	./movingAvg.py emg3_derivitive2nd emg3_derivitive2nd 30 |\
	./cast2float.py emg4 |\
	./movingAvg.py emg4 emg4 30 |\
	./movingAvg.py emg4 emg4 30 |\
#	./firstDerivitive.py emg4 emg4_derivitive 10000000 |\
#	./movingAvg.py emg4_derivitive emg4_derivitive 30 |\
#	./firstDerivitive.py emg4_derivitive emg4_derivitive2nd 10000000 |\
#	./movingAvg.py emg4_derivitive2nd emg4_derivitive2nd 30 |\
	./cast2float.py emg5 |\
	./movingAvg.py emg5 emg5 30 |\
	./movingAvg.py emg5 emg5 30 |\
#	./firstDerivitive.py emg5 emg5_derivitive 10000000 |\
#	./movingAvg.py emg5_derivitive emg5_derivitive 30 |\
#	./firstDerivitive.py emg5_derivitive emg5_derivitive2nd 10000000 |\
#	./movingAvg.py emg5_derivitive2nd emg5_derivitive2nd 30 |\
	./cast2float.py emg6 |\
	./movingAvg.py emg6 emg6 30 |\
	./movingAvg.py emg6 emg6 30 |\
#	./firstDerivitive.py emg6 emg6_derivitive 10000000 |\
#	./movingAvg.py emg6_derivitive emg6_derivitive 30 |\
#	./firstDerivitive.py emg6_derivitive emg6_derivitive2nd 10000000 |\
#	./movingAvg.py emg6_derivitive2nd emg6_derivitive2nd 30 |\
	./cast2float.py emg7 |\
	./movingAvg.py emg7 emg7 30 |\
	./movingAvg.py emg7 emg7 30 |\
#	./firstDerivitive.py emg7 emg7_derivitive 10000000 |\
#	./movingAvg.py emg7_derivitive emg7_derivitive 30 |\
#	./firstDerivitive.py emg7_derivitive emg7_derivitive2nd 10000000 |\
#	./movingAvg.py emg7_derivitive2nd emg7_derivitive2nd 30 |\
	./truncate.py 100 |\
#	./zeroCross.py emg0_derivitive2nd |\
#	./intervalAverage.py 20 emg0_derivitive2nd |\
#	./zeroCross.py emg1_derivitive2nd |\
#      ./intervalAverage.py 20 emg1_derivitive2nd |\
#	./zeroCross.py emg2_derivitive2nd |\
#	./intervalAverage.py 20 emg2_derivitive2nd |\
#	./zeroCross.py emg3_derivitive2nd |\
#       ./intervalAverage.py 20 emg3_derivitive2nd |\
#	./zeroCross.py emg4_derivitive2nd |\
#       ./intervalAverage.py 20 emg4_derivitive2nd |\
#	./zeroCross.py emg5_derivitive2nd |\
#        ./intervalAverage.py 20 emg5_derivitive2nd |\
#	./zeroCross.py emg6_derivitive2nd |\
#        ./intervalAverage.py 20 emg6_derivitive2nd |\
#	./zeroCross.py emg7_derivitive2nd |\
#        ./intervalAverage.py 20 emg7_derivitive2nd |\
	./zeroCross.py pwr2ndDerivitive |\
	./intervalAverage.py 10 pwr2ndDerivitive |\
	./stripColumn.py seqNum |\
	./stripColumn.py emg0_derivitive |\
	./stripColumn.py emg1_derivitive |\
	./stripColumn.py emg2_derivitive |\
	./stripColumn.py emg3_derivitive |\
	./stripColumn.py emg4_derivitive |\
      ./stripColumn.py emg5_derivitive |\
        ./stripColumn.py emg6_derivitive |\
        ./stripColumn.py emg7_derivitive |\
        ./stripColumn.py emg0_derivitive2nd |\
        ./stripColumn.py emg1_derivitive2nd |\
        ./stripColumn.py emg2_derivitive2nd |\
        ./stripColumn.py emg3_derivitive2nd |\
        ./stripColumn.py emg4_derivitive2nd |\
        ./stripColumn.py emg5_derivitive2nd |\
        ./stripColumn.py emg6_derivitive2nd |\
        ./stripColumn.py emg7_derivitive2nd |\
	./vectorize.py |\
	./rangeDetect.py >  "tmpFiles/""$LABEL""_postProcessed.spfmt"

./spfmt2dat.py < "tmpFiles/""$LABEL""_postProcessed.spfmt" > "tmpFiles/""$LABEL"".dat"

FINAL_TIMESTAMP=$(tail -n1 < "tmpFiles/""$LABEL"".dat" | cut -f1)

cp emg.gnu tmpFiles/tmp.gnu

#cat "tmpFiles/""$LABEL""_postProcessed.spfmt" |\
#	./topPercent.py |\
#	./interval2shadedRegion.py $FINAL_TIMESTAMP pwr2ndDerivitive > tmpFiles/rects

cp combined.gnu tmpFiles/combined.gnu
echo -n "plot " >> tmpFiles/combined.gnu
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

		cat "tmpFiles/""$LABEL""_postProcessed.spfmt" |\
			./topPercent.py |\
			./interval2shadedRegion.py $FINAL_TIMESTAMP $(echo $CHANNEL | cut -f1 -d'_') >> tmpFiles/tmp.gnu

		if [[ $CHANNEL == emg* ]]
		then
			echo -n "'tmpFiles/""$LABEL"".dat' using 1:""$COLUMN"" title \"""$CHANNEL""\"with lines, " >> tmpFiles/combined.gnu
			sed 's/XRANGE/'$FINAL_TIMESTAMP'/g' -i tmpFiles/combined.gnu
			sed 's/OUTPUT_FILENAME/'"$LABEL""\\/combined"'/g' -i tmpFiles/combined.gnu
		else
			sed 's/YRANGE//' -i tmpFiles/tmp.gnu
			echo "plot 'tmpFiles/INPUT_FILENAME.dat' using 1:OUTPUT_COLUMN notitle with lines" >> tmpFiles/tmp.gnu
			sed 's/TITLE/'$CHANNEL'/g' -i tmpFiles/tmp.gnu
			sed 's/INPUT_FILENAME/'$LABEL'/g' -i tmpFiles/tmp.gnu
			sed 's/OUTPUT_FILENAME/'"$LABEL""\\/""$CHANNEL"'/g' -i tmpFiles/tmp.gnu
			sed 's/OUTPUT_COLUMN/'"$COLUMN"'/g' -i tmpFiles/tmp.gnu
			sed 's/XRANGE/'$FINAL_TIMESTAMP'/g' -i tmpFiles/tmp.gnu
			gnuplot tmpFiles/tmp.gnu
			echo "<img src="'"'"$CHANNEL"".svg"'"'"><br>" >> $HOME/public_html/$LABEL/index.html
		fi

	done

echo "" >> tmpFiles/combined.gnu
sed -i 's/, $//' tmpFiles/combined.gnu
gnuplot tmpFiles/combined.gnu
echo "<img src="'"'"combined.svg"'"'"><br>" >> $HOME/public_html/$LABEL/index.html


INTERVAL_IDX=0
echo "<code>" >> $HOME/public_html/$LABEL/index.html
grep interval < "tmpFiles/""$LABEL""_postProcessed.spfmt" |\
	fgrep 'pwr2ndDerivitive' |\
	./topPercent.py |\
	while read pkt
	do
		INTERVAL_IDX=$(($INTERVAL_IDX + 1))

		echo "$pkt" >> $HOME/public_html/$LABEL/index.html
		echo '</code>'  >> $HOME/public_html/$LABEL/index.html

		echo "$pkt" | ./vector2dat.py > tmpFiles/vector.dat
		echo "$pkt" | ./vectorSum2dat.py > tmpFiles/vectorSum.dat

		cat tmpFiles/vector.dat >>  $HOME/public_html/$LABEL/vectors.dat
		cat tmpFiles/vectorSum.dat >> $HOME/public_html/$LABEL/vectorSums.dat

		cp vector.gnu tmpFiles/vector.gnu
		sed -i 's/INTERVAL_IDX/'"$INTERVAL_IDX"'/' tmpFiles/vector.gnu
		sed 's/OUTPUT_DIR/'"$LABEL""\\/""$CHANNEL"'/g' -i tmpFiles/vector.gnu
		gnuplot tmpFiles/vector.gnu
		
		echo '<br><img src="vector'"$INTERVAL_IDX"'.svg">' >> $HOME/public_html/$LABEL/index.html

		echo '<br><br><br><code>' >> $HOME/public_html/$LABEL/index.html
	done
echo "</code>" >> $HOME/public_html/$LABEL/index.html


chmod -R a+r $HOME/public_html/*
