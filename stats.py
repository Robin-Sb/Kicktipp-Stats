import matplotlib.pyplot as plt
import numpy as np
import pathlib
from Importer import import_match_data, prepare_html_files
from scipy.interpolate import make_interp_spline, BSpline
from DataProcessing import process_data

cwd = pathlib.Path.cwd()
# make local directories where the plots are saved 
pathlib.Path((cwd / "plots/scores_per_team").resolve()).mkdir(exist_ok=True, parents=True)
pathlib.Path((cwd / "plots/points_per_prediction").resolve()).mkdir(exist_ok=True, parents=True)
pathlib.Path((cwd / "plots/other").resolve()).mkdir(exist_ok=True, parents=True)

prepare_html_files()
players, game_days, placements = import_match_data()
team_results, all_results_merged, points_per_team, close_calls, missed_games = process_data(game_days, players)

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
    fig.savefig("plots/" + subfolder + "/" + title + ".png", bbox_inches="tight")
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

close_calls_dict = sort_dict(close_calls)
close_call_res, close_call_amp = dict_to_array(close_calls_dict)
save_bar_plot(close_call_amp, "other", "close_calls", close_call_res, range(0, max(close_call_amp) + 1), "player", "amount of games", min(close_call_amp) - 5, max(close_call_amp))

missed_games_dict = sort_dict(missed_games)
missed_games_res, missed_games_amp = dict_to_array(missed_games_dict)
save_bar_plot(missed_games_amp, "other", "missed_games", missed_games_res, range(0, max(missed_games_amp) + 1), "player", "amount of games")

points_per_team_merged_dict = {}

index = 0
for player_index in points_per_team:
    players_dict = points_per_team[player_index]
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
for player in placements:
    # interpolation of the placements, you can also comment this in and comment the last line in the for out to get the placements without interpolation
    placements_amp = placements[player]
    placements_res = np.array(range(0, len(placements[player])))
    xnew = np.linspace(placements_res.min(), placements_res.max(), 300) 
    spl = make_interp_spline(placements_res, placements_amp, k=3)  # type: BSpline
    power_smooth = spl(xnew)
    plt.plot(xnew, power_smooth, label=player, linewidth=2)
    
    # comment this out for the pure graph without interpolation
    #plt.plot(np.array(range(0, len(placements_dict[player]))), placements_dict[player], label=player, linewidth=2)
plt.legend(loc='best')
plt.savefig("plots/other/placements.png", bbox_inches="tight")
plt.close()