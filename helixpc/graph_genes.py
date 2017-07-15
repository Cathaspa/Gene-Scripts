import sys
import numpy as np
import pandas as pd
# import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot


def verify_inputs(inpt_arr, headers):
    cols = []
    for inpt in inpt_arr:
        if not inpt.isdigit():
            for j in range(len(headers)):
                valid = False
                if inpt == headers[j]:
                    cols.append(j)
                    valid = True
                    break
            if not valid:
                print('your input \'%s\' was invalid! E0' % (inpt))
                sys.exit()
        elif (int(inpt) > 1) & (int(inpt) <= len(headers)):
                cols.append(inpt)
        else:
            print('your input \'%s\' was invalid! E1' % (inpt))
            sys.exit()
    for i in range(len(cols)):
        cols[i] = int(cols[i]) - 1
    return cols


def gen_graphs(samples, gene_names):
    if len(samples) < 2:
        print('Something went wrong! E3')
        sys.exit()
    samples = remove_na_rows(samples, gene_names)
    for samp in samples:
        graph = go.Scatter(
            x=samp.iloc[:, 1].values,
            y=samp.iloc[:, 2].values,
            mode='markers',
            text=samp.iloc[:, 0].values)
        layout = go.Layout(
            title=('Sample ' + samp.columns.values[2]),
            xaxis=dict(title='Control: ' + samp.columns.values[1]),
            yaxis=dict(title=samp.columns.values[2])
        )
        fig = go.Figure(data=[graph], layout=layout)
        plot(fig, filename='Sample_' + str(samp.columns.values[2]) + '.html')


def remove_na_rows(series_arr, gene_names):
    output = []
    for i in range(1, len(series_arr)):
        na_frame = pd.DataFrame()
        na_frame['names'] = gene_names
        na_frame[series_arr[0].name] = series_arr[0]
        na_frame[series_arr[i].name] = pd.Series(series_arr[i])
        na_frame = na_frame.dropna(axis=0, how='any')
        output.append(na_frame)
    return(output)


# master function
def input(inputfile, scatter, heat, control, samples):
    print(samples)
    data = pd.read_csv(inputfile, skipinitialspace=True)
    index_arr = []  # array of DataFrames
    control_arr = verify_inputs(control.split(','), list(data))
    samples_arr =[]
    for sample in samples:
        validsamp = verify_inputs(sample.split(','), list(data))
        samples_arr.append(validsamp)
    index_arr = [control_arr, samples_arr]
    print(index_arr)
    # gen_graphs(graph_arr, np.array(data.iloc[:, 0].values).tolist())
