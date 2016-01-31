#!/bin/bash
find |\
	grep csv |\
	grep -v raw |\
	while read x
	do
		cat $x |\
			while read y
			do
				echo -n "$y,"
				echo $y |\
					grep -v ':' |\
					cut -d',' -f2- |\
					tr ',' '+' |\
					bc
				echo
			done > $x_with_total.csv
	done

