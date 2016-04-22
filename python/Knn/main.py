import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
from Knn import Knn

np.random.seed(0)
X = np.sort(5 * np.random.rand(40, 1), axis=0)
T = np.linspace(0, 5, 500)[:, np.newaxis]
y = np.sin(X).ravel();

# Add noise to targets
y[::5] += 1 * (0.5 - np.random.rand(8))
#y = y.ravel();

###############################################################################
# Fit regression model
trainer = Knn(complexity=0, numInputs=1, discreteOutputs=0, discreteInputs=0);
trainer.addBatchObservations(X,y);
trainer.train();


y_predict = np.empty([0]);

for i in range(T.shape[0]):
	result = trainer.execute(T[i]);
	y_predict = np.concatenate((y_predict,result));

plt.subplot(1, 1, 1)
plt.scatter(X, y, c='k', label='data')
plt.plot(T, y_predict, c='g', label='prediction')
plt.axis('tight')
plt.legend()
plt.title("KNeighborsRegressor (k = %i, weights = '%s')" % (2,
	"uniform"))

plt.show()