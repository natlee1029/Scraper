import sqlite3
import os

DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'program_info.db')

demo_string1 = 'SELECT program_url FROM program_info WHERE fee < ?'
demo_string2 = 'SELECT program_url FROM program_info WHERE subject = ?'
demo_arg1 = [500]
demo_arg2 = ['stem']

def demo(database, s, args):
	'''
	args (dictionary): list of the 
	'''
	connection = sqlite3.connect(database)
	cursor = connection.cursor()
	table = cursor.execute(s, args)
	header = get_header(table)
	courses = table.fetchall()
	return (header, courses)


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
