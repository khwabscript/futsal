import requests
from bs4 import BeautifulSoup as BS

def parse_fixture_lineups(url, headers, isHome = True):
	teamPlayers = []
	session = requests.Session()
	request = session.get(url, headers=headers)
	if request.status_code == 200:
		soup = BS(request.content, 'html.parser')
		lineupSection = soup.find_all('div', class_='match-tabs__section')[1]
		teamClass = 'is-left' if isHome else 'is-right'
		teamSection = lineupSection.find('div', class_=teamClass)
		trs = teamSection.find('tbody').find_all('tr')
		for tr in trs:
			player = {}
			tds = tr.find_all('td')
			player['number'] = int(tds[0].text)
			player['name'] = tds[1].text.strip()
			player['position'] = tds[2].text.strip()
			teamPlayers.append(player)
	else:
		print('ERROR')

	return teamPlayers