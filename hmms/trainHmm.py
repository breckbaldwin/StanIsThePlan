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

def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    for st in states:
        V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}
    # Run Viterbi when t > 0
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = V[t-1][states[0]]["prob"]*trans_p[states[0]][st]
            prev_st_selected = states[0]
            for prev_st in states[1:]:
                tr_prob = V[t-1][prev_st]["prob"]*trans_p[prev_st][st]
                if tr_prob > max_tr_prob:
                    max_tr_prob = tr_prob
                    prev_st_selected = prev_st
            print("st="+st+" t="+str(t)+" obs[t]="+obs[t]+" emit_p[st]="+str(emit_p[st]))
            max_prob = max_tr_prob * emit_p[st][obs[t]]
            V[t][st] = {"prob": max_prob, "prev": prev_st_selected}
                    
    for line in dptable(V):
        print (line)
    opt = []
    # The highest probability
    max_prob = max(value["prob"] for value in V[-1].values())
    previous = None
    # Get most probable state and its backtrack
    for st, data in V[-1].items():
        if data["prob"] == max_prob:
            opt.append(st)
            previous = st
            break
    # Follow the backtrack till the first observation
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t + 1][previous]["prev"]

    print ('The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob)

def dptable(V):
    # Print a table of steps from dictionary
    yield " ".join(("%12d" % i) for i in range(len(V)))
    for state in V[0]:
        yield "%.7s: " % state + " ".join("%.7s" % ("%f" % v[state]["prob"]) for v in V)




fileName = sys.argv[1]

with open(fileName) as f:
    content = f.readlines()

for i in range(0,len(content)):
    m = re.search(r'token pos="([^"]*)">([^<]*)<\/token>',content[i])
    if m is not None :
        pos = m.group(1)
        word = m.group(2)
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

stan_program = CmdStanModel(stan_file='stan/hmmStanManual.stan')
stan_program.compile()

fit = stan_program.sample(data=json_data,
                          csv_basename='./hmm',
                          fixed_param=True)
print(fit.summary())
#fit.save_csv_files('stan_output','hmm')


transition_p = fit.get_drawset(['transition_p'])
    
stan_emit_p = fit.get_drawset(['emit_p'])

#for each draw we build a hmm


for i in range(0,1):#len(transition_p.index)):
    pos_trans_p = {}
    for col_name in transition_p.columns:
            [name,fr,to] = col_name.split('.')
            pos_from = int_to_pos[int(fr)]
            pos_to = int_to_pos[int(to)]
            if pos_from not in pos_trans_p:
                pos_trans_p[pos_from] = {}
            pos_trans_p[pos_from][pos_to] = transition_p[col_name][i]

    emit_p = {}
    for col_name in stan_emit_p.columns:
            [name,fr,to] = col_name.split('.')
            pos_from = int_to_pos[int(fr)]
            word_to = int_to_word[int(to)]
            if pos_from not in emit_p:
                emit_p[pos_from] = {}
            emit_p[pos_from][word_to] = stan_emit_p[col_name][i]
    #print(pos_trans_p)
    #print(emit_p)
    obs = ('the','rain','on')
    start_state= {}
    for state in pos_to_int.keys():
        start_state[state] = 1/len(pos_to_int)
    #print(start_state)
    viterbi(obs, list(pos_to_int.keys()), start_state, pos_trans_p, emit_p)

    

