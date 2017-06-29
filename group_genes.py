'''
Copyright (c) 2017 Anne-Laure Ehresmann 
Licenced under the MIT License (https://en.wikipedia.org/wiki/MIT_License)
version 1.0.1

Guidelines

This script uses python3, and the package "pandas".

It allows you to take multiple batch comparisons, and generates a file with a single row for each gene.
If a specific gene was in batch 1 but not in batch 2, a value of "None" will be entered in the batch 2 column.

You can change what is written in case it is not found: change the value on line 66.

Call this script with: group_genes.py [filename].csv

The first line of your input file is ignored: it is understood that it will be used for titling.

It is assumed that the sheet is in the following format: odd numbered columns are gene
symbols, even numbered columns are log_FC (log fold change) values.
'''
 
import sys
import pandas as pd

def build_samples(data_file):
    headers = pd.read_csv(data_file, index_col=0,nrows=1) # reads only first row, just to get column quantity.
    samples = []
    i = 0
    while i < len(list(headers)):
        sample = pd.read_csv(data_file, skipinitialspace=True, usecols = [i, i + 1])
        sample = sample.dropna() # removing NaN rows
        finished = pd.DataFrame([["~~FinishedRow", 0]], columns = list(sample))
        sample = sample.append(finished, ignore_index = True) # adding this to delimit the end of the column. Note: obviously, don't name a gene '~~FinishedRow'.
        samples.append(sample)
        i += 2
    return samples

def build_indexes(length):
    indexes = []
    for i in range(length):
        indexes.append(0)
    return indexes

def get_last(samples):
    max = "!" # The first visible character in the ASCII table is '!'. This is to guarantee the variable will be rewritten.
    for sample  in samples:
        sample_max = sample.iloc[-2,0] 
        if(sample_max > max):
            max = sample_max
    return max

def process_line(vals, output):
    newline = []
    current = "~" # Same logic as in get_last() but reversed. '~' is one of the last characters.
    for i  in range(len(samples)):
        vals[i] = samples[i].iloc[indexes[i],0]
        if (vals[i] < current) & (vals[i] != "FinishedRow"):
            current = vals[i]
    newline.append(current)
    for i in range(len(samples)):
        if current == vals[i]:
            newline.append( samples[i].iloc[indexes[i],1])
            if (indexes[i] < len(samples[i]) - 1) & (vals[i] != "FinishedRow"):
                indexes[i] += 1
        else:
            newline.append("None")
    output.loc[len(output)] = newline
    return current

def capitalise(sample):
    samp_series = sample.iloc[:,0]
    samp_series = samp_series.str.capitalize()
    return pd.concat([samp_series, sample.iloc[:,1]],axis=1)

if (len(sys.argv) < 2):
    print("You must give me (at-least / only) one source file. Exiting.")
    sys.exit()

samples = build_samples(sys.argv[1])

if len(sys.argv) < 3 or (sys.argv[2] != 'y'):
    print("Capitalising genes... Note that if your input file already contains only capital letters, and is sorted, you can pass 'y' after passing your input file to skip this step.")
    for i in range(len(samples)):
        samples[i] = capitalise(samples[i])
    print("Sorting...")
    for i in range(len(samples)):
        samples[i] = samples[i].sort_values( [list(samples[i])[0]])

indexes = build_indexes(len(samples))
vals = build_indexes(len(samples))
last_gene = get_last(samples)
headers = []
headers.append(list(samples[0])[0]) # add first gene name
# add each log_FC columns' headers
for i in range(0, len(samples)):
    headers.append(list(samples[i])[1])

# empty dataframe to append to, with column headers built above
output = pd.DataFrame(columns=headers)
more = process_line(vals,output)
count = 0
print("Computing....")
while more != last_gene:
     count +=1
     more = process_line(vals,output)
     if( count%1000  == 0):
         print("Computed %d rows..." % (count))
print("Done")  
output.to_csv("output.csv", index=False)
