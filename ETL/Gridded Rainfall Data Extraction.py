# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 07:50:02 2021

@author: JOEL
"""


import geopandas as gpd 
import os 
import rasterio
import scipy.sparse as sparse 
import pandas as pd
import numpy as np

# Create an empty pandas dataframe called 'table'
table = pd.DataFrame(index = np.arange(0,1))

# Read the points shapefile using GeoPandas 
stations = gpd.read_file(r'C:/Users/JOEL/sde-columbia-iscgm_ethiopia_2008_builtupp-shapefile/columbia_iscgm_ethiopia_2008_builtupp.shp')
stations['lon'] = stations['geometry'].x
stations['lat'] = stations['geometry'].y
  
Matrix = pd.DataFrame()

# Iterate through the rasters and save the data as individual arrays to a Matrix 
for files in os.listdir(r'C:\Users\JOEL\chirps\1996-1999'):
    if files[-4: ] == '.tif':
        dataset = rasterio.open(r'C:\Users\JOEL\chirps\1996-1999'+'\\'+files)
        data_array = dataset.read(1)
        data_array_sparse = sparse.coo_matrix(data_array, shape = (320,300))
        data = files[ :-4]
        Matrix[data] = data_array_sparse.toarray().tolist()
        print('Processing is done for the raster: '+ files[:-4])

# Iterate through the stations and get the corresponding row and column for the related x, y coordinates    
for index, row in stations.iterrows(): 
    station_name = str(row['nam'])
    lon = float(row['lon'])
    lat = float(row['lat'])
    x,y = (lon, lat)
    row, col = dataset.index(x, y)
    print('Processing: '+ station_name)
    
    # Pick the rainfall value from each stored raster array and record it into the previously created 'table'
    for records_date in Matrix.columns.tolist():
        a = Matrix[records_date]
        rf_value = a.loc[int(row)][int(col)]
        table[records_date] = rf_value
        transpose_mat = table.T
        transpose_mat.rename(columns = {0: station_name}, inplace = True)
    
    transpose_mat.to_csv(r'C:\Users\JOEL\Ethiopia_Stations\eth1996-1999 '+'\\'+station_name+'.csv')
        
        