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
#python puttBetScale.py 1 18 19
#python puttBetScale.py 1 17 19 pretty bimodal lr


#stan_program_path = sys.argv[1]
shrinkage = float(sys.argv[1])
data_start = int(sys.argv[2])
data_finish = int(sys.argv[3])

J = min(19,data_finish)
Start = max(0,data_start)

x_distance = np.array([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],dtype=np.integer);
y_successes = np.array([1346,577,337,208,149,136,111,69,67,75,52,46,54,28,27,31,33,20,24],dtype=np.integer);
n_attempts = np.array([1443,694,455,353,272,256,240,217,200,237,202,192,174,167,201,195,191,147,152],dtype=np.integer);

prob_success = y_successes/n_attempts

y_successes_shrunk = np.array([round(y/shrinkage) for y in y_successes],dtype=int)
n_attempts_shrunk = np.array([round(n/shrinkage) for n in n_attempts],dtype=int)

print(y_successes_shrunk[Start:J])
print(n_attempts_shrunk[Start:J])


def runGolf(fit,path,ax,color):
    chance_in_1 = fit.get_drawset(['chance_in_1_for_dist']).to_numpy()
    x = np.arange(chance_in_1[0].size)
    ax.plot(x,chance_in_1[0],color,label="100 posterior draws:" + path)
    for i in range(1,25):
        ax.plot(x,chance_in_1[i],color)

    for i in range(1000,1025):
        ax.plot(x,chance_in_1[i],color)

    for i in range(2000,2025):
        ax.plot(x,chance_in_1[i],color)

    for i in range(3000,3025):
        ax.plot(x,chance_in_1[i],color)

    y_means=np.zeros(chance_in_1[0].size);
    for i in range(0,chance_in_1[0].size):
        y_means[i] = statistics.mean(chance_in_1[...,i])

    ax.plot(x,y_means,'w')



json_data = {"J":J-Start,"x_distance":x_distance[Start:J].tolist(),
             "y_successes":y_successes_shrunk[Start:J].tolist(),
             "n_attempts":n_attempts_shrunk[Start:J].tolist()}

fig, (ax2,ax) = plt.subplots(1,2)
ax.set_facecolor('grey')
ax.set_ylabel('chance in 1')
ax.set_xlabel('putt distance (feet)')

stan_program = CmdStanModel(stan_file='stan/logist.stan')
stan_program.compile()
fit = stan_program.sample(data=json_data,
                          csv_basename='./puttbetlog')
#print(fit.summary())
logistic_color = 'y'
runGolf(fit,'stan/logist.stan',ax,logistic_color)
a_draws = fit.get_drawset(['a_intercept']).to_numpy()
b_draws = fit.get_drawset(['b_slope']).to_numpy()
ax2.hist(a_draws,color=logistic_color,label='a_intercept')
ax2.hist(b_draws,label='b_slope')
ax2.legend(loc='upper right')
ax2.set_ylabel('number of draws')

stan_program = CmdStanModel(stan_file='stan/mechai.stan')
stan_program.compile()
fit2 = stan_program.sample(data=json_data,
                           csv_basename='./puttbetmech')
runGolf(fit2,'stan/mechai.stan',ax,'g')
sigma_draws = fit2.get_drawset(['sigma_error_in_degrees']).to_numpy()
ax2.hist(sigma_draws,color='g',label='sigma_error_in_degrees')
ax2.legend(loc='upper right')

add_training_label = True
add_ignored_label = True
for i in range(0,x_distance.size):
    size = max(round(n_attempts_shrunk[i]/1443*20),2)
    if (i>=Start and i < J) :
        if (add_training_label) :
                ax.plot(x_distance[i],prob_success[i],'ro',label='training starting at count:' + str(n_attempts_shrunk[i]), markersize=size)
                add_training_label = False
        else :
            ax.plot(x_distance[i],prob_success[i],'ro',markersize=size)
    else :
        if (add_ignored_label) :
            ax.plot(x_distance[i],prob_success[i],'co',label='ignored starting at count:' + str(n_attempts_shrunk[i]) , markersize=size)
            add_ignored_label = False
        else :
            ax.plot(x_distance[i],prob_success[i],'co',markersize=size)

plt.legend()
plt.show()

