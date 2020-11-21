import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.svm import OneClassSVM
from sklearn.model_selection import train_test_split

def prepare_train_test():
        df = pd.read_csv("NewDatasetSelection.csv")
        target = 'temps'
        # Define the x and y data
        X = np.array(df.drop(target, axis=1))
        y = np.array(df[target])
        # splitting training and testing data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, shuffle=True, random_state=100)
        #transform data
        scaler_x = preprocessing.RobustScaler().fit(X_train)
        X_train =scaler_x.transform(X_train)
        X_test =scaler_x.transform(X_test)
        # identify outliers in the training dataset
        ee = OneClassSVM(nu=0.1)
        yhat = ee.fit_predict(X_train)
        # select all rows that are not outliers
        mask = yhat != -1
        X_train, y_train = X_train[mask, :], y_train[mask]
        return (X_train, y_train, scaler_x)
