# This script loads in the catalog csv and outputs another catalog csv with completed fields flagged
# Can be run out of terminal or by calling the function beneath its definition

import os
import sys
import numpy as np
import pandas as pd
from pathlib import Path

# Getting current path
parent = Path(__file__).resolve().parent
# Moving to location of script
os.chdir(parent)


def return_cat(catalog, comp_fields, outfile):


    # Opening the catalog file
    type_dict = {'target_number':np.float32, 'target_name':np.float32, 'DEC_name':np.float32, 'RA_name':np.float32\
        , 'RA_actual':np.float32, 'DEC_actual':np.float32, 'obs_complete_flag':np.float32, 'target_notes':np.unicode_}

    coords = pd.read_csv(f'{catalog}', header=0, dtype=type_dict)
    coord_dat = coords.to_numpy(dtype=object)

    new_comp = np.genfromtxt(f'{comp_fields}', dtype=np.float32)


    comp_flag = np.zeros_like(coord_dat[:,7])

    # This loop adds a flag to 
    for i in new_comp:
        ptr = np.where((i) == coord_dat[:,2])
        comp_flag[ptr] = 1


    # Creating DataFrame to then save as csv
    dataset = pd.DataFrame({'field': coord_dat[:, 2], 'RA': coord_dat[:, 4], 'DEC': coord_dat[:, 6],  'obs_comp': comp_flag})
    dataset.to_csv(f'{outfile}')

# cat_path should be the filepath to the catalog file, in this case 'MDW_survey_coordinates_pyedit.csv'
# comp_fields is a txt file list of the completed fields as of Dec 24, it can be substituted for any similarly formatted txt file
# outfile is the name + path of where you want to save the updated catalog


# Below is the example, uncomment to test
# cat = 'MDW_survey_coordinates_pyedit.csv'
# comp = 'comp_fields_dec24_reformatted.txt'
# out_fname = 'catalog_w_compflag.csv'
# return_cat(cat, comp, out_fname)
