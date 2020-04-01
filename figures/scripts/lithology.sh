#!/bin/bash

grid="../../output/lithology.grd"
ps="../ps/lithology.ps"

gmt set PS_MEDIA = 7ix4i
gmt grdimage $grid --MAP_ANNOT_OFFSET_PRIMARY=8p -JH0/6i -Bg45 -C../cpt/lithology.cpt -P -Xc -Y.9i -K > $ps
gmt pscoast -J -R -Df -W1/.2p -K -O >> $ps
gmt psscale -C../cpt/lithology.cpt -R$grid -J -DJBC+w6i/.125i --FONT_ANNOT_PRIMARY=9p --FONT_LABEL=12p -Bx+l"Simplified Seafloor Lithology" -Li -O >> $ps

gmt psconvert -Tg -E600 $ps
mv ../ps/lithology.png ../png/