# Libraries
import argparse
import sys
import numpy as np
import pandas as pd
import calendar
from datetime import datetime

# Constants
TD_FORMAT_IN = "%Y-%m-%d %H:%M:%S.%f"
TD_FORMAT_OUT = "%Y-%m-%d %H:%M:%S"
DEFAULT_PERIOD = 0
DEFAULT_TIMESTAMP_POS_1 = 0
DEFAULT_HEADER_SIZE_1 = 1
DEFAULT_TIMESTAMP_POS_2 = 0
DEFAULT_HEADER_SIZE_2 = 1

# Convert NoneType to empty list and combines lists of lists into one list
def to_arr(arr):
	return [] if arr is None else [j for i in arr for j in i]

# Extract parameters from command line arguments
def parse_cmdline():
	parser = argparse.ArgumentParser(description="Merge two asynchronously timestamped csv files.")
	parser.add_argument('file_name_1', type=str, help="Indicates name of csv file 1")
	parser.add_argument('file_name_2', type=str, help="Indicates name of csv file 2")
	parser.add_argument('output_file_name', type=str, help="Indicates name of output csv file")
	parser.add_argument('-p', '--period', default=DEFAULT_PERIOD, type=int, help="Indicates period of output file, 0: combines timestamps from both files, -1: uses file 1's timestamps, -2: uses file 2's timestamps")
	parser.add_argument('-t1', '--timestamp_pos_1', default=DEFAULT_TIMESTAMP_POS_1, type=int, help="Indicates column containing timestamps in file 1")
	parser.add_argument('-h1', '--header_size_1', default=DEFAULT_HEADER_SIZE_1, type=int, help="Indicates size of file 1's header")
	parser.add_argument('-c1', '--characters_1', action='append', nargs='+', type=int, help="Indicates columns of characters from file 1 to be added to output")
	parser.add_argument('-i1', '--integers_1', action='append', nargs='+', type=int, help="Indicates columns of integers from file 1 to be added to output")
	parser.add_argument('-f1', '--floats_1', action='append', nargs='+', type=int, help="Indicates columns of floats from file 1 to be added to output")
	parser.add_argument('-t2', '--timestamp_pos_2', default=DEFAULT_TIMESTAMP_POS_2, type=int, help="Indicates column containing timestamps in file 2")
	parser.add_argument('-h2', '--header_size_2', default=DEFAULT_HEADER_SIZE_2, type=int, help="Indicates size of file 2's header")
	parser.add_argument('-c2', '--characters_2', action='append', nargs='+', type=int, help="Indicates columns of characters from file 2 to be added to output")
	parser.add_argument('-i2', '--integers_2', action='append', nargs='+', type=int, help="Indicates columns of integers from file 2 to be added to output")
	parser.add_argument('-f2', '--floats_2', action='append', nargs='+', type=int, help="Indicates columns of floats from file 2 to be added to output")
	parser.add_argument('-pr', '--print_result', action='store_true', help="Include flag to print results to console")
	return parser.parse_args()

# Extract data from input files
def extract_data(args):
	# verify file types and put data into numpy array objects
	if args.file_name_1.find('.csv') == -1:
		sys.exit("File 1 invalid file type.")
	d1 = np.genfromtxt(args.file_name_1, dtype=str, delimiter=',')
	if args.file_name_2.find('.csv') == -1:
		sys.exit("File 2 invalid file type.")
	d2 = np.genfromtxt(args.file_name_2, dtype=str, delimiter=',')

	# delete rows missing a parsed piece of data or if can't be casted to correct data type
	i1, f1, i2, f2 = [to_arr(i) for i in [args.integers_1, args.floats_1, args.integers_2, args.floats_2]]
	for i in range(args.header_size_1, d1.shape[0]):
		try:								# tries casting data to expected data types
			calendar.timegm(datetime.strptime(d1[i][args.timestamp_pos_1], TD_FORMAT_IN).timetuple())
			[int(d1[i][j]) for j in i1]
			[float(d1[i][j]) for j in f1]
		except:
			print(str(d1[i]) + " (" + args.file_name_1 + ", row " + str(i) + ") contains malformed data and will not influence output.")
			d1[i] = ['' for j in d1[i]]		# marks row for removal
	d1 = d1[~(d1 == '').all(1)]				# removes rows with invalid data
	for i in range(args.header_size_2, d2.shape[0]):
		try:								# tries casting data to expected data types
			calendar.timegm(datetime.strptime(d2[i][args.timestamp_pos_2], TD_FORMAT_IN).timetuple())
			[int(d2[i][j]) for j in i2]
			[float(d2[i][j]) for j in f2]
		except:
			print(str(d2[i]) + " (" + args.file_name_2 + ", row " + str(i) + ") contains malformed data and will not influence output.")
			d2[i] = ['' for j in d2[i]]		# marks row for removal
	d2 = d2[~(d2 == '').all(1)]				# removes rows with invalid data

	# create arrays of timestamps
	t1 = [calendar.timegm(datetime.strptime(i[args.timestamp_pos_1], TD_FORMAT_IN).timetuple()) for i in d1[args.header_size_1:]]
	t2 = [calendar.timegm(datetime.strptime(i[args.timestamp_pos_2], TD_FORMAT_IN).timetuple()) for i in d2[args.header_size_2:]]
	return d1, d2, t1, t2

# Determine timestamps to use in output file
def collect_timestamps(t1, t2):
	# move row indices to surround where data present in both datasets
	t1_i = 0
	t2_i = 0
	t1_i_end = len(t1) - 1
	t2_i_end = len(t2) - 1
	while t1[t1_i] < t2[0]:					# moves t1 index up until after first t2 index
		t1_i += 1
		if t1_i >= len(t1):
			sys.exit("File 1 data was all collected earlier than file 2 data.")
	while t2[t2_i] < t1[0]:					# moves t2 index up until after first t1 index
		t2_i += 1
		if t2_i >= len(t2):
			sys.exit("File 1 data was all collected later than file 2 data.")
	while t1[t1_i_end] > t2[len(t2) - 1]:	# moves t1 end index down until right after last t2 index
		t1_i_end -= 1
	t1_i_end += 1
	while t2[t2_i_end] > t1[len(t1) - 1]:	# moves t2 end index down until right after last t1 index
		t2_i_end -= 1
	t2_i_end += 1

	# generate output timestamps
	t0 = []
	if args.period == 0:					# combine timestamps from file 1 and 2
		t0 = t1[t1_i:t1_i_end] + t2[t2_i:t2_i_end]
	elif args.period == -1:					# use timestamps from file 1
		t0 = t1[t1_i:t1_i_end]
	elif args.period == -2:					# use timestamps from file 2
		t0 = t2[t2_i:t2_i_end]
	else:									# creates timestamps spaced period seconds apart
		if t1[t1_i] < t2[t2_i]:				# determine if first overlapped timestamp is in file 1 or 2
			t0.append(t1[t1_i])
		else:
			t0.append(t2[t2_i])
		i = 0
		while t0[i] < t1[t1_i_end - 1]:
			t0.append(t0[i] + args.period)
			i += 1
	t0.sort()
	return t0

# Save data to file
def save(od, of_name, h1_size, h2_size, headers1, headers2, print_result):
	od = [datetime.utcfromtimestamp(int(float(i[0]))).strftime(TD_FORMAT_OUT) for i in od]	# converts timestamp back into readable format
	if h1_size > 0 and h2_size > 0:			# adds headers back by concatenating names from f1 and f2 at indices listed in f1_format and f2_format
		od = np.insert(od, 0, np.concatenate((["Timestamp"], headers1, headers2)), axis = 0)
	elif h1_size > 0:						# if one file doesn't have headers but the other does, fill gaps with array of empty strings
		od = np.insert(od, 0, np.concatenate((["Timestamp"], headers1, ['' for i in headers2])), axis=0)
	elif h2_size > 0:
		od = np.insert(od, 0, np.concatenate((["Timestamp"], ['' for i in headers1], headers2)), axis=0)
	if print_result:
		print(od)
	pd.DataFrame(od).to_csv(of_name, header=False, index=False)

# Begin execution
args = parse_cmdline()						# command line arguments

# Reformat extracted arguments
h1_size = args.header_size_1
h2_size = args.header_size_2
c1, i1, f1, c2, i2, f2 = [to_arr(i) for i in [args.characters_1, args.integers_1, args.floats_1, args.characters_2, args.integers_2, args.floats_2]]

# Prepare data
d1, d2, t1, t2 = extract_data(args)			# spreadsheets' data, input timestamps
t0 = collect_timestamps(t1, t2)				# output timestamps

# Interpolate and append data one column at a time
od = [[i] for i in t0]		# od starts off as just the timestamps
t1_a = np.asarray(t1)
t2_a = np.asarray(t2)
for i in c1:				# appends a column of strings generated by copying strings corresponding to timestamps in t1 closest to requested timestamps in t0
	od = np.append(od, [[d1[(np.abs(t1_a - j)).argmin() + 1][i]] for j in t0], axis=1)
for i in i1:				# appends a column of integers generated from requesting values of t0 from an interpolation of t1 and a column of d1 specified by i1
	od = np.append(od, [[round(j)] for j in np.interp(t0, t1, [int(float(k)) for k in d1[h1_size:, i]])], axis=1)
for i in f1:				# appends a column of floats generated from requesting values of t0 from an interpolation of t1 and a column of d1 specified by f1
	od = np.append(od, [[j] for j in np.interp(t0, t1, [float(k) for k in d1[h1_size:, i]])], axis=1)
for i in c2:				# appends a column of strings generated by copying strings corresponding to timestamps in t2 closest to requested timestamps in t0
	od = np.append(od, [[d2[(np.abs(t2_a - j)).argmin() + 1][i]] for j in t0], axis=1)
for i in i2:				# appends a column of integers generated from requesting values of t1 from an interpolation of t2 and a column of d2 specified by i2
	od = np.append(od, [[round(j)] for j in np.interp(t0, t2, [int(float(k)) for k in d2[h2_size:, i]])], axis=1)
for i in f2:				# appends a column of floats generated from requesting values of t1 from an interpolation of t2 and a column of d2 specified by f2
	od = np.append(od, [[j] for j in np.interp(t0, t2, [float(k) for k in d2[h2_size:, i]])], axis=1)

save(od, args.output_file_name, h1_size, h2_size, [i for i in d1[h1_size - 1][[j for j in c1 + i1 + f1]]], [i for i in d2[h2_size - 1][[j for j in c2 + i2 + f2]]], args.print_result)
sys.exit("Completed.")