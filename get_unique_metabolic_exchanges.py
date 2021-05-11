# -*- coding: utf-8 -*-
"""
Plot heatmap of metabolic exchanges
Change line 16 for high fibre conditions to 'metexc_hf_withoutorgnames.csv'
Current code works for DMEM.

@author: raarthi
"""

import pandas as pd
from ast import literal_eval
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

org_names_fname = 'all_models_FINAL.txt'
df_metNames = pd.read_csv("metexc_hf_withoutorgnames.csv",index_col=0) #metexc_hf_withoutorgnames.csv"
with open(org_names_fname, 'r') as f:
    org_names = f.read().splitlines()
row_names = pd.Index(org_names, name='(from)')
column_names = pd.Index(org_names, name='(to)')
df_new = pd.DataFrame(index=row_names, columns=column_names)

for o1 in df_new:
    for o2 in df_new:
        try:
            if o1 != o2:
                df_new.at[o1,o2] = literal_eval(df_metNames.loc[o1,o2])
            else:
                df_new.at[o1,o2] = set([])
        except ValueError:
            df_new.at[o1, o2] = set([])
df_differences = df_new - df_new.T

all_mets_exc = []
for o1 in df_differences:
    for o2 in df_differences:
        if len(df_differences.loc[o1, o2]) != 0:
            for mets in list(df_differences.loc[o1, o2]):
                all_mets_exc.append(mets)


df_differences_num = pd.DataFrame(index=row_names, columns=column_names)
for o1 in df_new:
    for o2 in df_new:
        if o1 != o2:
            df_differences_num.at[o1,o2] = len(df_differences.at[o1, o2])
            
df_differences_num.fillna(0)

df_differences_num.fillna(0)
df_differences_without_nan = df_differences_num.fillna(0)

org_names_without_sp = []
for org in df_differences_without_nan:
    org_names_without_sp.append(org.split('_')[0] + ' ' + org.split('_')[1])
row_names_wosp = pd.Index(org_names_without_sp, name='organism')
column_names_wosp = pd.Index(org_names_without_sp, name='in the presence of')

diff_mat_without_sp_name = pd.DataFrame(index=row_names_wosp, columns=column_names_wosp)
diff_mat_num_without_sp_name = pd.DataFrame(index=row_names_wosp, columns=column_names_wosp)
for ele in df_differences_num:
    for keys in df_differences_num[ele].keys():
        if ele!= keys:
            keys1 = keys.split('_')[0] + ' ' + keys.split('_')[1]
            ele1 = ele.split('_')[0] + ' ' + ele.split('_')[1]
            diff_mat_without_sp_name[ele1][keys1] = df_differences_num[ele][keys]
            diff_mat_num_without_sp_name[ele1][keys1] = df_differences_num[ele][keys]

        elif ele == keys:
            print(ele)
            ele1 = ele.split('_')[0] + ' ' + ele.split('_')[1]
            keys1 = keys.split('_')[0] + ' ' + keys.split('_')[1]
            diff_mat_without_sp_name[ele1][keys1] = '-'
            diff_mat_num_without_sp_name[ele1][keys1]= 0

axis_labels = ['A. fermentans','A. muciniphila','A. finegoldii','A. putredinis','A. shahii','B. caccae','B. coprocola','B. eggerthii','B. fragilis','B. intestinalis','B. stercoris','B. thetaiotaomicron','B. uniformis','B. adolescentis','B. bifidum','B. longum','B. wadsworthia','B. wexlerae','C. amalonaticus','C. clostridioforme','C. tanakaei','C. catus','D. desulfuricans','D. piger','D. invisus','D. longicatena','E. cloacae','E. faecium','E. coli','E. rectale','F. prausnitzii','F. varium','H. parainfluenzae','H. pylori','K. pneumoniae','L. mucosae','L. reuteri','M. elsdenii','P. distasonis','P. johnsonii','P. succinatutens','P. ruminicola','P. capillosus','R. intestinalis','R. inulinivorans','R. bromii','R. callidus','R. torques','S. flexneri','S. salivarius','S. variabile','V. atypica']
diff_mat_num_without_sp_name_1 = diff_mat_num_without_sp_name.fillna(0) #xticklabels=axis_labels, yticklabels=axis_labels,
j = sns.heatmap(diff_mat_num_without_sp_name_1,  cmap="Blues",cbar=True, square=True, xticklabels=axis_labels, yticklabels=axis_labels) #,xticklabels = 1, yticklabels = 1)#annot_kws={"size":16})
plt.xticks(style='italic') #,size='large')
plt.yticks(style='italic')#,size='large')

plt.xlabel('(to)', weight= 'bold')
plt.ylabel('(from)', weight= 'bold')
colorbar = j.collections[0].colorbar
colorbar.set_ticks(list(range(0,42)))
colorbar.set_ticklabels(list(range(0,42)))
#diff_mat_num_without_sp_name_1.to_csv('dmem_diff_nummat.csv')
# SCFA plot
original_names = ['Acidaminococcus_fermentans_DSM_20731', 'Akkermansia_muciniphila_ATCC_BAA_835', 'Alistipes_finegoldii_DSM_17242', 'Alistipes_putredinis_DSM_17216', 'Alistipes_shahii_WAL_8301', 'Bacteroides_caccae_ATCC_43185', 'Bacteroides_coprocola_M16_DSM_17136', 'Bacteroides_eggerthii_DSM_20697', 'Bacteroides_fragilis_NCTC_9343', 'Bacteroides_intestinalis_341_DSM_17393', 'Bacteroides_stercoris_ATCC_43183', 'Bacteroides_thetaiotaomicron_VPI_5482', 'Bacteroides_uniformis_ATCC_8492', 'Bifidobacterium_adolescentis_ATCC_15703', 'Bifidobacterium_bifidum_PRL2010', 'Bifidobacterium_longum_NCC2705', 'Bilophila_wadsworthia_3_1_6', 'Blautia_wexlerae_DSM_19850', 'Citrobacter_amalonaticus_Y19', 'Clostridium_clostridioforme_CM201', 'Collinsella_tanakaei_YIT_12063', 'Coprococcus_catus_GD_7', 'Desulfovibrio_desulfuricans_subsp_desulfuricans_DSM_642', 'Desulfovibrio_piger_ATCC_29098', 'Dialister_invisus_DSM_15470', 'Dorea_longicatena_DSM_13814', 'Enterobacter_cloacae_EcWSU1', 'Enterococcus_faecium_TX1330', 'Escherichia_coli_str_K_12_substr_MG1655', 'Eubacterium_rectale_M104_1', 'Faecalibacterium_prausnitzii_L2_6', 'Fusobacterium_varium_ATCC_27725', 'Haemophilus_parainfluenzae_T3T1', 'Helicobacter_pylori_26695', 'Klebsiella_pneumoniae_pneumoniae_MGH78578', 'Lactobacillus_mucosae_LM1', 'Lactobacillus_reuteri_SD2112_ATCC_55730', 'Megasphaera_elsdenii_DSM_20460', 'Parabacteroides_distasonis_ATCC_8503', 'Parabacteroides_johnsonii_DSM_18315', 'Phascolarctobacterium_succinatutens_YIT_12067', 'Prevotella_ruminicola_23', 'Pseudoflavonifractor_capillosus_strain_ATCC_29799', 'Roseburia_intestinalis_L1_82', 'Roseburia_inulinivorans_DSM_16841', 'Ruminococcus_bromii_L2_63', 'Ruminococcus_callidus_ATCC_2776001', 'Ruminococcus_torques_ATCC_27756', 'Shigella_flexneri_2002017', 'Streptococcus_salivarius_JIM8777', 'Subdoligranulum_variabile_DSM_15176', 'Veillonella_atypica_ACS_049_V_Sch6']
dict_names = {}
for x, ent in enumerate(axis_labels):
    dict_names[original_names[x]] = ent
yaxisnames =['A. finegoldii', 'A. putredinis', 'A. shahii', 'B. adolescentis', 'C. amalonaticus', 'C. clostridioforme', 'C. catus', 'D. longicatena', 'E. faecium', 'E. coli', 'F. varium', 'H. pylori', 'L. mucosae', 'R. callidus']

scfaonly = pd.read_csv('metexc_scfa.csv', index_col=0)
req_org = list(scfaonly.T)
req_y_axis = []
for entr in req_org:
    req_y_axis.append(dict_names[entr])

cg = sns.heatmap(scfaonly.T,cbar=False, vmin=0, vmax=2, cmap='Oranges', square=True, linewidths=1, linecolor='black', yticklabels=yaxisnames, xticklabels=req_y_axis)
plt.xticks(style='italic', size=12,  fontname="Arial") #,size='large')
plt.yticks(style='italic', size=12,  fontname="Arial")#,size='large')
plt.xlabel('(from)', weight='bold')
plt.ylabel('(to)', weight='bold')