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
    # TODO check that there are as many index files are directories = that the index is complete/up to date

    # read all index files
    def read_index(f):
        with open(f, 'rb') as fh:
            ds = pickle.load(fh)
        return(ds)
    index = [read_index(f) for f in index_files]

    # concatenate them into one index for the whole dataset
    ds = xr.concat(index, dim='time')

    return(ds)
