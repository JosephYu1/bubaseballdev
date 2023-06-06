import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

df = px.data.iris()
print(df.head())

print(df["species"].unique())

df2 = df[df["species"] == "setosa"]
print(df2.head())


#----------------

base_path = r"./data_combined/"
date_str = r"20230327" # NOTE: change this here for the correct date of file (should be whatever that is latest)
filename_postfix = r'-combined-all.csv'

file_path = base_path + date_str + filename_postfix
print(f'''{file_path}''')

BASEBALL_ALL_DF = pd.read_csv(file_path, parse_dates=["Date_datetime", "Datetime"])

print(BASEBALL_ALL_DF.columns)

print(BASEBALL_ALL_DF["Date_datetime"].unique())

print(BASEBALL_ALL_DF["Date_datetime"] > '2022-10-18')

print(BASEBALL_ALL_DF["Date_datetime"].unique()[10])

print(BASEBALL_ALL_DF["Date_datetime"] > BASEBALL_ALL_DF["Date_datetime"].unique()[10])

print("\n\n-----------------")

mask = (BASEBALL_ALL_DF["Date_datetime"] >= BASEBALL_ALL_DF["Date_datetime"].unique()[10]) & (BASEBALL_ALL_DF["Date_datetime"] <= BASEBALL_ALL_DF["Date_datetime"].unique()[12])
print(mask)
print(BASEBALL_ALL_DF.loc[mask, :])

# method 2 using between
print("----between------------\n\n")

print(BASEBALL_ALL_DF.loc[BASEBALL_ALL_DF["Date_datetime"].between(
        BASEBALL_ALL_DF["Date_datetime"].unique()[10], 
        BASEBALL_ALL_DF["Date_datetime"].unique()[12]
        )
    ])

#------ test using the full datetime instead of just Date_datetime
print("----full datetime testing------------\n\n")
print(BASEBALL_ALL_DF.loc[BASEBALL_ALL_DF["Datetime"].between(
        BASEBALL_ALL_DF["Date_datetime"].unique()[10], 
        BASEBALL_ALL_DF["Date_datetime"].unique()[12]
        )
    ])

# ------- sorting
print("---sorting using dataframe-------\n\n")
df_asc = BASEBALL_ALL_DF.sort_values(by = "Date_datetime")
print(type(df_asc))
print(df_asc)
print(type(df_asc["Date_datetime"][0]))
print(df_asc["Date_datetime"][0])
print(BASEBALL_ALL_DF.sort_values(by = "Date_datetime", ascending= False))
print("----datetime type")
print(BASEBALL_ALL_DF["Date_datetime"].dtype)
print(BASEBALL_ALL_DF.dtypes)
print("---unique using np-------")
print(BASEBALL_ALL_DF["Date_datetime"].unique())
print(type(BASEBALL_ALL_DF["Date_datetime"].unique()))
print(type(BASEBALL_ALL_DF["Date_datetime"].unique()[0]))
print("---unique using pd-------") # keeping it in pd is better, since np convert type of the result
pd_uni = pd.unique(BASEBALL_ALL_DF["Date_datetime"])
print(pd_uni)
print(type(pd_uni))
print(type(pd_uni[0]))
print("\n---------sort")
sorted = np.sort(pd_uni)
print(type(sorted))
print(sorted)
print(sorted[0])
print(type(sorted[0]))

# to str
print("-------to str from datetime-----------\n\n")
print(sorted[0].astype(str))
print(df_asc["Date_datetime"][0].strftime("%Y/%m/%d"))
# use unique() to get selection options, but when converting to a string, the best option is to use strftime, 
# but this only works on TimeStamp or pandas.series.dt object! after using unique(), it converts into numpy.datetime64, which has no such function!

# but wait, there's moooooooooorrrreee!
print("---------numpy datetime_as_string------")
print(np.datetime_as_string(sorted[0], unit = 'D')) # big D is for day!

# ---

print("---------dt?----------")
print(df_asc["Datetime"].dt.strftime("%Y/%m/%d")) # this works
# print(df_asc["Datetime"].strftime("%Y/%m/%d")) # this no work