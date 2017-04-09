import argparse
import csv
import Levenshtein
import os
import sys

from sources import dataone
from sources import ncap1117
from sources import ncap9010
from sources import mismatch


def rank(row1, row2):
	if row1.myear != row2.myear:
		return float('inf')
	makeDistance = Levenshtein.distance(row1.make.lower(), row2.make.lower())
	modelDistance = Levenshtein.distance(row1.model.lower(), row2.model.lower())
	extra = 1
	if row2.body_style.lower().replace(' ', '') in row1.style.lower():
		extra += 1
	if row2.vehicle_type.lower().replace(' ', '') in row1.style.lower():
		extra += 1
	if row2.drive_train.lower().replace(' ', '') in row1.style.lower():
		extra += 1
	return makeDistance + modelDistance + (1 / extra)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Find best match in NCAP.')
	parser.add_argument('filename', type=str,
		help='Filename to save crosswalk index to.')
	parser.add_argument('--mismatch', action='store_true',
		help='Use mis instead of dataone.')
	parser.add_argument('--dataoneindexcol', type=str,
		help='Column name to index on - default is the row number.')
	
	args = parser.parse_args()

	dataset = dataone
	if args.mismatch:
		dataset = mismatch

	if os.path.exists(args.filename):
		print('{} already exists, move or delete it if you want to re-run this'.format(args.filename))
		sys.exit(1)
	f = open(args.filename, 'w')
	w = csv.writer(f)
	w.writerow(['dataone_index', 'ncap1117_index'])
	for i, row1 in dataset.iterrows():
		print i, len(dataset)
		dataone_index = i
		if args.dataoneindexcol:
			dataone_index = row1[args.dataoneindexcol]
		ranks = []
		for j, row2 in ncap1117.iterrows():
			ranks.append((j, rank(row1, row2)))
		ranks.sort(key=lambda (i, rank): rank)
		bestMatchIndex = -1
		if ranks[0][1] != float('inf'):
			bestMatchIndex = ranks[0][0]
		w.writerow((dataone_index, bestMatchIndex))
		f.flush()
	f.close()