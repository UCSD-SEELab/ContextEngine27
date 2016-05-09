from numpy import recfromcsv
from time import strptime
import matplotlib.pyplot as plt 
from Knn import Knn
import numpy as np

csv = recfromcsv('all.csv', delimiter=',')

trainer = Knn(complexity=0, numInputs=7, discreteOutputs=0, discreteInputs=0);
x_train = [];
y_train = [];
x_predict = [];
y_predict = np.empty([0]);
x_real=[];
y_real=[];

numRow = 96
day_train_start=0
day_train_end=10
day_predict=17
#read in csv and parse data to trainer
#use the first 4 weeks data as training set
for i in range(numRow*day_train_start,numRow*(day_train_end+1)):
#for row in csv:
#date = csv[0][0]
#energy = csv[0][1]
	row = csv[i]
	date=row[0]
	dishwasher=csv[i+1][3]

	date=date.replace("/"," ")
	date=date.replace(":"," ")
	#print date;
#time.struct_time(tm_year=2014, tm_mon=1, tm_mday=1, tm_hour=0, tm_min=15, tm_sec=0, 
#tm_wday=2, tm_yday=1, tm_isdst=-1)
#https://docs.python.org/2/library/time.html
	t=strptime(date, "%m %d %Y %H %M")
	weekday = t[6]; #range [0, 6], Monday is 0
	#print weekday
	hour=t[3]
	minute=t[4]
	sec=t[5]
	time = (t[3]*3600+t[4]*60+t[5])/(24*3600.0)
	x_obs = [time, row[2], row[4], row[5], row[6], row[7], row[8]]
	x_train.append(x_obs)
	y_obs = dishwasher
	y_train.append(y_obs)
 	trainer.addSingleObservation(x_obs, y_obs);

trainer.train();

for i in range(numRow*day_predict,numRow*(day_predict+1)):
	row = csv[i]
	date=row[0]
	date_predict = csv[i+1][0]
	dishwasher=csv[i+1][3]
	date=date.replace("/"," ")
	date=date.replace(":"," ")
	date_predict=date_predict.replace("/"," ")
	date_predict=date_predict.replace(":"," ")
	t=strptime(date, "%m %d %Y %H %M")
	t_predict = strptime(date_predict, "%m %d %Y %H %M")
	weekday = t[6]; #range [0, 6], Monday is 0
	hour=t[3]
	minute=t[4]
	sec=t[5]
	time = (t[3]*3600+t[4]*60+t[5])/(24*3600.0)
	time_predict = (t_predict[3]*3600+t_predict[4]*60+t_predict[5])/(24*3600.0)
	x_predict=[time_predict, row[2], row[4], row[5], row[6], row[7], row[8]];
	result = trainer.execute(x_predict);
	y_predict = np.concatenate((y_predict,result));
	x_real.append([time_predict])
	y_real.append(dishwasher)


plt.subplot(1, 1, 1)
plt.scatter(x_real, y_real, c='r', label='data')
plt.scatter(x_real, y_predict, c='g', label='prediction')
plt.axis('tight')
plt.legend()
plt.title("KNeighborsRegressor (k = %i, weights = '%s')" % (2,
	"uniform"))

plt.show()
