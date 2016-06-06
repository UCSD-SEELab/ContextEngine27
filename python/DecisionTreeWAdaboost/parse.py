# Wanlin Cui

#parse by time
from numpy import recfromcsv
import matplotlib.pyplot as plt
from knn import Knn
from svr import SVR
from dtAB import DecisionTreeAB
import numpy as np

import time
import math

start_time = time.time()

#csv = recfromcsv('adj_clotheswasher1.csv', delimiter=',')
#csv = recfromcsv('adj_dishwasher1.csv', delimiter=',')
#csv = recfromcsv('adj_dryer1.csv', delimiter=',')
#csv = recfromcsv('adj_furnace1.csv', delimiter=',')
#csv = recfromcsv('adj_microwave1.csv', delimiter=',')
#csv = recfromcsv('adj_oven1.csv', delimiter=',')
csv = recfromcsv('adj_refrigerator1.csv', delimiter=',')
#csv = recfromcsv('adj_use.csv', delimiter=',')

#c = open('adj_clotheswasher1.csv', 'r')
#c = open('adj_dishwasher1.csv', 'r')
#c = open('adj_dryer1.csv', 'r')
#c = open('adj_furnace1.csv', 'r')
#c = open('adj_microwave1.csv', 'r')
#c = open('adj_oven1.csv', 'r')
#c = open('adj_refrigerator1.csv', 'r')
c = open('adj_use.csv', 'r')

#trainer = Knn(complexity=0, numInputs=1, discreteOutputs=0, discreteInputs=0);
#trainer = SVR(complexity=0, numInputs=1, discreteOutputs=0, discreteInputs=0);
trainer = DecisionTreeAB(complexity=0, numInputs=1, discreteOutputs=0, discreteInputs=0);

x_train = [];
y_train = [];
x_predict = [];
x_real = [];
y_real = [];

numRow = 96
day_train_start = 0
day_train_end = 2
day_predict = 8

variance = 0
sum = 0

for i in range(numRow*day_train_start,numRow*(day_train_end+1)):
	row = csv[i]
	date = row[0]
	energy = row[1]

	date = date.replace("/"," ")
	date = date.replace(":"," ")
	#print date;

	t = time.strptime(date, "%d %m %Y %H %M %S")
	weekday = t[6]; #range [0, 6], Monday is 0
	#print weekday
	hour = t[3]
	minute = t[4]
	sec = t[5]
	tv = (t[3]*3600+t[4]*60+t[5])/(24*3600.0)
	x_obs = [tv]
	x_train.append(x_obs)
	y_obs = energy
	y_train.append(y_obs)
 	trainer.addSingleObservation(x_obs, y_obs);

trainer.train();

for i in range(numRow*day_predict,numRow*(day_predict+1)):
	row = csv[i]
	date = row[0]
	energy = row[1]

	date = date.replace("/"," ")
	date = date.replace(":"," ")
	t = time.strptime(date, "%d %m %Y %H %M %S")
	weekday = t[6]; #range [0, 6], Monday is 0
	hour = t[3]
	minute = t[4]
	sec = t[5]
	tv = (t[3]*3600+t[4]*60+t[5])/(24*3600.0)
	x_real.append([tv])
	y_real.append(energy)

T=np.linspace(0,1,96)
y_predict = np.empty([0])

for num in T:
	x_predict = [num]
	result = trainer.execute(x_predict)
	y_predict = np.concatenate((y_predict,result))

for i in range(len(y_real)):
	a = math.fabs((y_real[i].astype(float)) - (y_predict[i].astype(float)))
	sum = sum + a*a

average = sum / len(y_real)
variance = math.sqrt(average)
print("--- %s variance ---" % (variance))

plt.subplot(1, 1, 1)
plt.scatter(x_real, y_real, c='r', label='data')
plt.plot(T, y_predict, c='g', label='prediction')
plt.axis('tight')
plt.legend()
plt.title(c.name)
c.close()

print("--- %s seconds ---" % (time.time() - start_time))

plt.show()
