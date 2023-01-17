import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

import Raw_Data.configurations as cfg


def numerical_interpolation(original_data, original_time, new_time, kind):
    data_array = np.array(original_data)

    f = interp1d(original_time, data_array, kind=kind)
    interpolated_data = f(new_time)

    return interpolated_data


def categorical_interpolation(original_data, original_time, new_time):
    range_max = lambda x: min(x, len(original_data))

    interpolated_data = []
    interpolated_data.append(original_data[0])
    last_index = original_time[0]

    for i, time_frame in enumerate(new_time[1:]):
        search_space_end = range_max(last_index+cfg.search_lookup_const)
        original_time_search_space = original_time[last_index: search_space_end]

        original_time_search_space = original_time_search_space.copy() - time_frame
        closest_index = np.abs(original_time_search_space).argmin()
        closest_index += last_index
        last_index = closest_index

        interpolated_data.append(original_data[last_index])

    interpolated_data = np.array(interpolated_data)
    return interpolated_data



def signal_interpolation(series_data, original_time, new_time, kind):
    original_data = np.array(series_data)
    if series_data.dtype == 'object':
        interpolated_data = categorical_interpolation(original_data=original_data, original_time=original_time,
                                                      new_time=new_time)
    else:
        interpolated_data = numerical_interpolation(original_data=original_data, original_time=original_time,
                                                    new_time=new_time, kind=kind)
    return interpolated_data


def interpolate(data):
    kind = 'cubic'
    if cfg.pathes.trial_mode.startswith('pupil'):
        kind = 'linear'

    original_time = np.array(data['timestamp'])
    new_time = np.arange(0, original_time[-1], cfg.rate_hz)

    new_data = [new_time]

    for (name, series_data) in data.iteritems():
        # we don't interpolate timestamp column
        if name == 'timestamp':
            continue

        interpolated_data = signal_interpolation(series_data=series_data, original_time=original_time,
                                                 new_time=new_time, kind=kind)
        new_data.append(interpolated_data)

    new_data = np.array(new_data).T
    new_data = pd.DataFrame(new_data, columns=data.columns)

    return new_data


def data_interpolation(data):
    for i, (_, df) in enumerate(data):
        data[i] = (data[i][0], interpolate(df))

    return data
