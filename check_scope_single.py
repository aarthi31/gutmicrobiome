#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This code computes the scope on single graphs.
Modify lines 44,48, 49 for other seed metabolites.
Currently it uses high fibre seed metabolites.

@author: Aarthi Ravikrishnan
"""

import networkx as nx
import metquest
import os


def check_scope(path_name, graphname,seed_mets_nonmodel,filename_to_write,filename_to_write_withmetnames):
    filename = path_name +  graphname
    G = nx.read_gpickle(filename)
    seed_mets = set([])
    splitfilenames = graphname.split('_.gpickle')[0] + ' '
    for mets in seed_mets_nonmodel:
        seed_mets.add(mets)
        renamed_seedmets_1 = splitfilenames + mets
        seed_mets.add(renamed_seedmets_1)
    lowerboundmet, status_dict, scope = metquest.forward_pass(G, seed_mets)
    graphname_split = graphname.split('_.gpickle')[0]
    metsproducedbyfirst = []
    for mets in scope:
        if mets not in seed_mets:
            if graphname_split in mets:
                metsproducedbyfirst.append(mets)

    with open(filename_to_write_withmetnames,'a') as f:
        strtowrite2 = graphname.split('_.gpickle')[0] + '\t' + ','.join(metsproducedbyfirst)
        f.write(strtowrite2)
        f.write('\n')
    with open(filename_to_write,'a') as f:
        strtowrite2 = graphname.split('_.gpickle')[0] + '\t' + str(len(metsproducedbyfirst))
        f.write(strtowrite2)
        f.write('\n')

current_working_directory = os.getcwd()
path_name = os.path.join(current_working_directory, 'FinalSingle\\')
seed_metabolite_fname =  os.path.join(current_working_directory, 'MediaConditions\\seed_mets_high_fibre_both_eandc.txt')
with open(seed_metabolite_fname, 'r') as f:
    seed_mets_nonmodel = f.read().splitlines()

filename_to_write = os.path.join(current_working_directory,'scope_single_orgs_HFmedium.txt')
filename_to_write_withmetnames = os.path.join(current_working_directory,'scope_single_orgs_withmetnames_HFmedium.txt')

for graphname in os.listdir(path_name):
    if graphname.endswith('.gpickle'):
        check_scope(path_name, graphname,seed_mets_nonmodel,filename_to_write,filename_to_write_withmetnames)
