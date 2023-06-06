# Tested a bit and it looks like it works
# there's a jupyter notebook version, they do the same thing but the code is slightly different.

# useful links:
# how to use glob and fnmatch to filter: https://stackoverflow.com/questions/71958120/pattern-to-exclude-specific-files
# use re with glob? https://stackoverflow.com/questions/72036439/finding-file-name-using-regex-from-glob
# using re to find files? https://stackoverflow.com/questions/13031989/regular-expression-usage-in-glob-glob
# using re with glob: https://stackoverflow.com/questions/62863922/regular-expression-and-python-glob

# NOTE: the version I'm using is the simplest one and doesn't use re. 
# If anyone feels like it, go ahead and implement the re ver, maybe as a new file?

import pandas as pd
import glob
import os
from datetime import date
import cleanNames

DEBUG = True

PATH = r'./data_cleaned/' #choose path to data folder containing .csv here

# custom output pathing
# the current day is dynamic in runtime!
OUT_PATH = r'./data_combined/'
OUT_MIDFIX = r'-combined' # this is the current date of when the file is generated as a rstring!
OUT_FILE_SUFFIX_ALL = r'-all.csv' #NOTE: all needs to be the same type of string, i.e. both rstring
OUT_FILE_LATEST = r'latest.csv'

# df_gen is a generator object, from the pd.read_csv() which takes from glob.glob()
def concat_files_and_save(df_gen):
    # dynamically get today's date
    today = date.today()
    # dd/mm/YY
    date_str = today.strftime("%Y%m%d")
    print(f'''today's date in yyyymmdd: {date_str}''')

    # output path should be a rstring when the data is created, i.e. r'20230215-xxx.csv'
    out_current = OUT_PATH + date_str + OUT_MIDFIX
    out_full = out_current + OUT_FILE_SUFFIX_ALL
    print(out_full)

    if df_gen:
        concatenated_df = pd.concat(df_gen, ignore_index=True)
        # important: sort by datetime here!
        concatenated_df = concatenated_df.sort_values(by = "Datetime").reset_index(drop=True)
        concatenated_df = cleanNames.cleanNameBasedonID(concatenated_df)
        
        # NOTE: set output path above in global!
        # custom output pathing
        concatenated_df.to_csv(out_full) # base copy to keep
        concatenated_df.to_csv(OUT_PATH + OUT_FILE_LATEST) # another copy to be kept loading/overwriting. Basically, during file read, we'll always read in the "latest.csv"
        print(f'''Saved file to {out_full} and {OUT_PATH + OUT_FILE_LATEST}''')
    return

def main():
    #================================
    #--------- Input ----------------
    #================================

    # NOTE: Set path here!
    # this joins ALL the .csv files in a folder, so make sure there's no other combined files in there
    print(os.getcwd())

    # read in all files first
    folder = glob.glob(os.path.join(PATH, "*.csv"))

    # do all files, then filter by type
    df = (pd.read_csv(cur_f, header = 0) for cur_f in folder)

    # Check output path
    concat_files_and_save(df)

if __name__ == "__main__":
    main()