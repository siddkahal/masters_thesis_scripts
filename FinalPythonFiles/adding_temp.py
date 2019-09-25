from multiprocessing import Process
import netCDF4 as nc
import numpy as np
import pandas as pd
import sys
import json
import time
import math
import os.path
import matplotlib.pyplot as plt
from urllib.request import urlopen
from math import sin, cos, sqrt, atan2, radians

# MAIN METHOD
if __name__ == '__main__':

	# Change to correct filename 
	bf_df = pd.read_csv('data_500_cities_4.csv')

	counter = 0
	
	# Make sure the license number is correct
	str1 = 'http://api.wunderground.com/api/dfc34b8cb79bd3e7/history_'
	
	bf_df['temp_mean_F'] = np.nan
	bf_df['temp_max_F'] = np.nan
	bf_df['temp_min_F'] = np.nan
	bf_df['wspeed_mph'] = np.nan
	bf_df['percip_inches'] = np.nan


	for index,row in bf_df.iterrows():
		# Making only 10 api calls per minute

		# 10 sec over 1 minute (just for buffer, really only requires 1 minute)
		if (counter >= 1000):
			time.sleep(70)
			counter = 0


		date = row['Year']
		date *= 100
		date += row['Month']
		date *= 100
		date += row['Day']
		date_str = str(date)

		str2 = '/q/' + row['StatProv'] + '/' + row['city'] + '.json'

		# get the json file that conatins the weather data for that day
		api_link = str1 + date_str + str2
		f = urlopen(api_link)
		json_string = f.read()
		parsed_json = json.loads(json_string)

		# getting temp_f (temperature in F)
		if ('history' in parsed_json):
			if ('dailysummary' in parsed_json['history']):
				if (len(parsed_json['history']['dailysummary']) == 1):
					if ('meantempi' in parsed_json['history']['dailysummary'][0]):
						temp = parsed_json['history']['dailysummary'][0]['meantempi']
						bf_df.loc[index,'temp_mean_F'] = temp

					if ('maxtempi' in parsed_json['history']['dailysummary'][0]):
						temp_max = parsed_json['history']['dailysummary'][0]['maxtempi']
						bf_df.loc[index,'temp_max_F'] = temp_max

					if ('mintempi' in parsed_json['history']['dailysummary'][0]):
						temp_min = parsed_json['history']['dailysummary'][0]['mintempi']
						bf_df.loc[index,'temp_min_F'] = temp_min

					if ('meanwindspdi' in parsed_json['history']['dailysummary'][0]):
						wspeed = parsed_json['history']['dailysummary'][0]['meanwindspdi']
						bf_df.loc[index,'wspeed_mph'] = wspeed

					if ('precipi' in parsed_json['history']['dailysummary'][0]):
						percip = parsed_json['history']['dailysummary'][0]['precipi']
						bf_df.loc[index,'percip_inches'] = percip 

			counter += 1
			

	# Outputing the final csv with temperatures
	# Make sure the title is correct (change #)
	bf_df.to_csv('data_500_4.csv', sep=',')

	





