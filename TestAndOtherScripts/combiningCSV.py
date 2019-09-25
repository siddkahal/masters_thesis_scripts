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
	major_cities = pd.read_csv('topCities.csv')

	done = []
	dfs = []

	for index,row in major_cities.iterrows():
		curr_state = row['state_abbrv']
		#print(curr_state)
		if curr_state not in done:
			done.append(curr_state)
			csv_name = curr_state + '.csv'
			
			if os.path.exists(csv_name):
				temp = pd.read_csv(csv_name)
				dfs.append(temp)

	result = pd.concat(dfs)

	# Change the name properly 
	#result.to_csv('PFW2011-12_Subset_cities.csv', sep=',')
