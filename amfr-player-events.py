import requests
from bs4 import BeautifulSoup as BS
import json
import os.path
# from writeJson import writeJson

headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36'}
url = 'http://amfr.ru/match/869150/'

def parse_amfr_player_events(url, headers):
	session = requests.Session()
	request = session.get(url, headers=headers)
	if request.status_code == 200:
		playerEvents = []
		soup = BS(request.content, 'html.parser')
		matchContainer = soup.find('div', class_='match-container')
		matchDivs = matchContainer.find_all('div')
		matchRows = matchContainer.find_all('div', class_='match-row')
		for matchRow in matchRows:
			if (matchRow.find('div', class_='match-tabs__gols-title')):
				tbodys = matchRow.find_all('tbody')
				for tbody in tbodys:
					trs = tbody.find_all('tr')
					for tr in trs:
						playerEvent = {}
						tds = tr.find_all('td')
						playerEvent['number'] = int(tds[0].text)
						playerEvent['player_name'] = tds[1].text.strip()
						playerEvent['minute'] = int(tds[3].text)
						playerEvent['type'] = 'goal'
						playerEvents.append(playerEvent)
	else:
		print('ERROR')

	return playerEvents

r = parse_amfr_player_events('http://amfr.ru/match/869014/', headers)
print(r)