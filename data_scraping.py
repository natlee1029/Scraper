import pandas as pd
import sys
import csv


def clean_data(df):
	df = df.transpose()
    df = df.set_index(pd.Index(list(range(len(df)))))
    for index, row in df.iterrows():
    	if row['ages'] != '0':
    		value = df.at[index, 'ages'][2:4] + '-' + df.at[index, 'ages'][-4:-2]
		else:
			value = 'No age specified'
		df.set_value(index, 'ages', value)

    

