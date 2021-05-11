# -*- coding: utf-8 -*-
"""
This code creates the joint bipartite graph of all combinations of 52 organisms
present in the folder XML (Change this path appropriately).

@author: Aarthi Ravikrishnan
"""

import metquest
pathname_with_files = 'XML\\'
no_of_orgs = 2
metquest.construct_graph.create_graph(pathname_with_files, no_of_orgs)




