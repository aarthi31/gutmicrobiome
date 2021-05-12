# -*- coding: utf-8 -*-
"""
Created on Thu May 28 08:42:37 2020
This code finds the pathways between the DMEM medium components and everything else.
Change appropriately for HF conditions (see markings below) 

@author: Aarthi Ravikrishnan
"""

import networkx as nx
import metquest
from collections import Counter
import os
import gzip
import pickle
import sys
from joblib import Parallel, delayed

def find_pathways_in_highfiber(graphname, seed_mets_nonmodel, all_models, path_name, resfolder, extraname):
    print(graphname)

    filename = path_name +  graphname
    G = nx.read_gpickle(filename)

    seed_mets = set([])
    for entries in all_models:
        if graphname.find(entries) == 0:
            graphname1 = entries
        elif graphname.find(entries) > 0:
            graphname2 = entries

    for mets in seed_mets_nonmodel:
        #seed_mets.add(mets)
        renamed_seedmets_1 = graphname1 + ' ' + mets
        renamed_seedmets_2 = graphname2 + ' ' + mets
        seed_mets.add(renamed_seedmets_1)
        seed_mets.add(renamed_seedmets_2)
    path_len_cutoff = 30
    print('Entering pathway computation')
    pathway_table, cyclic_pathways, scope = metquest.find_pathways(G, seed_mets, path_len_cutoff)
    ptable_fname = graphname1 + '-twopple-' + graphname2 + '-' + extraname + '.pickle'
    print('Finished pathway computation')
    with gzip.open(resfolder+'/' + ptable_fname, 'wb') as f:
        pickle.dump([pathway_table, cyclic_pathways, scope], f)

double_pname = 'FinalDouble//'
seed_met_fname = 'MediaConditions//' + 'dmem_medium_supplements.txt' # Change for HF
models_name = 'all_models_FINAL.txt'
graphs_to_analyse = os.listdir(double_pname)
extraname = 'DMEM' # Change if it is high fibre
with open(models_name, 'r') as f:
    all_models = f.read().splitlines()

path_name_to_write = 'PathResults//'
if not os.path.exists(path_name_to_write):
    os.mkdir(path_name_to_write)

with open(seed_met_fname, 'r') as f:
    seed_mets_nonmodel = f.read().splitlines()
for graphname in graphs_to_analyse:
    find_pathways_in_highfiber(graphname, seed_mets_nonmodel, all_models, double_pname, path_name_to_write, extraname)
#Parallel(n_jobs=5)(delayed(find_pathways_in_highfiber)(graphname, seed_mets_nonmodel, all_models, double_pname, resultsfolder, resfoldertocreate) for graphname in graphs_to_analyse)
