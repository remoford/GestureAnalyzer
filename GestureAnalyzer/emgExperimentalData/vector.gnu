set terminal svg size 400,400 fixed enhanced fname 'Arial'
set output '~/public_html/OUTPUT_DIR/vectorINTERVAL_IDX.svg'

set grid nopolar

set ytics  norangelimit
set noxtics

set lmargin 0
set rmargin 0
set tmargin 0
set bmargin 0

set xrange [ -64 : 64 ] noreverse nowriteback

set yrange [ -64 : 64 ] noreverse nowriteback

set style arrow 1 linecolor rgb "black"
set style arrow 2 linecolor rgb "red" linewidth 5

plot 'tmpFiles/vector.dat' using 1:2:3:4 with vectors notitle arrowstyle 1, \
	'tmpFiles/vectorSum.dat' using 1:2:3:4 with vectors notitle arrowstyle 2,
