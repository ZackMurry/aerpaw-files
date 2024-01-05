OVERVIEW
csv_merge.py combines two asynchronously timestamped csv files into one csv with one set of timestamps. The output file can use the timestamps of either or both input files, or a user selected frequency. Data can be interpolated as characters (the string with the closer timestamp will be used), integers, or floats. Configurable parameters include file names, period/which file's timestamps to use, header size, column containing timestamp, and columns containing characters/integers/floats

USE
install numpy, pandas, and argparse
	pip3 install numpy pandas argparse
for input format run help command
	$ python3 csv_merge.py -h
the input files and output file names must be the first three arguments, optional arguments can be in any order
	$ python3 csv_merge.py input_file_1.csv input_file_2.csv output_file.csv ...

SUPPLEMENTAL INFO
column indices start counting from 0
input files are assumed to have in-order timestamps
rows with a parsed piece of data that is missing or of incorrect data type are removed before processing; floats will be casted to integers if need be
default values and time and date formats can be modified by changing the constants at the beginning of the script
default values
	period: 0 (uses timestamps from both files)
	timestamp column indices: 0 (first column)
	header sizes: 1 (1 row will be ignored)

EXAMPLE
$ python3 csv_merge.py if1.csv if2.csv of.csv -h1 0 -c1 2 -c2 5 2 -t2 3 -p -1 -f1 1 2 -c2 5 -i1 1 -pr
	if1.csv has no header and the timestamps are in column 0
	if2.csv has a 1 row header and the timestamps are in column 3
	output columns: timestamps from file 1 | file 1, column 2, treated as chars | 1, 1, ints | 1, 1, floats | 1, 2, floats | 2, 5, chars | 2, 2, chars | 2, 5, chars
	results will be printed to the console