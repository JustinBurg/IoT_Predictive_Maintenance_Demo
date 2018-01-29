'''
Batch IoT Sensor Forecasting using TensorFlow and RNN
Author:  Justin Brandenburg, Data Scientist
Email:   jbrandenburg@mapr.com

Requirements: Python 3.5 and TensorFlow 1.X
If these are not installed, this demo will not run

To install TF:
[user01@maprdemo ]$ conda install keras
[user01@maprdemo ]$ conda install tensorflow

This assumes that the XML files have been transformed into a csv file using Sensor_ETLsparksubmit.py

This script is best demo'd in a jupyter notebook to show the data exploration, feature transformation, model training and
testing on historical data that is in MapR-FS.  

create a folder that will capture our saved TF model
[user01@maprdemo ]$ mkdir rwTFmodel

Start jupyter notebook and acces it via your browser at 127.0.0.1:9999
[user01@maprdemo ]$ jupyter notebook

'''

import os
import pandas as pd
import csv
import numpy as np
import random
import glob
import matplotlib
import matplotlib.pyplot as plt
import random
get_ipython().magic('matplotlib inline')

#import the data from MapR-FS, super easy
df = pd.read_csv("/user/user01/rw_etl.csv/part-00000-45866095-f76d-4f6c-ba2d-a07f0ab2dc04.csv").sort_values(['TimeStamp'], ascending=True).reset_index()
df.drop(['::[scararobot]Ax_J1.PositionCommand','::[scararobot]Ax_J1.TorqueFeedback','::[scararobot]Ax_J2.PositionCommand','::[scararobot]Ax_J2.TorqueFeedback','::[scararobot]Ax_J3.TorqueFeedback','::[scararobot]Ax_J6.TorqueFeedback','::[scararobot]ScanTimeAverage','::[scararobot]Ax_J6.PositionCommand','::[scararobot]Ax_J3.PositionCommand','index'], axis=1, inplace=True)
df['TimeStamp']=pd.to_datetime(df['TimeStamp'])
df.head(5)

#plot some of the columns to get an idea of the trends over time
df.plot(x="TimeStamp", y="::[scararobot]Ax_J1.ActualPosition", kind="line")
df.plot(x="TimeStamp", y=["::[scararobot]Ax_J1.ActualPosition","::[scararobot]Ax_J3.TorqueCommand"], kind="line")
df.plot(x="TimeStamp", y=["::[scararobot]CS_Cartesian.ActualPosition[0]","::[scararobot]CS_Cartesian.ActualPosition[1]"], kind="line")

#remove rows that are all zeros
df1 = df[df["::[scararobot]speed"] != 0].set_index('TimeStamp')   
print (len(df1))

#create a new column that will be our feature variable for our model
#df1['total']=df1.sum(axis=1)
df1['Total']= df1.select_dtypes(include=['float64','float32']).apply(lambda row: np.sum(row),axis=1)

#convert into a time series object
ts = pd.Series(df1['Total'])
ts.plot(c='b', title='RW Total Sensor Aggregation')

#prepare data and inputs for our TF model
num_periods = 100
f_horizon = 1       #number of periods into the future we are forecasting
TS = np.array(ts)   #convert time series object to an array
print (TS[0:10])
print (len(TS))

#create our training input data set "X"
x_data = TS[:(len(TS)-(len(TS) % num_periods))]
print (x_data[0:5])
x_batches = x_data.reshape(-1, num_periods, 1)
print (len(x_batches))
print (x_batches.shape)
#print (x_batches[0:3])

#create our training output dataset "y"
y_data = TS[1:(len(TS)-(len(TS) % num_periods))+f_horizon]
#print (y_data)
#print (len(y_data))
#y_data = TS[(num_periods+(f_horizon-1))::(num_periods)]
print (y_data)
print (len(y_data))
y_batches = y_data.reshape(-1, num_periods, 1)
print (len(y_batches))

#create our test X and y data
def test_data(series,forecast,num_periods):
    test_x_setup = series[-(num_periods + forecast):]
    testX = test_x_setup[:num_periods].reshape(-1, num_periods, 1)
    testY = TS[-(num_periods):].reshape(-1, num_periods, 1)
    return testX,testY

X_test, Y_test = test_data(TS,f_horizon,num_periods)
print (X_test.shape)
print (X_test[:,(num_periods-1):num_periods])
print (Y_test.shape)
print (Y_test[:,(num_periods-1):num_periods])

#import tensorflow libraries
import tensorflow as tf
import shutil
import tensorflow.contrib.learn as tflearn
import tensorflow.contrib.layers as tflayers
from tensorflow.contrib.learn.python.learn import learn_runner
import tensorflow.contrib.metrics as metrics
import tensorflow.contrib.rnn as rnn

#set up our TF model parameters

tf.reset_default_graph()   #We didn't have any previous graph objects running, but this would reset the graphs

inputs = 1            #number of vectors submitted
hidden = 100          #number of neurons we will recursively work through, can be changed to improve accuracy
output = 1            #number of output vectors

X = tf.placeholder(tf.float32, [None, num_periods, inputs], name = "X")   #create variable objects
y = tf.placeholder(tf.float32, [None, num_periods, output], name = "y")


basic_cell = tf.contrib.rnn.BasicRNNCell(num_units=hidden, activation=tf.nn.relu)   #create our RNN object
rnn_output, states = tf.nn.dynamic_rnn(basic_cell, X, dtype=tf.float32)               #choose dynamic over static

learning_rate = 0.001   #small learning rate so we don't overshoot the minimum
#tf.app.flags.DEFINE_float('learning_rate', 0.001, 'Initial learning rate.')

stacked_rnn_output = tf.reshape(rnn_output, [-1, hidden])           #change the form into a tensor
stacked_outputs = tf.layers.dense(stacked_rnn_output, output)        #specify the type of layer (dense)
outputs = tf.reshape(stacked_outputs, [-1, num_periods, output])          #shape of results
 
loss = tf.reduce_sum(tf.square(outputs - y),name='loss')    #define the cost function which evaluates the quality of our model
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)          #gradient descent method
training_op = optimizer.minimize(loss)          #train the result of the application of the cost_function                                 

init = tf.global_variables_initializer()

epochs = 1000     #number of iterations or training cycles, includes both the FeedFoward and Backpropogation
saver = tf.train.Saver()   #we are going to save the model
DIR="/user/user01/rwTFmodel"  #path where the model will be saved

with tf.Session() as sess:
    init.run()
    for ep in range(epochs):
        sess.run(training_op, feed_dict={X: x_batches, y: y_batches})
        if ep % 100 == 0:
            mse = loss.eval(feed_dict={X: x_batches, y: y_batches})
            print(ep, "\tMSE:", mse) 
            
    y_pred = sess.run(outputs, feed_dict={X: X_test})
    print(y_pred[:,(num_periods-1):num_periods])
    saver.save(sess, os.path.join(DIR,"RWsensorTFmodel"),global_step = epochs)



#Plot our test y data and our y-predicted forecast
plt.title("Forecast vs Actual", fontsize=14)
plt.plot(pd.Series(np.ravel(Y_test)), "bo", markersize=10, label="Actual")
#plt.plot(pd.Series(np.ravel(Y_test)), "w*", markersize=10)
plt.plot(pd.Series(np.ravel(y_pred)), "r.", markersize=10, label="Forecast")
plt.legend(loc="upper left")
plt.xlabel("Time Periods")
plt.show()









