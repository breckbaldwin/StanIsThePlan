import os
from cmdstanpy import cmdstan_path, CmdStanModel
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import fileinput
import sys
import statistics
import random

import keras 
from keras.models import Sequential
from keras.layers import Dense 
from keras.utils import to_categorical 
from keras import optimizers

x_distance = np.array([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],dtype=np.integer);
y_successes = np.array([1346,577,337,208,149,136,111,69,67,75,52,46,54,28,27,31,33,20,24],dtype=np.integer);
n_attempts = np.array([1443,694,455,353,272,256,240,217,200,237,202,192,174,167,201,195,191,147,152],dtype=np.integer);

prob_success = y_successes/n_attempts

fig, (ax) = plt.subplots(1,1)
ax.set_facecolor('grey')
ax.set_ylabel('chance in 1')
ax.set_xlabel('putt distance (feet)')
input_out = np.zeros(shape=(n_attempts.sum(),2)) #[inputs,0/1]

index = 0
for i in range(0,x_distance.size):
    for j in range(0,n_attempts[i]):
        input_out[index][0] = x_distance[i]
        if (j <= y_successes[i]):  #modify last elt to 1 if putt went in.
           input_out[index][1] = 1
        else :
           input_out[index][1] = 0
        index = index+1

X=input_out[...,0]
Y=input_out[...,1]

sgd = optimizers.SGD(lr=0.15)            

model = Sequential() 
model.add(Dense(1, batch_input_shape=(None, 1),activation='sigmoid'))
model.compile(loss='binary_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

model2 = Sequential() 
model2.add(Dense(1, batch_input_shape=(None, 1),activation='sigmoid'))
model2.add(Dense(1,activation='sigmoid'))                      
model2.compile(loss='binary_crossentropy',
              optimizer=sgd,                                # using the stochastic gradient descent optimizer
              metrics=['accuracy'])

"""
model = Sequential() # from http://signalsurgeon.com/how-to-make-predictions-with-keras/
model.add(Dense(4, input_dim=1, activation='relu'))
model.add(Dense(4, activation='relu'))
model.add(Dense(1, activation='sigmoid'))#linear is two straight
model.compile(loss='mse', optimizer='adam')
"""

# Training of the network
history = model.fit(X, Y,                          
          epochs=400,                              
          batch_size=128,                           
          verbose=1)

history2 = model2.fit(X, Y,                          
          epochs=400,                             
          batch_size=128,                      
                    verbose=1)

Xnew = np.zeros(shape=(30,1))

for i in range(0,30):
        Xnew[i]=i

y_new = model.predict_proba(Xnew)
y2_new = model2.predict_proba(Xnew)

add_training_label = True
add_ignored_label = True
for i in range(0,x_distance.size):
    size = max(round(n_attempts[i]/1443*20),2)
    if (add_training_label) :
         ax.plot(x_distance[i],prob_success[i],'ro',label='training starting at count:' + str(n_attempts[i]), markersize=size)
         add_training_label = False
    else :
         ax.plot(x_distance[i],prob_success[i],'ro',markersize=size)
        
ax.plot(Xnew,y_new,'b',label='one node neural net')
ax.plot(Xnew,y2_new,'c',label='one hidden node neural net')


plt.legend()
plt.show()

