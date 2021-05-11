# -*- coding: utf-8 -*-
"""
This code computes the scope on joint graphs.
Modify lines 56,57,58 for other seed metabolites.
Currently it uses high fibre seed metabolites.
@author: Aarthi Ravikrishnan
"""

import networkx as nx
import metquest
import os

def check_scope(graphname, seed_mets_nonmodel, all_models, fnamewihmetas, fnamewithnum):
    print(graphname)
    filename = path_name +  graphname
    G = nx.read_gpickle(filename)
    seed_mets = set([])
    for entries in all_models:
        if graphname.find(entries) == 0:
            graphname1 = entries
        elif graphname.find(entries) > 0:
            graphname2 = entries
    print(graphname1, graphname2)
    for mets in seed_mets_nonmodel:
        renamed_seedmets_1 = graphname1 + ' ' + mets
        renamed_seedmets_2 = graphname2 + ' ' + mets
        seed_mets.add(renamed_seedmets_1)
        seed_mets.add(renamed_seedmets_2)
    lowerboundmet, status_dict, scope = metquest.forward_pass(G, seed_mets)
    metsproducedbyfirst = []
    metsproducedbysecond = []
    for mets in scope:
        if mets not in seed_mets:
            if graphname1 in mets:
                metsproducedbyfirst.append(mets)
            elif graphname2 in mets:
                metsproducedbysecond.append(mets)
    print(len(metsproducedbyfirst), len(metsproducedbysecond))
    with open(fnamewihmetas, 'a') as f:
        strtowrite1 = '\t' + graphname1 + '\t' + graphname2
        f.write(strtowrite1)
        f.write('\n')
        strtowrite2 = graphname.split('.gpickle')[0] + '\t' + ','.join(metsproducedbyfirst) + '\t' + ','.join(metsproducedbysecond)
        f.write(strtowrite2)
        f.write('\n')
    with open(fnamewithnum, 'a') as f:
        strtowrite2 = graphname.split('.gpickle')[0] + '\t' + str(len(metsproducedbyfirst)) + '\t' + str(len(metsproducedbysecond))
        f.write(strtowrite2)
        f.write('\n')


current_working_directory = os.getcwd()
path_name = os.path.join(current_working_directory, 'FinalDouble\\')
path_single = os.path.join(current_working_directory, 'FinalSingle\\')

#  Change these for scope (this uses high fibre seed - change line 58 for other seed metabolites)
fnamewithmetas = os.path.join(current_working_directory, 'scope_combined_orgs_withmetas_HFmedium.txt')
fnamewithnum = os.path.join(current_working_directory, 'scope_combined_orgs_HFmedium.txt')
seed_metabolite_fname = os.path.join(current_working_directory, 'MediaConditions\\seed_mets_high_fibre_both_eandc.txt')
models_name = os.path.join(current_working_directory, 'all_models_FINAL.txt')
with open(models_name, 'r') as f:
    all_models = f.read().splitlines()
with open(seed_metabolite_fname, 'r') as f:
    seed_mets_nonmodel = f.read().splitlines()
for graphname in os.listdir(path_name):
    if graphname.endswith('.gpickle'):
        check_scope(graphname, seed_mets_nonmodel, all_models, fnamewithmetas, fnamewithnum)
