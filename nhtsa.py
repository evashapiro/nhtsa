import json
import os
import sys
import requests
import urllib

import cache


_API_CACHE_FILENAME = 'api_cache.json'


class APIError(IOError):
	def __init__(self, url, resp):
		self.url = url
		self.resp = resp
		super(IOError, self).__init__(
			'{:}\nStatus Code {:}\nHeaders\n{:}\nResponse\n{:}'.format(
			url, resp.status_code, resp.headers, resp.text.encode('utf-8')))


def url_fmt(arg):
	if not isinstance(arg, str):
		arg = str(arg).strip()
	return urllib.quote(arg, '')


def enum_with_count(lst):
	"""Enumerate over a list with an index and count of total items."""
	total = len(lst)
	for i, val in enumerate(lst):
		yield i, val, total


api_cache = cache.Cache(_API_CACHE_FILENAME)


class API(object):
	def __init__(self, base_url):
		self._base_url = base_url

	def do_api_request(self, fmt_string, *args):
		path = fmt_string.format(*map(url_fmt, args))
		url = self._base_url + path + '?format=json'
		if api_cache.contains(url):
			return api_cache.get(url)
		resp = requests.get(url)
		if resp.status_code == 404:
			print "404 error: " + path
			return []
		elif resp.status_code != 200:
			api_cache.persist()
			raise APIError(url, resp)
		try:
			results = resp.json()['Results']
		except ValueError as ex:
			raise APIError(url, resp)
		api_cache.put(url, results)
		return results
