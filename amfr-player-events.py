import requests
from bs4 import BeautifulSoup as BS
import json
import os.path
# from writeJson import writeJson

headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36'}
url = 'http://amfr.ru/match/869150/'
eventTypes = {'голы': 'goal', 'предупреждения': 'yellow_card', 'удаления': 'red_card', 'фолы': 'foul'}

def parse_amfr_player_events(url, headers):
	playerEvents = []
	session = requests.Session()
	request = session.get(url, headers=headers)
	if request.status_code == 200:
		soup = BS(request.content, 'html.parser')
		matchContainer = soup.find('div', class_='match-container')
		matchDivs = matchContainer.find_all('div', recursive=False)
		eventType = 'undefined'
		for matchDiv in matchDivs:
			if ('match-tabs__gols-top' in matchDiv.get('class')):
				eventType = eventTypes[matchDiv.find('h3').text.lower()]
				if eventType == 'foul':
					break
				continue
			tbodys = matchDiv.find_all('tbody')
			for tbody in tbodys:
				trs = tbody.find_all('tr')
				for tr in trs:
					playerEvent = {}
					tds = tr.find_all('td')
					playerEvent['number'] = int(tds[0].text)
					playerEvent['player_name'] = tds[1].text.strip()
					minuteColumn = 3 if eventType == 'goal' else 2
					try:
						playerEvent['minute'] = int(tds[minuteColumn].text)
					except Exception as e:
						playerEvent['minute'] = int(tds[3 if minuteColumn == 2 else 2].text)
					playerEvent['type'] = eventType
					playerEvents.append(playerEvent)
	else:
		print('ERROR')

	return playerEvents

r = parse_amfr_player_events('http://amfr.ru/match/869014/', headers)
print(r)
