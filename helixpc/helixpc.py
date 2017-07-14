'''
Copyright (c) 2017 Anne-Laure Ehresmann
Licenced under the MIT License (https://en.wikipedia.org/wiki/MIT_License)
helix.py - the CLI for easy employment of various automisation scripts.

Usage:
helix.py group <group_input> [--nonan | -n]
helix.py graph <graph_input> [--heat] [--scatter] <control> <sample> [<sample> ...]
helix.py group <group_input> [--nonan | -n] graph <graph_input> [--heat] [--scatter] <control> <sample> [<sample> ...]
helix.py (-h | --help)

The control and samples can either be column names, either column indexes.
In the graphing options, if you specify neither --scatter nor --heat, it will be assumed you want both.

Examples:
helix.py group input.csv
helix.py graph output.csv heat 1 log_fc_2,log_fc_3,log_fc_4
helix.py group input.csv graph output.csv scatter 1,2 log_fc_3,4 5,log_fc_6

Options:
-h --help       prints this message and exit
-v              verbose mode
-q		quiet mode

'''
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
