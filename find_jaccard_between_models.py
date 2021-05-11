# -*- coding: utf-8 -*-
"""
This code computes the Jaccard distance between the XML models.

@author: Aarthi Ravikrishnan
"""

import cobra
import os
from collections import Counter
import itertools
wdwithmodels="XML\\"


def write_jaccard(combo1):
    fname =  "jaccard_val.txt"
    model1 = cobra.io.read_sbml_model(wdwithmodels+combo1[0])
    model2 = cobra.io.read_sbml_model(wdwithmodels+combo1[1])
    reaction1 = []
    reaction2 = []
    modelname1 = combo1[0].split('_')[0] + ' ' + combo1[0].split('_')[1]
    modelname2 = combo1[1].split('_')[0] + ' ' + combo1[1].split('_')[1]
    for i in range(len(model1.reactions)):
        reaction1.append(model1.reactions[i].id)
    for j in range(len(model2.reactions)):
        reaction2.append(model2.reactions[j].id)
    intersect_set = set(reaction1).intersection(reaction2)
    union_set = set(reaction1).union(reaction2)
    jaccard_val = round(1-(float(len(intersect_set))/float(len(union_set))), 3)
    with open(fname, 'a') as f:
        f.write(modelname1 + '\t' + modelname2 + '\t' + str(jaccard_val)+'\n')


all_models = os.listdir(wdwithmodels)
all_combos = itertools.combinations(all_models, 2)
for models in all_combos:
    write_jaccard(models)
