import pandas as pd


INDEX_IGNORE = set(['a', 'also', 'an', 'and', 'are', 'as', 'at', 'be',
                    'but', 'by', 'course', 'for', 'from', 'how', 'i',
                    'ii', 'iii', 'in', 'include', 'is', 'not', 'of',
                    'on', 'or', 's', 'sequence', 'so', 'social', 'students',
                    'such', 'that', 'the', 'their', 'this', 'through', 'to',
                    'topics', 'units', 'we', 'were', 'which', 'will', 'with',
                    'yet', 'summer', 'program', 'on', 'teenlife'])


def clean_teenlife_data(df):
	dictionary_na = {'ages': '0', 'application fee': 0, 'description' : 'No description specified',
					 'category': 'No subject specified', 'destinations': 'No country specified',
					 'location': 'No city specified', 'minimum cost': 0, 'website': 'No url specified',
					 'title': 'No title specified'}
	min_ages = []
	max_ages = []
	total_cost = []
	description_list = []
	columns_to_drop = []
	for i in df.columns:
		if i not in dictionary_na:
			columns_to_drop.append(i)
	df = df.fillna(dictionary_na)
	for index, row in df.iterrows():
		# description_dict = {}
		# list_of_words = row['description'].split(' ')
		# for i in list_of_words:
		# 	if i in INDEX_IGNORE:
		# 		list_of_words.remove(i)
		# for word in list_of_words:
		# 	description_dict[index] = word
		row['title'] = row['title'][16:-13]
		cost = int(row['application fee']) + int(row['minimum cost'])
		total_cost.append(cost)
		if row['ages'] != '0':
			min_ages.append(int(df.at[index, 'ages'][0]))
			max_ages.append(int(df.at[index, 'ages'][-1]))
		else:
			min_ages.append(0)
			max_ages.append(0)
		if row['destinations'][0] == '[' or row['destinations'][-1] == ']' or type(row['destinations']) == list:
			destination = 'multiple countries'
		else:
			destination = row['destinations']
		df.at[index, 'destinations'] = destination
		# description_list.append(description_dict)
	df['min_ages'] = min_ages
	df['max_ages'] = max_ages
	df['total_cost'] = total_cost
	columns_to_drop.append('ages')
	columns_to_drop.append('minimum cost')
	columns_to_drop.append('application fee')
	# columns_to_drop.append('description')
	df = df.drop(columns = columns_to_drop)
	return df

def write_to_csv_teenlife(df, file_path):
	df = clean_teenlife_data(df)
	df.to_csv(file_path)
