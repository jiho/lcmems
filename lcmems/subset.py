import xarray as xr
import numpy as np

def subset_data(
    dataset,
    variables = None,
    minimum_longitude = None,
    maximum_longitude = None,
    minimum_latitude = None,
    maximum_latitude = None,
    start_datetime = None,
    end_datetime = None,
    load = True
):
    # TODO add depth
    """Extract a subset of data from a dataset

    Args:
        dataset: object returned by open_dataset().
        variables (str, list[str]): names of the variables to extract. Default: all.
        minimum_longitude (float)
        maximum_longitude (float): longitude range to extract. In [-180, 180].
        minimum_latitude (float)
        maximum_latitude (float): latitude range to extract. In [-90, 90].
        start_datetime
        end_datetime (datetime64[ns],str): time range to extract. When specified
          as a string, should be YYYY-MM-DD, possibly with HH:MM:SS. When not a
          string it should be a datetime64[ns] object (from numpy).
        load (boolean): when True (the default) actually load the data from disk.
          When False, the array is created in a lazy manner and data is read only
          when accessed (which requires the data to still be present).

    Returns:
        A xarray.DataArray() containing the data, with coodinates: variables, 
        time, longitude, latitude. The data can be included (load = True) or
        lazyly loaded (load = False).
    """

    ## Check arguments

    # if None, select all
    if variables is None:
        variables = list(dataset.data_vars)
    # variables need to be iterable => wrap into list
    elif isinstance(variables, str):
        variables = [variables]

    # check geographic boundaries
    def check_bounds(x, min_x, max_x):
        if x > max_x:
            x = max_x
        elif x < min_x:
            x = min_x
        return(x)

    if minimum_longitude is None:
        minimum_longitude = np.min(dataset.longitude.values)
        # NB: could also hardcode -180...
    else:
        minimum_longitude = check_bounds(minimum_longitude, -180, 180)
    if maximum_longitude is None:
        maximum_longitude = np.max(dataset.longitude.values)
    else:
        maximum_longitude = check_bounds(maximum_longitude, -180, 180)

    if minimum_latitude is None:
        minimum_latitude = np.min(dataset.latitude.values)
    else:
        minimum_latitude = check_bounds(minimum_latitude, -90, 90)
    if maximum_latitude is None:
        maximum_latitude = np.max(dataset.latitude.values)
    else:
        maximum_latitude = check_bounds(maximum_latitude, -90, 90)

    # check date and time
    if start_datetime is None:
        start_datetime = np.min(dataset.time.values)
    # parse the string
    elif isinstance(start_datetime, str):
        start_datetime = np.array([start_datetime]).astype('datetime64[ns]')
    if end_datetime is None:
        end_datetime = np.max(dataset.time.values)
    elif isinstance(end_datetime, str):
        end_datetime = np.array([end_datetime]).astype('datetime64[ns]')


    ## Select range of coordinates to extract

    selected_lon = dataset.longitude[
        (dataset.longitude >= minimum_longitude) &
        (dataset.longitude <= maximum_longitude)]
    selected_lat = dataset.latitude[
        (dataset.latitude  >= minimum_latitude ) &
        (dataset.latitude  <= maximum_latitude )]
    selected_time = dataset.time[
        (dataset.time >= start_datetime) &
        (dataset.time <= end_datetime  )]

    # check amount of data to be read
    n_values = len(variables) * len(selected_time) * len(selected_lon) * len(selected_lat)
    # refuse if this is too many
    if (n_values > 3*10**6):
        raise ValueError('You are trying to extract ' + str(n_values) + ' values, which is too many. Reduce the dimensions of the array to be extracted.')


    ## Extract and reformat data
    # per variable
    d_sel = [dataset[variable].sel(indexers={
        'time': selected_time,
        'longitude': selected_lon,
        'latitude': selected_lat}) for variable in variables]
    # combine in a single array (like copernicusmarine.open_dataset())
    # NB: only keep common attributes
    d_sel = xr.concat(d_sel, dim='variable', combine_attrs='drop_conflicts')
    # define the variables as an explicit coordinate
    d_sel = d_sel.assign_coords({'variable': variables})
    # and remove the name of the array
    # (which was the name of the first variable)
    d_sel.name = None

    if load:
        # actually read the data from disk
        d_sel = d_sel.load()

    return(d_sel)


