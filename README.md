
# Read from a local copy of CMEMS datasets

`lcmems` allows to browse through and read data from a local copy of the data files, typically downloaded with `copernicusmarine.get()`. Indeed, for large jobs, downloading the whole archive and working from it is often faster than working fully online.


## Installation

Install `lcmems` from this repository

    pip3 install git+https://github.com/jiho/lcmems

This should install other python packages `lcmems` depends on. 

# Usage

`open_dataset()` queries a dataset and returns the result as an `xarray.DataSet`
