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


def parse_superleague_fixtures(url, headers):
    fixtures = []
    session = requests.Session()
    request = session.get(url, headers=headers)
    if request.status_code != 200:
        print("ERROR")
        return []

    soup = BS(request.content, "html.parser")
    tours = soup.find_all("ul", {"class": "schedule__matches-list"})
    for tour in tours:
        tour_fixtures = tour.find_all("li")

        for tour_fixture in tour_fixtures:
            fixture = {"home_team": {}, "away_team": {}}

            result = tour_fixture.find("a", {"class": "schedule__score"})

            fixture["id"] = int(result["href"].replace("/match/", ""))

            datetime = tour_fixture.find("span", {"class": "schedule__time"}).text.strip().split("/")
            try:
                fixture["datetime"] = (
                    datetime[0].strip().replace(".", "").replace(" ", ".")
                    .replace("СЕНТ", "09")
                    .replace("ОКТ", "10")
                    .replace("НОЯБ", "11")
                    .replace("ДЕК", "12")
                    .replace("ЯНВ", "01")
                    .replace("ФЕВР", "02")
                    .replace("МАР", "03")
                    .replace("АПР", "04")
                    + (", " if datetime[0].__contains__("2023") else ".2024, ")
                    + datetime[len(datetime) - 1].strip()
                )
            except Exception as e:
                print("Problem with datetime")
                print(datetime)
                return

            home_team = tour_fixture.find("a", {"class": "schedule__team-1"})
            fixture["home_team"]["id"] = int(home_team["href"].split("=")[1])
            fixture["home_team"]["name"] = home_team.text.strip()

            away_team = tour_fixture.find("a", {"class": "schedule__team-2"})
            fixture["away_team"]["id"] = int(away_team["href"].split("=")[1])
            fixture["away_team"]["name"] = away_team.text.strip()

            try:
                score = result.text.strip()
                # for penalty shootout
                score = score.split("(")[0]
                fixture["home_team_goals"] = int(score.split(":")[0].strip())
                fixture["away_team_goals"] = int(score.split(":")[1].strip())
            except Exception as e:
                pass

            fixtures.append(fixture)

    store_fixtures(fixtures)

    return fixtures


def store_fixtures(fixtures):
    directory = "superleague/fixtures"

    if not os.path.exists(directory):
        os.makedirs(directory)
        print("The directory " + directory + " is created!")
    writeJson(fixtures, "superleague/fixtures.json")


# r = parse_superleague_fixtures('https://superliga.rfs.ru/tournament/1032038/calendar?round_id=1058048&type=tours', headers)
# print(r)
