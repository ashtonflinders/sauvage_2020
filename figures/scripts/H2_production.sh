#!/bin/bash

grid="../../output/H2_production.grd"
ps="../ps/H2_production.ps"

gmt set PS_MEDIA = 7ix4i

gmt makecpt -C../cpt/bcyr.cpt -T-6/0/1 -Q -Z > tmp.cpt
gmt grdimage $grid --MAP_ANNOT_OFFSET_PRIMARY=8p -JH0/6i -Bg45 -Ctmp.cpt -P -Xc -Y.9i -K > $ps
gmt pscoast -J -R -Df -W1/.2p -K -O >> $ps
gmt psscale -Ctmp.cpt -R$grid -J -DJBC+w6i/.125i --FONT_LABEL=12p -Q -Bx1p+l"Radiolytic H@-2@- Production (mol H@-2@- m@+-2@+ year@+-1@+)" -By -O >> $ps
/bin/rm -rf tmp.cpt

gmt psconvert -Tg -E600 $ps
mv ../ps/H2_production.png ../png/