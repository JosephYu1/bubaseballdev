import re
import pandas 
import warnings

# take away: 
#   1. the write file will add an index column. 
#   2. And if we read in the header, the output will still write the header row, so no worries there.
#   3. And even if we process the file and save it as the correct type, the change is not reflected since .csv doesn't have string type, so it'll always be an object type
#   4. use low_memory = false when reading in a single file

myfile = './data_combined/20230329-combined-all.csv'
target_type = str  # The desired output type

with warnings.catch_warnings(record=True) as ws:
    warnings.simplefilter("always")

    mydata = pandas.read_csv(myfile, header = 0)
    print("Warnings raised:", ws)
    # We have an error on specific columns, try and load them as string
    for w in ws:
        s = str(w.message)
        print("Warning message:", s)
        match = re.search(r"Columns \(([0-9,]+)\) have mixed types\.", s)
        if match:
            columns = match.group(1).split(',') # Get columns as a list
            columns = [int(c) for c in columns]
            print("Applying %s dtype to columns:" % target_type, columns)
            mydata.iloc[:,columns] = mydata.iloc[:,columns].astype(target_type)
    mydata.to_csv('./data_combined/test.csv')

    mydata2 = pandas.read_csv("./data_combined/test.csv", header = 0)
    print("Warnings raised:", ws)
    # We have an error on specific columns, try and load them as string
    for w in ws:
        s = str(w.message)
        print("Warning message:", s)
        match = re.search(r"Columns \(([0-9,]+)\) have mixed types\.", s)
        if match:
            columns = match.group(1).split(',') # Get columns as a list
            columns = [int(c) for c in columns]
            print("Applying %s dtype to columns:" % target_type, columns)
            mydata2.iloc[:,columns] = mydata.iloc[:,columns].astype(target_type)