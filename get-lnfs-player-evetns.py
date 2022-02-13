import requests
from bs4 import BeautifulSoup as BS
import json
import os.path
from parse_lnfs_fixture import parse_lnfs_fixture, headers, translate
from parse_lnfs_fixtures import parse_lnfs_fixtures
from writeJson import writeJson

fixtures = parse_lnfs_fixtures('http://www.lnfs.es/competicion/primera/2022/calendario/1', headers)
writeJson(fixtures, 'lnfs/fixtures.json')

with open('lnfs/fixtures.json') as json_file:
    fixtures = json.load(json_file)
for fixture in fixtures:
	if 'home_team_goals' not in fixture:
		continue
	link = fixture['href'].replace('https', 'http')
	fixtureId = link.split('/')[-2:-1][0]
	filePath = 'lnfs/fixtures/' + fixtureId + '.json'
	if not os.path.isfile(filePath):
		playerEvents = parse_lnfs_fixture(link, headers)
		writeJson(playerEvents, filePath)