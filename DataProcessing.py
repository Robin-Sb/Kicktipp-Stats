def process_data(game_days, players):
  team_results = {}
  all_results_merged = {}
  points_per_team = {}
  close_calls = {}
  missed_games = {}

  for game_day in game_days:
    for match in game_day:
        fill_team_results_dict(match, team_results)
        fill_all_results_dict(match, all_results_merged)
        
        index = 0
        for prediction in match.predictions:
            fill_points_per_team_dict(match, index, points_per_team)
            fill_close_calls_dict(match, index, close_calls, players)
            fill_missed_games_dict(match, index, missed_games, players)
            index = index + 1
  return team_results, all_results_merged, points_per_team, close_calls, missed_games

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