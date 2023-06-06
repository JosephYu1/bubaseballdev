# This combined both addPublicColumn and cleanCSVDateTime into one single file for faster batch processing.
# NOTE: the starting folder get input from is from data_raw and output is data_cleaned. 
# Still need to run join_file.py after this!

# TODO: write command line function for this? Or combine this with join_file.py in a new file?

import pandas as pd
import os
import re
# import addPublicColumn as addPC
# import cleanCSVDateTime as cleanCSV
# import zoneCalcualtion as zone
from . import addPublicColumn as addPC
from . import cleanCSVDateTime as cleanCSV
from . import zoneCalcualtion as zone

DEBUG = True

# pathing
DATA_FOLDER_PATH = r".\data_raw"
OUTPUT_FILE_PREFIX = r".\data_cleaned"
OUTPUT_FILE_SUFFIX = r"_cat__cleanDT"

# other globals
REGEX_FILTER = r"\.csv$" # checks for the end string to see if' it's a .csv file

# input: a df that has been columns properly converted and handled elsewhere already
# output: a "cleaned" df that has no data that can break the code, like no NaNs nor unwanted columns
def treat_special_columns_and_clean_data(df):
    # drop the useless columns here
    try:
        df = df.drop(["Tilt"], axis = 1) # this Tilt column breaks the code, and its data is also captured by SpinAxis so it's safe to drop
    except KeyError:
        print(f'''No target column to be dropped''')
    if DEBUG:
        print(f'''After dropping Tilt: {"Tilt Dropped" if "Tilt" not in df.columns else "No Tilt dropped"}''')
        print(f'''\t-----DF dimension before dropping NA: {df.shape}''')
        print(f'''\t-----DF dimension after dropping NA: {df.dropna().shape}''')
    return df

def process_w_date(df, filename_str, date_format_str):
    if df is None or df.shape[0] <= 0:
        return
    df = treat_special_columns_and_clean_data(df)
    df = addPC.add_public_col(df, filename_str)
    df = cleanCSV.handle_all(df, date_format_str)
    df = zone.zones_calculation(df)
    return df

def main():
    com_filter = re.compile(REGEX_FILTER)

    list_starting_datetime_str = []

    for filename in os.scandir(DATA_FOLDER_PATH):
        if filename.is_file(): # filename is a nt.DirEntry object!
            if DEBUG:
                print(f'''\n------------\nFilename: {filename.path}\n-------------\n''')
            # ONLY read in if it's a .csv file
            if (re.search(com_filter, filename.path)):
                curDF = pd.read_csv(filename.path)
                if DEBUG:
                    print(f'''\n\t>>>file info before:\n{curDF.info()}''')

                # do work
                if curDF.shape[0] <= 0: #avoid reading empty files
                    continue
                curDF = treat_special_columns_and_clean_data(curDF)
                curDF = cleanCSV.handle_all(curDF)
                # avoid duplicate data here by checking the starting datetime_str
                if DEBUG:
                    print(f'\n\n>>>>>> Datetime_str at 0 : {curDF["Datetime_str"][0]}')
                cur_starting_datetime_str = curDF["Datetime_str"][0]
                if cur_starting_datetime_str not in list_starting_datetime_str:
                    list_starting_datetime_str.append(cur_starting_datetime_str)
                else:
                    if DEBUG:
                        print(f'''\n>>>>>> Found duplicate: {filename.path}''')
                    continue # go to next file if datetime_str is seen before
                curDF = addPC.add_public_col(curDF, filename.path)
                curDF = zone.zones_calculation(curDF)

                # output
                pathSplit = filename.path.split(DATA_FOLDER_PATH)[-1]
                out_path = OUTPUT_FILE_PREFIX + pathSplit[:-4] + OUTPUT_FILE_SUFFIX + pathSplit[-4:]
                if DEBUG:
                    print(f'''\n\t>>>>>> file info after:\n{curDF.info()}''')
                curDF.to_csv(out_path)
                print(f'''File saved to: {out_path}''')

    return

if __name__ == "__main__":
    main()