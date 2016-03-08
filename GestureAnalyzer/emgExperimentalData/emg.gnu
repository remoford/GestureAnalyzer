set terminal svg size 1800,80 fixed enhanced fname 'Arial'
set output '~/public_html/OUTPUT_FILENAME.svg'

set grid nopolar

set ytics  norangelimit
set noxtics

set label 3 'TITLE' at graph 0, graph 0 offset 1,1

set lmargin 0
set rmargin 0
set tmargin 0
set bmargin 0

set xrange [ 0.0000 : XRANGE ] noreverse nowriteback
#set yrange [ YRANGENEG : YRANGE ] noreverse nowriteback

set style rect fc lt -1 fs solid 0.15 noborder

