import re
import util
import bs4
import queue
import json
import sys
import csv


def crawler(filename, index_filename):
	starting_url = "https://www.teenlife.com/search"
	limiting_domain = "teenlife.com"

	