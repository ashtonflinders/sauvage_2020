import os
import numpy as np
from netCDF4 import Dataset

def BST_array(BST_file, set_southern_ooze = True, outdir = './output'):
    '''
    Calculate a simplified six-category bottom sediment type dataset from the preprocessed
    NAVO BST dataset;
    
    Naval Oceanographic Office. Database description for bottom sediment type.
    OAML-DBD-86, Stennis Space Center, Mississsippi: Acoustics Division (2003).
    
    https://www.oc.nps.edu/~bird/oc2930/sediments/Bottom_Sediment_Type_dbdd_navo.doc
    
    The six categories are: lithogenous, si_ooze, ca_ooze, marl, clay, other. We define
    new numeric identifiers for each category. If these are changed you also have to change
    the corresponding values in get_sediment_parameters.py!
    '''
    lith_simplified={'lithogenous':1, 'si_ooze':2, 'ca_ooze':3, 'marl':4, 'clay':5, 'other':6}

    if os.path.exists(os.path.join(outdir, 'lithology.np')):
        os.remove(os.path.join(outdir, 'lithology.np'))
    
    if os.path.exists(os.path.join(outdir, 'lats.np')):
        os.remove(os.path.join(outdir, 'lats.np'))
    
    if os.path.exists(os.path.join(outdir, 'lons.np')):
        os.remove(os.path.join(outdir, 'lons.np'))

    lithology = Dataset(BST_file, mode = 'r')
    lith_lons = np.ma.filled(lithology.variables['lon'][:],None)
    lith_lats = np.ma.filled(lithology.variables['lat'][:],None)
    lith = lithology.variables['z'][:]
    lithology.close()

    '''
    The following numbers refer to the NAVO seafloor bottom sediment type (BST)
    database, "Enhanced" category number.
    '''
    for p in np.nditer(lith.data, op_flags = ['readwrite']):
        if 102 <= p <=	197:
            p[...] = lith_simplified['lithogenous']
        elif 202 <= p <=	209:
            p[...] = lith_simplified['ca_ooze']   
        elif p == 211:
            p[...] = lith_simplified['marl']       
        elif 212 <= p <=	310:
            p[...] = lith_simplified['ca_ooze']   
        elif 405 <= p <=	511:
            p[...] = lith_simplified['si_ooze']
        elif 706 <= p <=	708:
            p[...] = lith_simplified['clay']
        elif 802 <= p <=	807:
            p[...] = lith_simplified['lithogenous']                         
        elif p == 888:
            p[...] = lith_simplified['other']                 
        elif p == 999:
            p[...] = np.Nan      
        elif 1101 <= p <= 1199:
            p[...] = lith_simplified['lithogenous']   
        elif 1201 <= p <= 1207:
            p[...] = lith_simplified['ca_ooze']     
        elif p == 1208 :
            p[...] = lith_simplified['marl']   
        elif 1209 <= p <= 1210:
            p[...] = lith_simplified['ca_ooze']   
        elif p == 1211:
            p[...] = lith_simplified['marl']   
        elif 1212 <= p <= 1241:
            p[...] = lith_simplified['ca_ooze']         
        elif p == 1242:
            p[...] = lith_simplified['marl']   
        elif 1243 <= p <= 1299:
            p[...] = lith_simplified['ca_ooze']               
        elif 1405 <= p <= 1511:
            p[...] = lith_simplified['si_ooze']   
        elif 1802 <= p <= 1875:
            p[...] = lith_simplified['lithogenous']                 
        elif 2205 <= p <= 2209:
            p[...] = lith_simplified['ca_ooze']   
        elif p == 2211:
            p[...] = lith_simplified['marl']                   
        elif 2405 <= p <= 2408:
            p[...] = lith_simplified['si_ooze']   
        elif p == 2210:
            p[...] = lith_simplified['ca_ooze']               
        elif 2603 <= p <= 2682:
            p[...] = lith_simplified['lithogenous']   
        elif 3201 <= p <= 3207:
            p[...] = lith_simplified['ca_ooze']
        elif p == 3208:
            p[...] = lith_simplified['marl']      
        elif 3209 <= p <= 3299:
            p[...] = lith_simplified['ca_ooze']       
        elif 3301 <= p <= 3897:
            p[...] = lith_simplified['lithogenous']                    
        elif p == 3510:
            p[...] = lith_simplified['si_ooze']  
        elif p == 9999:
            p[...] = lith_simplified['other']
        elif p != p:
            p[...] = np.NaN
        else:
            p[...] = lith_simplified['other']

    lith = lith.data

    # For the Southern Ocean, between latitude 57-66 S, add an opal belt (siliceous ooze)
    if set_southern_ooze:
        southern_ocean_boundary = [-57, -66]
        n_socean_idx = (np.abs(lith_lats - southern_ocean_boundary[0])).argmin()                                                                        
        s_socean_idx = (np.abs(lith_lats - southern_ocean_boundary[1])).argmin()

        for y in np.arange(s_socean_idx, n_socean_idx + 1):
            for x in np.arange(lith.shape[1]):
                if lith[y][x] != 0:
                    lith[y][x] = lith_simplified['si_ooze']

    return lith, lith_lats, lith_lons