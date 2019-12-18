"""
import pandas as pd
from custombar import TickBar, Imbalance_Bar, Imbalance_Run_Bar
toy_data = "..//data//interim//IVE_tickbidask.parq"
df = pd.read_parquet(toy_data)
df.reset_index(inplace=True)
df = df[['dates', 'price', 'v']]
colmap = {"dates":"datetime","v": "volume"}

d = Imbalance_Run_Bar(dictcol=colmap, mode='volume', exp_num_ticks_init=100)
new_df = d.transform(df)
print(new_df.head())
"""
import sys
print(sys.path)