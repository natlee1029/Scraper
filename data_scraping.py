import pandas as pd
import sys
import csv

def clean_data(df):
	dictionary_na = {'ages': '0', 'application deadline' : 0, 'application fee': 0,
					 'category': 'No subject specified', 'destinations': '0', 'location': '0',
					 'minimum_cost': 0, 'website': 'No url specified'}
	df = df.transpose()
	df = df.set_index(pd.Index(list(range(len(df)))))
	columns_to_drop = []
	for i in df.columns:
		if i not in dictionary_na:
			columns_to_drop.append(i)
	df = df.drop(columns = columns_to_drop)
	df = df.fillna(dictionary_na)
	for index, row in df.iterrows():
		if row['ages'] != '0':
			value = df.at[index, 'ages'][0] + '-' + df.at[index, 'ages'][-1]
		else:
			value = 'No age specified'
		if row['destinations'][0] == '[':
			destination = 'multiple'
		elif row['destinations'] == '0':
			destination = 'No country specified'
		else:
			destination = row['destinations']
		df.at[index, 'ages'] = value
		df.at[index, 'destinations'] = destination
	return df

def write_to_csv(df, file_path):
	df = clean_data(df)
	df.to_csv(file_path, sep = '|')
