set term png small size 800,600
set output "mem-graph.png"

set ylabel "%CPU"
set y2label "%MEM"

set ytics nomirror
set y2tics nomirror in

set yrange [0:*]
set y2range [0:*]

plot "mem.dat" using 1 with lines axes x1y1 title "%CPU", \
     "mem.dat" using 2 with lines axes x1y2 title "%MEM"