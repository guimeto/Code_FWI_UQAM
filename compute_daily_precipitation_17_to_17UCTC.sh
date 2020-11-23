#!/bin/sh

set -aex

model=era5_edna_ea
pathin=/snow3/dueymes/REANALYSES/ERA5/PR_1h
pathout=/snow3/dueymes/REANALYSES/ERA5/PR_daily

      yyyy=1979
      yend=2009

      while [ "${yyyy}" -le "${yend}" ] 
      do
         date1=${yyyy}

         cdo mergetime ${pathin}/${model}_${date1}*_sfc.nc in.nc
         cdo daysum -shifttime,-5hour in.nc daysum.nc
         cdo splitmon daysum.nc ${pathin}/ERA5_daily_PR_17hUTC_

      yyyy=`expr $yyyy + 1`

      done   # year loop
   



