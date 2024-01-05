import csv

from argparse import ArgumentParser

def convert_csv(input_file, output_file):
    f_in = open(input_file, 'r')
    f_out = open(output_file, 'w+')
    writer = csv.writer(f_out)

    for line in f_in:
        line_num, lon, lat, alt, volt, timestamp, fix, num_sat = line.strip().split(",")
        attitude_str = "(0,0,0)"
        vel = "(0,0,0)"
        writer.writerow(
            [line_num, lon, lat, alt, attitude_str, vel, volt, timestamp, fix, num_sat]
        )
    f_in.close()
    f_out.close()
    

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--input", help="input file", required=True)
    parser.add_argument("--output", help="output file", required=False, default="out.csv")
    args = parser.parse_args()

    convert_csv(args.input, args.output)