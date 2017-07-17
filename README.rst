========
HelixPC
========

A series of scripts for gene database automation. Developed for the
Philippe Campeau Laboratory.


.. image:: http://i.imgur.com/pRZoaiC.png
  :width: 800px
  :align: center
  :alt: alternate text


Installation
------------

Dependencies
^^^^^^^^^^^^
* pandas 
* numpy 
* plotly


Clone the repository, and install the dependencies. Looking into
`pip <https://pypi.python.org/pypi/pip>`_ will make installing the
python packages notably easier.

Once finished, you can call the script with::

  $ python helixpc.py [options] 
    
Usage
-----

Generating a file for the graphing utility
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::
 
$ helixpc.py group <group_input> [--nonan]

If you do not yet have a valid input file for graph generation, the
command ``group`` can help you generate one automatically. Simply stick
all your batches in a single csv file, call the utility and a file
named ``output.csv`` will be generated. You can then feed to the
graphing utility.

input file format: 
""""""""""""""""""

- Check the example ``group_input.csv``
- The first row should specify the column titles.  
- You *must* call the columns containing gene names ``gene_symbol``, 
  they are used as columns of reference by the scripts.

note that: 

- If certain genes are included multiple times, their
  mean will be calculated, and only a single entry will appear in 
  the output.
 
- you may pass ``[--nonan]`` or ``[-n]`` to omit any gene that
  are missing entries in a batch.  

Using the graphing utility
^^^^^^^^^^^^^^^^^^^^^^^^^^
::

$ helixpc.py graph <graph_input> [--heat] [--scatter] <control> <sample> [<sample> ...]

Once you have a csv file that you want to use for generating graph,
you may feed it to the graphing utility.  You must give the csv file a
series of arguments for it to function properly:

``--scatter``

Specifies that you want scatter graph(s).  Scatter graphs are
generated with a control (always the same) in the x axis, and a sample
in the y axis. Giving more than one sample will return to you multiple
graphs, one for each sample. You can hover over each point to see the
name of the gene it is representing.

``--heat``

Specifies that you want a heat graph.  Not implemented yet.

``<control>``

Specifies the control. You may give an index or the name of a
column. You may also give a series of indexes/column-names separated
by a comma, and the values used will be the mean of each row for the
series of columns given.

``<sample>``

Specifies the first sample. You may give an index or the name of a
column. You may also give a series of indexes/column-names separated
by a comma, and the values used will be the mean of each row for the
series of columns given.

``[<sample> ...]``

indicates that you can give more than one sample, simply separate each
sample with a space.

input file format:
""""""""""""""""""

- Check the example ``graph_input.csv`` The first row should specify
  the column titles.
- The first col should contain ``gene_symbol`` 
