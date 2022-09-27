import requests
from bs4 import BeautifulSoup as BS
from copy import copy, deepcopy

headers = {
    'user-agent': (
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/80.0.3987.116 Mobile Safari/537.36'
    )
}

def parse_superleague_fixture_lineups(url, headers, is_home = True):
    lineups = []
    session = requests.Session()
    request = session.get(url, headers=headers)
    if request.status_code == 200:
        soup = BS(request.content, 'html.parser')
        lineups_container = soup.find('div', class_='match-protocol__composition')

        position = 'left' if is_home else 'right'

        team_lineups_container = lineups_container.find('ul', class_='match-protocol__team match-protocol__team--' + position)
        team_players = team_lineups_container.find_all('li', class_='match-protocol__member match-protocol__member--'  + position)

        for team_player in team_players:
            player = {}
            player_data = team_player.find('a', class_='match-protocol__member-name')
            player['id'] = int(player_data['href'].replace('/player/', ''))
            player['name'] = player_data.text.strip()
            try:
                player['number'] = int(team_player.find('span', class_='match-protocol__member-number').text.strip())
                player['position'] = team_player.find('span', class_='match-protocol__member-amplua').text.strip().replace('.','')
            except:
                pass
            lineups.append(player)
    else:
        print('ERROR')

    return lineups

r = parse_superleague_fixture_lineups('https://superliga.rfs.ru/match/2937683', headers)
# print(r)
