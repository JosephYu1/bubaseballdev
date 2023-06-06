# there are TWO ways to use this file:
# 1. run this by setting the paths below, and it'll "clean" all the date and time of the files inside that folder.
# 2. call datetime_pip_cleaner.py in the terminal also in the src/tools folder. This only works on ONE file at a time

# What this does: 
#   - Fill in NAs by using previous valid entry and also modify them to to give arbitrary time difference
#   - add 3 more columns to each .csv file:
#       - Date_datetime: the Date column as a datetime object, probably parsed
#       - Time_str: the Time column as a str obj, with all the same length and truncated microseconds
#       - Datetime: Concatenate Date and Time together as a datetime object

import numpy as np
import pandas as pd
import glob
import os
import sys
import re
from datetime import datetime

DEBUG = False
WRITE = True

# I/O paths
DATA_FOLDER_PATH = r".\data_categorized"
OUTPUT_FILE_PREFIX = r".\data_cleaned"
OUTPUT_FILE_SUFFIX = r"_cleanDT"

# Other globals
FILL_TIMESTEP = 5
REGEX_FILTER = r"\.csv$" # alternative: "([^\\s]+(\\.(?i)(csv))$)" | scan for if the file is a *.csv file
LENGTH_TIME_DEFAULT = 8 # this is the expected length of a cell in Time2 AFTER removing the microseconds. Time2 is the result of removing the microsecond.
LENGTH_BAD_TIME_DEFAULT = 5 # this is the length of cell in Time2 that is handled badly in excel, AFTER removing the microseconds
LENGTH_SINGLE_HOUR_TIME_DEFAULT = 7

def handle_NA(df):
    if df is None:
        return
    # =====================================
    # ---------- handle NA in date ----------
    # =====================================

    # Method 1: fill NA
    # instead of dropping na, infer the date and time from previous entry for date, just copy the previous valid date
    # get the indices so we can use them later
    idx_na_d = np.where(df["Date"].isna())[0] # the 0 just grab the indices
    idx_na_t = np.where(df["Time"].isna())[0] 
    if DEBUG:
        print('\n----handling NA---------\n')
        print(f'''Where is NA in Time:\n{idx_na_t}''')
        print(f'''{df.iloc[idx_na_t, :]}''')
        print(f'''Where is NA in Date:\n{idx_na_d}''')
        print(df.iloc[idx_na_d, :])

    df["Date"] = df["Date"].fillna(method="ffill") # fills the missing NA

    if DEBUG:
        print(f'''\nafter forward fill in Date:\n{df.loc[idx_na_d, "Date"]}''')
        print("---------------")
    
    # now handles the missing time
    df["Time"] = df["Time"].fillna(method = "ffill")

    if DEBUG:
        if len(idx_na_t) > 0:
            print(f'''the missing time rows:\n{df["Time"][idx_na_t]}''')
            print(f'''the nearby rows - start - 1:\n{df["Time"][idx_na_t[0] - 1]}''') if idx_na_t[0] <= 0 else print("first row, no earlier entry")
            print(f'''the nearby rows - end + 1:\n{df["Time"][idx_na_t[-1] + 1]}''') if idx_na_t[-1] + 1 < len(df["Time"]) else print("last row, no later entry")
            print("\n------end NA------------\n")
    # NOTE: NOT done yet, we merely replaced the values, next we need to adjust them so they don't all have the same time
    # but first, we need to convert the Time column to datetime so we can do arithmetic on it.
    # see others parts for convert and adjust.
    
    # # Method 2: drop na and reset index
    # print("\n------drop na------\n")
    # print(f'''Where is NA in Time:\n{np.where(df["Time"].isna())}''')
    # print(df.iloc[3112, :])
    # print(df.iloc[3198, :])
    # df = df.dropna(subset=["Date", "Time"]).reset_index()
    # print(df.head())
    # print(df.info())
    # print("-----------drop done")
    
    return df, idx_na_d, idx_na_t

# the expected date_format_str is pandas datetime str, like %Y/%m/%d, see: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
def handle_issues(df, idx_na_d, idx_na_t, date_format_str = ""):
    # =====================================
    # ---------- Handle issues ----------
    # =====================================

    # issue 1: inconsistent date format entry
    # To handle this, simply running the to_datetime() can smartly handle the edge case... NOT tested against all cases tho!
    # NOTE: 20221018 file has a different data format! usually it's yyyy/mm/dd, but for Oct 18 it's mm/dd/yyyy!
    if df is None:
        return
    
    if date_format_str == "":
        df["Date_datetime"] = pd.to_datetime(df["Date"])
    else:
        df["Date_datetime"] = pd.to_datetime(df["Date"], format = date_format_str)
    
    if DEBUG and len(df) > 0:
        print("===========start datetime handling======\n\n")
        print(df["Date_datetime"][0])
        print(df["Date_datetime"].dtype)
        # print(df["Date_datetime"][1600:1610]) # shows 20221018 data, this is for the combined big data file.
        print("---------------\n")
    
    # for filter testing and getting the questionable dates
    df_bad_date = df.loc[(df["Date_datetime"] == '2022-10-18')]
    if DEBUG:
        print(f'''---bad date head:\n{df_bad_date.head()}''') # head() is self-monitored, so if it's too small, it won't trigger

    # issue 2: bad microsecond in the format of '.xx' at the end of Time
    df["Time_str"] = df["Time"].astype(str) # just to make sure it's a string so we can use str.rsplit()
    # NOTE: The next line is NOT needed, because rsplit works even when the character for splitting isn't there. But it's left here just in case...
    # df["Time2"] = df['Time2'].apply(lambda x: x + '.' if not re.search(r'\.', x) else x)
    df["Time_str"] = df["Time_str"].apply(lambda x : x.rsplit('.')[0]) # the [0] index grabs the first thing, which is the part before the dot. We don't care about microseconds
    
    if DEBUG:
        print(f'''time with no trailing microseconds:\n{df.head()}''')

    # issue 3: bad time entry : need 2 digits for hour
    # The edge case here is when the Time starts at 0:xx:xx, in excel entry, the 0: is simply truncated, resulting it in a string of length 5.
    # https://stackoverflow.com/questions/56441190/zero-padding-pandas-column
    df_bad_time = df[(df["Time_str"].astype(str).str.len() != LENGTH_TIME_DEFAULT)]
    if DEBUG and df.shape[0] > 0:
        print("\n\n--------before padding")
        print(df["Time"][0])
        print(f'''---bad time head:\n{df_bad_time.head()}''')

    # this matches the length of the Time cells and pad to the correct length accordingly
    for idx in df_bad_time.index:
        # this is when the cell is missing the two digit hours entirely, along with the ':'
        curLen = len(df.loc[idx, "Time_str"])
        if curLen == LENGTH_BAD_TIME_DEFAULT:
            df.loc[idx, "Time_str"] = "00:" + df.loc[idx, "Time_str"]
        # to pad just one extra zero to the front if the hour is a single digit instead of double digit, like excel truncating 07 into just 7
        elif curLen == LENGTH_SINGLE_HOUR_TIME_DEFAULT:
            df.loc[idx, "Time_str"] = "0" + df.loc[idx, "Time_str"]
        # NOTE: here we just forces all cases to copy previous valid entry, and let the add timedelta part to mimic real data.
        else:
            # copy the valid entry. If the idx is the first one, we'll just copy the first valid entry
            df_good_time = df[(df["Time_str"].astype(str).str.len() == LENGTH_TIME_DEFAULT)]
            df.loc[idx, "Time_str"] = df.loc[idx - 1, "Time_str"] if idx > 0 else df.loc[df_good_time.index[0], "Time_str"]
            idx_na_t.append(idx) # this will let the code below handle adding timedelta to fake valid entries

    # the line below does ONE thing in one line, maybe faster but it'll be too complicated to read if we add more cases
    # df["Time"] = (np.where(df["Time"].astype(str).str.len() == LENGTH_BAD_TIME_DEFAULT, "00:" + df["Time"].astype(str), df["Time"].astype(str)))

    if DEBUG and df.shape[0] > 0:
        print("\n\n--------after padding")
        print(df["Time_str"][0]) # would not see a difference if no padding is needed
        print(df_bad_time.head())
        print("---------------\n")

    # finally, join the date string and newly edited time string together as a datetime object
    df["Datetime_str"] = df["Date_datetime"].astype(str) + r" " + df["Time_str"]
    if DEBUG and df.shape[0] > 0:
        print(df["Datetime_str"][0])
        if df_bad_time.shape[0] > 0:
            print(df.loc[df_bad_time.index[0], "Datetime_str"])
    df["Datetime"] = pd.to_datetime(df["Datetime_str"], format="%Y-%m-%d %H:%M:%S")
    if DEBUG and df.shape[0] > 0:
        print(df["Datetime"][0])
        if df_bad_time.shape[0] > 0:
            print(df.loc[df_bad_time.index[0], "Datetime"])
        print(df.dtypes)

    # don't forget to adjust the filled Time values
    # here we simply loop through the affected indices and and add multipliers if applicable
    prev = -1
    count = 1
    for idx in idx_na_t:
        count = count + 1 if prev == (idx - 1) else 1 # sequential entries should get more padding
        prev = idx # remember to update
        if DEBUG:
            print(count)
            print(df["Datetime"][idx] + pd.Timedelta(seconds = FILL_TIMESTEP * count))
        df.loc[idx, "Datetime"] = df["Datetime"][idx] + pd.Timedelta(seconds = FILL_TIMESTEP * count)
        if DEBUG:
            print(f'''cur: {df["Datetime"][idx]} | prev: {df["Datetime"][idx - 1]} | next: {df["Datetime"][idx + 1]}''')
    if DEBUG:
        print(df["Datetime"][idx_na_t])
    
    return df



def handle_all(df, date_format_str = ""):
    if df is None:
        return
    df, idx_d, idx_t = handle_NA(df)
    return handle_issues(df, idx_d, idx_t, date_format_str)

def example():
    # create a sample dataframe
    df = pd.DataFrame({'col1': ['abc', 'def', 'ghi', "123"], 'col2': ['jkl.mno', 'pqr.stu', 'vwx', "1223.43"]})

    # use apply() to check for '.' character in column
    dot_indexes = df['col2'].apply(lambda x: re.search(r'\.', x)).dropna().index

    print(dot_indexes)
    print(type(dot_indexes))
    print(df['col2'][dot_indexes])
    print(len(dot_indexes))

    # use apply() to add '.' character to cells that don't have one
    added = df['col2'].apply(lambda x: x + '.' if not re.search(r'\.', x) else x)
    print(added)

    # test if splitting will return empty. (it does)
    s = "b1.3"
    s2 = "b2."
    s3 = "bx"
    s4 = "b1.3.5"
    print(f'''one dot: {s}: {s.rsplit(".")}''')
    print(f'''one dot but nothing after dot: {s2}: {s2.rsplit(".")}''')
    print(f'''no dot: {s3}: {s3.rsplit(".")}''')
    print(f'''2 dots: {s4}: {s4.rsplit(".")}''')

    print(s4[:-2] + OUTPUT_FILE_SUFFIX + s4[-2:])
    
    sf = r".\data\20230218-Baylor-1_unverified.csv"
    sfsplit = sf.split(DATA_FOLDER_PATH)
    print(sfsplit)
    print(sfsplit[0])
    print(sfsplit[-1])
    print(OUTPUT_FILE_PREFIX + sfsplit[-1][:-4] + OUTPUT_FILE_SUFFIX + sfsplit[-1][-4:]) # test the final filepath

# this is for working in comment line.
# Input: a input and output file path. NOTE: this works on ONE file at a time
# Output: modified .csv file with Datetime and Datetime_str added to columns, among other things
def clean_and_save(in_filename_str, out_filename_str, date_format_str = ""):
    com_filter = re.compile(REGEX_FILTER)
    if (re.search(com_filter, in_filename_str)):
        df = pd.read_csv(in_filename_str)
        df = handle_all(df, date_format_str)
        df.to_csv(out_filename_str)
    return

def main():
    # =====================================
    # ---------- Input ----------
    # =====================================

    # Input Method 1:
    # NOTE: deprecated! But you can still use this if you want to directly use this program on data instead of files
    # This method works on the data that has been read in. Due to performance, it's better to do preprocessing on the files so this is not used.
    # # NOTE: change this according to your folder structure!
    # # set pathing first

    # # relative path where the this file is present.
    # current = os.path.dirname(os.path.realpath(__file__))
    # print(current)
    
    # # Getting the parent directory name
    # # where the current directory is present.
    # parent = os.path.dirname(current)
    # print(parent)

    # grandparent = os.path.dirname(parent)
    # print(grandparent)
    
    # # adding the parent directory to
    # # the sys.path.
    # sys.path.append(grandparent)
    # print(sys.path)

    # import data # import here AFTER sys change

    # # set data here
    # df = data.BASEBALL_ALL_DF

    # print(df.head())
    # print(df.info())
    # print(df.dtypes)

    # for testing
    # example()

    #---------------------------------

    # Input method 2:
    # the current way of reading files as .csv using os and folder    
    com_filter = re.compile(REGEX_FILTER)

    for filename in os.scandir(DATA_FOLDER_PATH):
        if filename.is_file(): # filename is a nt.DirEntry object!
            if DEBUG:
                print(f'''\n------------\nFilename: {filename.path}\n-------------\n''')
            # ONLY read in if it's a .csv file
            if (re.search(com_filter, filename.path)):
                curDF = pd.read_csv(filename.path, header=0,)
                if DEBUG:
                    if "20221018" in filename.path:
                        print(curDF.loc[:5, ["Date", "Time"]])

                # do work here
                curDF = handle_all(curDF)

                if DEBUG: 
                    if "20221018" in filename.path:
                        print(curDF.loc[:5, ["Date", "Time", "Datetime"]])

                # =====================================
                # ---------- Output file ----------
                # =====================================
                pathSplit = filename.path.split(DATA_FOLDER_PATH)[-1]
                out_path = OUTPUT_FILE_PREFIX + pathSplit[:-4] + OUTPUT_FILE_SUFFIX + pathSplit[-4:]
                
                if WRITE:
                    curDF.to_csv(out_path)
                print(f'''output file path: {out_path}''')

if __name__ == "__main__":
    main()