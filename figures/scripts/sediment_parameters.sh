#!/bin/bash

grid_U="../../output/U.grd"
grid_Th="../../output/Th.grd"
grid_K="../../output/K.grd"
grid_alpha="../../output/H2_alpha.grd"
grid_beta="../../output/H2_beta.grd"
grid_gamma="../../output/H2_gamma.grd"
grid_rho="../../output/density.grd"

ps="../ps/sediment_parameters.ps"

gmt set PS_MEDIA = 9.3ix7.4i

map="H0/2.5i"
color_range="-T.5e5/2.5e5"
gmt makecpt -C../cpt/thermal.cpt $color_range -Z -N128/128/128 > tmp.cpt
gmt grdimage $grid_alpha --MAP_ANNOT_OFFSET_PRIMARY=8p -J$map -Bg45 -Ctmp.cpt -P -X.5 -Y3.5i -K > $ps
gmt pscoast -J -R -Df -W1/.1p -K -O >> $ps
gmt psscale -Ctmp.cpt -R$grid_alpha -J -DJBC+w2.5i/.125i --FONT_ANNOT_PRIMARY=12p --FONT_LABEL=12p -W1e-5 -Bxa.5+l"@~\141@~-decay yield (10@+5@+ molecules MeV@+-1@+)" -By -K -O >> $ps

color_range="-T2750/18250"
gmt makecpt -C../cpt/thermal.cpt $color_range -Z -N128/128/128 > tmp.cpt
gmt grdimage $grid_beta --MAP_ANNOT_OFFSET_PRIMARY=8p -J$map -Bg45 -Ctmp.cpt -X3.15i -K -O >> $ps
gmt pscoast -J -R -Df -W1/.1p -K -O >> $ps
gmt psscale -Ctmp.cpt -R$grid_beta -J -DJBC+w2.5i/.125i --FONT_ANNOT_PRIMARY=12p --FONT_LABEL=12p -W1e-4 -Bxa.385-.105+l"@~\142@~-decay yield (10@+4@+ molecules MeV@+-1@+)" -By -K -O >> $ps

color_range="-T2750/18250"
gmt makecpt -C../cpt/thermal.cpt $color_range -Z -N128/128/128 > tmp.cpt
gmt grdimage $grid_gamma --MAP_ANNOT_OFFSET_PRIMARY=8p -J$map -Bg45 -Ctmp.cpt -X3.15i -K -O >> $ps
gmt pscoast -J -R -Df -W1/.1p -K -O >> $ps
gmt psscale -Ctmp.cpt -R$grid_gamma -J -DJBC+w2.5i/.125i --FONT_ANNOT_PRIMARY=12p --FONT_LABEL=12p -W1e-4 -Bxa.385-.105+l"@~\147@~-decay yield (10@+4@+ molecules MeV@+-1@+)" -By -K -O >> $ps

color_range="-T.725/2.725"
gmt makecpt -C../cpt/bcyr.cpt $color_range -Z > tmp.cpt
gmt grdimage $grid_U --MAP_ANNOT_OFFSET_PRIMARY=8p -J$map -Bg45 -Ctmp.cpt -X-6.3i -Y2.5i -K -O >> $ps
gmt pscoast -J -R -Df -W1/.1p -K -O >> $ps
gmt psscale -Ctmp.cpt -R$grid_U -J -DJBC+w2.5i/.125i --FONT_ANNOT_PRIMARY=12p --FONT_LABEL=12p -Bxa.5-.275+l"[U] (ppm)" -By -K -O >> $ps

color_range="-T0.25/12.25"
gmt makecpt -C../cpt/bcyr.cpt $color_range -Z > tmp.cpt
gmt grdimage $grid_Th --MAP_ANNOT_OFFSET_PRIMARY=8p -J$map -Bg45 -Ctmp.cpt -X3.15i -K -O >> $ps
gmt pscoast -J -R -Df -W1/.1p -K -O >> $ps
gmt psscale -Ctmp.cpt -R$grid_Th -J -DJBC+w2.5i/.125i --FONT_ANNOT_PRIMARY=12p --FONT_LABEL=12p -Bxa3+l"[Th] (ppm)" -By -K -O >> $ps

color_range="-T500/24500"
gmt makecpt -C../cpt/bcyr.cpt $color_range -Z > tmp.cpt
gmt grdimage $grid_K --MAP_ANNOT_OFFSET_PRIMARY=8p -J$map -Bg45 -Ctmp.cpt -X3.15i -K -O >> $ps
gmt pscoast -J -R -Df -W1/.1p -K -O >> $ps
gmt psscale -Ctmp.cpt -R$grid_K -J -DJBC+w2.5i/.125i --FONT_ANNOT_PRIMARY=12p --FONT_LABEL=12p -W1e-3 -Bxa6+l"[K] (10@+3@+ ppm)" -By -K -O >> $ps

color_range="-T2.3/2.701"
gmt makecpt -C../cpt/haline.cpt $color_range -Z > tmp.cpt
gmt grdimage $grid_rho --MAP_ANNOT_OFFSET_PRIMARY=8p -J$map -Bg45 -Ctmp.cpt -X-3.15i -Y-5i -K -O >> $ps
gmt pscoast -J -R -Df -W1/.1p -K -O >> $ps
gmt psscale -Ctmp.cpt -R$grid_rho -J -DJBC+w2.5i/.125i --FONT_ANNOT_PRIMARY=12p --FONT_LABEL=12p -Bxa.1+l"Density (g/cm@+3@+)" -By -O >> $ps



/bin/rm -rf tmp.cpt

gmt psconvert -Tg -E800 $ps
mv ../ps/sediment_parameters.png ../png/