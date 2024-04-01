import glob
import pickle
import xarray as xr

def open_dataset(path):
    """Open the index of a dataset

    Args:
        path (str): path to the root of the dataset.

    Returns:
        A xarray.Dataset object indexing the whole dataset.
    """
    # list all index files
    index_files = glob.glob(path+'/*_xarray.pickle')
    index_files.sort()
    # index_files

    # read all index files
    index = [pickle.load(open(f,'rb')) for f in index_files]

    # concatenate them into one index for the whole dataset
    ds = xr.concat(index, dim='time')

    return(ds)
