import json
import os.path
from writeJson import writeJson
from parse_lnfs_fixtures import parse_lnfs_fixtures

headers = {
	'user-agent': (
		'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
		'AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/80.0.3987.116 Mobile Safari/537.36'
	)
}

fixtures = parse_lnfs_fixtures('http://www.lnfs.es/competicion/primera/2022/calendario/1', headers)
directory = 'lnfs'
if not os.path.exists(directory):
	os.makedirs(directory)
	print('The directory ' + directory + ' is created!')
writeJson(fixtures, 'lnfs/fixtures.json')
