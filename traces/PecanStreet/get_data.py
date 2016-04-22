import numpy as np
import psycopg2
import matplotlib.pyplot as plt
import matplotlib.dates as md
from pylab import *
import datetime
import os

try:
    conn = psycopg2.connect(database='postgres', user='5e2NFTWJxmxc', host='dataport.pecanstreet.org', password='JHKvbd5kYSob', port='5434')
except:
    print "I am unable to connect to the database"

cur = conn.cursor()

f = open("pecan_st_distinct_houses.txt", "r")
home_ids = f.read().split()
f.close()
print "Number of distcint houses: ",len(home_ids)

# appliance_list = ['dishwasher1', 'clotheswasher1', 'drye1', 'oven1', 'microwave1', 'refrigerator1', 'furnace1', 'bathroom1', 'bedroom1', 'diningroom1', 'car1', 'heater1', 'livingroom1', 'poolpump1']
appliance_list = ['use']

number_of_houses_analyzed = 0
house_start_point = 0
number_of_houses_analysis_limit = 0
number_data_found = 0

for home_id in home_ids:

	if number_of_houses_analyzed < house_start_point:
		number_of_houses_analyzed = number_of_houses_analyzed + 1
		continue

	home_id = int(home_id)

	if number_of_houses_analysis_limit > 0:
		if number_of_houses_analyzed == number_of_houses_analysis_limit:
			break

	directory = str(home_id)

	for appliance in appliance_list:

		print "%d.\t Getting data ... House id: %d Appliance: %s" % (number_of_houses_analyzed+1, home_id, appliance)

		cur.execute("""SELECT local_15min, """ + appliance + """ FROM university.electricity_egauge_15min WHERE dataid=""" + str(home_id) + """ AND local_15min BETWEEN '01-01-2014' AND '01-01-2015'""")
		rows = cur.fetchall()

		if rows == []:
			continue


		if rows[0][1] == None:
			continue 

		results_file_name = directory + "/" + str(home_id) + "_power_values_" + appliance + ".csv"

		f = open(results_file_name, "w")
		for row in rows:
			t = row[0].strftime("%d/%m/%Y %H:%M:%S")
			p = row[1]
			if p == None:
				p = 0.0
			else:
				p = float(p)
			f.write(t + "," + str(p) + "\n")
		f.close()
		number_data_found = number_data_found + 1

	number_of_houses_analyzed = number_of_houses_analyzed + 1
print number_data_found
