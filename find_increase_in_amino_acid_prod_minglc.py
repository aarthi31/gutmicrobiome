# -*- coding: utf-8 -*-
"""
This code finds the increase in amino acids synthesised in minimal glucose 
medium.

@author: raarthi
"""

import pandas as pd
import numpy as np
amino_acids = ['glu_L__91__c__93__', 'gln_L__91__c__93__', 'asp_L__91__c__93__', 'ala_L__91__c__93__', 'his_L__91__c__93__', 'leu_L__91__c__93__', 'thr_L__91__c__93__', 'cys_L__91__c__93__', 'arg_L__91__c__93__', 'asn_L__91__c__93__', 'met_L__91__c__93__', 'ser_L__91__c__93__', 'lys_L__91__c__93__', 'phe_L__91__c__93__', 'pro_L__91__c__93__', 'tyr_L__91__c__93__', 'ile_L__91__c__93__', 'trp_L__91__c__93__',
               'val_L__91__c__93__','gly__91__c__93__']
models_fname = 'all_models_FINAL.txt'

with open(models_fname, 'r') as f:
    org_names = f.read().splitlines()
org_names_without_sp = []
for org in org_names:
    org_names_without_sp.append(org.split('_')[0] + ' ' + org.split('_')[1])
row_names_wosp = pd.Index(org_names_without_sp, name='organism')
column_names_wosp = pd.Index(org_names_without_sp, name='in the presence of')
row_names = pd.Index(org_names, name='organism')
column_names = pd.Index(org_names, name='in the presence of')
df = pd.DataFrame(index=row_names, columns=column_names)
df_diagval = pd.DataFrame(index=row_names, columns=column_names)
df4_metmap = pd.DataFrame(index=row_names, columns=column_names)
df4_metmap= df4_metmap.astype('object')

path_name_to_read = 'scoperesFinal\\'
filename_to_read_combined = path_name_to_read + 'scope_combined_orgs_withmetas_minimalglucosemedium.txt'
with open(filename_to_read_combined, 'r') as f:
    scope_data_withmetnames = f.read().splitlines()

for entries in scope_data_withmetnames:
    if entries.startswith('\t'):
        orgnames = []
        fororgs = entries.split('\t')
        orgnames.append(fororgs[1])
        orgnames.append(fororgs[2])
    else:
        splitentries = entries.split('\t')
        splitentries.pop(0)
        metsfromorg1 = set([])
        metsfromorg2 = set([])
        for mets in splitentries:
            splitmets1 = mets.split(',')
            for addmet in splitmets1:
                splitmets = addmet.split(' ')
                if splitmets[0] in orgnames[0]:
                    metsfromorg1.add(splitmets[1])
                elif splitmets[0] in orgnames[1]:
                    metsfromorg2.add(splitmets[1])
        
        df4_metmap.at[orgnames[0],orgnames[1]] = metsfromorg1
        df4_metmap.at[orgnames[1],orgnames[0]] = metsfromorg2

filename_to_read_single = path_name_to_read + 'scope_single_orgs_withmetnames_minimalglucosemedium.txt'
with open(filename_to_read_single, 'r') as f:
    scope_data_single_withmetnames = f.read().splitlines()
for entries in scope_data_single_withmetnames:
    currentent = entries.split('\t')
    metsprodbysingle = set([])
    metstoanalyse = currentent[1].split(',')
    for singlemets in metstoanalyse:
        metsprodbysingle.add(singlemets.split(' ')[1])
    df4_metmap.at[currentent[0], currentent[0]] = metsprodbysingle

diff_mat_met = df4_metmap.sub(np.diag(df4_metmap), axis=0)
# From the difference DF we find which AA can be synthesised in addition
aa_df =  pd.DataFrame(index=row_names, columns=column_names)
aa_df =  aa_df.astype('object')
for organisms in list(diff_mat_met.keys()):
    for org2 in list(diff_mat_met.keys()):
        if organisms != org2:
            presentmets = diff_mat_met.at[organisms, org2]   
            presentaa = []
            for aa in amino_acids:
                if aa in presentmets:
                    presentaa.append(aa)
            aa_df.at[organisms, org2] = presentaa
                
#aa_df.to_csv('aa.csv')
aa_df_num = pd.DataFrame(index=row_names, columns=column_names)              
for items in aa_df:
    aa_df_num[items] = aa_df[items].str.len()
aa_df_num_wonan = aa_df_num.fillna(0)
with open('aminoacid_production.txt', 'w') as f:
    for items in aa_df_num_wonan:
        for items2 in aa_df_num_wonan:
            if aa_df_num_wonan.at[items,items2] > 0.0:
                f.write(items+'\t'+ items2+'\t'+str(aa_df_num_wonan.at[items,items2])+'\n')
            
