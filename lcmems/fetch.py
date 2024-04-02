import numpy as np
from .subset import subset_data

def fetch_data(
    dataset,
    datetime, lon, lat,
    variables=None,
    space_buffer=0.5,
    datetime_buffer=0,
    **kwargs):
    """Get a cube of data from CMEMS
    
    Args:
        dataset: object returned by open_dataset().
        datetime (datetime64[ns],str): target date (and time). When specified
          as a string, should be YYYY-MM-DD, possibly with HH:MM:SS. When not a
          string it should be a datetime64[ns] object (from numpy).
        variables (str, list[str]): names of the variables to extract. Default: all.
        lon,lat (float): target coordinates.
        space_buf (float, list[2]): buffer around lon,lat in degrees. If it is a
          single number, the same buffer will be applied to both sides of the 
          target point. If it is a list it needs to be of length 2 and specify the
          buffer before and after the point.
        date_buf (int, list[2]): buffer around the target date in days. As above
          if it is a single number it will be applied to both sides of date. Otherwise
          it needs to be a list of length 2 that specifies the number of days
          before and after the target date
        **kwargs: passed to lcmems.subset_data()

    Returns:
        A xarray.DataArray() containing the data, with coodinates: variables, 
        time, longitude, latitude. The data can be included (load = True) or
        lazyly loaded (load = False).
    """
    
    # deal with var specified as string

    # parse date when it is a string
    if isinstance(datetime, str):
        datetime = np.array([datetime]).astype('datetime64[ns]')

    # make space_buf a list of length 2
    if (isinstance(space_buffer, list)):
        if (len(space_buffer) != 2):
            raise ValueError("space_buffer should be a list of length 2")
    else:
        # replicate the value on either side
        space_buffer=[space_buffer,space_buffer]
    # TODO We would likely prefer to do this in km, not degrees.
    #      That would require to compute the bounds in lon-lat using
    #      e.g. geopy.distance.Distance.destination in the 4 directions
  
    # do the same with datetime_buffer
    if (isinstance(datetime_buffer, list)):
        if (len(datetime_buffer) != 2):
            raise ValueError("datetime_buffer should be a list of length 2")
    else:
        datetime_buffer=[datetime_buffer,datetime_buffer]
    
    da = subset_data(
        dataset=dataset,
        variables=variables,
        minimum_longitude = lon - space_buffer[0],
        maximum_longitude = lon + space_buffer[1],
        minimum_latitude = lat - space_buffer[0],
        maximum_latitude = lat + space_buffer[1],
        start_datetime = datetime - np.timedelta64(datetime_buffer[0], 'D'),
        end_datetime = datetime + np.timedelta64(datetime_buffer[1], 'D'),
        **kwargs
    )
    return(da)
    