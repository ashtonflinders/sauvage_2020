#!/bin/bash

grid="../../input/depth.grd"
ps="../ps/depth.ps"

gmt set PS_MEDIA = 7ix4i
color_range="-T0/8000"
gmt makecpt -C../cpt/haxby_cont.cpt $color_range -Z -I > tmp.cpt
gmt grdimage $grid --MAP_ANNOT_OFFSET_PRIMARY=8p -JH0/6i -Bg45 -Ctmp.cpt -P -Xc -Y.9i -K > $ps
gmt pscoast -J -R -Df -W1/.2p -K -O >> $ps
gmt psscale -Ctmp.cpt -R$grid -J -DJBC+w6i/.125i --FONT_ANNOT_PRIMARY=12p --FONT_LABEL=12p -Bxa1000+l"Ocean Depth (meters)" -By -O >> $ps
/bin/rm -rf tmp.cpt

gmt psconvert -Tg -E600 $ps
mv ../ps/depth.png ../png/