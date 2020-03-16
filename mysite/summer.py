import sqlite3
import os

DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'program_info.db')

demo_string1 = 'SELECT program_url FROM program_info WHERE fee < ?'
demo_string2 = 'SELECT program_url FROM program_info WHERE subject = ?'
demo_arg1 = [500]
demo_arg2 = ['stem']

def demo(database, args):
	'''
	args (dictionary): list of the
	'''
	connection = sqlite3.connect(database)
	cursor = connection.cursor()
	select_string, search_values = get_s(args)
	table = cursor.execute(select_string, search_values)
	header = get_header(table)
	programs = table.fetchall()
	return (header, programs)

def get_s(args_from_ui):
	select_string = 'SELECT '
	select_columns(args_from_ui, select_string)
	select_string += " FROM program_info WHERE "
	list_of_args = []
	for key, value in args_from_ui.items():
		if key == "terms":
			select_string += 'description LIKE \'%?%\' AND '
		if key == 'cost_lower':
			select_string += '? >= fee AND '
		if key == 'cost_upper':
			select_string += 'fee <= ? AND '
		if key == 'age_lower':
			select_string += 'min_ages >= ? AND '
		if key == 'age_upper':
			select_string += 'max_ages <= ? AND '
		if key == 'city' or key == "state" or key == "country":
			select_string += 'location LIKE \'%?%\' AND '
		if key == 'subject':
			select_string += 'subject = ? AND '
		list_of_args.append(value)
	select_string = select_string[:-5] + ';'
	return (select_string, list_of_args)


def select_columns(args_from_ui, select_string):
	terms = ["title"]
	for key in args_from_ui:
		if key == "cost_lower" or key == "cost_upper":
			terms.append("minimum_cost")
		if key == "age_lower" or "age_upper":
			terms.append("ages")
		if key == 'city' or key == "state" or key == "country":
			terms.append("location")
		if key == "subject":
			terms.append("category")
	terms.append('website')
	select_string += str(terms).strip('[]')


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
