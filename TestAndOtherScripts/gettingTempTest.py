from multiprocessing import Process
import netCDF4 as nc
import numpy as np
import pandas as pd
import sys
import json
import time
import os.path
import matplotlib.pyplot as plt
from urllib.request import urlopen
from math import sin, cos, sqrt, atan2, radians

# MAIN METHOD
if __name__ == '__main__':

	# Still need to test the below code

	bf_df = pd.read_csv('PFW2011-12_Subset_cities.csv')

	counter1 = 0
	counter2 = 0
	str1 = 'http://api.wunderground.com/api/f12eaf4e009a36bb/history_'
	
	bf_df['temp'] = np.nan

	for index,row in bf_df.iterrows():
		if (counter1 < 500):
			if (counter2 < 10):
				date = row['Year']
				date *= 100
				date += row['Month']
				date *= 100
				date += row['Day']
				date_str = str(date)

				str2 = '/q/' + row['StatProv'] + '/' + row['city'] + '.json'

				# get the json file that conatins the temperature for the link
				api_link = str1 + date_str + str2
				f = urlopen(api_link)
				json_string = f.read()
				parsed_json = json.loads(json_string)

				# checking to make sure the returned json has the correct data
				if ('history' in parsed_json):
				    if ('dailysummary' in parsed_json['history']):
						if (len(parsed_json['history']['dailysummary']) == 1):
							if ('meantempi' in parsed_json['history']['dailysummary'][0]):
								temp = parsed_json['history']['dailysummary'][0]['meantempi']
								bf_df.set_value(index, 'temp', temp)
				counter2 += 1
				counter1 += 1
			else:
				time.sleep(60)
				counter2 = 0
		else:
			time.sleep(86400)
			counter1 = 0


	





