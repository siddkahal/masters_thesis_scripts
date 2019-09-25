
# coding: utf-8

# In[26]:


import netCDF4 as nc
import numpy as np
import pandas as pd
import sys
import json
import time
import matplotlib.pyplot as plt
from urllib.request import urlopen
from math import sin, cos, sqrt, atan2, radians


# In[16]:


major_cities = pd.read_csv('topCities.csv')
birdfeeder_df = pd.read_csv('PFW2011-12_Subset.csv')


# In[3]:


major_cities.head()


# In[44]:


statesConv = {
    'AL':'"AL"',
    'AK':'"AK"',
    'AZ':'"AZ"',
    'AR':'"AR"',
    'CA':'"CA"',
    'CO':'"CO"',
    'CT':'"CT"',
    'DE':'"DE"',
    'FL':'"FL"',
    'GA':'"GA"',
    'HI':'"HI"',
    'ID':'"ID"',
    'IL':'"IL"',
    'IN':'"IN"',
    'IA':'"IA"',
    'KS':'"KS"',
    'KY':'"KY"',
    'LA':'"LA"',
    'ME':'"ME"',
    'MD':'"MD"',
    'MA':'"MA"',
    'MI':'"MI"',
    'MN':'"MN"',
    'MS':'"MS"',
    'MO':'"MO"',
    'MT':'"MT"',
    'NE':'"NE"',
    'NV':'"NV"',
    'NH':'"NH"',
    'NJ':'"NJ"',
    'NM':'"NM"',
    'NY':'"NY"',
    'NC':'"NC"',
    'ND':'"ND"',
    'OH':'"OH"',
    'OK':'"OK"',
    'OR':'"OR"',
    'PA':'"PA"',
    'RI':'"RI"',
    'SC':'"SC"',
    'SD':'"SD"',
    'TN':'"TN"',
    'TX':'"TX"',
    'UT':'"UT"',
    'VT':'"VT"',
    'VA':'"VA"',
    'WA':'"WA"',
    'WV':'"WV"',
    'WI':'"WI"',
    'WY':'"WY"',
    'DC':'"DC"'
}


done = []
state_dfs = []

for index,row in major_cities.iterrows():
    curr_state = row['state_abbrv']
    if curr_state not in done:
        done.append(curr_state)
        state = statesConv[curr_state]
        string = 'StatProv==' + state
        state_subset = birdfeeder_df.query(string).copy()
        state_dfs.append(state_subset)
        #if not state_subset.empty:
            #csv_title = 'PFW2011-12_' + curr_state + '.csv'
            #state_subset.to_csv(csv_title, sep=',')



# In[45]:


class city:
    def __init__(self, lat, long, name):
        self.lat = lat
        self.long = long
        self.name = name

               
states_dict = {}

for index,row in major_cities.iterrows():
    x = city(row['lat'], row['long'], row['City'])
    if (row['state_abbrv'] in states_dict):
        states_dict[row['state_abbrv']].append(x)
    else :
        states_dict[row['state_abbrv']] = []
        states_dict[row['state_abbrv']].append(x)


# In[52]:


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

def processRow(lat, long, cities):
    distance = sys.maxsize
    city = ''
    for c in cities:
        temp = calcDistance(lat, long, c.lat, c.long)
        
        if (temp < distance):
            city = c.name
            distance = temp
    
    if (distance <= 40):
        return city
    else:
        return ''
        

s_df = state_dfs[1]


        
    


# In[53]:


s_df['city'] = ''

for index,row in s_df.iterrows():
    lat = row['LATITUDE']
    long = row['LONGITUDE']
    cities = states_dict[row['StatProv']]
    city = processRow(lat, long, cities)
    s_df.set_value(index, 'city', city)



# In[54]:


s_df.head()


# In[55]:


for i,r in s_df.iterrows():
    if(r['city'] == ''):
        s_df.drop(i, inplace=True)


# In[57]:


s_df.tail()

