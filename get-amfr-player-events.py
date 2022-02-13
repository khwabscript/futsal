import json
import os.path
from write_amfr_fixture_data import write_amfr_fixture_data
from parse_amfr_fixtures import parse_amfr_fixtures

parse_amfr_fixtures()
with open('superliga/fixtures.json') as json_file:
    fixtures = json.load(json_file)

for fixture in fixtures:
	path = 'superliga/fixtures/' + str(fixture['id'])
	if os.path.isdir(path):
		continue
	if 'home_team_goals' not in fixture:
		continue
	# print('fetching ' + str(fixture['id']) + '...')
	write_amfr_fixture_data(str(fixture['id']))
