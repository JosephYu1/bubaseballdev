import pandas as pd
import numpy as np
from data_calculations import *

# ----------------------------------------
# ----- Globals and folder path ----------
# ----------------------------------------

DEBUG = True

base_path = r"./data_combined/"
date_str = r"20230418" # NOTE: change this here for the correct date of file (should be whatever that is latest)
filename_postfix = r'-combined-all.csv'
latest_file = r"latest.csv"

file_path = base_path + date_str + filename_postfix


'''
Function: get_uniques_sort_insert_top

Purpose:
This function retrieves unique values from a specified column of a given DataFrame, sorts them (optional), 
inserts a provided string at the top (optional), and returns the sorted unique values as both a NumPy array and a list of dictionaries.

Inputs:
1. df: DataFrame - The input DataFrame from which unique values are extracted.
   - State: The DataFrame should be properly initialized and contain the specified column.

2. col_str: str - The name of the column in the DataFrame from which unique values are extracted.
   - State: The column should exist in the DataFrame.

3. sort_bool: bool (optional) - A flag indicating whether the unique values should be sorted.
   - State: True or False. Default value is True if not provided.

4. insert_str: str (optional) - The string to be inserted at the top of the unique values.
   - State: Any non-empty string can be provided. Default value is an empty string if not provided.

Outputs:
1. ndarr: NumPy array - An array containing the sorted (if applicable) and unique values from the specified column.
   - State: The array will be in sorted order if sort_bool is True. Otherwise, it will retain the original order of unique values.

2. dict_list: List of dictionaries - A list of dictionaries, where each dictionary represents a unique value.
   - State: Each dictionary will have two keys: "label" and "value". The "label" key will hold the unique value, and the "value" key will also hold the unique value.
'''
def get_uniques_sort_insert_top(df, col_str, sort_bool = True, insert_str = ""):
    if sort_bool:
        ndarr = np.sort(df[col_str].unique())
    else:
        ndarr = df[col_str].unique()
    if insert_str is not None and insert_str != "":
        ndarr = np.insert(ndarr, 0, insert_str)
    dict_list = [{"label" : p, "value": p} for p in ndarr]
    return ndarr, dict_list

# -----------------------------------------------------------------------------------
# have 3 different sets of data:
# 1. all players, private and public matches
# 2. only private
# 3. only public

# NOTE: assume directory start at /capstone. rstring for literal input
# NOTE: the parse_dates is required if we want to process the column as a datetime object, otherwise it's a str object!
# for more, see: https://psgpyc.medium.com/datetime-in-pandas-read-csv-everything-you-have-to-know-8245bd048fa
BASEBALL_ALL_DF = pd.read_csv(base_path + latest_file, 
                              header=0, 
                              parse_dates=["Date_datetime", "Datetime"],
                              low_memory=False) # this is important, for some columns, even thought it's just strings and empty, they will be "mixed".
                                                # see: https://stackoverflow.com/questions/25488675/mixed-types-when-reading-csv-files-causes-fixes-and-consequences

BASEBALL_ALL_DF = BASEBALL_ALL_DF.sort_values(by = "Datetime").reset_index(drop=True) # NOTE: data will ALWAYS be sorted after this, remember to sort by Datetime, not anything else!
PLAYERS_ALL_DEFAULT_STR = "All"
PLAYERS_ALL_NDARR, PLAYERS_ALL_DICT_LIST = get_uniques_sort_insert_top(BASEBALL_ALL_DF, "Pitcher", True, PLAYERS_ALL_DEFAULT_STR)

'''
DATA CLEANSING 
'''
# CHECK THAT ONLY BAYLOR PLAYERS ARE INCLUDED
BASEBALL_ALL_DF_BAY = BASEBALL_ALL_DF[BASEBALL_ALL_DF['PitcherTeam'] == 'BAY_BEA']
# PLAYERS_BAYLOR_NDARR = np.sort(BASEBALL_ALL_DF_BAY['Pitcher'].unique())

BASEBALL_PRIVATE_DF = BASEBALL_ALL_DF[BASEBALL_ALL_DF["Public"] == 0]
# PLAYERS_PRIVATE_NDARR = np.sort(BASEBALL_PRIVATE_DF['Pitcher'].unique())

BASEBALL_PUBLIC_DF = BASEBALL_ALL_DF[BASEBALL_ALL_DF["Public"] == 1]
# PLAYERS_PUBLIC_NDARR = np.sort(BASEBALL_PUBLIC_DF['Pitcher'].unique())

# Match types
MATCH_TYPES_LIST = ["All", "Public", "Private"]
MATCH_TYPES_DICT_LIST = [{"label" : t, "value": t} for t in MATCH_TYPES_LIST]


# all attributes
ATTRIBUTES_NDARR = BASEBALL_ALL_DF.columns.values # this assumes that all files, between private and public, have the same columns
ATTRIBUTES_NDARR = np.sort(ATTRIBUTES_NDARR) # using sorted values makes it easier to look up things, despite we also have search
ATTRIBUTES_DICT_LIST = [{"label" : p, "value": p} for p in ATTRIBUTES_NDARR]
# NOTE: do NOT use this, as this can break the graphing on x or y where some value is expected. Use clearable parameter in dcc.Dropdown to allow for None.
# ATTRIBUTES_NDARR = np.append(ATTRIBUTES_NDARR, "None")

# base on the coachablility list given by Coach Furlong & Dr. Speegle
# NOTE: we skipped Tilt because the column contains data that is duplicate of SpinAxis, also the data itself can break code
COACHABLE_LIST = ['RelSpeed', 'VertRelAngle', 'HorzRelAngle', 'SpinRate', 
                  'SpinAxis','RelHeight', 'RelSide', 'Extension', 'HorzBreak', 
                  'PlateLocHeight', 'PlateLocSide', 'ZoneSpeed', 'VertApprAngle',
                  'HorzApprAngle', 'ZoneTime', 'EffectiveVelo', 'SpeedDrop']
COACHABLE_LIST = np.sort(COACHABLE_LIST)
COACHABLE_DICT_LIST = [{"label" : p, "value": p} for p in COACHABLE_LIST]

# Get all teams
TEAM_DEFAULT_STR = "BAY_BEA" # default to Baylor instead of All, because All is not as useful
ALL_TEAMS_NDARR, ALL_TEAMS_DICT_LIST = get_uniques_sort_insert_top(BASEBALL_ALL_DF, "PitcherTeam", True, "All")

# pitch types
PITCH_DEFAULT_STR = "All"
PITCH_TYPES_NDARR, PITCH_TYPES_DICT_LIST = get_uniques_sort_insert_top(BASEBALL_ALL_DF, "TaggedPitchType", True, PITCH_DEFAULT_STR)

# Pitch Calls
PITCH_CALL_DEFAULT_STR = "All"
PITCH_CALL_NDARR, PITCH_CALL_DICT_LIST = get_uniques_sort_insert_top(BASEBALL_ALL_DF, "PitchCall", True, PITCH_CALL_DEFAULT_STR)

# ---------------------------------------------------
# --- date convert for DateRange Picker use later ---
# ---------------------------------------------------
NUM2DATE = [n for n in range(len(BASEBALL_ALL_DF["Date_datetime"].unique()))]
# this function can be called later in callback for dynamic updating the date range!
# input: df_in, assume it is SORTED by datetime
# output: a list of all unique dates
def get_date2num_from_df(df_in):
    if df_in is None:
        return
    # pandas version proofing for the future
    # For older pandas (<=1.5), the two unique() returns numpy objects: numpy ndarray and numpy datetime
    # For newer pandas (>=2.0), the two unique() returns pandas objects: pandas list/series and pandas datetime
    # Here, we determine type of output from the function call to see how we should handle the output:
    # case 1: returned numpy obj after using unique:
    if isinstance(df_in["Date_datetime"].unique()[0], type(np.datetime64("2020-01-01"))):
        d2n = [np.datetime_as_string(d, unit = 'D') for d in df_in["Date_datetime"].unique()] # numpy only!
    # we consider all other cases to be case 2: returned a pandas obj using unique
    else:
        d2n = [d for d in df_in["Datetime"].dt.date.astype(str)] # The reading the Datetime col is NOT a typo, since we are calling .dt.date()
    return d2n
DATE2NUM = get_date2num_from_df(BASEBALL_ALL_DF)

# datetime data structures
# these are globals, but there are dynamic runtime functions to change them below!
# the chunk below creates 2 arrays that are the keys for each other.

# Default dates
START_DATE = "1950-01-01"
END_DATE = "2050-12-31"

# all defaults
ATTR_X_STR = 'TaggedPitchType' 
ATTR_Y_STR = 'Pitcher'
ATTR_Z_STR = 'SpinRate'
CTX_MSG_STR = ""
TS_X_STR = 'SpinRate' 
TS_Y_STR = 'RelHeight' 
TS_ANIMTION_STR = 'Inning'
TS_COLOR_TEAM_STR = 'Pitcher' 
TS_COLOR_PLAYER_STR = 'TaggedPitchType' 

# location heatmap data
LOCATION_ALL = zones_calculation(BASEBALL_ALL_DF)

# extracting column values for location data -> it has 
# an added derived column
LOCATION_COLUMNS = LOCATION_ALL.columns.values

# type locations for pitch type
PITCH_TYPE = ["All", "Fastball", "Sinker", "Cutter",
              "Curveball", "Slider",
              "Changeup", "Splitter", "Knuckleball",
              "Underfined", "Other"]
AUTO_TYPE = ["Four-Seam", "Sinker", "Cutter",
             "Changeup", "Splitter", "Slider",
             "Curveball", "Other"]

# NOTE: there are "nan" for BatterSide, which is bad and breaks the graph update! This need to be handled in data cleaning!
# TODO: add BatterSide in data cleaning
# -- old method -- use baylor df only to avoid NaN
# HAND_LIST = BASEBALL_ALL_DF_BAY["BatterSide"].unique() # NOTE: using the baylor side is important, because somehow using the entire data breaks the graph!
# --- new method -- dropna on the column to avoid NaN
HAND_LIST = BASEBALL_ALL_DF.dropna(subset=["BatterSide"])["BatterSide"].unique() # NOTE: the NaN is supposedly handled here
# HAND_LIST_BAY = BASEBALL_ALL_DF_BAY["BatterSide"].unique()
# print(f'''hand list for baylor only:\n{HAND_LIST_BAY}''')
HAND_LIST = np.append("All", HAND_LIST)
PLAYERS_LIST_NOT_ALL = BASEBALL_ALL_DF['Pitcher'].unique()
PLAYERS_LIST_ALL = np.append("All", PLAYERS_LIST_NOT_ALL)

# for datetime correction for uploaded files
DATE_DICT = {
    "yyyy/mm/dd" : "%Y/%m/%d",
    "mm/dd/yyyy" : "%m/%d/%Y",
    "dd/mm/yyyy" : "%d/%m/%Y",
}

# WOBA
WOBA_SORT_OPTION = ["wOBA", "Last Name"]
WOBA_YEARS_STR_LIST = ["2017", "2018", "2019", "2020", "2021", "2022", "Custom"]
WOBA_YEARS_DICT_LIST = [{"label" : p, "value": p} for p in WOBA_YEARS_STR_LIST]


