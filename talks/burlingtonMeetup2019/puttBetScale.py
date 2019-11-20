import os
from cmdstanpy import cmdstan_path, CmdStanModel
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import fileinput
import sys
import statistics
import random


#python puttBetScale.py 100 2 bimodal for log reg
#python puttBetScale.py 10 2 bimodal as well

#stan_program_path = sys.argv[1]
shrinkage = float(sys.argv[1])
data_size = int(sys.argv[2])

J = min(19,data_size);
x_distance = np.array([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],dtype=np.integer);
y_successes = np.array([1346,577,337,208,149,136,111,69,67,75,52,46,54,28,27,31,33,20,24],dtype=np.integer);
n_attempts = np.array([1443,694,455,353,272,256,240,217,200,237,202,192,174,167,201,195,191,147,152],dtype=np.integer);




prob_success = y_successes/n_attempts



y_successes_shrunk = np.array([round(y/shrinkage) for y in y_successes],dtype=int)
n_attempts_shrunk = np.array([round(n/shrinkage) for n in n_attempts],dtype=int)

print(y_successes_shrunk[0:J])
print(n_attempts_shrunk[0:J])



def runGolf(path,plt,color):
    stan_program = CmdStanModel(stan_file=path)
    stan_program.compile()

    json_data = {"J":J,"x_distance":x_distance[0:J].tolist(),
                 "y_successes":y_successes_shrunk[0:J].tolist(),
                 "n_attempts":n_attempts_shrunk[0:J].tolist()}

    fit = stan_program.sample(data=json_data,
                          csv_basename='./puttbet')
    print(fit.summary())
    chance_in_1 = fit.get_drawset(['chance_in_1_for_dist']).to_numpy()
    x = np.arange(chance_in_1[0].size)
    plt.plot(x,chance_in_1[0],color,label=path)
    for i in range(1,25):
        plt.plot(x,chance_in_1[i],color)

    for i in range(1000,1025):
        plt.plot(x,chance_in_1[i],color)

    for i in range(2000,2025):
        plt.plot(x,chance_in_1[i],color)

    for i in range(3000,3025):
        plt.plot(x,chance_in_1[i],color)

    y_means=np.zeros(chance_in_1[0].size);
    for i in range(0,chance_in_1[0].size):
        y_means[i] = statistics.mean(chance_in_1[...,i])

    plt.plot(x,y_means,'w')

    
runGolf('stan/mecca_golf_external_data.stan',plt,'g')
runGolf('stan/logistic_golf_external_data.stan',plt,'y')
add_training_label = True
add_ignored_label = True
for i in range(0,x_distance.size):
    size = max(round(n_attempts_shrunk[i]/1443*20),2)
    if (i < J) :
        if (add_training_label) :
                plt.plot(x_distance[i],prob_success[i],'ro',label='training data starting at count:' + str(n_attempts_shrunk[i]), markersize=size)
                add_training_label = False
        else :
            plt.plot(x_distance[i],prob_success[i],'ro',markersize=size)
    else :
        if (add_ignored_label) :
            plt.plot(x_distance[i],prob_success[i],'bo',label='ignored data starting at count:' + str(n_attempts_shrunk[i]) , markersize=size)
            add_ignored_label = False
        else :
            plt.plot(x_distance[i],prob_success[i],'bo',markersize=size)

plt.legend()
plt.show()

