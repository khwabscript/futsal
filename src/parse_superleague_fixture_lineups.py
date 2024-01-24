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
        lineups_container = soup.find('div', {'id': 'match-protocol'}).find('div', class_='protocol')

        position = 'left' if is_home else 'right'
        position = 0 if is_home else 1

        team_lineups_container = lineups_container.find_all('ul', class_='protocol__list')[position]
        team_players = team_lineups_container.find_all('li', class_='protocol__item')
        if len(team_players) <= 1:
            lineups_container = soup.find('section', class_='match-protocol__substitutes')
            team_lineups_container = lineups_container.find('ul', class_='match-protocol__team match-protocol__team--' + position)
            team_players = team_lineups_container.find_all('li', class_='match-protocol__member match-protocol__member--'  + position)

        for team_player in team_players:
            if 'protocol__item--empty' in team_player.get('class'):
                continue
            player = {}
            player_data = team_player.find('a', class_='protocol__link')
            player['id'] = int(player_data['href'].replace('/player/', ''))
            player['name'] = player_data.find('div', class_='protocol__name').text.strip()
            try:
                player['number'] = int(team_player.find('span', class_='protocol__number-text').text.strip())
                player['position'] = team_player.find('div', class_='protocol__role').text.strip().replace('.','')
            except:
                pass
            lineups.append(player)
    else:
        print('ERROR')

    return lineups

# r = parse_superleague_fixture_lineups('https://superliga.rfs.ru/match/2938144', headers)
# print(r)
