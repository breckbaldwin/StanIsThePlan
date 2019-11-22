import os
from cmdstanpy import cmdstan_path, CmdStanModel
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import fileinput
import sys
import statistics
import random
import re

word_to_int = {}
int_to_word = {}
pos_to_int = {}
int_to_pos = {}
word_order = []
pos_order = []
word_count = 0
pos_count = 0

fileName = sys.argv[1]

with open(fileName) as f:
    content = f.readlines()

for i in range(0,len(content)):
    m = re.search(r'token pos="([^"]*)">([^<]*)<\/token>',content[i])
    if m is not None :
        word = m.group(1)
        pos = m.group(2)
        if word not in word_to_int :
            word_count += 1
            word_to_int[word] = word_count
            int_to_word[word_count] = word
        if pos not in pos_to_int :
            pos_count += 1
            pos_to_int[pos] = pos_count
            int_to_pos[pos_count] = pos
        word_order.append(word_to_int[word])
        pos_order.append(pos_to_int[pos])
        

alpha = np.full((len(pos_to_int)),.5).tolist()
beta = np.full((len(word_to_int)),.5).tolist()
        
                
json_data = {"cat_count":len(pos_to_int),
             "word_count":len(word_to_int),
             "data_count":len(word_order),
             "words":word_order,
             "categories":pos_order,
             "alpha":alpha,
             "beta":beta}

print(json_data)

stan_program = CmdStanModel(stan_file='hmmStanManual.stan')
stan_program.compile()

fit = stan_program.sample(data=json_data,
                          csv_basename='./hmm')
print(fit.summary())
#chance_in_1 = fit.get_drawset(['chance_in_1_for_dist']).to_numpy()

#obs('the','rain','in')
#start_p(
