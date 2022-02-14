import os.path
from writeJson import writeJson
from parse_amfr_player_events import parse_amfr_player_events
from parse_fixture_lineups import parse_fixture_lineups

headers = {
	'user-agent': (
		'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
		'AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/80.0.3987.116 Mobile Safari/537.36'
	)
}

def write_amfr_fixture_data(matchHash: str):
	path = 'superliga/fixtures/' + matchHash

	eventFile = path + '_events.json'
	homeTeamFile = path + '_homeTeam.json'
	awayTeamFile = path + '_awayTeam.json'

	if not os.path.isfile(eventFile):
		events = parse_amfr_player_events('http://amfr.ru/match/' + matchHash + '/', headers)
		writeJson(events, eventFile)
	if not os.path.isfile(homeTeamFile):
		homeTeam = parse_fixture_lineups('http://amfr.ru/match/' + matchHash + '/', headers, True)
		writeJson(homeTeam, homeTeamFile)
	if not os.path.isfile(awayTeamFile):
		awayTeam = parse_fixture_lineups('http://amfr.ru/match/' + matchHash + '/', headers, False)
		writeJson(awayTeam, awayTeamFile)