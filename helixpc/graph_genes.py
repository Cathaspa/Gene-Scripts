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


def gen_graphs(samples, gene_names, alpha, colour, label, nolegend):    
    if len(samples) < 2:
        print('Something went wrong! E3')
        sys.exit()
    graph_sets = remove_na_rows(samples, gene_names, colour, label)
    count = 1
    for gs in graph_sets:
        print('Sample ' + str(count) + ':')
        count = count + 1
        graphs = []
        print('Computing main graph...')
        graph = go.Scattergl(
            x=gs.iloc[:, 1].values,
            y=gs.iloc[:, 2].values,
            mode='markers',
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
                name = 'largest',
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
                name = 'smallest',
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
            showlegend=nolegend
        )

        fig = go.Figure(data=graphs, layout=layout)
        plot(fig, filename='Sample_' + str(gs.columns.values[2]) + '.html', auto_open=False)


# master function
def input(inputfile, scatter, heat, alpha, colour, label, nolegend, control, samples):

    if scatter:
        if bool(alpha) ^ bool(colour):  # if alpha xor colour
            print('When using alpha or colour, you must specify *both* values!')
            system.exit()

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


        gen_graphs(graph_arr, gene_symbols, alpha, colour, label, nolegend)
        
    if heat:
        print(' Heat not implemented yet.')
    print('Done.')

