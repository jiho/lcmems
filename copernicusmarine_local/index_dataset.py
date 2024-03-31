import os
os.environ['HDF5_USE_FILE_LOCKING']='FALSE'

import xarray as xr
import pickle as pkl

# path = '/remote/complex/home/share/cmems_new/OCEANCOLOUR_GLO_BGC_L3_MY_009_107/c3s_obs-oc_glo_bgc-reflectance_my_l3-multi-4km_P1D_202303'

def index_dataset(path):
    """Create an xarray index of a dataset
    
    For each year, open the netCDF files as xarrays and store their structure in
    a pickle file, that can then be easily loaded
    
    Args:
        path (str): path to the dataset. See list_datasets() to discover them.
        
    Returns:
        'True' upon success. A pickle file is written per sub-directory of
        `path` (which are usually years); it contains and object of type
        xarray.Dataset which points to the data (but does not contain it)
    """
    # list all first level directories at the root
    years = next(os.walk(path))[1]
    years.sort()

    for y in years:
        print('indexing ' + y)
        ds = xr.open_mfdataset(path+'/'+y+'/*/*.nc',
                               decode_cf=False, decode_times=False,
                               join='exact',coords='minimal', compat='override')
        ds = xr.decode_cf(ds)
        with open(path+'/'+y+'_xarray.pickle', 'wb') as file:
            pkl.dump(ds, file)
    
    return(True)
