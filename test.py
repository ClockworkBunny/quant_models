import pandas as pd
from custombar import TickBar
toy_data = "..//data//interim//IVE_tickbidask.parq"
df = pd.read_parquet(toy_data)
df.reset_index(inplace=True)
df = df[['dates', 'price', 'v']]
colmap = {"dates":"datetime","v": "volume"}

print(df.head())
d = TickBar(5, colmap)
print(d.threshold)
new_df = d.transform(df)
print('sampled df')
print(new_df.head())