#!/bin/bash

#for x in formattedSamples/*
#do
#	nice /usr/bin/time -a -o pipeline.time ./pipeline.sh $x
#done


rm ~/public_html/sums.html
rm ~/public_html/vectorSums*
echo '<head><style> h2 { margin: 0; padding: 0; } </style>' >> ~/public_html/sums.html
echo '<style> h4 { margin: 0; padding: 0; } </style></head>' >> ~/public_html/sums.html
echo '<body><table border=0><tr><td colspan="1">' >> ~/public_html/sums.html
echo '<div align="left"><h2>Vector Sums</h2></div></td>' >> ~/public_html/sums.html
echo '<td colspan="6"><div align="center"><h2>Color Key: ' >> ~/public_html/sums.html
echo '<font color="black">ahmed  </font>' >> ~/public_html/sums.html
echo '<font color="red">ashlin  </font>' >> ~/public_html/sums.html
echo '<font color="green">bwisengo  </font>' >> ~/public_html/sums.html
echo '<font color="blue">hang  </font>' >> ~/public_html/sums.html
echo '<font color="yellow">john  </font>' >> ~/public_html/sums.html
echo '<font color="brown">josh  </font>' >> ~/public_html/sums.html
echo '<font color="orange">stacy</font>' >> ~/public_html/sums.html
echo '</h2></div>' >> ~/public_html/sums.html
echo '</td></tr><tr>' >> ~/public_html/sums.html
find ~/public_html -maxdepth 1 -type d | \
	tail -n +2 |\
	while read x
	do
		basename $x
	done | \
	cut -d'_' -f2 |\
	sort -u |\
	while read gesture
	do
		cp vectorSums.gnu ./tmpFiles/vectorSums.gnu
		sed -i 's/GESTURE/'"$gesture"'/' ./tmpFiles/vectorSums.gnu
		rm ./tmpFiles/vectorSums*.dat
		cat ~/public_html/ahmed_"$gesture"_*/vectorSums.dat > ./tmpFiles/vectorSums_"$gesture"_ahmed.dat
		cat ~/public_html/ashlin_"$gesture"_*/vectorSums.dat > ./tmpFiles/vectorSums_"$gesture"_ashlin.dat
		cat ~/public_html/bwisengo_"$gesture"_*/vectorSums.dat > ./tmpFiles/vectorSums_"$gesture"_bwisengo.dat
		cat ~/public_html/hang_"$gesture"_*/vectorSums.dat > ./tmpFiles/vectorSums_"$gesture"_hang.dat
		cat ~/public_html/john_"$gesture"_*/vectorSums.dat > ./tmpFiles/vectorSums_"$gesture"_john.dat
		cat ~/public_html/josh_"$gesture"_*/vectorSums.dat > ./tmpFiles/vectorSums_"$gesture"_josh.dat
		cat ~/public_html/stacy_"$gesture"_*/vectorSums.dat > ./tmpFiles/vectorSums_"$gesture"_stacy.dat
		gnuplot ./tmpFiles/vectorSums.gnu
		echo "<td><h4>$gesture</h4><br>" >> ~/public_html/sums.html
		echo '<img src="vectorSums_'"$gesture"'.svg"></td>' >> ~/public_html/sums.html
	done
echo '</tr><tr><td colspan="7"><h2>All Vectors</h2></td></tr><tr>' >> ~/public_html/sums.html
find ~/public_html -maxdepth 1 -type d | \
        tail -n +2 |\
        while read x
        do
                basename $x
        done | \
        cut -d'_' -f2 |\
        sort -u |\
        while read gesture
        do
                cp vectors.gnu ./tmpFiles/vectors.gnu
                sed -i 's/GESTURE/'"$gesture"'/' ./tmpFiles/vectors.gnu
                rm ./tmpFiles/vectors*.dat
                cat ~/public_html/ahmed_"$gesture"_*/vectors.dat > ./tmpFiles/vectors_"$gesture"_ahmed.dat
                cat ~/public_html/ashlin_"$gesture"_*/vectors.dat > ./tmpFiles/vectors_"$gesture"_ashlin.dat
                cat ~/public_html/bwisengo_"$gesture"_*/vectors.dat > ./tmpFiles/vectors_"$gesture"_bwisengo.dat
                cat ~/public_html/hang_"$gesture"_*/vectors.dat > ./tmpFiles/vectors_"$gesture"_hang.dat
                cat ~/public_html/john_"$gesture"_*/vectors.dat > ./tmpFiles/vectors_"$gesture"_john.dat
                cat ~/public_html/josh_"$gesture"_*/vectors.dat > ./tmpFiles/vectors_"$gesture"_josh.dat
                cat ~/public_html/stacy_"$gesture"_*/vectors.dat > ./tmpFiles/vectors_"$gesture"_stacy.dat
                gnuplot ./tmpFiles/vectors.gnu
                echo "<td><h4>$gesture</h4><br>" >> ~/public_html/sums.html
                echo '<img src="vectors_'"$gesture"'.svg"></td>' >> ~/public_html/sums.html
        done
echo '</tr><tr><td colspan="7"><h2>Individual Data Runs</h2></td></tr><tr>' >> ~/public_html/sums.html
find ~/public_html -maxdepth 1 -type d | \
        tail -n +2 |\
        while read x
        do
                basename $x
        done | \
        cut -d'_' -f2 |\
        sort -u |\
        while read gesture
        do
		echo '<td valign="top"><h4>'"$gesture"'</h4><br>' >> ~/public_html/sums.html
        
		find ~/public_html -maxdepth 1 -type d |\
			tail -n +2 |\
			fgrep "_""$gesture""_" |\
			while read x
			do
				basename $x
			done |\
			while read dir
			do
				echo '<a href="'"$dir"'">'"$dir"'</a><br>' >> ~/public_html/sums.html
			done
		
		echo "</td>" >> ~/public_html/sums.html

	done


echo '</tr><table></body>' >> ~/public_html/sums.html

chmod a+r ~/public_html/*


