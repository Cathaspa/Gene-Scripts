import sys
import time
import numpy as np
import pandas as pd
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
                print('ERROR: your input \'%s\' was invalid! E0' % (inpt))
                sys.exit()
        elif (int(inpt) > 1) & (int(inpt) <= len(headers)):
                cols.append(inpt)
        else:
            print('ERROR: your input \'%s\' was invalid! E1' % (inpt))
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


def remove_na_rows(series_arr, gene_names, colour, label):
    output = []
    for i in range(1, len(series_arr)):
        na_frame = pd.DataFrame()
        na_frame['names'] = gene_names
        na_frame[series_arr[0].name] = series_arr[0]  # append control
        na_frame[series_arr[i].name] = pd.Series(series_arr[i])  # append sample
        if colour is not None:
            na_frame[colour.name] = colour
        if label is not None:
            na_frame['label'] = label
        na_frame = na_frame.dropna(axis=0, how='any')
        output.append(na_frame)
    return(output)


def log2(series):
    return series.apply(lambda x: np.log2(x))


def gen_scatter_graphs(samples, gene_names, alpha, colour, label, nolegend, nolog, nodiagonal):  
  
    if len(samples) < 2:
        print('ERROR: Something went wrong! E3')
        sys.exit()
    graph_sets = remove_na_rows(samples, gene_names, colour, label)   

    count = 1
    for gs in graph_sets:
        if not nolog:
            gs.iloc[:,1] = log2(gs.iloc[:,1])
            gs.iloc[:,2] = log2(gs.iloc[:,2])

        if not nodiagonal:
            shapes = [
                {
                    'type': 'line',
                    'opacity': 0.5,
                    'xref': 'paper',
                    'yref': 'paper',
                    'x0': 0,
                    'y0': 0,
                    'x1': 1,
                    'y1': 1,
                    'line': {
                        'color': '#1f77b4',
                        'width': 2,
                }}]
        else:
            shapes = []

        print('Sample ' + str(count) + ':')
        count = count + 1
        graphs = []
        print('Computing main graph...')
        graph = go.Scatter(
            x=gs.iloc[:, 1].values,
            y=gs.iloc[:, 2].values,
            mode='markers',
            name='Sample ' + str(gs.columns.values[2]),
            text=gs.iloc[:, 0].values)
        graphs.append(graph)

        if label is not None:
            print('Computing 10 largest and 10 smallest values of given label input...')
            sorted = gs.sort_values(['label'])
            largest = sorted.iloc[0:10,]
            smallest = sorted.iloc[-10:,]
            graph = go.Scatter(
                x=largest.iloc[:, 1].values,
                y=largest.iloc[:, 2].values,
                mode = 'markers+text',
                name = 'Largest',
                marker = dict(color = 'rgba(0,0,152,1)'),
                text=largest.iloc[:, 0].values,
                textposition='bottom',
                textfont=dict(
                    family='sans serif',
                    size=18,
                    color='#cf3523'
            ))
            graphs.append(graph)
            graph = go.Scatter(
                x=smallest.iloc[:, 1].values,
                y=smallest.iloc[:, 2].values,
                mode = 'markers+text',
                name = 'Smallest',
                marker = dict(color = 'rgba(0,0,152,1)'),
                text=smallest.iloc[:, 0].values,
                textposition='bottom',
                textfont=dict(
                    family='sans serif',
                    size=18,
                    color='#1f77b4'
            ))
            graphs.append(graph)

        if colour is not None:
            graphs.pop(0)  # Removing main graph, since it will be represented
            # by the pvalue comparisons anyway.
            print('Computing pvalues relative to alpha...')
            more = gs[gs.iloc[:,3] > alpha]
            less = gs[gs.iloc[:,3] <= alpha]
            graph = go.Scatter(
                x=more.iloc[:, 1].values,
                y=more.iloc[:, 2].values,
                mode = 'markers',
                name = 'Above ' + str(alpha),
                marker = dict(color = 'rgba(0,0,0,1)'),
                text=more.iloc[:, 0].values)
            graphs.append(graph)
            graph = go.Scatter(
                x=less.iloc[:, 1].values,
                y=less.iloc[:, 2].values,
                mode = 'markers',
                name = 'Below ' + str(alpha),
                marker = dict(color = 'rgba(255,0,0,1)'),
                text=less.iloc[:, 0].values)
            graphs.append(graph)

        
        layout = go.Layout(
            title=('Sample ' + gs.columns.values[2]),
            xaxis=dict(title='Control: ' + gs.columns.values[1]),
            yaxis=dict(title=gs.columns.values[2]),
            shapes=shapes,
            showlegend=nolegend
        )

        fig = go.Figure(data=graphs, layout=layout)
        plot(fig, filename='sample_' + str(gs.columns.values[2]) + '.html', auto_open=False)


def gen_heat_graphs(samples, gene_names, nolog):
    # samples = list of Series
    df = pd.concat(samples, axis=1, keys=[s.name for s in samples])
    df = pd.concat([pd.DataFrame(gene_names), df], axis=1)
    df = df.dropna(how='any')
    samples = df.iloc[:,1:]
    if not nolog:
        for i in range(len(list(samples))):
            samples.iloc[:,i] = log2(samples.iloc[:,i])
        samples = samples.dropna(how='any')
    gene_names = df.iloc[:,0:1].squeeze()
    
    # colorscales
    max = samples.values.max()
    min = samples.values.min()
    if min < 0:
        min = min * (-1)
    truemax = max if max > min else min
    colorscale=[[0.0, 'FF0000'],
                [0.1, 'FF3333'],
                [0.2, 'FF6666'],
                [0.3, 'FF9999'], 
                [0.4, 'FFCCCC'],
                [0.5, 'FFFFFF'],
                [0.6, 'CCCCFF'],
                [0.7, '9999FF'],
                [0.8, '6666FF'],
                [0.9, '3333FF'],
                [1.0, '0000FF']]
    print(samples)
    graph = go.Heatmap(
        z=samples.values.tolist(), 
        x=list(samples), 
        y=gene_names, 
        colorscale=colorscale, 
        zmin = truemax * (-1), 
        zmax = truemax)
    name = 'heatmap'
    for s in list(samples):
        name = name + '_' + str(s)
    plot([graph], filename = 'ttt.html', auto_open=False)
    
# master function
def input(inputfile, scatter, heat, alpha, colour, label, nolegend, nolog, nodiagonal, control, samples):
    if bool(alpha) ^ bool(colour):  # if alpha xor colour
            print('ERROR: When using alpha or colour, you must specify *both* values! Exiting.')
            sys.exit()

    data = pd.read_csv(inputfile, skipinitialspace=True)
    index_arr = []
    index_arr.append(verify_inputs(control.split(','), list(data)))
    for sample in samples:
        index_arr.append(verify_inputs(sample.split(','), list(data)))

    graph_arr = gen_graph_array(data, index_arr)
    gene_symbols = np.array(data.iloc[:, 0].values).tolist()

    # Extra stuff
    if colour:
        col_arr = verify_inputs(colour.split(','), list(data))
        colour = gen_graph_array(data, [col_arr])[0]
    if label:
        label_arr = verify_inputs(label.split(','), list(data))
        label = gen_graph_array(data, [label_arr])[0]

    if scatter:
        print('\nGenerating scatter graph(s).')
        gen_scatter_graphs(graph_arr, gene_symbols, alpha, colour, label, nolegend, nolog, nodiagonal)
    if heat:
        print('\nGenerating heat graph.')
        gen_heat_graphs(graph_arr, gene_symbols, nolog)
    print('Done.')

