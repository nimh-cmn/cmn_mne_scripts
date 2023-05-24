#!/bin/bash

#units issue - need josh to modify
#multiplying by 1000 fixed size, but then it was out of center
#calculated average x,y,z (3dBrickStat) in last column (difference btw std 60 and ours)
#eeg surfaces are done in meters instead of mm

echo $1

#get coordinates out
SurfaceMetrics -i $1 -coords

centerX=`3dBrickStat -mean ${1}.coord.1D.dset[1]`
centerY=`3dBrickStat -mean ${1}.coord.1D.dset[2]`
centerZ=`3dBrickStat -mean ${1}.coord.1D.dset[3]`

echo "Center for your dataset: ${centerX} ${centerY} ${centerZ}"

SurfaceMetrics -i SUMA/std.60.lh.white.gii -coords
stdCenterX=`3dBrickStat -mean std.60.lh.white.gii.coord.1D.dset[1]`
stdCenterY=`3dBrickStat -mean std.60.lh.white.gii.coord.1D.dset[2]`
stdCenterZ=`3dBrickStat -mean std.60.lh.white.gii.coord.1D.dset[3]`

echo "Center for your std.60: ${stdCenterX} ${stdCenterY} ${stdCenterZ}"

scaleX=`ccalc ${stdCenterX} - ${centerX}`
scaleY=`ccalc ${stdCenterY} - ${centerY}`
scaleZ=`ccalc ${stdCenterZ} - ${centerZ}`

echo "Shifting..."
echo "${scaleX} ${scaleY} ${scaleZ}"

#build scalar
if [ -e center_al.1D ]; then
    rm center_al.1D
fi
echo "1 0 0 ${scaleX}" >> center_al.1D
echo "0 1 0 ${scaleY}" >> center_al.1D
echo "0 0 1 ${scaleZ}" >> center_al.1D

ConvertSurface -xmat_1D center_al.1D -i $1 -o ${1%.gii}_centered.gii

SurfToSurf -i_gii SUMA/std.60.lh.white.gii \
-i_gii ${1%.gii}_centered.gii \
-dset NEF_S01_nov-lh.time.gii \
-prefix std.60.

#check the overlap of surface meshes
#suma -onestate -i NEF_S01_nov-lh_centered.gii SUMA/std.60.lh.white.gii

#visualize the time data on std.60 surfaces
#suma -spec SUMA/std.60.NEF_S01_lh.spec -sv SUMA/NEF_S01_SurfVol.nii