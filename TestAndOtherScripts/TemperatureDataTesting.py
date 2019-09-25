
# coding: utf-8

# In[2]:


import netCDF4 as nc
import numpy as np
import pandas as pd
import sys
from netCDF4 import Dataset
from math import sin, cos, sqrt, atan2, radians


# In[3]:


grid = Dataset('air.2011.nc', 'r')
dims = grid.dimensions
variables = grid.variables
attrs = grid.ncattrs


# In[4]:


dims.keys()


# In[5]:


grid['lon']


# In[6]:


variables.keys()


# In[7]:


variables['air']


# In[8]:


air = variables['air'][:]
lats = variables['lat'][:]
time = variables['time'][:]
lons = variables['lon'][:]
levels = variables['level'][:]


# In[9]:


len(air[0][0][0])


# In[10]:


len(lons)


# In[ ]:


for lat in range(len(lats)):
    for lon in range(len(lons)):
        for t in range(len(time)):
            for l in range(len(levels)):
                print(air[t][l][lat][lon])
            


# In[ ]:


for i in variables:
    print(i,variables[i].units,variables[i].shape)


# In[ ]:


birdfeeder_df = pd.read_csv('PFW2011-12_Subset.csv')


# In[ ]:


birdfeeder_df.head()


# In[ ]:


birdfeeder_df["air_temp"] = np.nan


# In[ ]:


len(birdfeeder_df)


# In[ ]:


temp_2011 = Dataset('air.sig995.2011.nc', 'r')
dims = temp_2011.dimensions
variables = temp_2011.variables
attrs = temp_2011.ncattrs


# In[ ]:


temp_2011


# In[ ]:


variables


# In[ ]:


time = variables['time'][:]


# In[ ]:


for t in time:
    print(t)


# In[ ]:


len(time)


# In[ ]:


dtime = nc.num2date(time[:],variables['time'].units)


# In[ ]:


len(dtime)


# In[ ]:


for d in dtime:
    print(d)


# In[ ]:


lat = variables['lat'][:]


# In[ ]:


air.shape()


# In[ ]:


for l in range(len(lat)):
    print (lat[l])


# In[ ]:


row = next(birdfeeder_df.iterrows())[1]
print(row['Year'])


# In[ ]:


birdfeeder_df = pd.read_csv('PFW2011-12_Subset.csv')
birdfeeder_df["air_temp"] = np.nan

temp_2011 = Dataset('air.sig995.2011.nc', 'r')
dims = temp_2011.dimensions
variables = temp_2011.variables
attrs = temp_2011.ncattrs

air = variables['air'][:]
lats = variables['lat'][:]
time = variables['time'][:]
lons = variables['lon'][:]

dtime = nc.num2date(time[:],variables['time'].units)


# In[ ]:


def calcDistance(lat1, lon1, lat2, lon2):
    R = 6373.0
    
    latitude1 = radians(lat1)
    longitude1 = radians(lon1)
    latitude2 = radians(lat2)
    longitude2 = radians(lon2)
    
    dlon = longitude2 - longitude1
    dlat = latitude2 - latitude1
    
    a = sin(dlat / 2)**2 + cos(latitude1) * cos(latitude2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return (R * c)
    


# In[ ]:


def getAirTemp(month, day, year, lat, lon):
    tuples_dtime = []
    
    for d in range(len(dtime)):
        tuples_dtime.append((dtime[d].month, dtime[d].day, dtime[d].year))
    
    if (year == 2011):
        tuples_dtime_idx = tuples_dtime.index((month, day, year))

        for la in range (len(lats)):
            for lo in range (len(lons)):
                distance = calcDistance(lats[la], lons[lo], lat, lon)
                if (distance <= 100):
                    return air[tuples_dtime_idx][la][lo]
            
    return (-sys.maxsize- 1)


# In[96]:


counter = 0

for index, row in birdfeeder_df.iterrows():
    if (counter == 5):
        break
    
    temp = getAirTemp(row['Month'], row['Day'], row['Year'], row['LATITUDE'], row['LONGITUDE'])
    if (temp != (-sys.maxsize - 1)):
        counter += 1
        birdfeeder_df.set_value(index, 'air_temp', temp)
        print(row['air_temp'])


# In[97]:


birdfeeder_df.head()


# In[80]:


for index, row in birdfeeder_df.iterrows():
    if (row['air_temp'] != np.nan):
        print(row['air_temp'])

