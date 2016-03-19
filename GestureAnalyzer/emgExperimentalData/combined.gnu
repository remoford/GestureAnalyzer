set terminal svg size 1800,400 fixed enhanced fname 'Arial'
set output '~/public_html/OUTPUT_FILENAME.svg'

set grid nopolar

set ytics  norangelimit
set noxtics

set lmargin 0
set rmargin 0
set tmargin 0
set bmargin 0

set xrange [ 0.0000 : XRANGE ] noreverse nowriteback

#set yrange [ 0 : 128 ] noreverse nowriteback


