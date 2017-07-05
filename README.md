# Helix
A series of scripts for gene database automation. Use helix.py to give
your input.

## Dependencies

* python3.6

#### Python Packages

* pandas
* numpy
* plotly

## Usage

#### Generating a file for the graphing utility

##### `helix.py group <group_input>`

If you do not yet have a valid input file for graph generation, the
command `group` can help you generate one automatically. Simply stick
all your batches in a single csv file, call the utility and a file named `output.csv` will be
generated. You can then feed to the graphing utility.

The first line of your input file  is ignored: it is understood that
it will be used for titling. You can check the example file
`group_input.csv`

### Using the graphing utility

##### `helix.py graph <graph_input> [--heat] [--scatter] <control> <sample> [<sample> ...]`

Once you have a csv file that you want to use for generating graph, you may feed it to the graphing utility.
You must give the csv file a series of arguments for it to function
properly:

###### `--scatter`
Specifies that you want scatter graph(s).

Scatter graphs are generated with a control (always the same) in the x
axis, and a sample in the y axis. Giving more than one sample will
return to you multiple graphs, one for each sample. You can hover over
each point to see the name of the gene it is representing.

###### `--heat`
Specifies that you want a heat graph.

Not implemented yet.

###### `<control>`
Specifies the control. You may give an index or the
name of a column. You may also give a series of indexes/column-names
separated by a comma, and the values used will be the mean of each
row for the series of columns given.

###### `<sample>`
Specifies the first sample. You may give an index or the
name of a column. You may also give a series of indexes/column-names
separated by a comma, and the values used will be the mean of each
row for the series of columns given.

###### `[<sample> ...]`
indicates that you can give more than one sample,
simply separate each sample with a space.
