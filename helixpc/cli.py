import argparse
import sys
from helixpc import group_genes, graph_genes
# import group_genes, graph_genes  # for development use.

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands - Type \'helix.py' +
                                       ' [function] -h\' to find out more',
                                       metavar='', dest='command')

    # group subcommand
    group_parser = subparsers.add_parser('group', help='Group a series of fold ' +
                                         'change samples into a sing,le file ' +
                                         'with entries for every gene.')
    group_parser.add_argument('input', help='input file name')
    group_parser.add_argument('output', nargs='?',
                              help='output file name (optional)',
                              default='output')
    group_parser.add_argument('-n', '--nonan', action='store_true',
                              help='specifies if rows including at least  ' +
                              'one missing entry should be omitted.')
    group_parser.add_argument('-y', '--yes', action='store_true',
                              help='specifies if the file is already ' +
                              'capitalised and sorted or not.')
    group_parser.add_argument('-r','--round', type=int,
                              help='specifies by how much the values ' +
                              'should be rounded by.')


    # graph subcommand
    graph_parser = subparsers.add_parser('graph', help='Graphs a database of ' +
                                         'genes according to given controls.' +
                                         ' Takes the output of the [group]' +
                                         ' function as input.')
    graph_parser.add_argument('input', help='input file name')
    graph_parser.add_argument('-s', '--scatter', action='store_true',
                              help='generates scatter graph(s)')
    graph_parser.add_argument('-he', '--heat', action='store_true',
                              help='generates heat graph(s)')
    graph_parser.add_argument('control', help='specifies the control')
    graph_parser.add_argument('samples', nargs='+', help='specifies the ' +
                              'samples')

    args = parser.parse_args()

    # early error handling

    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit()
    if (args.input is not None and args.input[-4:] != '.csv'):
        print("Input file must be in the .csv format.")
        sys.exit()
    if args.command == 'graph':
        if args.heat is not True and args.scatter is not True:
            args.heat = True
            args.scatter = True
        graph_genes.input(args.input, args.scatter, args.heat, args.control, args.samples)
    else:
        group_genes.input(args.input, args.output, args.nonan, args.yes, args.round)


main()
