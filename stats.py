import pathlib
from Importer import import_match_data, prepare_html_files
from DataProcessing import process_data
from DataPlotter import map_data, get_y_ticks, plot_line_chart, save_bar_plot, save_pie_plot
from Definition import Dicts

cwd = pathlib.Path.cwd()
# make local directories where the plots are saved 
pathlib.Path((cwd / "plots/scores_per_team").resolve()).mkdir(exist_ok=True, parents=True)
pathlib.Path((cwd / "plots/points_per_team").resolve()).mkdir(exist_ok=True, parents=True)
pathlib.Path((cwd / "plots/other").resolve()).mkdir(exist_ok=True, parents=True)
pathlib.Path((cwd / "plots/points_per_prediction").resolve()).mkdir(exist_ok=True, parents=True)

prepare_html_files()
players, game_days, placements = import_match_data()
dict_of_dicts = process_data(game_days, players)

def plot_scores_per_team(input, title):
    resolution, amplitude = map_data(input)
    y_ticks = get_y_ticks(amplitude, max_offset=1)
    save_bar_plot(resolution, amplitude, "scores_per_team", title, y_ticks)

def plot_all_scores_per_team(input):
    resolution, amplitude = map_data(input)
    y_ticks = get_y_ticks(amplitude, max_offset=1)
    save_bar_plot(resolution, amplitude, "scores_per_team", "all_teams", y_ticks)

def plot_close_calls(input):
    resolution, amplitude = map_data(input)
    y_ticks = get_y_ticks(amplitude, max_offset=1, y_zero=0)
    save_bar_plot(resolution, amplitude, "other", "close_calls", y_ticks, "player", "amount of games", min(amplitude) - 5, max(amplitude))

def plot_missed_games(input):
    resolution, amplitude = map_data(input)
    y_ticks = get_y_ticks(amplitude, max_offset=1, y_zero=0)
    save_bar_plot(resolution, amplitude, "other", "missed_games", y_ticks, "player", "amount of games")

def plot_points_per_team_merged(input):
    resolution, amplitude = map_data(input)
    save_pie_plot(resolution, amplitude, "points_per_team", "all")

def plot_points_per_prediction(input, title):
    resolution, amplitude = map_data(input)
    y_ticks = get_y_ticks(amplitude, max_offset=4, y_zero=True, step_size=5)
    save_bar_plot(resolution, amplitude, "points_per_prediction", title, y_ticks, "prediction", "amount of points")

def plot_amount_of_predictions(input, title):
    resolution, amplitude = map_data(input)
    y_ticks = get_y_ticks(amplitude, max_offset=4, y_zero=True, step_size=5)
    save_bar_plot(resolution, amplitude, "points_per_prediction", title, y_ticks, "prediction", "amount of predictions")

def plot_points_per_prediction_normalized(input, title):
    resolution, amplitude = map_data(input)
    save_bar_plot(resolution, amplitude, "points_per_prediction", title, x_name="prediction", y_name= "amount of points/amount of predictions")

def plot_points_per_prediction_agglomerated(input):
    resolution, amplitude = map_data(input)
    y_ticks = get_y_ticks(amplitude, max_offset=10, y_zero=True, step_size=20)
    save_bar_plot(resolution, amplitude, "points_per_prediction", "all", y_ticks, "prediction", "amount of predictions")

def plot_amount_of_predictions_agglomerated(input):
    resolution, amplitude = map_data(input)
    y_ticks = get_y_ticks(amplitude, max_offset=10, y_zero=True, step_size=20)
    save_bar_plot(resolution, amplitude, "points_per_prediction", "amount_all", y_ticks, "prediction", "amount of predictions")

def plot_points_per_prediction_agglomerated_normalized(input):
    resolution, amplitude = map_data(input)
    save_bar_plot(resolution, amplitude, "points_per_prediction", "normalized_all", x_name="prediction", y_name= "amount of points/amount of predictions")

for team in dict_of_dicts[Dicts.TEAM_RESULTS]:
    plot_scores_per_team(dict_of_dicts[Dicts.TEAM_RESULTS][team], team)

points_per_prediction_normalized = {}
for player_index in dict_of_dicts[Dicts.POINTS_PER_PREDICTED_RESULT]:
    plot_points_per_prediction(dict_of_dicts[Dicts.POINTS_PER_PREDICTED_RESULT][player_index], players[player_index])
    plot_amount_of_predictions(dict_of_dicts[Dicts.AMOUNT_OF_PREDICTIONS][player_index], "amount_" + players[player_index])
    points_per_prediction_normalized[player_index] = {}
    for prediction in dict_of_dicts[Dicts.POINTS_PER_PREDICTED_RESULT][player_index]:
        points_per_prediction_normalized[player_index][prediction] = dict_of_dicts[Dicts.POINTS_PER_PREDICTED_RESULT][player_index][prediction] / dict_of_dicts[Dicts.AMOUNT_OF_PREDICTIONS][player_index][prediction]
    plot_points_per_prediction_normalized(points_per_prediction_normalized[player_index], "normalized_" + players[player_index])
 
points_per_prediction_agglomerated_normalized = {}
for prediction in dict_of_dicts[Dicts.POINTS_PER_PREDICTED_RESULT_AGGLOMERATED]:
    points_per_prediction_agglomerated_normalized[prediction] = dict_of_dicts[Dicts.POINTS_PER_PREDICTED_RESULT_AGGLOMERATED][prediction] / dict_of_dicts[Dicts.AMOUNT_OF_PREDICTIONS_AGGLOMERATED][prediction]

plot_points_per_prediction_agglomerated(dict_of_dicts[Dicts.POINTS_PER_PREDICTED_RESULT_AGGLOMERATED])
plot_amount_of_predictions_agglomerated(dict_of_dicts[Dicts.AMOUNT_OF_PREDICTIONS_AGGLOMERATED])
plot_points_per_prediction_agglomerated_normalized(points_per_prediction_agglomerated_normalized)

plot_all_scores_per_team(dict_of_dicts[Dicts.ALL_RESULTS_AGGLOMERATED])
plot_close_calls(dict_of_dicts[Dicts.CLOSE_CALLS])
plot_missed_games(dict_of_dicts[Dicts.MISSED_GAMES])

points_per_team_merged_dict = {}

index = 0
for player_index in dict_of_dicts[Dicts.POINTS_PER_TEAM]:
    players_dict = dict_of_dicts[Dicts.POINTS_PER_TEAM][player_index]
    resolution, amplitude = map_data(players_dict)
    save_pie_plot(resolution, amplitude, "points_per_team", players[index])

    for team in players_dict:
        if team in points_per_team_merged_dict:
            points_per_team_merged_dict[team] = points_per_team_merged_dict[team] + players_dict[team]
        else:
            points_per_team_merged_dict[team] = players_dict[team]
    index = index + 1

plot_points_per_team_merged(points_per_team_merged_dict)
plot_line_chart(placements, "other", "placements", (16, 10))