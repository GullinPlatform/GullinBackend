import os
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json_file = os.path.join(base_dir, 'country_code/country_codes.json')
data = json.load(open(json_file))


def is_valid_country(country_name):
	for country in data:
		if country['CLDR display name'] == country_name:
			return True
	return False


def get_phone_prefix_by_country_name(country_name):
	for country in data:
		if country['CLDR display name'] == country_name:
			return country['Dial']
	return False


def get_ISO3166_code_by_country_name(country_name):
	for country in data:
		if country['CLDR display name'] == country_name:
			return country['ISO3166-1-Alpha-2']
	return False
