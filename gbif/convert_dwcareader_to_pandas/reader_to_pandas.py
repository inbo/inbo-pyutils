# -*- coding: utf-8 -*-
"""
Read a DwcA using the DwcA reader and
extract the core as a pandas dataframe
for further analysis

@author: stijn_vanhoey
"""

import pandas as pd
from dwca.read import DwCAReader


dwca_name = './broedvogel_example_subset.zip'
with DwCAReader(dwca_name) as dwca:

    #get the location of the core file, stored in temporary folder
    path = dwca.absolute_temporary_path('occurrence.txt')

    # read the core as dataframe
    core_df = pd.read_csv(path, delimiter="\t")

# further analysis with the df:
print(core_df.head())
