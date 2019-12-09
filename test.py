import pandas as pd
from custombar import TickBar, Imbalance_Bar
toy_data = "..//data//interim//IVE_tickbidask.parq"
df = pd.read_parquet(toy_data)
df.reset_index(inplace=True)
df = df[['dates', 'price', 'v']]
colmap = {"dates":"datetime","v": "volume"}

d = Imbalance_Bar(dictcol=colmap, mode='volume')
new_df = d.transform(df)
print(df.head())
