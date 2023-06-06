import numpy as np
import pandas as pd
import glob
import os
import sys
import re
from datetime import datetime

dt = pd.to_datetime("2022-08-10")

print(dt)
print(type(dt))

df = pd.DataFrame.from_dict({
    'DateTime': ['2022-01-01 15:34:21', '2022-02-03 10:13:45', '2022-03-04 12:12:45', '2022-04-03 14:45:23', '2022-05-27 18:23:45'],
    'Name': ['Nik', 'Kate', 'Lou', 'Samrat', 'Jim'],
    'Age': [33, 32, 45, 37, 23]
})
df['DateTime'] = pd.to_datetime(df['DateTime'])

print(df)

print(df["DateTime"].dt.date)

print(type(df["DateTime"].dt.date))
print(df["DateTime"].dt.date[0])
print(type(df["DateTime"].dt.date[0]))

print(type(df["DateTime"].dt.date.astype(str)))
print(df["DateTime"].dt.date.astype(str)[0])
print(type(df["DateTime"].dt.date.astype(str)[0]))