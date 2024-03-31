import os
import pandas as pd

# root='/remote/complex/home/share/cmems_new/'

def list_products(root):
    """List products present in `root`
    
    Products should be downloaded with the `get` argument of the copernicusmarine command line utility.
    
    Args:
        root (str): path where products have been dowloaded
        
    Returns:
        pandas.DataFrame with columns
            product : name of the product
            path    : full path to the product
    """
    products = next(os.walk(root))[1]
    products.sort()
    products = pd.DataFrame({'product':products, 'path':[os.path.join(root, p) for p in products]})
    return(products)

def list_datasets(root):
    """List datasets (and products) present in `root`
    
    Datasets should be downloaded with the `get` argument of the copernicusmarine command line utility.
    
    Args:
        root (str): path where datasets have been dowloaded
        
    Returns:
        pandas.DataFrame with columns
            dataset : name of the dataset
            product : name of the product that contains this dataset
            path    : full path to the dataset
    """
    products = next(os.walk(root))[1]
    datasets = [
        pd.DataFrame(
            {'dataset':next(os.walk(root+'/'+p))[1],
             'product': p,
             'path':[os.path.join(root, p, d) for d in next(os.walk(root+'/'+p))[1]]}
        ) for p in products
    ]
    datasets = pd.concat(datasets)
    return(datasets)
