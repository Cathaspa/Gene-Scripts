''' Copyright (c) 2017 Anne-Laure Ehresmann
Licenced under the MIT License (https://en.wikipedia.org/wiki/MIT_License)
'''
## TODO: Make labels work for mean, figure out bug when receiving more than one sample
import sys
import numpy as np
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

def verify_inputs(inpt_arr, headers):
    cols = []
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
                 "entering samples.\n> ")
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
        sample_frame = pd.DataFrame()
        for index in index_arr[i]:
            sample_frame[str(list(data)[i+1])] = data.iloc[:,index].values
        if len(sample_frame.columns) > 1:  # If two or more cols have been given,
            print("mean")
            print(sample_frame)
            sample_frame = sample_frame.mean(axis = 1)  # get the mean
        name = list(sample_frame)[0]
        sample_frame = sample_frame.squeeze()
        sample_frame.rename(name)
        output.append(sample_frame.squeeze())  # Append only series
    return output

def gen_graphs(samples, gene_names):
    if len(samples) < 2:
        print("Something went wrong! E3")
        sys.exit()
    samples = remove_na_rows(samples, gene_names)
    for samp in samples:
        graph = go.Scatter(
            x=samp.iloc[:,1].values,
            y=samp.iloc[:,2].values,
            mode='markers',
            text = samp.iloc[:,0].values)
        layout = go.Layout(
            title=("Sample " + samp.columns.values[2]),
            xaxis = dict(title="Control: " + samp.columns.values[1]),
            yaxis = dict(title=samp.columns.values[2])
        )
        fig = go.Figure(data=[graph], layout=layout)
        plot_url = plot(fig, filename="Sample_" + str(samp.columns.values[2]) + ".html")

        
def remove_na_rows(series_arr, gene_names):
    output = []
    for i in range(1, len(series_arr)):
        na_frame = pd.DataFrame()
        na_frame["names"] = gene_names
        na_frame[series_arr[0].name] = series_arr[0]
        na_frame[series_arr[i].name] = pd.Series(series_arr[i])
        na_frame = na_frame.dropna(axis=0, how = "any")
        output.append(na_frame)
    return(output)
         
     
if len(sys.argv) != 2:
    print("You must give me (at-least / only) one source file. Exiting.")
    sys.exit()

data = pd.read_csv(sys.argv[1], skipinitialspace=True)
index_arr = gen_index_array(data)
graph_arr = gen_graph_array(data, index_arr)
gen_graphs(graph_arr, np.array(data.iloc[:,0].values).tolist())
