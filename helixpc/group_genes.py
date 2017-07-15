import sys
import pandas as pd


def build_samples(data_file):
    data = pd.read_csv(data_file, skipinitialspace=True)
    headers = list(data)
    samples = []

    sample = pd.DataFrame()
    current = 0
    next = 1
    max = len(data.columns)
    while next <= max:
        # removing NaN rows at the very end of the file
        col = data.iloc[:, current].dropna()
        sample[headers[current]] = col
        if (next == max) or ('gene_symbol' in headers[next]):
            samples.append(sample)
            sample = pd.DataFrame()
        current += 1
        next += 1
    return samples


def capitalise(sample):
    samp_series = sample.iloc[:, 0]
    samp_series = samp_series.str.upper()
    return pd.concat([samp_series, sample.iloc[:, 1:len(sample)]], axis=1)


def get_mean_of_dups(sample):
    sample = sample.groupby('gene_symbol').mean().reset_index()
    return sample

# master function
def input(inputfile, output, nonan, sort):
    print(output)
    print('Building database structure...')
    samples = build_samples(inputfile)
    if  not sort:
        print('Capitalising genes...')
        for i in range(len(samples)):
            samples[i] = capitalise(samples[i])
        print('Sorting...')
        for i in range(len(samples)):
            samples[i] = samples[i].sort_values([list(samples[i])[0]])

    all = samples[0].copy(deep=True)
    all = get_mean_of_dups(all)
    for i in range(1, len(samples)):
        s = samples[i]
        if 'gene_symbol' in s.columns[0]:
            cols = s.columns.values
            cols[0] = 'gene_symbol'
            s.columns = cols
        s = get_mean_of_dups(s)
        all = all.merge(s, how='outer', on='gene_symbol', copy=False)
    all = all.sort_values([list(all)[0]])
    if nonan:
        print('Excluding rows with missing entries...')
        all = all.dropna()
    all.to_csv((output+'.csv'), index=False)
