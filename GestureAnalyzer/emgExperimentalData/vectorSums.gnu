set terminal svg size 300,300 fixed enhanced fname 'Arial'
set output '~/public_html/vectorSums_GESTURE.svg'

set grid nopolar

set ytics  norangelimit
set noxtics

set lmargin 0
set rmargin 0
set tmargin 0
set bmargin 0

set xrange [ -8 : 8 ] noreverse nowriteback

set yrange [ -8 : 8 ] noreverse nowriteback


set style arrow 1 linecolor rgb "black"
set style arrow 2 linecolor rgb "red"
set style arrow 3 linecolor rgb "green"
set style arrow 4 linecolor rgb "blue"
set style arrow 5 linecolor rgb "yellow"
set style arrow 6 linecolor rgb "brown"
set style arrow 7 linecolor rgb "orange"

plot	'tmpFiles/vectorSums_GESTURE_ahmed.dat'		using 1:2:3:4 with vectors notitle arrowstyle 1, \
	'tmpFiles/vectorSums_GESTURE_ashlin.dat'	using 1:2:3:4 with vectors notitle arrowstyle 2, \
	'tmpFiles/vectorSums_GESTURE_bwisengo.dat'	using 1:2:3:4 with vectors notitle arrowstyle 3, \
	'tmpFiles/vectorSums_GESTURE_hang.dat'		using 1:2:3:4 with vectors notitle arrowstyle 4, \
	'tmpFiles/vectorSums_GESTURE_john.dat'		using 1:2:3:4 with vectors notitle arrowstyle 5, \
	'tmpFiles/vectorSums_GESTURE_josh.dat'		using 1:2:3:4 with vectors notitle arrowstyle 6, \
	'tmpFiles/vectorSums_GESTURE_stacy.dat'		using 1:2:3:4 with vectors notitle arrowstyle 7
