import os
from pathlib import Path
import numpy as np
import pandas as pd
from astropy import units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt


# Getting current path
parent = Path(__file__).resolve().parent
# Moving to location of script
os.chdir(parent)

def make_map(catalog, outfile):

    type_dict = {'field':np.int64, 'RA':np.float32, 'DEC':np.float32, 'obs_comp':np.float32}

    # This is the udpated catalog
    coords = pd.read_csv(catalog, header=0, dtype=type_dict)
    coord_dat = coords.to_numpy(dtype=object)


    # Creating skycoord object
    c = SkyCoord(ra=coord_dat[:,2]*u.hourangle, dec=coord_dat[:,3]*u.deg, frame='icrs')


    width = 3.214*u.deg # This is approximate
    height = 3.225*u.deg
    up_width = 5.29*u.deg # Also approximate, so there aren't gaps on the heigher dec fields

    # Creating plot
    fig = plt.figure(figsize=(15,10))
    plt.tight_layout()
    ax = plt.subplot(111, projection="aitoff")
    plt.title("Map of completed regions (ICRS)")
    plt.grid(True)
    plt.subplots_adjust(top=0.95,bottom=0.0)

    # Looping to plot all points
    for idx, val in enumerate(c):


        if val.dec >= 45*u.deg:
            ur = SkyCoord(ra=val.ra + (up_width/2), dec= val.dec + (height/2))
            ul = SkyCoord(ra=val.ra - (up_width/2), dec= val.dec + (height/2))
            br = SkyCoord(ra=val.ra + (up_width/2), dec= val.dec - (height/2))
            bl = SkyCoord(ra=val.ra - (up_width/2), dec= val.dec - (height/2))

        else:
            ur = SkyCoord(ra=val.ra + (width/2), dec= val.dec + (height/2))
            ul = SkyCoord(ra=val.ra - (width/2), dec= val.dec + (height/2))
            br = SkyCoord(ra=val.ra + (width/2), dec= val.dec - (height/2))
            bl = SkyCoord(ra=val.ra - (width/2), dec= val.dec - (height/2))

        y = [ur.dec.radian, ul.dec.radian, bl.dec.radian, br.dec.radian]
        x = [ur.ra.wrap_at(180 * u.deg).radian, ul.ra.wrap_at(180 * u.deg).radian, \
        bl.ra.wrap_at(180 * u.deg).radian, br.ra.wrap_at(180 * u.deg).radian]
        

        if coord_dat[idx,4] == 1:

            plt.fill(x, y, alpha=0.6, color='#0585ed', label='Observations Complete') 
        else:        
            plt.fill(x, y, alpha=0.1, color='#DC267F', label='Observations Incomplete')

        
    # plt.show()
    plt.savefig(outfile) 

# This is the example
# cat = 'catalog_w_compflag.csv'
# out = 'completed_fields.png'
# make_map(cat, out)
