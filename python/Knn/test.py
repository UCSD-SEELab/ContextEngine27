import numpy as np
import matplotlib.pyplot as plt
from sklearn import neighbors

np.random.seed(0)
X = np.sort(5 * np.random.rand(40, 1), axis=0)
T = np.linspace(0, 5, 500)[:, np.newaxis]
y = np.sin(X).ravel()

# Add noise to targets
y[::5] += 1 * (0.5 - np.random.rand(8))

###############################################################################
# Fit regression model
n_neighbors = 5


knn = neighbors.KNeighborsRegressor(n_neighbors);
x_ = np.array([[2.3],[3.4]]);
x_.reshape(2,1);
y_ = knn.fit(X, y).predict(x_);
print(y_);
print(y_.shape);
