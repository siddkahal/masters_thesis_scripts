from multiprocessing import Process
import netCDF4 as nc
import numpy as np
import pandas as pd
import sys
import json
import time
import matplotlib.pyplot as plt
from urllib.request import urlopen
from math import sin, cos, sqrt, atan2, radians

# CLASS FOR ORGANIZING THE TOP CITIES
class city:
    def __init__(self, lat, lon, name):
        self.lat = lat
        self.lon = lon
        self.name = name

# CALCULATING THE DISTANCE GIVEN 2 LAT LONG POINTS
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

# ATTACH A CITY TO THE ROW IF POSSIBLE
def processRow(lat, lon, cities):
    distance = sys.maxsize
    city = ''
    for c in cities:
        temp = calcDistance(lat, lon, c.lat, c.lon)
        
        # find the closes city
        if (temp < distance):
            city = c.name
            distance = temp
    
    # IF THE POINT IS WITHIN 40KM OF CITY
    if (distance <= 40):
        return city
    else:
        return ''


# FIND ALL ROWS CLOSE TO A MAJOR CITY IN THE STATE
def processState(s, states_dict):
	curr_state = ''
	s['city'] = ''
	# FOR EACH ROW FIND A CITY IF POSSIBLE
	for index,row in s.iterrows():
		curr_state = row['StatProv']
		lat = row['LATITUDE']
		lon = row['LONGITUDE']
		cities = states_dict[row['StatProv']]
		city = processRow(lat, lon, cities)
		s.set_value(index, 'city', city)

	# DELETING ROWS WITH NO CITY
	for i,r in s.iterrows():
		if(r['city'] == ''):
			s.drop(i, inplace=True)

	if (curr_state != ''):
		file_name = curr_state + '.csv'
		# create the csv for state with the city added
		s.to_csv(file_name, sep=',')

	
# MAIN METHOD
if __name__ == '__main__':
	states_dict = {}

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

	major_cities = pd.read_csv('topCities.csv')
	
	# Change name of file
	# birdfeeder_df = pd.read_csv('PFW2011-12_Subset.csv')

	done = []
	state_dfs = []

	# ORGANIZING BIRDFEEDER DATA BY STATE

	for index,row in major_cities.iterrows():
	    curr_state = row['state_abbrv']
	    if curr_state not in done:
	        done.append(curr_state)
	        state = statesConv[curr_state]
	        string = 'StatProv==' + state
	        state_subset = birdfeeder_df.query(string).copy()
	        state_dfs.append(state_subset)
	        
	        # UNCOMMENT THE CODE BELOW IF YOU WANT STATE SPECIFIC CSV's of the PFW data

			# if not state_subset.empty:
			# 	csv_title = 'PFW2011-12_' + curr_state + '.csv'
			# 	state_subset.to_csv(csv_title, sep=',')

	              
	# CREATING A HASHMAP (STATE : CITES LIST)

	for index,row in major_cities.iterrows():
		x = city(row['lat'], row['long'], row['City'])
		if (row['state_abbrv'] in states_dict):
			states_dict[row['state_abbrv']].append(x)
		else :
			states_dict[row['state_abbrv']] = []
			states_dict[row['state_abbrv']].append(x)

	# MAIN LOOP FOR GOING THROUGH ALL OF THE STATES
	# Parallel processes
	i = 0
	while i < len(state_dfs):
		s1 = state_dfs[i]
		i += 1

		p1 = Process(target=processState, args=(s1,states_dict))
		p1.start()




	
































