'''
Copyright (c) 2017 Anne-Laure Ehresmann
Licenced under the MIT License (https://en.wikipedia.org/wiki/MIT_License)
'''

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


if (len(sys.argv) < 2):
    print('You must give me (at-least / only) one source file. Exiting.')
    sys.exit()
samples = build_samples(sys.argv[1])

if len(sys.argv) < 3 or (sys.argv[2] != 'y'):
    print('Capitalising genes... Note that if your input file ' +
          'already contains only capital letters, and is sorted, you ' +
          'can pass \'y\' after passing your input file to skip this step.')
    for i in range(len(samples)):
        samples[i] = capitalise(samples[i])
    print('Sorting...')
    for i in range(len(samples)):
        samples[i] = samples[i].sort_values([list(samples[i])[0]])


def get_mean_of_dups(sample):
    sample = sample.groupby('gene_symbol').mean().reset_index()
    return sample


all = samples[0].copy(deep=True)
all = get_mean_of_dups(all)
for i in range(1, len(samples)):
    s = samples[i]
    if 'gene_symbol' in s.columns[0]:
        cols = s.columns.values
        cols[0] = 'gene_symbol'
        s.columns = cols
    s = get_mean_of_dups(s)
    print(type(s))
    all = all.merge(s, how='outer', on='gene_symbol', copy=False)
print(all)
all.to_csv('output.csv', index=False)
