import os
import pandas
import time
import sqlite3


PATH = os.path.dirname(__file__)
NCAP = [
	os.path.join(PATH, 'ncap', filename) for filename in [
	'2011_NCAP_Combined_Crashworthiness_Ratings_Calculator.csv',
	'2012_NCAP_Combined_Crashworthiness_Ratings_Calculator.csv',
	'2013_NCAP_Combined_Crashworthiness_Ratings_Calculator.csv',
	'2014_NCAP_Combined_Crashworthiness_Ratings_Calculator.csv',
	'2015_NCAP_Combined_Crashworthiness_Ratings_Calculator.csv',
	'2016_NCAP_Combined_Crashworthiness_Ratings_Calculator.csv']
]
NCAP_HEADER = [
	'date_on_web',
	'make',
	'model',
	'year',
	'front_stars_driver',
	'front_stars_passenger',
	'front_stars_combiner',
	'sidemdb_stars_driver',
	'sidemdb_stars_passenger',
	'sidemdb_stars_combiner',
	'sidepole_stars_driver',
	'overall_driver_stars_driver',
	'overall_side_stars_combined',
	'rollover_stars',
	'combined_vss',
	'combined_stars'
]

FARS = {
	i: os.path.join(PATH, 'fars', 'vehicle_%d.dta' % i) for i in range(1975, 2016)
}

DB = os.path.join(PATH, 'dataset.db')


def load_fars():
	print('generating FARS dataset, this will take a few minutes...')
	dataset = pandas.DataFrame()
	for (year, filename) in FILES.items():
		start = time.time()
		dataset = dataset.append(pandas.read_stata(filename))
		elapsed = time.time() - start
		print('{} took {:.2f}s'.format(year, elapsed))
	conn = sqlite3.connect(DB)
	conn.execute('DROP TABLE fars')
	conn.text_factory = str
	dataset.to_sql('fars', conn)
	print('done.')


def load_ncap():
	print('generating ncap dataset...')
	dataset = pandas.DataFrame()
	for filename in NCAP:
		dataset = dataset.append(pandas.read_csv(
			filename,
			names=NCAP_HEADER,
			skiprows=2,
			index_col=False,
			usecols=range(len(NCAP_HEADER)),
			na_values=['#VALUE!','#NUM!']))
	conn = sqlite3.connect(DB)
	conn.execute('DROP TABLE ncap')
	conn.text_factory = str
	dataset.to_sql('ncap', conn)
	print('done.')


if __name__ == '__main__':
	pass
	#conn = sqlite3.connect(DB)
	#conn.text_factory = str
	#dataset = pandas.read_sql_query('''SELECT * from fars WHERE year = 1975''', conn)
	#print dataset.describe()
