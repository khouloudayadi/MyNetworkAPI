import importlib
import xgboost
import pickle
import pandas as pd
global scaler_x

prepareData = importlib.import_module('prepareData')

X_train, y_train, scaler_x = prepareData.prepare_train_test()
def XGB_model(X_train,  y_train):
    xgb_model = xgboost.XGBRegressor(n_estimators=100,
                                     learning_rate=0.1,
                                     subsample=0.9,
                                     # pourcentage d'échantillons utilisés par arbre. Une valeur faible peut entraîner un sous-ajustement.
                                     colsample_bytree=1,
                                     # pourcentage d'entités utilisées par arborescence. Une valeur élevée peut entraîner un sur-ajustement
                                     n_jobs=-1,
                                     max_depth=18,
                                     objective="reg:squarederror")
    xgb_results = xgb_model.fit(X_train, y_train, verbose=True)
    return xgb_results
xgb_results = XGB_model(X_train, y_train)

pickle.dump(xgb_results, open('model.pkl', 'wb'))
print("Model dumped!")
