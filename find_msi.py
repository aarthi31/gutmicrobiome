# -*- coding: utf-8 -*-
"""
This code computes the MSI between pairs of organisms
Change line 149 with seed metabolites from other cases


@author: Aarthi Ravikrishnan
"""

import metquest
import networkx as nx
from collections import Counter
import os
import pdb
import pandas as pd 
import pickle
import seaborn as sns
import matplotlib.pyplot as plt

def find_metabolic_support_index(path, path_single, graph_name_combined, graph_name_firstorg, graph_name_secondorg, seed_metabolites):
    '''
    This function evaluates the metabolic support index which defines the
    Fraction of blocked or stuck reactions relieved by the presence of another
    organism.

    Parameters
    ----------

    pname - Pathname with all the datafiles
    graph_name_combined - Filename of the combined graphs
    graph_name_firstorg - Filename of the first organism graph
    graph_name_secondorg - Filename of the second organism graph
    seed_metabolite_fname - Filename of the seed metabolite list

    Returns
    -------
    None

    '''
    combined_graph = nx.read_gpickle(path + graph_name_combined) #seed_mets.txt'
    first_org_graph = nx.read_gpickle(path_single + graph_name_firstorg)
    second_org_graph = nx.read_gpickle(path_single + graph_name_secondorg)

    lb_m_org_1, status_dict_org_1, scope_org_1 = metquest.forward_pass(first_org_graph, seed_metabolites)
    org_1_reactions = []
    org_1_metabolites = []
    node_attr = nx.get_node_attributes(first_org_graph, 'bipartite')
    for nodes in first_org_graph:
        if node_attr[nodes] == 1:
            org_1_reactions.append(nodes)
        else:
            metname = nodes.split(' ')[0]
            if metname not in org_1_metabolites and '_e' not in metname:
                org_1_metabolites.append(metname)

    lb_m_org_2, status_dict_org_2, scope_org_2 = metquest.forward_pass(second_org_graph, seed_metabolites)
    org_2_reactions = []
    org_2_metabolites = []
    node_attr = nx.get_node_attributes(second_org_graph, 'bipartite')
    for nodes in second_org_graph:
        if node_attr[nodes] == 1:
            org_2_reactions.append(nodes)
        else:
            metname = nodes.split(' ')[0]
            if metname not in org_2_metabolites and '_e' not in metname:
                org_2_metabolites.append(metname)
    org_1 = graph_name_firstorg.split('_.gpickle')[0]
    org_2 = graph_name_secondorg.split('_.gpickle')[0]
    reactions = []
    lb_m, status_dict, scope = metquest.forward_pass(combined_graph, seed_metabolites)
    reactions = []
    node_attr = nx.get_node_attributes(combined_graph, 'bipartite')
    for nodes in combined_graph:
        if node_attr[nodes] == 1:
            reactions.append(nodes)
    stuck_internal_rxns_in_org_1_combined = []
    stuck_internal_rxns_in_org_2_combined = []
    stuck_external_rxns_in_org_1_combined = set([])
    stuck_external_rxns_in_org_2_combined = set([])
    # Combined stuck nodes
    all_stuck_nodes = set(reactions) - set(status_dict)
    for nodes in all_stuck_nodes:
        nodesplit = nodes.split(' ')[1]
        if org_2 in nodes:
            if 'IR' in nodesplit or 'RR' in nodesplit or 'RevBR' in nodesplit:
                if 'ER' not in nodesplit:
                    stuck_internal_rxns_in_org_2_combined.append(nodes)
                else:
                    stuck_external_rxns_in_org_2_combined.add(nodes)
            else:
                 stuck_external_rxns_in_org_2_combined.add(nodes)
   
        elif org_1 in nodes:
            if 'IR' in nodesplit or 'RR' in nodesplit or 'RevBR' in nodesplit:
                if 'ER' not in nodesplit:
                    stuck_internal_rxns_in_org_1_combined.append(nodes)
                else:
                    stuck_external_rxns_in_org_1_combined.add(nodes)
            else:
                stuck_external_rxns_in_org_1_combined.add(nodes)


    org_2_stuck_nodes = set(org_2_reactions) - set(status_dict_org_2)
    org_2_stuck_internal_single = []
    org_2_stuck_external = []
    for nodes in org_2_stuck_nodes:
        nodesplit = nodes.split(' ')[1]
        if 'IR' in nodes or 'RR' in nodes or 'RevBR' in nodes:
            if 'ER' not in nodes:
                org_2_stuck_internal_single.append(nodes)

            else: #ERR nodes
                org_2_stuck_external.append(nodes)
        else:
            org_2_stuck_external.append(nodes)
    org_1_stuck_nodes_internal = set(org_1_reactions) - set(status_dict_org_1) #Status dict has all visited nodes
    org_1_stuck_internal_single = []
    org_1_stuck_external = []
    for nodes in org_1_stuck_nodes_internal:
        nodesplit = nodes.split(' ')[1]
        if 'IR' in nodesplit or 'RR' in nodesplit or 'RevBR' in nodesplit: 
            if 'ER' not in nodesplit: #To avoid entries like NCERR and ERR
                org_1_stuck_internal_single.append(nodesplit)
            else:
                org_1_stuck_external.append(nodesplit)
        else:
            org_1_stuck_external.append(nodesplit)
    msi_org1 = round(1-(len(stuck_internal_rxns_in_org_1_combined)/ len(org_1_stuck_internal_single)), 3)
    msi_org2 = round(1-(len(stuck_internal_rxns_in_org_2_combined)/ len(org_2_stuck_internal_single)), 3)

    print('stuck_external_rxns_in_org_1_combined ' + org_1, len(stuck_external_rxns_in_org_1_combined))
    print('stuck_external_rxns_in_org_2_combined ' + org_2, len(stuck_external_rxns_in_org_2_combined))
    print('stuck_internal_rxns_in_org_2_combined ' + org_2, len(stuck_internal_rxns_in_org_2_combined))
    print('stuck_internal_rxns_in_org_1_combined ' + org_1, len(stuck_internal_rxns_in_org_1_combined))
    print('org_1_stuck_internal_single ' + org_1, len(org_1_stuck_internal_single))
    print('org_2_stuck_internal_single ' + org_2, len(org_2_stuck_internal_single))
    print('org_2_stuck_external ' + org_2, len(org_2_stuck_external))
    print('org_1_stuck_external ' + org_1, len(org_1_stuck_external))
    print('Metabolic support index ' + org_1, msi_org1) 
    print('Metabolic support index ' + org_2, msi_org2)
    if len(splitfilenames) == 1:
        df.at[splitfilenames[0], splitfilenames[0]] = 0
    elif len(splitfilenames) >= 1:
        df.at[splitfilenames[0], splitfilenames[1]] = msi_org1 
        df.at[splitfilenames[1], splitfilenames[0]] = msi_org2


current_working_directory = os.getcwd()
path = os.path.join(current_working_directory, 'FinalDouble\\')
path_single = os.path.join(current_working_directory, 'FinalSingle\\')
seed_metabolite_fname = os.path.join(current_working_directory, 'MediaConditions\\seed_mets_high_fibre_both_eandc.txt')
org_names_fname =  os.path.join(current_working_directory, 'all_models_FINAL.txt')
res_paths = os.path.join(current_working_directory, 'MSIResults\\')
if not os.path.exists(res_paths):
    os.makedirs(res_paths)
with open(org_names_fname, 'r') as f:
    org_names = f.read().splitlines()
org_names_without_xml = []
for names in org_names:
    org_names_without_xml.append(names.strip('.xml'))
row_names = pd.Index(org_names_without_xml, name='rows')
column_names = pd.Index(org_names_without_xml, name='columns')
df = pd.DataFrame(index=row_names, columns=column_names) #df with all the scope entries
with open(seed_metabolite_fname, 'r') as f:
    seed_mets_from_file = f.read().splitlines()
for graphname in os.listdir(path):
    if graphname.endswith('.gpickle'):
        splitfilenames = []
        for names in org_names:
            if names.split('.xml')[0] in graphname:
                splitfilenames.append(names.split('.xml')[0])
        seed_mets = set(seed_mets_from_file)
        for fname in splitfilenames:
            for mets in seed_mets_from_file:
                seed_mets.add(fname + ' ' + mets)
        graph_name_firstorg = splitfilenames[0] + '_.gpickle'
        graph_name_secondorg = splitfilenames[1] + '_.gpickle'
        find_metabolic_support_index(path, path_single, graphname, graph_name_firstorg, graph_name_secondorg, seed_mets)

df.to_csv(res_paths + 'msi_high_fibre.csv')
