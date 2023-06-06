#  we're first importing the os and sys modules as before, and then checking if the correct number of command line arguments 
# have been provided. If not, we print a usage message and exit the program.
# We then use the os.path.abspath() function to get the absolute paths of the input and output files, just like in the previous
# version of the code.
# Next, we add the path to the folder containing the other Python file that we want to run, using the sys.path.append() 
# function. This will allow us to import the py module from that folder in the next step.
# We then import the py module, which should be a separate Python file located in the folder we added to the path. We call the 
# clean() function from that module to modify the contents of the input file.
# Finally, we write the modified content to the output file using the write() method of a file object created with 
# the open() function. We also print a message indicating where the modified content was saved.

# usage:
# general form:
# $ python program.py input_files/my_file.txt output_files/output_file.txt
# Modified content saved to /path/to/output_files/output_file.txt
# explicit form:
# python ./src/tools/sample_piping.py ./data_combined/20230208-combined-all.csv ./data_combined/20230208-combined-all-cleaned.csv

import sys
import os

if len(sys.argv) < 2:
    print("Usage: python program.py <file> [<output_file>]")
    sys.exit(1)

in_file_path = os.path.abspath(sys.argv[1])

if len(sys.argv) >= 3:
    output_file_path = os.path.abspath(sys.argv[2])
else:
    output_file_path = in_file_path

# Run another Python file to modify the input
sys.path.append(r'./src/tools')
import cleanCSVDateTime
modified_content = cleanCSVDateTime.clean_and_save(in_file_path, output_file_path)

# Write the modified content to the output file
# with open(output_file_path, 'w') as output_file:
    # output_file.write(modified_content)

print(f"Modified content saved to {output_file_path}")
