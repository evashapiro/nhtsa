import nhtsa
import json


class API(nhtsa.API):
	def __init__(self):
		super(API, self).__init__('https://vpic.nhtsa.dot.gov/api')

	def get_all_makes(self):
		return self.do_api_request('/vehicles/GetAllMakes')

	def get_models_for_make(self, make):
		if '.' in make:
			make = make[:make.find('.')]
		if '/' in make:
			make = make[:make.find('/')]
		return self.do_api_request('/vehicles/GetModelsForMake/{0}', make)


if __name__ == '__main__':
	api = API()
	all_models = []
	missing = []
	for i, res, total_i in nhtsa.enum_with_count(api.get_all_makes()):
		make = res['Make_Name']
		try:
			models = api.get_models_for_make(make)
		except nhtsa.APIError as err:
			print(err)
			missing.append(make)
		for j, res, total_j in nhtsa.enum_with_count(models):
			model = res['Model_Name']
			print(make, model,
				'Make: {0}/{1} Model: {2}/{3}'.format(
					i, total_i, j, total_j))
			all_models.append(res)

	with open('vpic_models.json', 'w') as f:
		json.dump(all_models, f)
	with open('vpic_missing.json', 'w') as f:
		json.dump(missing, f)
