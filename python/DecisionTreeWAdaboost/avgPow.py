# Wanlin Cui

#average power at time of a day per year
from numpy import recfromcsv
import matplotlib.pyplot as plt
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
#csv = recfromcsv('adj_refrigerator1.csv', delimiter=',')
csv = recfromcsv('adj_use.csv', delimiter=',')

#c = open('adj_clotheswasher1.csv', 'r')
#c = open('adj_dishwasher1.csv', 'r')
#c = open('adj_dryer1.csv', 'r')
#c = open('adj_furnace1.csv', 'r')
#c = open('adj_microwave1.csv', 'r')
#c = open('adj_oven1.csv', 'r')
#c = open('adj_refrigerator1.csv', 'r')
c = open('adj_use.csv', 'r')

#trainer = Knn(complexity=0, numInputs=1, discreteOutputs=0, discreteInputs=0)
#trainer = SVR(complexity=0, numInputs=1, discreteOutputs=0, discreteInputs=0)
trainer = DecisionTreeAB(complexity=0, numInputs=1, discreteOutputs=0, discreteInputs=0)

x_train = []
y_train = []
x_predict = []
x_real=[]
y_real=[]

totRow = 35040
index = 96
day_train_start = 0
day_train_end = 3
day_predict = 4

preSum = 0
variance = 0
sum = 0

for i in range(index):
    j = i
    #for the day before May 9 (we miss May 9, 2:00am-2:45am's data)
    while j < totRow:
        row = csv[j]
        date = row[0]
        power = row[1]

        date = date.replace("/"," ")
        date = date.replace(":"," ")

        t = time.strptime(date, "%d %m %Y %H %M %S")
        weekday = t[6]
        hour = t[3]
        minute = t[4]
        sec = t[5]
        tv = (t[3]*3600+t[4]*60+t[5])/(24*3600.0)
        preSum = preSum + power

        j = j + index

    avg = preSum / 365
    x_obs = [tv]
    y_obs = avg
    x_train.append(x_obs)
    y_train.append(y_obs)
    trainer.addSingleObservation(x_obs, y_obs)
    preSum = 0

trainer.train();

for i in range(index):
    row = csv[i]
    date = row[0]
    power = row[1]

    date = date.replace("/"," ")
    date = date.replace(":"," ")
    t = time.strptime(date, "%d %m %Y %H %M %S")
    weekday = t[6]; #range [0, 6], Monday is 0
    hour = t[3]
    minute = t[4]
    sec = t[5]
    tv = (t[3]*3600+t[4]*60+t[5])/(24*3600.0)
    x_real.append([tv])
    y_real.append(power)

length = len(y_real)

T = np.linspace(0,1,96)
y_predict = np.empty([0])

for num in T:
	x_predict = [num]
	result = trainer.execute(x_predict)
	y_predict = np.concatenate((y_predict,result))

for i in range(len(y_real)):
    a = math.fabs((y_real[i]).astype(float) - (y_predict[i]).astype(float))
    sum = sum + a*a

average = sum / length
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
