# Adds a column to the .csv files inside a folder. If it's a public game, then the value is 1, else it's 0.
# Wether a game is public or not is in the filename, has xxx-Private-xxx.csv
# Obviously this only works if the filename is consistent

import pandas as pd
import os
import re

DEBUG = False

# I/O paths
DATA_FOLDER_PATH = r".\data_raw"
OUTPUT_FILE_PREFIX = r".\data_categorized"
OUTPUT_FILE_SUFFIX = r"_cat"

# globals
REGEX_FILTER = r"\.csv$" #scan for if the file is a *.csv file

# add a Public column. 1 if the file is public match, 0 if private
# Input:
#   filepath_str: the string of the filepath e.g.: ("./data/20221018-xxx.csv")
#   df: the dataframe we want to change. Normally this is pass by reference by we expect this function to be called by another file
# Output:
#   A modified dataframe with the Public column
def add_public_col(df, filepath_str):
    if df is None:
        return
    if len(df) > 0 and len(filepath_str) > 0:
        df["Public"] = 0 if "private" in filepath_str.lower() else 1
    return df

def main():
    # =====================================
    # ---------- Input ----------
    # =====================================

    # the current way of reading files as .csv using os and folder    
    com_filter = re.compile(REGEX_FILTER)

    for filename in os.scandir(DATA_FOLDER_PATH):
        if filename.is_file(): # filename is a nt.DirEntry object!
            if DEBUG:
                print(f'''\n------------\nFilename: {filename.path}\n-------------\n''')
            # ONLY read in if it's a .csv file
            if (re.search(com_filter, filename.path)):
                curDF = pd.read_csv(filename.path, header=0,)

                # do work here
                if DEBUG:
                    print(filename.path)
                    print("\nbefore-------------\n")
                    print(curDF.head())

                # do work here. Case insensitive
                curDF["Public"] = 0 if "private" in filename.path.lower() else 1
                
                if DEBUG:
                    print("\nafter-------------\n")
                    print(curDF.head())
                
                # =====================================
                # ---------- Output file ----------
                # =====================================
                pathSplit = filename.path.split(DATA_FOLDER_PATH)[-1]
                out_path = OUTPUT_FILE_PREFIX + pathSplit[:-4] + OUTPUT_FILE_SUFFIX + pathSplit[-4:]

                curDF.to_csv(out_path)
                print(f'''output file path: {out_path}''')

if __name__ == "__main__":
    main()