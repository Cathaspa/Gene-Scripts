''' Copyright (c) 2017 Anne-Laure Ehresmann
Licenced under the MIT License (https://en.wikipedia.org/wiki/MIT_License)
version 0.0.1
'''

import sys
import numpy as np
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


#TODO: gen_graphs

def verify_inputs(inpt_arr, headers):
    cols = []
    # print("headers: ", headers)
    # print("inpt_arr", inpt_arr)
    if (len(inpt_arr) == 1) & (inpt_arr[0] == "end"):
        return "end"
    for inpt in inpt_arr:
        if not inpt.isdigit():
            for j in range(len(headers)):
                valid = False
                if inpt == headers[j]:
                    cols.append(j)
                    valid = True
                    break
            if not valid:
                print("your input '%s' was invalid! E0" % (inpt))
                return None
        elif (int(inpt) > 1) & (int(inpt) <= len(headers)):
                cols.append(inpt)
        else:
            print("your input '%s' was invalid! E1" % (inpt))
            return None
    for i in range(len(cols)):
        cols[i] = int(cols[i]) - 1
    return cols


def ask_for(query, headers):
    valid = False
    while not valid:
        valid = True
        inpt_arr = input(query).split()
        cols = verify_inputs(inpt_arr, headers)
        if cols is None:
            valid = False
            print("\nRemember, you can logically not give the first" +
                  "row (gene names) as an input. Make sure to spell " +
                  "your column names correctly!\n")
    return cols


def gen_index_array(data):
    output = []
    controls = ask_for("\nAsking for Control(s). Which column(s) are "
                       "the control(s)? \nEnter them " +
                       "with a space in between each. \nYou may enter " +
                       "their name (log_fc...) or their number index " +
                       "(2, 3, ....).\n> ", list(data))
    if controls == "end":
        print("Invalid Control. Exiting.")
        sys.exit()

    output.append(controls)
    more = True
    while more:
        query = ("\nAsking for sample %d. Which " % (len(output)) +
                 "column(s) are in the sample? enter 'end' to stop " +
                 "entering samples.\n>")
        sample = ask_for(query, list(data))
        if sample == "end":
            more = False
        else:
            output.append(sample)

    if len(output) == 1:
        print("No samples. Exiting.")
        sys.exit()
    return output


def gen_graph_array(data, index_arr):
    output = []  # array of DataFrames
    for i in range(len(index_arr)):
        col_arr = pd.DataFrame() 
        for index in index_arr[i]:
            col_arr[str(index)] = data.iloc[:,index].values
        if len(col_arr.columns) > 1:  # if two or more cols have been given,
            col_arr = col_arr.mean(axis = 1)  # get the mean
        output.append(col_arr)
    return output

def gen_graphs(samples,gene_names):
    if len(samples) < 2:
        print("Something went wrong! E3")
    control = np.array(samples[0].values).tolist()

    for i in range(1, len(samples)):
        sample = np.array(samples[i].values).tolist()
        for j in range(len(control)):
            if np.isnan(control[j]):
                control[j] = "NA"
            if np.isnan(sample[j]):
                sample[j] == "NA"
        print("len:",len(control),len(samples[i]))
        print(control)
        print(sample)
        graph = go.Scatter(
            x=control,
            y=sample,
            mode='markers')
        layout = go.Layout(title=("Sample"))
        fig = go.Figure(data=graph, layout=layout)
        plot_url = plot(fig, filename="Sample.html")
    
if len(sys.argv) != 2:
    print("You must give me (at-least / only) one source file. Exiting.")
    sys.exit()

data = pd.read_csv(sys.argv[1], skipinitialspace=True)
print(np.array(data.iloc[:,0].values).tolist())
graph_arr = gen_graph_array(data, gen_index_array(data))
gen_graphs(graph_arr, np.array(data.iloc[:,0].values).tolist())
