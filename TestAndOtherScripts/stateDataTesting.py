
# coding: utf-8

# In[107]:


import netCDF4 as nc
import numpy as np
import pandas as pd
import sys
import json
import time
import matplotlib.pyplot as plt
from urllib.request import urlopen
from math import sin, cos, sqrt, atan2, radians


# In[26]:


birdfeeder_df = pd.read_csv('PFW2011-12_Subset.csv')


# In[27]:


birdfeeder_df.tail()


# In[50]:


newYork = birdfeeder_df.query('StatProv=="NY"').copy()


# In[51]:


newYork.shape


# In[30]:


ohio = birdfeeder_df.query('StatProv=="OH"')


# In[31]:


ohio.shape


# In[32]:


mass = birdfeeder_df.query('StatProv=="MA"')


# In[33]:


mass.shape


# In[34]:


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


# In[65]:


newYork = birdfeeder_df.query('StatProv=="NY"').copy()
for index, row in newYork.iterrows():
    dis = calcDistance(row['LATITUDE'], row['LONGITUDE'], 40.730610, -73.935242)   
    if (dis > 10):
        newYork.drop(index, inplace=True)

newYork.shape

    


# In[58]:


newYork.tail()


# In[63]:


boston = birdfeeder_df.query('StatProv=="MA"').copy()
for index, row in boston.iterrows():
    dis = calcDistance(row['LATITUDE'], row['LONGITUDE'], 42.361145, 71.057083)   
    if (dis > 10):
        boston.drop(index, inplace=True)

boston.shape


# In[62]:


columbusOH = birdfeeder_df.query('StatProv=="OH"').copy()
for index, row in columbusOH.iterrows():
    dis = calcDistance(row['LATITUDE'], row['LONGITUDE'], 39.949413, -82.959656)   
    if (dis > 10):
        columbusOH.drop(index, inplace=True)

columbusOH.shape


# In[64]:


sfCA = birdfeeder_df.query('StatProv=="CA"').copy()
for index, row in sfCA.iterrows():
    dis = calcDistance(row['LATITUDE'], row['LONGITUDE'], 37.733795, -122.446747)   
    if (dis > 10):
        sfCA.drop(index, inplace=True)

sfCA.shape


# In[68]:


laCA = birdfeeder_df.query('StatProv=="CA"').copy()
for index, row in laCA.iterrows():
    dis = calcDistance(row['LATITUDE'], row['LONGITUDE'], 34.052235, -118.243683)   
    if (dis > 10):
        laCA.drop(index, inplace=True)
laCA.shape


# In[93]:


counter = 0
str1 = 'http://api.wunderground.com/api/f12eaf4e009a36bb/history_'
str2 = '/q/CA/Los_Angeles.json'
laCA['temp'] = np.nan

for index,row in laCA.iterrows():
    if (counter < 10):
        date = row['Year']
        date *= 100
        date += row['Month']
        date *= 100
        date += row['Day']
        date_str = str(date)
        
        api_link = str1 + date_str + str2
        f = urlopen(api_link)
        json_string = f.read()
        parsed_json = json.loads(json_string)
        
        if ('history' in parsed_json):
            if ('dailysummary' in parsed_json['history']):
                if (len(parsed_json['history']['dailysummary']) == 1):
                    if ('meantempi' in parsed_json['history']['dailysummary'][0]):
                        temp = parsed_json['history']['dailysummary'][0]['meantempi']
                        laCA.set_value(index, 'temp', temp)
        
        #temps.append(temp)
        
        counter += 1
    else:
        time.sleep(60)
        counter = 0
    


# In[95]:


laCA.shape


# In[96]:


for index, row in laCA.iterrows():
    if(row['temp'] == np.nan):
        laCA.drop(index, inplace=True)


# In[97]:


laCA.shape


# In[99]:


laCA.keys()


# In[100]:


laCA.head()


# In[113]:


laCA.plot(x='temp', y='NSeen', kind='scatter')


# In[114]:


plt.show()


# In[ ]:


counter = 0
str1 = 'http://api.wunderground.com/api/f12eaf4e009a36bb/history_'
str2 = '/q/NY/New_York.json'
newYork['temp'] = np.nan

for index,row in newYork.iterrows():
    if (counter < 10):
        date = row['Year']
        date *= 100
        date += row['Month']
        date *= 100
        date += row['Day']
        date_str = str(date)
        
        api_link = str1 + date_str + str2
        f = urlopen(api_link)
        json_string = f.read()
        parsed_json = json.loads(json_string)
        
        if ('history' in parsed_json):
            if ('dailysummary' in parsed_json['history']):
                if (len(parsed_json['history']['dailysummary']) == 1):
                    if ('meantempi' in parsed_json['history']['dailysummary'][0]):
                        temp = parsed_json['history']['dailysummary'][0]['meantempi']
                        newYork.set_value(index, 'temp', temp)
        counter += 1
    else:
        time.sleep(60)
        counter = 0

