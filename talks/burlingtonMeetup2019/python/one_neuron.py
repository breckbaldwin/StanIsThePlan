import numpy as np
import matplotlib.pyplot as plt
plt.style.use('default')

import keras 
from keras.models import Sequential
from keras.layers import Dense 
from keras.utils import to_categorical 
from keras import optimizers




X=np.array([2,2])
Y=np.array([1,1])

model = Sequential() 
model.add(Dense(1, batch_input_shape=(None, 1),
                activation='sigmoid'))
                #activation='linear'))                      
#model.add(Dense(19, batch_input_shape=(None, 18),activation='sigmoid'))
#model.add(Dense(2, activation='softmax'))

# Definition of the optimizer
sgd = optimizers.SGD(lr=0.15)            

# compile model                                             # compile model, which ends the definition of the model 
model.compile(loss='binary_crossentropy',
#model.compile(loss='categorical_crossentropy',
              optimizer=sgd,                                # using the stochastic gradient descent optimizer
              metrics=['accuracy'])

model.summary()
print(X.shape)
# Training of the network
history = model.fit(X, Y,                           # training of the model using the training data stored in X and Y for 4100 epochs
          epochs=400,                               # for 400 epochs
          batch_size=128,                           # fix the batch size to 128 examples
                    verbose=1)


Xnew = np.zeros(shape=(100))

for i in range(0,Xnew.size):
    #for j in range(0,i):
    #    Xnew[i][j]=1
        Xnew[i]=i

    
y_new = model.predict_proba(Xnew)

#print(y_new[:,1].tolist())
print(y_new[:,0].tolist())
# show the inputs and predicted outputs
for i in range(len(Xnew)):
	print("X=%s, Predicted=%s" % (Xnew[i], y_new[i]))


plt.plot(x_dist,y_new,'ro',label='data')

plt.legend()
#plt.show()

        
 
