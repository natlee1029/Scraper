import pandas as pd

def clean_teenlife_data(df):
	dictionary_na = {'ages': '0', 'application fee': 0, 'description' : 'No description specified',
					 'category': 'No subject specified', 'destinations': 'No country specified',
					 'location': 'No city specified', 'minimum cost': 0, 'website': 'No url specified',
					 'title': 'No title specified'}
	min_ages = []
	max_ages = []
	total_cost = []
	columns_to_drop = []
	for i in df.columns:
		if i not in dictionary_na:
			columns_to_drop.append(i)
	df = df.fillna(dictionary_na)
	for index, row in df.iterrows():
		row['title'] = row['title'][16:-13]
		cost = int(row['application fee']) + int(row['minimum cost'])
		total_cost.append(cost)
		if row['ages'] != '0':
			min_ages.append(int(df.at[index, 'ages'][0]))
			max_ages.append(int(df.at[index, 'ages'][-1]))
		else:
			min_ages.append(0)
			max_ages.append(0)
		if row['destinations'][0] == '[' or row['destinations'][-1] == ']':
			destination = 'multiple'
		else:
			destination = row['destinations']
		df.at[index, 'destinations'] = destination
	df['min_ages'] = min_ages
	df['max_ages'] = max_ages
	df['total_cost'] = total_cost
	columns_to_drop.append('ages')
	columns_to_drop.append('minimum cost')
	columns_to_drop.append('application fee')
	df = df.drop(columns = columns_to_drop)
	return df

def write_to_csv_teenlife(df, file_path):
	df = clean_teenlife_data(df)
	df.to_csv(file_path)
