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


def gen_graph_array(data, index_arr):
    output = []  # array of DataFrames
    for i in range(len(index_arr)):
        sample_frame = pd.DataFrame()
        for index in index_arr[i]:
            sample_frame[str(list(data)[index])] = data.iloc[:, index].values
        name = sample_frame.columns[0]
        for col in range(1, len(sample_frame.columns)):
            name = name + ', ' + sample_frame.columns[col]
        if len(sample_frame.columns) > 1:
            sample_frame = sample_frame.mean(axis=1)
        sample_frame = sample_frame.squeeze()
        sample_frame = sample_frame.rename(name)
        output.append(sample_frame.squeeze())  # Append only series
    return output


def gen_graphs(samples, gene_names):
    print('gl')
    if len(samples) < 2:
        print('Something went wrong! E3')
        sys.exit()
    samples = remove_na_rows(samples, gene_names)
    for samp in samples:
        graph = go.Scattergl(
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
        plot(fig, filename='Sample_' + str(samp.columns.values[2]) + '.html', auto_open=False)


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
    print('neat')
    data = pd.read_csv(inputfile, skipinitialspace=True)
    index_arr = []  # array of DataFrames
    index_arr.append(verify_inputs(control.split(','), list(data)))
    for sample in samples:
        index_arr.append(verify_inputs(sample.split(','), list(data)))
    graph_arr = gen_graph_array(data, index_arr)
    gen_graphs(graph_arr, np.array(data.iloc[:, 0].values).tolist())
