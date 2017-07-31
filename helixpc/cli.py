import argparse
import sys
from helixpc import group_genes, graph_genes, __version__
# import group_genes, graph_genes  # for development use.
# __version__ = 'CHANGETHIS'  # for development use.


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--version', action='version', 
                        version='%(prog)s ' + __version__)
    subparsers = parser.add_subparsers(title='subcommands - Type \'helix.py' +
                                       ' [function] -h\' to find out more. It ' +
                                       ' is highly recommended that you read '+
                                       'the README.rst for guidance.',
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
    graph_parser.add_argument('-a', '--alpha', type=float,
                              help='Determines the alpha value for scatter ' +
                              ' graphs. Everything underneath (including) this ' +
                              'value will be colored red.')
    graph_parser.add_argument('-p','--pvalue', help='Lists the column(s) to be ' +
                              'used for pvalues.')
    graph_parser.add_argument('-l', '--label', help='specifies which column ' +
                              'should be used for labelling the 10 with the ' +
                              'highest values and the 10 with the lowest values.')
    graph_parser.add_argument('-nl', '--no-legend', action='store_false', 
                              help='disables legend display', default=True)
    graph_parser.add_argument('-nlg', '--no-log', action='store_true', 
                              help='disables log_2 of all values.', default=False)
    graph_parser.add_argument('-nd', '--no-diagonal', action='store_true',
                              help='disables the diagonal blue x=x line going across the graph.', default=False)
    graph_parser.add_argument('control', help='specifies the control')
    graph_parser.add_argument('samples', nargs='+', help='specifies the ' +
                              'samples.')



    args = parser.parse_args()

    # early error handling
    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit()
    if (args.input is not None and args.input[-4:] != '.csv'):
        print("ERROR: Input file must be in the .csv format.")
        sys.exit()
    if args.command == 'graph':
        if args.heat is not True and args.scatter is not True:
            args.heat = True
            args.scatter = True
        graph_genes.input(args.input, args.scatter, args.heat, args.alpha, args.pvalue, 
                          args.label, args.no_legend, args.no_log, args.no_diagonal, args.control, args.samples)
    else:
        group_genes.input(args.input, args.output, args.nonan, args.yes, args.round)


main()
