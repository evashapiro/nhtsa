import pandas as pd

from sources import dataone
from sources import ncap1117
from sources import crosswalk

dataone['ncap_index'] = crosswalk.ncap1117_index

cross = dataone.merge(ncap1117,
	how='left',
	left_on='ncap_index',
	right_index=True,
	suffixes=('', '_ncap'))

cross.index = crosswalk.ncap1117_index

cross.to_csv('cross.csv')