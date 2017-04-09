import os
import numpy
import pandas


PATH = os.path.dirname(__file__)

dataoneFilepath = os.path.join(
	PATH,
	'TEMP-CROSSWALK-WORK',
	'DataOne-unique-variables-for-crosswalk-to-NCAP-1990-2016MY.csv')

ncap1117Filepath = os.path.join(
	PATH,
	'TEMP-CROSSWALK-WORK',
	'NCAP-Safercar-unique-variables-for-crosswalk-to-DataOne-2011-2017MY.csv')

ncap9010Filepath = os.path.join(
	PATH,
	'TEMP-CROSSWALK-WORK',
	'NCAP-Safercar-unique-variables-for-crosswalk-to-DataOne-1990-2010MY.csv')

misFilepath = os.path.join(
	PATH,
	'TEMP-CROSSWALK-WORK',
	'mismatch.csv')

crosswalkFilepath = os.path.join(
		PATH,'crosswalk.csv')

DATAONE_HEADER = [
	'make',
	'model',
	'myear',
	'trim',
	'style'
]

DATAONE_TYPES = {
	'make': str,
	'model': str,
	'myear': numpy.int32,
	'trim': str,
	'style': str,
}

NCAP1117_HEADER = [
	'make',
	'model',
	'myear',
	'body_style',
	'vehicle_type',
	'drive_train',
	'production_release'
]

NCAP1117_TYPES = {
	'make': str,
	'model': str,
	'myear': numpy.int32,
	'body_style': str,
	'vehicle_type': str,
	'drive_train': 'S10',
	'production_release': str
}

NCAP9010_HEADER = [
	'carid'
	'make',
	'model',
	'myear',
	'doors',
	'size_class',
	'sh_desc'
]

NCAP9010_HEADER = [
	'carid': numpy.int32,
	'make': str,
	'model': str,
	'myear': numpy.int32,
	'doors': str,
	'size_class': str,
	'sh_desc': str
]

MISMATCH_HEADER = [
	'ncap1117_index',
	'make',
	'model',
	'myear',
	'trim',
	'style',
	'ncap_index',
	'make_ncap',
	'model_ncap',
	'myear_ncap',
	'body_style',
	'vehicle_type',
	'drive_train',
	'production_release',
	'dataone_index'
]

MISMATCH_TYPES = {
	'ncap1117_index': numpy.int32,
	'make': str,
	'model': str,
	'myear': numpy.int32,
	'trim': str,
	'style': str,
	'ncap_index': numpy.int32,
	'make_ncap': str,
	'model_ncap': str,
	'myear_ncap': str,
	'body_style': str,
	'vehicle_type': str,
	'drive_train': str,
	'production_release': numpy.int32,
	'dataone_index': numpy.int32
}

dataone = pandas.read_csv(
			dataoneFilepath,
			names=DATAONE_HEADER,
			dtype=DATAONE_TYPES,
			skiprows=1,
			index_col=False,
			usecols=range(len(DATAONE_HEADER)),
			na_values=['#VALUE!','#NUM!'])

ncap1117 = pandas.read_csv(
			ncap1117Filepath,
			names=NCAP1117_HEADER,
			dtype=NCAP1117_TYPES,
			skiprows=1,
			index_col=False,
			usecols=range(len(NCAP1117_HEADER)),
			na_values=['#VALUE!','#NUM!'])

ncap9010 = pandas.read_csv(
			ncap9010Filepath,
			names=NCAP9010_HEADER,
			dtype=NCAP9010_TYPES,
			skiprows=1,
			index_col=False,
			usecols=range(len(NCAP9010_HEADER)),
			na_values=['#VALUE!','#NUM!'])



mismatch = pandas.read_csv(
			misFilepath,
			names=MISMATCH_HEADER,
			dtype=MISMATCH_TYPES,
			skiprows=1,
			index_col=False,
			usecols=range(len(MISMATCH_HEADER)),
			na_values=['#VALUE!','#NUM!'])

crosswalk = pandas.read_csv(crosswalkFilepath)