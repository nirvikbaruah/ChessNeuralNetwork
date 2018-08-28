import pandas as pd  
import numpy as np  
import tensorflow as tf  
from sklearn.metrics import explained_variance_score, mean_absolute_error, median_absolute_error
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt  

df = pd.read_csv('positions.csv', engine = "python").set_index('Count')

#Convert data to float
df.apply(pd.to_numeric)

X = df[[col for col in df.columns if col != '66']]

# y will be a pandas series of the output
y = df['66']  


#split dataset
X_train, X_tmp, y_train, y_tmp = train_test_split(X, y, test_size=0.2, random_state=23)  

# take the remaining 20% of data in X_tmp, y_tmp and split them evenly
X_test, X_val, y_test, y_val = train_test_split(X_tmp, y_tmp, test_size=0.5, random_state=23)

feature_cols = [tf.feature_column.numeric_column(col) for col in X.columns]  

regressor = tf.estimator.DNNRegressor(feature_columns=feature_cols,  
                                      hidden_units=[65, 65], 
                                      model_dir = "/Users/nirvikbaruah/Desktop/NeuralChess-master/model")

def wx_input_fn(X, y=None, num_epochs=None, shuffle=True, batch_size=1):  
    return tf.estimator.inputs.pandas_input_fn(x=X,
                                               y=y,
                                               num_epochs=num_epochs,
                                               shuffle=shuffle,
                                               batch_size=batch_size)

evaluations = []  
for i in range(50):  
    regressor.train(input_fn=wx_input_fn(X_train, y=y_train), steps=100)
    evaluations.append(regressor.evaluate(input_fn=wx_input_fn(X_val,
                                                               y_val,
                                                               num_epochs=1,
                                                               shuffle=False)))


#Plot graph to visualise
plt.rcParams['figure.figsize'] = [14, 10]
loss_values = [ev['average_loss'] for ev in evaluations]  
training_steps = [ev['global_step'] for ev in evaluations]

plt.scatter(x=training_steps, y=loss_values)  
plt.xlabel('Epochs')  
plt.ylabel('Average Loss (MSE)')  
plt.show()  
