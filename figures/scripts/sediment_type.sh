#!/bin/bash

grid="../../input/sediment_type.grd"
ps="../ps/sediment_type.ps"

gmt set PS_MEDIA = 7ix4i
color_range="-T201/3309"
gmt makecpt -C../cpt/GTS2012_epochs.cpt $color_range > tmp.cpt
gmt grdimage $grid --MAP_ANNOT_OFFSET_PRIMARY=8p -JH0/6i -Bg45 -Ctmp.cpt -P -Xc -Y.9i -K > $ps
gmt pscoast -J -R -Df -W1/.2p -K -O >> $ps
gmt psscale -Ctmp.cpt -R$grid -J -DJBC+w6i/.125i --FONT_ANNOT_PRIMARY=12p --FONT_LABEL=12p -Bxa259-58+l"Seafloor Bottom Sediment Type (NAVO Enhanced category number)" -By -O >> $ps
/bin/rm -rf tmp.cpt

gmt psconvert -Tg -E600 $ps
mv ../ps/sediment_type.png ../png/