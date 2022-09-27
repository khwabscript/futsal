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

eventTypes = {
    'гол': 'goal',
    'нереализованные пенальти': 'penalty_missed',
    'жёлтая карточка': 'yellow_card',
    'красная карточка': 'red_card',
    'удаления': 'red_card',
    'фол': 'foul',
    'автогол': 'own_goal'
}

def parse_superleague_player_events(url, headers):
    playerEvents = []
    class_prefix = 'vertical-timeline'
    session = requests.Session()
    request = session.get(url, headers=headers)
    if request.status_code == 200:
        soup = BS(request.content, 'html.parser')
        matchContainer = soup.find('div', class_=class_prefix)
        matchDivs = matchContainer.find_all('li', class_=class_prefix + '__event-item')
        eventType = 'undefined'
        for matchDiv in matchDivs:
            playerEvent = {'player': {}}
            player = matchDiv.find('a', class_='vertical-timeline__event-author')
            playerEvent['player']['id'] = int(player['href'].replace("/player/", ""))
            playerEvent['player']['name'] = player.text.strip()
            playerEvent['type'] = eventTypes[matchDiv.find('div', class_='event-item')['title'].strip().lower()]
            try:
                playerEvent['minute'] = int(matchDiv.find('div', class_='vertical-timeline__event-minute').text.strip().replace("'", ''))
            except Exception as e:
                pass
            playerEvents.append(playerEvent)
            assistant = matchDiv.find('a', class_='vertical-timeline__event-assist')
            if not assistant:
                continue
            assistEvent = {'player': {}, 'minute': playerEvent.get('minute', 0)}
            assistEvent['player']['id'] = int(assistant['href'].replace("/player/", ""))
            assistEvent['player']['name'] = assistant.text.strip()
            assistEvent['type'] = 'assist'
            playerEvents.append(assistEvent)
            # print(playerEvents)
            # return
    else:
        print('ERROR')

    return playerEvents

# r = parse_superleague_player_events('https://superliga.rfs.ru/match/2937683', headers)
# print(r)
