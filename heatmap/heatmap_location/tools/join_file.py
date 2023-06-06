# Tested a bit and it looks like it works
# there's a jupyter notebook version, they do the same thing but the code is slightly different.

import pandas as pd
import glob
import os


def main():
    # NOTE: this joins ALL the .csv files in a folder, so make sure there's no other combined files in there
    path = r'./data/' #choose path to data folder containing .csv here
    print(os.getcwd())
    folder = glob.glob(os.path.join(path, "*.csv"))

    df = (pd.read_csv(f, header = 0) for f in folder)
    concatenated_df = pd.concat(df, ignore_index=True)

    # show output
    print(concatenated_df)

    # custom output pathing
    out_path = r'./data_combined/'
    out_filename = r'20230215-combined.csv' #NOTE: both needs to be the same type of string, i.e. both rstring
    print(out_path + out_filename)
    concatenated_df.to_csv(out_path + out_filename)

if __name__ == "__main__":
    main()