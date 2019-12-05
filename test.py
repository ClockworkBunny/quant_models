import pandas as pd
from custombar import TickBar
toy_data = "..//data//interim//IVE_tickbidask.parq"
df = pd.read_parquet(toy_data)
print(df.head())
d = TickBar()
print(d.threshold)