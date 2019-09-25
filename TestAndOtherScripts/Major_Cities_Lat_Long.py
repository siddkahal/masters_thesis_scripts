
# coding: utf-8

# In[101]:


import netCDF4 as nc
import numpy as np
import pandas as pd
import sys


# In[102]:


us_cities = pd.read_csv('uscitiesv1.3.csv')


# In[103]:


major_cities = pd.read_csv('topCities.csv')


# In[104]:


major_cities.head()


# In[105]:


us_cities.head()


# In[106]:


print(us_cities.loc[((us_cities['state_name'] == 'North Dakota') & (us_cities['city'] == 'Dunseith'))].lat)


# In[107]:


major_cities['lat'] = np.nan
major_cities['long'] = np.nan
for index,row in major_cities.iterrows():
    for i,r in us_cities.iterrows():
        if ((r['state_name'] == row['State']) & (r['city'] == row['City'])):
            lat = r['lat']
            long = r['lng']
            major_cities.set_value(index, 'lat', lat)
            major_cities.set_value(index, 'long', long)
            break


# In[108]:


top_cities = major_cities.copy()


# In[109]:


top_cities.head()


# In[80]:


#for index,row in major_cities.iterrows():
    #city_name = row['City'].replace(" ", "_")
    #major_cities.set_value(index, 'City', city_name)


# In[110]:


major_cities.tail()


# In[111]:


major_cities.to_csv('majorCities.csv', sep=',')


# In[112]:


top_cities.dropna(subset=['lat'], inplace=True)


# In[115]:


top_cities.size


# In[118]:


top_cities.to_csv('topCities.csv', sep=',')


# In[119]:


states_abbv = pd.read_csv('states.csv')


# In[120]:


states_abbv.head()


# In[122]:


top_cities['state_abbrv'] = ""

for index,row in top_cities.iterrows():
    for i,r in states_abbv.iterrows():
        if (r['State'] == row['State']):
            abbrev = r['Abbreviation']
            top_cities.set_value(index, 'state_abbrv', abbrev)
            break


# In[123]:


top_cities.head()


# In[124]:


top_cities.tail()


# In[125]:


for index,row in top_cities.iterrows():
    city_name = row['City'].replace(" ", "_")
    top_cities.set_value(index, 'City', city_name)


# In[126]:


top_cities.tail()


# In[127]:


top_cities.to_csv('topCities.csv', sep=',')


# In[129]:


class city:
    def __init__(self, lat, long, name):
        self.lat = lat
        self.long = long
        self.name = name
            
x = city(4,5,'sidd_city')
        

            


# In[131]:


city_list = []
city_list.append(x)


# In[136]:


city_list[0].name
city_list[0].lat
#city_list[0].long

