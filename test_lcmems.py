# make it work with files on mounted NFS drives
import os
os.environ['HDF5_USE_FILE_LOCKING']='FALSE'

# import and reload the latest changes from the local directory
from importlib import reload
import lcmems
reload(lcmems)

# list products and datasets
root = '/remote/complex/home/share/cmems_new'
lcmems.list_products(root)
dsl = lcmems.list_datasets(root)
dsl

# index products
lcmems.index_dataset(dsl.path[3])

# open a dataset
ds = lcmems.open_dataset(dsl.path[0])
ds

# get a subset of a dataset
da = lcmems.subset_data(ds,
    variables='RRS412',
    minimum_longitude = -16,
    maximum_longitude = -15,
    minimum_latitude = 10,
    maximum_latitude = 11,
    start_datetime = '2024-02-01',
    end_datetime = '2024-02-03'
)
from matplotlib import pyplot as plt
da[0,2,:,:].plot()
plt.show()
