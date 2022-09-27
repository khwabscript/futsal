import json
import os.path
from write_superleague_fixture_data import write_superleague_fixture_data
from parse_superleague_fixtures import parse_superleague_fixtures, headers

parse_superleague_fixtures('https://superliga.rfs.ru/tournament/1025599/calendar?round_id=1044861&type=tours', headers)

with open('superleague/fixtures.json') as json_file:
    fixtures = json.load(json_file)

for fixture in fixtures:
    path = 'superleague/fixtures/' + str(fixture['id'])
    if os.path.isdir(path):
        continue
    if 'home_team_goals' not in fixture:
        continue
    try:
        write_superleague_fixture_data(str(fixture['id']))
    except:
        print('problem with fixture: #' + str(fixture['id']))
