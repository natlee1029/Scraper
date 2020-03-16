import sqlite3
import os

DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'programs.db')


def demo(args):
	'''
	args (dictionary): list of the
	'''
	connection = sqlite3.connect(DATABASE_FILENAME)
	cursor = connection.cursor()
	select_string, search_values = get_s(args)
	print(select_string)
	print(search_values)
	table = cursor.execute(select_string, search_values)
	header = get_header(table)
	programs = table.fetchall()
	print(programs)
	return (header, programs)

def get_s(args_from_ui):
	select_string = 'SELECT '
	select_string += select_columns(args_from_ui, select_string)
	select_string += " FROM programs WHERE "
	list_of_args = []
	for key, value in args_from_ui.items():
		if key == "terms":
			select_string += 'description LIKE ? AND '
			value = '%' + str(value) + '%'
		if key == 'cost_lower':
			select_string += 'cost >= ? AND '
		if key == 'cost_upper':
			select_string += 'cost <= ? AND '
		if key == 'age_lower':
			select_string += 'min_age >= ? AND '
		if key == 'age_upper':
			select_string += 'max_age <= ? AND '
		if key == 'city' or key == "state":
			select_string += 'city LIKE ? AND '
			value = "%" + str(value) + "%"
		if key == "country":
			select_string += 'country LIKE ? AND '
			value = "%" + str(value) + "%"
		if key == 'subject':
			select_string += 'category LIKE ? AND '
			value = "%" + str(value) + "%"
		list_of_args.append(value)
	select_string = select_string[:-5] + ';'
	return (select_string, list_of_args)


def select_columns(args_from_ui, select_string):
	terms = ["title"]
	for key in args_from_ui.keys():
		if key == "cost_lower" or key == "cost_upper":
			if 'cost' not in terms:
				terms.append("cost")
		if key == "age_lower" or key == "age_upper":
			if "min_age" not in terms or "max_age" not in terms:
				terms.append("min_age")
				terms.append('max_age')
		if key == 'city':
			terms.append("location")
		if key == "country":
			terms.append('country')
		if key == "subject":
			terms.append("category")
	terms.append('website')
	return ", ".join(terms)


def get_header(cursor):
    '''
    Given a cursor object, returns the appropriate header (column names)
    '''
    desc = cursor.description
    header = ()

    for i in desc:
        header = header + (clean_header(i[0]),)

    return list(header)


def clean_header(s):
    '''
    Removes table name from header
    '''
    for i, _ in enumerate(s):
        if s[i] == ".":
            s = s[i + 1:]
            break

    return s
