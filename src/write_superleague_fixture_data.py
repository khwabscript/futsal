import os.path
from writeJson import writeJson
from parse_superleague_player_events import parse_superleague_player_events
from parse_superleague_fixture_lineups import parse_superleague_fixture_lineups

headers = {
    'user-agent': (
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/80.0.3987.116 Mobile Safari/537.36'
    )
}

base_url = 'https://superliga.rfs.ru/match/'

def write_superleague_fixture_data(matchHash: str):
    path = 'superleague/fixtures/' + matchHash

    eventFile = path + '_events.json'
    homeTeamFile = path + '_homeTeam.json'
    awayTeamFile = path + '_awayTeam.json'

    if not os.path.isfile(eventFile):
        events = parse_superleague_player_events(base_url + matchHash, headers)
        writeJson(events, eventFile)
    if not os.path.isfile(homeTeamFile):
        homeTeam = parse_superleague_fixture_lineups(base_url + matchHash, headers, True)
        writeJson(homeTeam, homeTeamFile)
    if not os.path.isfile(awayTeamFile):
        awayTeam = parse_superleague_fixture_lineups(base_url + matchHash, headers, False)
        writeJson(awayTeam, awayTeamFile)
