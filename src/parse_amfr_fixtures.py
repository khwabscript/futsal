import os
import requests
from bs4 import BeautifulSoup as BS
from writeJson import writeJson

headers = {
    "user-agent": (
        "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.116 Mobile Safari/537.36"
    )
}


def parse_amfr_fixtures_page(url, headers):
    fixtures = []
    session = requests.Session()
    request = session.get(url, headers=headers)
    if request.status_code != 200:
        print("ERROR")
        return []

    soup = BS(request.content, "html.parser")
    tobdy = soup.find("tbody", {"id": "league-games"})
    trs = tobdy.find_all("tr")
    tour = None
    for tr in trs:
        datetime = tr.find("td", class_="is-date")
        if not datetime:
            continue
        fixture = {}
        fixture["datetime"] = datetime.find(text=True, recursive=False).strip()
        fixtureInfo = tr.find("td", class_="is-inf")
        fixture["home_team_name"] = fixtureInfo.find(
            "div", class_="league-item__team-inn is-right"
        ).text.strip()
        fixture["away_team_name"] = fixtureInfo.find(
            "div", class_="league-item__team-inn is-left"
        ).text.strip()
        try:
            score = fixtureInfo.find(
                "div", class_="league-item__score"
            ).text.strip()
            fixture["home_team_goals"] = int(score.split("-")[0].strip())
            fixture["away_team_goals"] = int(score.split("-")[1].strip())
        except Exception as e:
            pass

        fixture["id"] = int(
            tr["data-link"].replace("/match/", "").replace("/", "")
        )
        fixtures.append(fixture)

    return fixtures


def parse_amfr_fixtures():
    fixtures = []
    directory = "superleague/fixtures"
    for i in range(9, 0, -1):
        fixtures = fixtures + parse_amfr_fixtures_page(
            "http://amfr.ru/league/super/calendar/?TOUR=ALL&PAGEN_3=" + str(i),
            headers,
        )
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("The directory " + directory + " is created!")
    writeJson(fixtures, "superleague/fixtures.json")


parse_amfr_fixtures()
# r = parse_amfr_fixtures_page('http://amfr.ru/league/super/calendar/?TOUR=ALL&PAGEN_3=5', headers)
# print(r)
