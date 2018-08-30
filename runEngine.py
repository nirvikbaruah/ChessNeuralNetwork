import pandas as pd  
import numpy as np  
import tensorflow as tf  
from sklearn.metrics import explained_variance_score, mean_absolute_error, median_absolute_error
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import itertools


df = pd.read_csv('positions.csv', engine = "python").set_index('Count')

#Convert data to float
df.apply(pd.to_numeric)

X = df[[col for col in df.columns if col != '66']]
y = df['66']  


inputList = [0,0,0,0,-1000,0,0,0,0,0,-30,0,0,0,-10,0,0,0,0,0,0,0,0,1000,0,0,35,0,0,10,0,0,0,-10,0,0,0,0,0,0,0,0,0,10,10,0,30,0,0,0,0,0,100,0,0,0,-50,0,0,0,0,-35,0,-100,1]

feature_cols = [tf.feature_column.numeric_column(col) for col in X.columns]  

X_test = pd.DataFrame(np.array([i for i in inputList]).reshape(1,65), columns = [i for i in X])

regressor = tf.estimator.DNNRegressor(feature_columns=feature_cols,  
                                      hidden_units=[65, 65], 
                                      model_dir = "/Users/nirvikbaruah/Desktop/NeuralChess-master/model")


def wx_input_fn(X, y=None, num_epochs=None, shuffle=True, batch_size=1):  
    return tf.estimator.inputs.pandas_input_fn(x=X,
                                               y=y,
                                               num_epochs=num_epochs,
                                               shuffle=shuffle,
                                               batch_size=batch_size)


predict = regressor.predict(input_fn=wx_input_fn(X_test))

predictions = list(p["predictions"] for p in itertools.islice(predict, 1))
print predictions
print("Prediction: {}".format(str(predictions[0][0])))

