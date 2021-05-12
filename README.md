This folder contains all the codes and the files required to generate the images in the paper titled  **Unraveling microbial interactions in the gut microbiome**

## Before running the codes
Unzip the contents of ``XML.zip`` folder.
`XML.zip` will have one folder named `XML`.

## Codes and their description
1. `check_scope_double_graphs.py` - Computes the metabolic scope of joint metabolic networks. 
Input required - Bipartite network of individual organisms and the joint organisms (found inside `FinalSingle` & `FinalDouble` folder respectively), seed metabolites (which can be found inside `MediaConditions` folder, Names of all organisms used (`all_models_FINAL.txt`)
2. `check_scope_single.py` -Computes the metabolic scope of single metabolic networks. 
Input required - Bipartite network of individual organisms (found inside `FinalSingle` folder), seed metabolites (which can be found inside `MediaConditions` folder, Names of all organisms used (`all_models_FINAL.txt`)
3. `find_msi.py` - Computes the metabolic support index of the 52 organism combinations.
4. `msi_box_plot_based_on_org_benefit.R` - Uses the output from (3) and computes the statistical significances of MSI values and produce Fig 1 in main manuscript.
5. `find_increase_in_amino_acid_prod_minglc.py` - Computes the increase in amino acids produced in minimal glucose conditions by one organism in the presence of the other.
6. `draw_circled_heatmap.R` - Uses the output from 3 to draw the circled heatmap (Fig 4 in main manuscript).
7. `get_bar_plot_metexc.R` - Produces Fig 5.
8. `get_unique_metabolic_exchanges.py` - Produces Fig 6 and 7. 
9. `create_graph.py` - Creates the joint and single bipartite graphs of organisms in `XML` folder.
10. `find_pathways_from_medium.py` - Computes all the pathways between the seed metabolites and all the metabolites in scope.

## Other data files
1. `Association_Network_Edges_in_both_DMEM_and_HF.txt` - Edge list file which was used to generate Fig 3.
2. `metexc_dmem_withoutorgnames.csv` & `metexc_hf_withoutorgnames.csv` - Metabolites exchanged between 52 organisms on DMEM and HF conditions respectively.
3. `metexc_scfa.csv` - Number of short-chain fatty acids exchanged between the organisms (if any)
4. `scoperesFinal` - Has 4 files of metabolic scope of joint and individual microbes (one with organism identifier, other with just the name).
5. `MSIResults` - Used by `msi_box_plot_based_on_org_benefit.R` to generate Fig 1.
6. `MediaConditions` - Has all the seed metabolite constituents of DMEM, HF and minimal glucose conditions.

## Citation
Aarthi Ravikrishnan & Karthik Raman, Unraveling microbial interactions in the gut microbiome __(submitted for publication)__