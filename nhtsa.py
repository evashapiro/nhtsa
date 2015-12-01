import json
import os
import sys
import requests
import urllib

import cache

_BASE_URL = 'http://www.nhtsa.gov/webapi/api/SafetyRatings'
_API_CACHE_FILENAME = 'api_cache.json'

class APIError(IOError):
	def __init__(self, url, resp):
		self.url = url
		self.resp = resp
		super(IOError, self).__init__(
			'{0}\nStatus Code {1}\nResponse\n{2}'.format(
			url, resp.status_code, resp.text.encode('utf-8')))

def url_fmt(arg):
	if not isinstance(arg, str):
		arg = str(arg)
	return urllib.quote(arg, '')

api_cache = cache.Cache(_API_CACHE_FILENAME)

def do_api_request(fmt_string, *args):
	path = fmt_string.format(*map(url_fmt, args))
	url = _BASE_URL + path
	if api_cache.contains(url):
		return api_cache.get(url)
	resp = requests.get(url)
	if resp.status_code == 404:
		print "404 error: " + path
		return []
	elif resp.status_code != 200:
		raise APIError(url, resp)
	try:
		results = resp.json()['Results']
	except ValueError as ex:
		raise APIError(url, resp)
	api_cache.put(url, results)
	return results

def get_all_model_years():
	return do_api_request('')

def get_all_makes_for_year(year):
	return do_api_request('/modelyear/{0}', year)

def get_all_models_for_make_and_year(year, make):
	return do_api_request('/modelyear/{0}/make/{1}', year, make)

def get_by_year_make_model(year, make, model):
	return do_api_request('/modelyear/{0}/make/{1}/model/{2}', year, make, model)

def get_by_vehicle_id(vehicle_id):
	return do_api_request('/VehicleId/{0}'.format(vehicle_id))

def enumerate_with_count(lst):
	"""Enumerate over a list with an index and count of total items."""
	total = len(lst)
	for i, val in enumerate(lst):
		yield i, val, total

if __name__ == '__main__':
	vehicles = []
	for i, res, total_i in enumerate_with_count(get_all_model_years()):
		year = res['ModelYear']
		for j, res, total_j in enumerate_with_count(get_all_makes_for_year(year)):
			make = res['Make'].replace(' ', '')
			for k, res, total_k in enumerate_with_count(get_all_models_for_make_and_year(year, make)):
				model = res['Model'].replace(' ', '')
				for l, res, total_l in enumerate_with_count(get_by_year_make_model(year, make, model)):
					vehicleID = res['VehicleId']
					print(year, make, model, vehicleID,
						'Year: {0}/{1} Make: {2}/{3} Model: {4}/{5}'.format(
							i, total_i, j, total_j, k, total_k, l, total_l))
					vehicles.append(get_by_vehicle_id(vehicleID))

	with open('vehicles.json', 'w') as f:
		json.dump(vehicles, f)