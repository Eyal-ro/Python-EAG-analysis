from pathlib import Path
import pandas as pd

df = pd.read_csv('All_experiments.ASC', sep="\t", names=['Time','Value'])
Times= df.iloc[:,0]

Find_Signal = Times[Times.str.contains('Signal') == True]
#returns all the places were the word signal is in
Signal_index = Find_Signal.index
#returns the indexes that df later be sliced by
names = []
#the next loop will slice the dataframe and split it into a list of data frames.
#Each object in this list is an experiment
for i,j in enumerate(Signal_index):
    names.append(i)
    if i < (len(Signal_index) - 1):
        names[i] = pd.DataFrame(df[Signal_index[i]:Signal_index[i+1]])
        names[i].reset_index(drop=True, inplace=True)
    else:
        names[len(Signal_index)-1]= pd.DataFrame(df[Signal_index[i]:])
        names[-1].reset_index(drop=True, inplace=True)

Output = pd.concat(names, axis=1)
#Combines all list objects into 1 dataframe
Output.to_excel("oil (1-3,13-14).ASC.xlsx")
#Exporting this df into a file

# Next steps:
# outputs to excel all files into sheets.

