import os

import pandas as pd
import numpy as np

import numerox as nx

TEST_DATA = os.path.join(os.path.dirname(__file__), 'tests', 'test_data.hdf')


def shares_memory(data1, data_or_array2):
    "True if `data1` shares memory with `data_or_array2`; False otherwise"
    isdata_like = isinstance(data_or_array2, nx.Data)
    isdata_like = isdata_like or isinstance(data_or_array2, nx.Prediction)
    for col in data1._column_list():
        a1 = data1.df[col].values
        if isdata_like:
            a2 = data_or_array2.df[col].values
        else:
            a2 = data_or_array2
        if np.shares_memory(a1, a2):
            return True
    return False


def load_play_data():
    return nx.load_data(TEST_DATA)


def update_play_data(numerai_zip_path):
    data = nx.load_zip(numerai_zip_path)
    play = nx.row_sample(data, fraction=0.01, seed=0)
    play.save(TEST_DATA)


def assert_data_equal(data1, data2, msg=None):
    "Assert that two data objects are equal"
    try:
        pd.testing.assert_frame_equal(data1.df, data2.df)
    except AssertionError as e:
        # pd.testing.assert_frame_equal doesn't take an error message as input
        # so let's hack our own
        if msg is not None:
            msg = '\n\n' + msg + '\n\n' + e.args[0]
            e.args = (msg,)
        raise


def micro_data(index=None, nfeatures=3):
    "Returns a tiny data object for use in unit testing"
    cols = ['era', 'region']
    cols += ['x' + str(i) for i in range(1, nfeatures + 1)]
    cols += ['y']
    df = pd.DataFrame(columns=cols)
    df.loc['index0'] = ['era1', 'train'] + [0.0] * nfeatures + [0.]
    df.loc['index1'] = ['era2', 'train'] + [0.1] * nfeatures + [1.]
    df.loc['index2'] = ['era2', 'train'] + [0.2] * nfeatures + [0.]
    df.loc['index3'] = ['era3', 'valuation'] + [0.3] * nfeatures + [1.]
    df.loc['index4'] = ['era3', 'valuation'] + [0.4] * nfeatures + [0.]
    df.loc['index5'] = ['era3', 'valuation'] + [0.5] * nfeatures + [1.]
    df.loc['index6'] = ['era4', 'valuation'] + [0.6] * nfeatures + [0.]
    df.loc['index7'] = ['eraX', 'test'] + [0.7] * nfeatures + [1.]
    df.loc['index8'] = ['eraX', 'test'] + [0.8] * nfeatures + [0.]
    df.loc['index9'] = ['eraX', 'live'] + [0.9] * nfeatures + [1.]
    if index is not None:
        df = df.iloc[index]
    data = nx.Data(df)
    return data
