from Definition import Dicts

def process_data(game_days, players):
    dict_of_dicts = {}
    team_results = {}
    all_results_merged = {}
    points_per_team = {}
    close_calls = {}
    missed_games = {}
    points_per_predicted_result = {}
    amount_of_predictions = {}
    points_per_predicted_result_agglomerated = {}
    amount_of_predictions_agglomerated = {}


    for game_day in game_days:
        for match in game_day:
            fill_team_results_dict(match, team_results)
            fill_all_results_dict(match, all_results_merged)
            #fill_all_points_per_predicted_result(match, points_per_predicted_result_agglomerated, amount_of_predictions_agglomerated)
            for index in range(len(match.predictions)):
                fill_points_per_team_dict(match, index, points_per_team)
                fill_close_calls_dict(match, index, close_calls, players)
                fill_missed_games_dict(match, index, missed_games, players)
                fill_points_per_predicted_result(match, index, points_per_predicted_result, amount_of_predictions, points_per_predicted_result_agglomerated, amount_of_predictions_agglomerated)
    
    dict_of_dicts[Dicts.TEAM_RESULTS] = team_results
    dict_of_dicts[Dicts.ALL_RESULTS_AGGLOMERATED] = all_results_merged
    dict_of_dicts[Dicts.POINTS_PER_TEAM] = points_per_team
    dict_of_dicts[Dicts.CLOSE_CALLS] = close_calls
    dict_of_dicts[Dicts.POINTS_PER_PREDICTED_RESULT] = points_per_predicted_result
    dict_of_dicts[Dicts.AMOUNT_OF_PREDICTIONS] = amount_of_predictions
    dict_of_dicts[Dicts.MISSED_GAMES] = missed_games
    dict_of_dicts[Dicts.AMOUNT_OF_PREDICTIONS_AGGLOMERATED] = amount_of_predictions_agglomerated
    dict_of_dicts[Dicts.POINTS_PER_PREDICTED_RESULT_AGGLOMERATED] = points_per_predicted_result_agglomerated
    return dict_of_dicts

def fill_team_results_dict(match, team_results):
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

def fill_all_results_dict(match, all_results_merged):
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

def fill_points_per_team_dict(match, index, points_per_team_dict):
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

def fill_points_per_predicted_result(match, index, points_per_predicted_result, amount_of_predictions, points_per_predicted_result_agglomerated, amount_of_predictions_agglomerated):
    prediction = match.predictions[index]
    if prediction.goals_home == None or prediction.goals_guest == None:
        return

    if index not in amount_of_predictions:
        amount_of_predictions[index] = {}

    score = award_points_per_game(match.goals_home, match.goals_guest, match.predictions[index])
    if index not in points_per_predicted_result:
        points_per_predicted_result[index] = {}

    if prediction.goals_home > prediction.goals_guest:
        prediction_as_string = str(prediction.goals_home) + ":" + str(prediction.goals_guest)
    else:
        prediction_as_string = str(prediction.goals_guest) + ":" + str(prediction.goals_home)

    # fill amount per predicted results agglomerated
    if prediction_as_string not in amount_of_predictions_agglomerated:
        old_amount_all = 0
    else:
        old_amount_all = amount_of_predictions_agglomerated[prediction_as_string]
    amount_of_predictions_agglomerated[prediction_as_string] = old_amount_all + 1

    # fill points per predicted results agglomerated
    if prediction_as_string not in points_per_predicted_result_agglomerated:
        old_score_all = 0
    else:
        old_score_all = points_per_predicted_result_agglomerated[prediction_as_string]
    points_per_predicted_result_agglomerated[prediction_as_string] = old_score_all + score

    # fill amount of predictions
    if prediction_as_string not in amount_of_predictions[index]:
        amount_of_predictions[index][prediction_as_string] = {}
        old_amount = 0
    else:
        old_amount = amount_of_predictions[index][prediction_as_string]
    amount_of_predictions[index][prediction_as_string] = old_amount + 1


    # fill point per predicted resul 
    if prediction_as_string not in points_per_predicted_result[index]:
        points_per_predicted_result[index][prediction_as_string] = {}
        old_score = 0
    else:
        old_score = points_per_predicted_result[index][prediction_as_string]
    points_per_predicted_result[index][prediction_as_string] = old_score + score

def assign_close_calls(goals_home, goals_guest, prediction):
    real_score = award_points_per_game(goals_home, goals_guest, prediction)
    home_inc_score = award_points_per_game(goals_home + 1, goals_guest, prediction)
    guest_inc_score = award_points_per_game(goals_home, goals_guest + 1, prediction)

    if home_inc_score > real_score or guest_inc_score > real_score:
        return 1
    return 0

def fill_close_calls_dict(match, index, close_calls_dict, players):
    score = assign_close_calls(match.goals_home, match.goals_guest, match.predictions[index])
    player = players[index]
    if player not in close_calls_dict:
        close_calls_dict[player] = 0
    close_calls_dict[player] = close_calls_dict[player] + score

def fill_missed_games_dict(match, index, missed_games_dict, players):
    player = players[index]
    if player not in missed_games_dict:
        missed_games_dict[player] = 0
    if match.predictions[index].goals_home is None or match.predictions[index].goals_guest is None:
        missed_games_dict[player] = missed_games_dict[player] + 1