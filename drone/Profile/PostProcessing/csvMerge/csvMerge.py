import argparse
import sys
import pandas as pd

def trimByTs(df, ts):
    """ trims rows from DataFrame with diferent timestamps
        Parameters:
            df - the DataFrame to be trimmed
            ts - the timestamp to keep
        Returns:
            trimmed DataFrame
    """
    for i in df.index:
        if i not in ts:
            df = df.drop(i)

    return df

parser = argparse.ArgumentParser(description='Merge csv.')
parser.add_argument('file1', nargs=1, type=argparse.FileType('r'),
                    help='first file to be merged')
parser.add_argument('file2', nargs=1, type=argparse.FileType('r'),
                    help='second file to be merged')
parser.add_argument('--output', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
                    help='output file for merged csv, default is standart output (screen)')
parser.add_argument('--format', nargs='?', choices=['c*','i*'], default='c*',
                    help='specifies format of data merged from file2 as copy (c*) or interpolate (i*), default is copy')

args = vars(parser.parse_args())

file1_df = pd.read_csv(args['file1'][0],index_col='time', parse_dates=True)
file2_df = pd.read_csv(args['file2'][0], index_col='time', parse_dates=True)

ts = file1_df.index

mergedDf = file1_df.append(file2_df, sort=True).sort_values(by='time')

if args['format'] == 'i*':
    mergedDf = mergedDf.interpolate(method='time')
    mergedDf = trimByTs(mergedDf, ts)
else:
    mergedDf = mergedDf.interpolate(method='pad')
    mergedDf = trimByTs(mergedDf, ts)

mergedDf.to_csv(path_or_buf=args['output'], float_format='%.1f')