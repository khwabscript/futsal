import requests
from bs4 import BeautifulSoup as BS

headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36'}
url = 'https://www.lnfs.es/partido/bar%C3%A7a/pe%C3%B1%C3%ADscola-fs/12/2021'
translate = {
	'Tarjeta Amarilla': 'yellow_card', 'Falta': 'foul', 'Quinta falta': 'fifth_foul', 'Gol en propia puerta': 'own_goal', 'Gol': 'goal',
	'Gol Anulado': 'goal_canceled', 'Gol de Falta': 'set_piece_goal', 'Gol de penalti': 'penalty_scored', 'Gol doble penalti': 'double_penalty_scored', 
	'Penalti Fallado': 'penalty_missed', 'Doble penalti fallado': 'double_penalty_missed', 'Lesionado': 'injury', '2a Amarilla y Roja': 'red_card',
	'Tarjeta Roja': 'red_card'
}

def parse_lnfs_fixture(url, headers):
	session = requests.Session()
	request = session.get(url, headers=headers)
	if request.status_code == 200:
		# print('OK')
		soup = BS(request.content, 'html.parser')
		matchHeader = soup.find('div', class_='match-header')
		tour = int(matchHeader.select("div.content>div>div")[0].text.replace('\n', '').replace('\t', '').split('Jornada')[1])
		datetime = matchHeader.find('div', class_='date-hour').text.split('|')[1].strip()
		teamLinks = matchHeader.find('div', class_='content-match').find_all('a')
		# print(teamLinks)
		teams = [{'lnfs_id': int(teamLink['href'].split('/')[-2:-1][0]), 'name': teamLink.find('h2').text.strip()} for teamLink in teamLinks]
		score = matchHeader.find(id="result_match").text.split(' - ')
		fixture = {'tour': tour, 'datetime': datetime, 'teams': teams, 'score': score}
		# print(score)
		# return 0
		matcheDetails = soup.find('div', class_='table-detail-match')
		rows = matcheDetails.find_all('div', class_='row')
		playerEvents = []
		penaltiesMissed = []

		for row in rows[:2]:
			for place in ['local', 'visitor']:
				side = row.find('div', class_='team_' + place)
				# detailedData = side.find_all('div', class_='detail-data')
				links = side.find_all('a', class_='block')
				teamIndex = 0 if place == 'visitor' else 1
				for link in links:
					data = link.find('div', class_='detail-data')
					player = {}
					player['id'] = int(link['href'].split('/')[-1:][0])
					player['teamIndex'] = teamIndex
					player['goals_conceded'] = int(score[teamIndex])
					player['number'] = int(data.find('div', class_='r-dorsal').text)
					player['name'] = data.find('div', class_='name').find('p').text
					player['pos'] = data.find('div', class_='name').find('div').text
					actions = data.find('div', class_='actions').find_all('div')
					for action in actions:
						img = action.find('img')
						if (img):
							key = img['alt']
							if (key in ['Penalti Fallado', 'Doble penalti fallado']):
								penaltiesMissed.append({'teamIndex': teamIndex, 'event': translate[key]})
							player[ translate[key] ] = player.get(translate[key], 0) + 1
					playerEvents.append(player)
		for penaltyMissed in penaltiesMissed:
			for player in playerEvents:
				if player['teamIndex'] != penaltyMissed['teamIndex'] and player['pos'] == 'por':
					player[ penaltyMissed['event'].replace('missed', 'saved') ] = player.get(penaltyMissed['event'], 0) + 1
	else:
		print('ERROR')

	fixture['playerEvents'] = playerEvents

	return fixture

# print(parse_lnfs_fixture('http://www.lnfs.es/partido/xota-fs/manzanares-fs/1/2022', headers))

