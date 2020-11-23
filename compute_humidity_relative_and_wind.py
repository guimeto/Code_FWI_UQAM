# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 10:31:05 2019
Code pour calculer le module du vent et approximer l'humidité relative d'ERA5
@author: guillaume
pour importer xarray 

module load python3/miniconda3
source activate cdo
"""
import xarray as xr
import numpy as np
model = 'era5_edna_ea_UU_VV_TD_TT'
modelout = 'ERA5'

yi = 2019
yf = 2020
#########################################################
path_in = '/snow3/dueymes/REANALYSES/ERA5/UU_VV_TD_TT_17h/'
path_out = '/snow3/dueymes/REANALYSES/ERA5/UU_VV_TC/' 
hum_out = '/snow3/dueymes/REANALYSES/ERA5/HR/'
for year in range(yi,yf+1):
    for i in range (1,13,1):  
        lat_bnd = [62, 43]
        lon_bnd = [276, 306]
        
        data = path_in + model + '_'+str(year) +'{:02d}'.format(i)+'_17hUTC.nc'
        ds = xr.open_dataset(data)  
        ds = ds.sel(longitude=slice(*lon_bnd), latitude=slice(*lat_bnd))  
        
        tc = ds.t2m
        td = ds.d2m  
      
        humidity = np.zeros((len(tc),len(tc[0]),len(tc[0][0])),dtype=float)
        for ni in range(0, len(tc[0])):
            for nj in range(0, len(tc[0][0])):
                    humidity[:,ni,nj] =((6.11 * np.exp(5417.7530 * ((1 / 273.16) - (1 / td[:,ni,nj]))))/( 6.11 * np.exp(5417.7530 * ((1 / 273.16) - (1 / tc[:,ni,nj])))))*100
       
         # sauvegarde du champs en xarray
        data_set = xr.Dataset( coords={'lon': ([ 'lon'], ds.variables['longitude'][:]),
                                     'lat': (['lat',], ds.variables['latitude'][:]),
                                     'time': ds.variables['time'][:]})
        
        data_set["Humidity"] = (['time','lat', 'lon'],  humidity)

        #data_set= data_set.sel(lon=slice(*lon_bnd), lat=slice(*lat_bnd)) 
        data_set.to_netcdf(hum_out + modelout + '_Humidity_'+str(year) +'{:02d}'.format(i)+'_17h.nc')
        
        
        ds3 = np.sqrt(np.square(ds.u10) + np.square(ds.v10))
               
        # conversion mm.s-1 to km.h-1
        ds['wind'] = 3.6 * ds3
        # conversion Kelvin to Celcius
        ds['Tc'] =  ds.t2m - 273.15
        
        lat_bnd = [62, 43]
        lon_bnd = [276, 306]
        ds = ds.sel(longitude=slice(*lon_bnd), latitude=slice(*lat_bnd))    
        ds.to_netcdf(path_out + modelout + '_TC_WIND_'+str(year) +'{:02d}'.format(i)+'_17h.nc')
