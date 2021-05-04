from bs4 import BeautifulSoup
import requests
import re
from Prediction import Prediction
from Match import Match
from Definition import URL, SAVE_FILES, BASE_URL, LOCAL_URL

def import_match_data():
  players = get_players_list()
  game_days, placements = parse_html(players)
  return players, game_days, placements

def prepare_html_files():
  if SAVE_FILES:
    try:
        open(URL + "1.html")
    except:
        download_html_files()

def download_html_files():
    for i in range(1, 35): 
        req = requests.get(BASE_URL + str(i))
        file = open(LOCAL_URL + str(i) + ".html", "w")
        file.write(req.text)
        file.close()

def get_players_list():
  players = []
  url = URL + "1"
  if SAVE_FILES:
      url = url + ".html"
      first_file = open(url)
      first_soup = BeautifulSoup(first_file.read(), "html.parser")
  else:
      first_file = requests.get(url)
      first_soup = BeautifulSoup(first_file.text, "html.parser")
  first_table = first_soup.find("table", class_ = "tippuebersicht")

  for row in first_table.tbody.findAll('tr'):
      column = row.find("td", class_ = "mg_class name")
      players.append(column.string)
  return players


# hacky function to parse through the kicktipps html page since they have no api
def parse_html(players):
    game_days = []
    placements_dict = {}

    #range is number of match days, so 35 (since range is not closed) in total
    for game_day in range(1, 30):
        url = URL + str(game_day)
        if SAVE_FILES:
            url = url + ".html"
            req = open(url)
            soup = BeautifulSoup(req.read(), "html.parser")
        else:
            req = requests.get(url).text
            soup = BeautifulSoup(req, "html.parser")

        table = soup.find("table", class_ = "tippuebersicht")

        home_teams = []
        guest_teams = []
        home_goals = []
        guest_goals = []

        for row in table.thead.findAll('tr')[0].findAll("th", class_="ereignis"):
            header_res = row.findAll("div", class_="headerbox")
            home_teams.append(header_res[0].string)
            guest_teams.append(header_res[1].string)
            result = header_res[2].find("span")
            home_goals.append(int(result.find("span", class_="kicktipp-heim").string))
            guest_goals.append(int(result.find("span", class_="kicktipp-gast").string))

        matches = []
        for game_index in range(9):
            predictions = []
            for player in players:
                row = table.tbody.find(text=player).parent.parent.parent
                result_class = "ereignis" + str(game_index)
                try: 
                    pred = row.find('td', class_= result_class).contents[0].string
                    splitted_result = re.split(":", pred)
                    prediction = Prediction(splitted_result[0], splitted_result[1])
                except: 
                    prediction = Prediction(None, None)
                predictions.append(prediction)

            this_match = Match(home_teams[game_index], guest_teams[game_index], home_goals[game_index], guest_goals[game_index], predictions)
            matches.append(this_match)

        # save the placements here already since it's easier compared to adding up the results later
        for player in players:
            if player not in placements_dict:
                placements_dict[player] = []
            row = table.tbody.find(text=player).parent.parent.parent
            placements_dict[player].append(int(row.find('td', class_= "gesamtpunkte").string))
        
        game_days.append(matches)
    return game_days, placements_dict