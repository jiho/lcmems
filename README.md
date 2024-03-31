
# Access a local copy of CMEMS datasets

`copernicusmarine_local` mimics the behaviour of some functions of `copernicusmarine` but reads from a local copy of the data files, typically downloaded with `copernicusmarine.get()`. For large jobs, downloading the whole archive and working from it is faster than working fully online.


## Installation

Install `copernicusmarine_local` from this repository

    pip3 install git+https://github.com/jiho/copernicusmarine_local

This should install other python packages `apeep` depends on. 

# Usage

`open_dataset()` queries a dataset and returns the result as an `xarray.DataSet`
