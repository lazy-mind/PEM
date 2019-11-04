import h5py
import pandas as pd

def save_to_hdf5(dataframe, dataset_name, path='.'):
    df = dataframe.sort_index(axis=0).sort_index(axis=1)
    with h5py.File(f'{path}/{dataset_name}.h5', 'w') as h:
        h.create_dataset('data', dtype='f', data=df.values)
        h.create_dataset('permno', dtype='i', data=df.columns.get_level_values('permno').values.astype(int))
        h.create_dataset('date', dtype='i', data=[int(pd.Timestamp(x).strftime('%Y%m%d')) for x in df.index.values])
        
def hdf5_to_dataframe(h5_path):
    with h5py.File(h5_path, 'r') as h:
        data = h['data'][...]
        permno = h['permno'][...]
        date = pd.to_datetime([str(x) for x in h['date'][...]])
    return pd.DataFrame(data, pd.Index(date, name='date'),
                        pd.Index(permno, name='permno'))
