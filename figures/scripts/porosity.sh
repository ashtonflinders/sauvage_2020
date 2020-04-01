#!/bin/bash

grid="../../input/porosity.grd"
ps="../ps/porosity.ps"

gmt set PS_MEDIA = 7ix4i
color_range="-T40/90"
gmt makecpt -C../cpt/cequal.cpt $color_range -Z -N128/128/128 > tmp.cpt
gmt grdimage $grid --MAP_ANNOT_OFFSET_PRIMARY=8p -JH0/6i -Bg45 -Ctmp.cpt -P -Xc -Y.9i -K > $ps
gmt pscoast -J -R -Df -W1/.2p -K -O >> $ps
gmt psscale -Ctmp.cpt -R$grid -J -DJBC+w6i/.125i --FONT_ANNOT_PRIMARY=12p --FONT_LABEL=12p -Bxa10+l"Seafloor Sediment Porosity (%)" -By -O >> $ps
/bin/rm -rf tmp.cpt

gmt psconvert -Tg -E600 $ps
mv ../ps/porosity.png ../png/