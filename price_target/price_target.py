import pandas as pd
import numpy as np
import h5py
import configs
import re
import math

def hdf5_to_dataframe(h5_path):
    with h5py.File(h5_path, 'r') as h:
        data = h['data'][...]
        permno = h['permno'][...]
        date = pd.to_datetime([str(x) for x in h['date'][...]])
        # date = h['date'][...]
    return pd.DataFrame(data, pd.Index(date, name='date'),
                        pd.Index(permno, name='permno'))



adj_close = hdf5_to_dataframe('../hdf5/adj_close.h5')

identifiers = pd.read_csv("stock_identifiers.csv")
identifiers["cusip"] = [x[:-1] for x in identifiers["cusip"].tolist()]
identifiers_by_cusip = identifiers.groupby("cusip")


targets = pd.read_csv("Summary_History_Price_Target_Unadjusted.csv")
targets["PERMNO"] = ""
targets["close_px"] = math.nan
targets["up_down_price_target"] = math.nan

for idx, row in targets.iterrows():
    cusip = row["CUSIP"] ; 
    date = str(row["STATPERS"]) ; date = date[:4]+"-"+ date[4:6] +"-" + date[6:]
    permno = identifiers_by_cusip.get_group(cusip)["PERMNO"].tolist()[0]; 
    try:
        targets.at[idx,"PERMNO"] = permno
        targets.at[idx,"close_px"] = adj_close[permno].loc[date]
        targets.at[idx,"up_down_price_target"] = (row["MEANPTG"]-adj_close[permno].loc[date])/adj_close[permno].loc[date]
    except Exception as e:
        pass
    if (idx+1)%10000==0:
        print((idx+1)/targets.shape[0])


targets["STATPERS"] = [str(date)[:4]+"-"+ str(date)[4:6] +"-" + str(date)[6:] for date in targets["STATPERS"]]
targets.dropna().to_csv("Up_Down_Price_Target.csv")



