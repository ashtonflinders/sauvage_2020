#!/bin/bash

grid="../../input/whittaker_sedthick.grd"
ps="../ps/whittaker_sedthick.ps"

gmt set PS_MEDIA = 7ix4i
color_range="-T0/14000"
gmt makecpt -C../cpt/bgyr.cpt $color_range -Z > tmp.cpt
gmt grdimage $grid --MAP_ANNOT_OFFSET_PRIMARY=8p -JH0/6i -Bg45 -Ctmp.cpt -P -Xc -Y.9i -K > $ps
gmt pscoast -J -R -Df -W1/.2p -K -O >> $ps
gmt psscale -Ctmp.cpt -R$grid -J -DJBC+w6i/.125i --FONT_ANNOT_PRIMARY=12p --FONT_LABEL=12p -Bxa2000+l"Seafloor Sediment Thickness (meters; Whittaker et al., 2013)" -By -O >> $ps
/bin/rm -rf tmp.cpt

gmt psconvert -Tg -E600 $ps
mv ../ps/whittaker_sedthick.png ../png/