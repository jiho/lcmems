from plotnine import ggplot,aes,geom_raster,facet_grid,scale_x_continuous,scale_y_continuous,coord_fixed

def plot_array(x):
    """Plot a data array

    Args:
        x (xarray.DataArray): a multidimensional array with dimensions
          variable, time, longitude and latitude, typically extracted by
          subset_data()

    Returns:
        A plotnine object.
    """
    df = x.to_dataframe(name='value').reset_index()
    p = ggplot(df) +\
        facet_grid('variable ~ time') +\
        geom_raster(aes(x='longitude', y='latitude', fill='value')) +\
        coord_fixed() +\
        scale_x_continuous(expand=(0,0)) + scale_y_continuous(expand=(0,0))

    return(p)
