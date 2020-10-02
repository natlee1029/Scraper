This was a quarter long CS project to apply webscraping to a unique dataset. We scraped, cleaned, and updated summer camp datapoints from various websites and aggregated them into a simplistic interface platform created through django. 

## Packages:
Pandas
BeautifulSoup
RegEx


## Files:
teenlife_crawler.py (crawler for teenlife database)
rustic_pathways.py (crawler for rustic pathways website)
summer_discovery.py (crawler for summer discovery website)
data_scraping.py (cleans data scraped from all crawlers and aggregates them into a dataframe)

mysite (django)
    create_tables.sql (converts csv to SQL database)
    data.csv (csv of data from websites)
    summer.py (runs SQL queries)
    

## Usage:
(Run within mysite folder)
python3 manage.py runserver

(for crawlers, used 'mysite/data.csv' as the path for the csv file)
datascraping.write_to_csv(path)

(to create database, change directory into my site folder)
sqlite3 programs.db < create_tables.sql
