import sqlite3
import os

DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'course-info.db')

def find_listings(args):
	'''
	args (dictionary): list of the 
	'''