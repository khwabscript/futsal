import requests
from bs4 import BeautifulSoup as BS

def parse_lnfs_fixtures(url, headers):
	fixtures = []
	session = requests.Session()
	request = session.get(url, headers=headers)
	if request.status_code == 200:
		soup = BS(request.content, 'html.parser')
		listMatches = soup.find("div", {"id": "list_matches"})
		listMatchDivs = listMatches.find_all('div', recursive=False)
		tour = None
		for matchDiv in listMatchDivs:
			if ('bg3' in matchDiv.get('class')):
				tour = int(matchDiv.text.replace('Jornada ', '')) + 1
				continue
			fixture = {}
			fixture['datetime'] = matchDiv.find('div', class_='info ib va-m ta-l').text.strip()
			fixture['home_team_name'] = matchDiv.find('div', class_='ib va-m team ta-r').find('a').text.strip()
			fixture['away_team_name'] = matchDiv.find('div', class_='ib va-m team ta-l').text.strip()
			scoreHref = matchDiv.find('div', class_='marker').find('a')
			score = scoreHref.text.strip()
			# return score
			try:
				fixture['home_team_goals'] = int(score.split('-')[0].strip())
				fixture['away_team_goals'] = int(score.split('-')[1].strip())
			except Exception as e:
				pass
			
			fixture['href'] = scoreHref['href']
			fixture['tour'] = tour
			fixtures.append(fixture)
			# break
	else:
		print('ERROR')

	return fixtures
