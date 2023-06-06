# Usage: this is meant to be used with join_file.py! Or rather, it's meant to be used on the full dataframe with the entire dataset
# This is because entry errors happens across multiple files, not within the same file.

import pandas as pd
import numpy as np
import os
import re
from functools import reduce
from collections import Counter

DEBUG = True

# pathing
DATA_FOLDER_PATH = r".\data_raw"
OUTPUT_FILE_PREFIX = r".\data_cleaned"
OUTPUT_FILE_SUFFIX = r"_cat__cleanDT"

# other globals
REGEX_FILTER = r"\.csv$"

def cleanNameBasedonID(df):
    id_cols_list = ["Pitcher", "Batter"]
    # handle pitchers first, then deal with batters

    # Ideally, we should use Pitcherid to identity unique players, BUT the ids do NOT match the names - the same player can have different IDs!
    # This is likely from the system automatically issue IDs based on the name entered, but wrong names means "Cone," and "cone," and "Cone, Henry" would 
    # all have different IDs! So, do NOT rely on IDs, but we need to use the names themselves as identifiers.
    # Here, the assumption we make is that all Pitchers have unique full strings with case-insensitive... which is terrible, but it will not overwrite pitchers with the same
    # last name, which can happen. However, this means that "Cone," and "Cone, Henry" are two different entries, but this is safe for future entries when
    # there is another player named "Cone, Jose". In fact, there are players like with the same last name, such as : 'Anderson, Blake' and 'Anderson, Brandin'.
    
    # Here are all the edge cases:
    # case 1: the name is unique
    # case 2: there are 2 occurrence of the same last name, but one such first name is a space/empty. This means we CAN replace the names. (i.e. "Doe, John", "Doe,  ")
    #   It's 2 occurrence because it counts the last name only entry and the full name entry, and that's it.
    # case 3: the last name is NOT unique, but the full names are unique and non empty (i.e. "Doe, John", "Doe, Bob")
    # case 4: the last name is NOT unique, but there are also unique first name with empty first name. (i.e. "Doe,  ", "Doe, John", "Doe, Bob")
    # case 5: there names are the same, but they go to different schools, so they must be different people!
    df["Pitcher"] = df['Pitcher'].str.title() # fix case sensitivity here
    all_unique_names_ndarr = df["Pitcher"].unique()
    all_unique_splitnames_ndarr = [curName.split(',') for curName in all_unique_names_ndarr]
 
    for curSplitName in all_unique_splitnames_ndarr:
        count = 0
        curFirstname = ""
        if curSplitName[1] == " ":
            for curSplitName2 in all_unique_splitnames_ndarr:
                if curSplitName[0] == curSplitName2[0]:
                    count += 1
                    # grab the non-empty first name...
                    # what if the person only has missing first name entry? no worries, it'll stay empty from the initialization above
                    if curSplitName2[1] != " ":
                        curFirstname = curSplitName2[1]
            # handles case 3, meaning we CAN replace the name safely:
            if count <= 2:
                mask = df["Pitcher"].apply(lambda x: x.startswith(curSplitName[0])) # get the boolean mask of True for each row that matches the same lastname
                mask2 = df["Pitcher"].apply(lambda x: x.startswith(curSplitName[0]) & x.endswith(" ")) # get the boolean mask of True for each row that matches the same lastname
                # indices = list(filter(lambda i: df.iloc[i]['Pitcher'].startswith(curSplitName[0]), range(len(df))))
                # indices2 = list(filter(lambda i: df.iloc[i]['Pitcher'].startswith(curSplitName[0]) & df.iloc[i]['Pitcher'].endswith(" "), range(len(df))))
                indices = df.index.where(df['Pitcher'].str.startswith(curSplitName[0])).dropna().astype(int).tolist()
                indices2 = df.index.where(df['Pitcher'].str.startswith(curSplitName[0]) & df['Pitcher'].str.endswith(" ")).dropna().astype(int).tolist()
                idx = np.where(mask)[0]
                idx2 = np.where(mask2)[0]
                print(indices)
                print(indices2)
                fullname = curSplitName[0] + "," + curFirstname
                if DEBUG:
                    print(f'''\n\nFullname: {fullname}''')
                    print(f'''\n----before\n{df.loc[indices2, "Pitcher"]}''')
                df.loc[indices, "Pitcher"] = fullname
                if DEBUG:
                    print(f'''\n----after\n{df.loc[indices2, "Pitcher"]}''')

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
                if curDF.shape[0] > 0:
                    curDF = cleanNameBasedonID(curDF)
                
                # output
                pathSplit = filename.path.split(DATA_FOLDER_PATH)[-1]
                out_path = OUTPUT_FILE_PREFIX + pathSplit[:-4] + OUTPUT_FILE_SUFFIX + pathSplit[-4:]
                if DEBUG:
                    print(f'''\n\t>>>>>> file info after:\n{curDF.info()}''')
                # curDF.to_csv(out_path)
                print(f'''File saved to: {out_path}''')

    return

if __name__ == "__main__":
    main()