# Guillaume Dueymes: version 29-10-2019
# Code python permettant d extraire de ERA5
#
# https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=form
# Besoin d'avoir une clef API d'ECMWF
# 
import cdsapi
c = cdsapi.Client()

yearStart = 2020
yearEnd = 2020
monthStart = 1
monthEnd = 10

for year in list(range(yearStart, yearEnd + 1)):
    
    requestMonthList = []
    for month in list(range(monthStart, monthEnd + 1)):
        # we submit a data request for the current year
        target = "era5_edna_ea_UU_VV_TD_TT_"+str(year)+"{:02d}".format(month)+"_17hUTC.nc"  
        c.retrieve(
            'reanalysis-era5-single-levels',
            {
                'product_type':'reanalysis',
                'pressure_level': '1000',
                'variable': [
            '10m_u_component_of_wind', '10m_v_component_of_wind', '2m_dewpoint_temperature',
            '2m_temperature',
        ],
                'year':year,
                'month':month,
                'day':[
                    '01','02','03',
                    '04','05','06',
                    '07','08','09',
                    '10','11','12',
                    '13','14','15',
                    '16','17','18',
                    '19','20','21',
                    '22','23','24',
                    '25','26','27',
                    '28','29','30',
                    '31'
                ],
                'time':[
                    '17:00'
                ],
                'format':'netcdf'
            },target)
