import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import struct
import argparse
import os

from sys import exit

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def make_graph(source_path, dest_path):
    x_data = []
    y_data = []
    z_data = []

    stat = os.stat(source_path)
    filesize = stat.st_size
    sample_count = filesize / 4
    seconds = (sample_count / 3.0) / 100.0

    with open(source_path, 'rb') as f:
        data = struct.unpack('f' * sample_count, f.read())

        for chunk in chunks(data, 3):
            x_data.append(chunk[0])
            y_data.append(chunk[1])
            z_data.append(chunk[2])

    t, step_size = np.linspace(0.0, seconds, num=len(x_data), retstep=True)

    print "File Size: %s" % filesize
    print "Total Sample Count: %s" % sample_count
    print "Seconds: %s" % seconds
    print "Samples Per Axis: %s" % len(x_data)
    print "T: %s" % len(t)
    print "Step Size: %s" % step_size

    plt.xlim(0, seconds)
    plt.plot(t, x_data, t, y_data, t, z_data)

    plt.xlabel("time (s)")
    plt.ylabel("stuff")
    plt.title("Getting Ripped")
    plt.grid(True)
    plt.savefig(dest_path)
    plt.clf()
    plt.close('all')


def main():
    args = parse_args()
    filepath = args.filepath

    make_graph(filepath, "test.png")

    exit(0)


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='graph accelerometer data'
    )

    # Positional Arguments
    parser.add_argument(
        'filepath', type=str.lower,
        help='filepath for binary data file'
    )

    return parser.parse_args()


if __name__ == '__main__':
    main()
