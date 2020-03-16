import pandas as pd
import rustic_pathways
import teenlife_crawler
import summer_discovery


df_teenlife = teenlife_crawler.crawler()
df_rustic = rustic_pathways.crawler()
df_summer = summer_discovery.crawler()

for i, row in df_teenlife.iterrows():
	row['title'] = row['title'][16:-13]

for i, row in df_rustic.iterrows():
	row


INDEX_IGNORE = set(['a', 'also', 'an', 'and', 'are', 'as', 'at', 'be',
                    'but', 'by', 'course', 'for', 'from', 'how', 'i',
                    'ii', 'iii', 'in', 'include', 'is', 'not', 'of',
                    'on', 'or', 's', 'sequence', 'so', 'social', 'students',
                    'such', 'that', 'the', 'their', 'this', 'through', 'to',
                    'topics', 'units', 'we', 'were', 'which', 'will', 'with',
                    'yet', 'summer', 'program', 'on', 'teenlife'])

dictionary_na = {'ages': '0', 'description' : 'No description specified',
					 'category': 'No subject specified', 'destinations': 'No country specified',
					 'location': 'No city specified', 'minimum cost': 0, 'website': 'No url specified',
					 'title': 'No title specified'}

rename_rustic = {'service types' : 'category', 'countries': 'destinations'}

rename_summer = {}



def clean_teenlife_data(df):
	min_ages = []
	max_ages = []
	columns_to_drop = []
	for i in df.columns:
		if i not in dictionary_na:
			columns_to_drop.append(i)
	df = df.fillna(dictionary_na)
	for index, row in df.iterrows():
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
	df['min_ages'] = min_ages
	df['max_ages'] = max_ages
	columns_to_drop.append('ages')
	df = df.drop(columns = columns_to_drop)
	return df

def write_to_csv_teenlife(df, file_path):
	df = clean_teenlife_data(df)
	df.to_csv(file_path)
