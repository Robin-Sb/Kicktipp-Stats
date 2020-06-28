from bs4 import BeautifulSoup
import requests
import re
import matplotlib.pyplot as plt
import numpy as np
import pathlib
from scipy.interpolate import make_interp_spline, BSpline

# flag whether files should be saved to disk in order to avoid making requests every time, you probably won't need this unless you intend to change the code
SAVE_FILES = False
# insert the name of your kicktipp lobby here
LOBBY_NAME = "asbuli2019"


LOCAL_URL = "files/game_day"
BASE_URL = "https://www.kicktipp.de/" + LOBBY_NAME + "/tippuebersicht?&spieltagIndex="
URL = ""

if SAVE_FILES:
    URL = LOCAL_URL
else:
    URL = BASE_URL


# representation of the games in objects
class Match:
    def __init__(self, home_team, guest_team, goals_home, goals_guest, predictions):
        self.home_team = home_team
        self.guest_team = guest_team
        self.goals_home = goals_home
        self.goals_guest = goals_guest
        self.predictions = predictions

    def __repr__(self):
        if self.goals_home == None or self.goals_guest == None:
            return "none"
        return self.home_team + " " + str(self.goals_home) + ":" + str(self.goals_guest) + " " + self.guest_team + str(self.predictions)

class Prediction:
    def __init__(self, goals_home, goals_guest):
        self.goals_home = goals_home
        self.goals_guest = goals_guest

    def __repr__(self):
        if self.goals_home is None or self.goals_guest is None:
            return "none"

        return self.goals_home + ":" + self.goals_guest

# download to html files locally to avoid making requests every time
def download_html_files():
    for i in range(1, 35): 
        req = requests.get(BASE_URL + str(i))
        file = open(LOCAL_URL + str(i) + ".html", "w")
        file.write(req.text)
        file.close()

# get the list of the players by parsing through the first file and putting the names in an array
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

placements_dict = {}

# hacky function to parse through the kicktipps html page since they have no api
def parse_html():
    game_days = []

    #range is number of match days, so 35 (since range is not closed) in total
    for game_day in range(1, 35):
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

        for row in table.thead.findAll('tr')[0]:
            if (row.string != " "):
                home_teams.append(row.string)

        for row in table.thead.findAll('tr')[1]:
            if (row.string != " "):
                guest_teams.append(row.string)

        for row in table.thead.select( "tr[class='headerErgebnis']"):
            for th in row.findAll("th", class_="ereignis"):
                result = th.find("span")
                this_home_goals = result.find("span", class_="kicktipp-heim")
                this_guest_goals = result.find("span", class_="kicktipp-gast")
                home_goals.append(int(this_home_goals.string))
                guest_goals.append(int(this_guest_goals.string))

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

        # safe the placements here already since it's easier compared to adding up the results later
        for player in players:
            if player not in placements_dict:
                placements_dict[player] = []
            row = table.tbody.find(text=player).parent.parent.parent
            placements_dict[player].append(int(row.find('td', class_= "gesamtpunkte").string))
        
        game_days.append(matches)
    return game_days


cwd = pathlib.Path.cwd()

# make local directories where the plots are saved 
pathlib.Path((cwd / "plots/scores_per_team").resolve()).mkdir(exist_ok=True, parents=True)
pathlib.Path((cwd / "plots/points_per_prediction").resolve()).mkdir(exist_ok=True, parents=True)
pathlib.Path((cwd / "plots/other").resolve()).mkdir(exist_ok=True, parents=True)

if SAVE_FILES:
    try:
        open(URL + "1.html")
    except:
        download_html_files()


players = get_players_list()
game_days = parse_html()

team_results = {}
all_results_merged = {}
points_per_team_dict = {}
close_calls_dict = {}
missed_games_dict = {}

def fill_team_results_dict(match):
    if match.home_team in team_results:
        team_dict = team_results[match.home_team]
    else:
        team_dict = {}
    result_string = str(match.goals_home) + ":" + str(match.goals_guest)
    if result_string in team_dict:
        team_dict[result_string] = team_dict[result_string] + 1
    else:
        team_dict[result_string] = 1
    team_results[match.home_team] = team_dict

    if match.guest_team in team_results:
        team_dict = team_results[match.guest_team]
    else:
        team_dict = {}
    result_string = str(match.goals_guest) + ":" + str(match.goals_home)
    if result_string in team_dict:
        team_dict[result_string] = team_dict[result_string] + 1        
    else:
        team_dict[result_string] = 1
    team_results[match.guest_team] = team_dict

def fill_all_results_dict(match):
    result_string = str(match.goals_home) + ":" + str(match.goals_guest)
    if result_string in all_results_merged:
        all_results_merged[result_string] = all_results_merged[result_string] + 1
    else:
        all_results_merged[result_string] = 1

def award_points_per_game(goals_home, goals_guest, prediction):
    goals_home = int(goals_home)
    goals_guest = int(goals_guest)
    try:
        pred_goals_home = int(prediction.goals_home)
        pred_goals_guest = int(prediction.goals_guest)
    except:
        return 0
    if goals_home == pred_goals_home and goals_guest == pred_goals_guest:
        return 4
    elif goals_home - goals_guest == pred_goals_home - pred_goals_guest and goals_home != goals_guest:
        return 3
    elif (goals_home > goals_guest and pred_goals_home > pred_goals_guest) or (goals_home < goals_guest and pred_goals_home < pred_goals_guest) or (goals_home - goals_guest == pred_goals_home - pred_goals_guest):
        return 2
    else: 
        return 0

def fill_points_per_team_dict(match, index):
    score = award_points_per_game(match.goals_home, match.goals_guest, match.predictions[index])
    if index not in points_per_team_dict:
        points_per_team_dict[index] = {}
    
    if match.home_team in points_per_team_dict[index]:
        old_score = points_per_team_dict[index][match.home_team]
    else:
        old_score = 0
    points_per_team_dict[index][match.home_team] = old_score + score

    if match.guest_team in points_per_team_dict[index]:
        old_score = points_per_team_dict[index][match.guest_team]
    else:
        old_score = 0
    points_per_team_dict[index][match.guest_team] = old_score + score

def assign_close_calls(goals_home, goals_guest, prediction):
    real_score = award_points_per_game(goals_home, goals_guest, prediction)
    home_inc_score = award_points_per_game(goals_home + 1, goals_guest, prediction)
    guest_inc_score = award_points_per_game(goals_home, goals_guest + 1, prediction)

    if home_inc_score > real_score or guest_inc_score > real_score:
        return 1
    return 0

def fill_close_calls_dict(match, index):
    score = assign_close_calls(match.goals_home, match.goals_guest, match.predictions[index])
    player = players[index]
    if player not in close_calls_dict:
        close_calls_dict[player] = 0
    close_calls_dict[player] = close_calls_dict[player] + score

def fill_missed_games_dict(match, index):
    player = players[index]
    if player not in missed_games_dict:
        missed_games_dict[player] = 0
    if match.predictions[index].goals_home is None or match.predictions[index].goals_guest is None:
        missed_games_dict[player] = missed_games_dict[player] + 1

# main loop through the data to fill the dictionaries
for game_day in game_days:
    for match in game_day:
        new_match = True
        fill_team_results_dict(match)
        fill_all_results_dict(match)
        
        index = 0
        for prediction in match.predictions:
            fill_points_per_team_dict(match, index)
            fill_close_calls_dict(match, index)
            fill_missed_games_dict(match, index)
            index = index + 1


# matplot functions to save the plot
def save_bar_plot(amplitude, subfolder, title, results, y_ticks, x_name = "result", y_name = "amount of occurences", y_min = None, y_max = None):
    fig, ax = plt.subplots()
    x_pos = [i for i, _ in enumerate(results)]
    ax.bar(x_pos, amplitude, color=(0.2, 0.8, 0.0, 0.8))
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    ax.set_title(title)
    plt.xticks(x_pos, results, rotation = 90)
    plt.yticks(y_ticks)
    if y_min != None:
        axes = plt.gca()
        axes.set_ylim([y_min,y_max])
    fig.set_size_inches(12.8, 9.6)
    fig.savefig("plots/" + subfolder + "/" + title + ".png", bbox_inches="tight")
    plt.close()


def func(pct, allvals):
    absolute = int(round(pct/100.*np.sum(allvals)))
    return "{:.1f}%\n{:d}".format(pct, absolute)

def save_pie_plot(labels, amplitude, subfolder, title):
    fig, ax = plt.subplots()
    ax.pie(amplitude, labels = labels, autopct=lambda pct: func(pct, amplitude), startangle=90)
    ax.axis('equal')
    ax.set_title(title)
    plt.savefig("plots/" + subfolder + "/" + title + ".png", bbox_inches="tight")
    plt.close()

def dict_to_array(inp_dict):
    keys = [(k) for k,v in inp_dict.items()]
    values = [(v) for k,v in inp_dict.items()]
    return keys, values

def sort_dict(inp_dict): 
    return {k: v for k, v in sorted(inp_dict.items(), key=lambda item: item[1], reverse=True)}

for team in team_results:
    results_per_team = team_results[team]
    results_per_team = sort_dict(results_per_team)
    results, amplitude = dict_to_array(results_per_team)

    y_ticks = range(min(amplitude), max(amplitude) + 1)
    save_bar_plot(amplitude, "scores_per_team", team, results, y_ticks)


all_results_merged = sort_dict(all_results_merged)
all_res, all_ampl = dict_to_array(all_results_merged)

save_bar_plot(all_ampl, "scores_per_team", "all_teams", all_res, range(min(all_ampl), max(all_ampl) + 1))

close_calls_dict = sort_dict(close_calls_dict)
close_call_res, close_call_amp = dict_to_array(close_calls_dict)
save_bar_plot(close_call_amp, "other", "close_calls", close_call_res, range(0, max(close_call_amp) + 1), "player", "amount of games", min(close_call_amp) - 5, max(close_call_amp))

missed_games_dict = sort_dict(missed_games_dict)
missed_games_res, missed_games_amp = dict_to_array(missed_games_dict)
save_bar_plot(missed_games_amp, "other", "missed_games", missed_games_res, range(0, max(missed_games_amp) + 1), "player", "amount of games")

points_per_team_merged_dict = {}

index = 0
for player_index in points_per_team_dict:
    players_dict = points_per_team_dict[player_index]
    players_dict = sort_dict(players_dict)
    labels, amplitude = dict_to_array(players_dict)
    save_pie_plot(labels, amplitude, "points_per_prediction", players[index])

    for team in players_dict:
        if team in points_per_team_merged_dict:
            points_per_team_merged_dict[team] = points_per_team_merged_dict[team] + players_dict[team]
        else:
            points_per_team_merged_dict[team] = players_dict[team]
    index = index + 1

points_per_team_merged_dict = sort_dict(points_per_team_merged_dict)
point_res, point_ampl = dict_to_array(points_per_team_merged_dict)
save_pie_plot(point_res, point_ampl, "points_per_prediction", "all")


plt.figure(figsize=(16,10))
for player in placements_dict:
    # interpolation of the placements, you can also comment this in and comment the last line in the for out to get the placements without interpolation
    placements_amp = placements_dict[player]
    placements_res = np.array(range(0, len(placements_dict[player])))
    xnew = np.linspace(placements_res.min(), placements_res.max(), 300) 
    spl = make_interp_spline(placements_res, placements_amp, k=3)  # type: BSpline
    power_smooth = spl(xnew)
    plt.plot(xnew, power_smooth, label=player, linewidth=2)
    
    # comment this out for the pure graph without interpolation
    #plt.plot(np.array(range(0, len(placements_dict[player]))), placements_dict[player], label=player, linewidth=2)
plt.legend(loc='best')
plt.savefig("plots/other/placements.png", bbox_inches="tight")
plt.close()