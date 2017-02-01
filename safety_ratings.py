import nhtsa


class API(nhtsa.API):
	def __init__(self):
		super(API, self).__init__('https://www.nhtsa.gov/webapi/api/SafetyRatings')

	def get_all_model_years(self):
		return self.do_api_request('')

	def get_all_makes_for_year(self, year):
		return self.do_api_request('/modelyear/{0}', year)

	def get_all_models_for_make_and_year(self, year, make):
		return self.do_api_request('/modelyear/{0}/make/{1}', year, make)

	def get_by_year_make_model(self, year, make, model):
		return self.do_api_request('/modelyear/{0}/make/{1}/model/{2}', year, make, model)

	def get_by_vehicle_id(self, vehicle_id):
		return self.do_api_request('/VehicleId/{0}'.format(vehicle_id))


if __name__ == '__main__':
	api = API()
	vehicles = []
	missing = []
	for i, res, total_i in nhtsa.enum_with_count(api.get_all_model_years()):
		year = res['ModelYear']
		for j, res, total_j in nhtsa.enum_with_count(api.get_all_makes_for_year(year)):
			make = res['Make'].replace(' ', '')
			for k, res, total_k in nhtsa.enum_with_count(api.get_all_models_for_make_and_year(year, make)):
				model = res['Model'].replace(' ', '')
				vehicleIDs = api.get_by_year_make_model(year, make, model)
				if not vehicleIDs:
					print('Missing {0} {1} {2}'.format(year, make, model))
					missing.append((year, make, model))
				for l, res, total_l in nhtsa.enum_with_count(vehicleIDs):
					vehicleID = res['VehicleId']
					print(year, make, model, vehicleID,
						'Year: {0}/{1} Make: {2}/{3} Model: {4}/{5}'.format(
							i, total_i, j, total_j, k, total_k, l, total_l))
					vehicles.append(api.get_by_vehicle_id(vehicleID))

	with open('safety_ratings.json', 'w') as f:
		json.dump(vehicles, f)
	with open('missing.json', 'w') as f:
		json.dump(missing, f)