from statistics import Statistics
statistics = Statistics()
import pandas as pd

#HOW TO GET TEAM ID
# int(statistics.team_ids[0]["Team Name"])

#ADDS GAME IDS
atlanta_hawks_game_ids_list = statistics.get_game_ids(int(statistics.team_ids[0]["Atlanta Hawks"]))
# statistics.add_to_csv(atlanta_hawks_game_ids_list,"game_id",next(iter(statistics.team_ids[0].keys())))

#ADD SEASON
# season = statistics.get_season(statistics.team_ids[0]["Atlanta Hawks"],2023)
# statistics.add_to_csv(season,"season",next(iter(statistics.team_ids[0].keys())))

#ADD DATES
# dates_list = statistics.get_dates(team_id=statistics.team_ids[0]["Atlanta Hawks"],year=2023)
# statistics.add_to_csv(list=dates_list,statistic="date",team=next(iter(statistics.team_ids[0].keys())))

# Get opponents
# opp_list = statistics.get_opponent(team_id=statistics.team_ids[0]['Atlanta Hawks'],year=2026)
# statistics.add_to_csv(list=opp_list,statistic="opponent",team=next(iter(statistics.team_ids[0].keys())))

#Get wins
# win_list = statistics.get_win_loss(1,2023)
# statistics.add_to_csv(list=win_list,statistic="result", team=next(iter(statistics.team_ids[0].keys())))

#Get home
# home = statistics.get_home_away(1,atlanta_hawks_game_ids_list)
# statistics.add_to_csv(list=home,statistic="home",team=next(iter(statistics.team_ids[0].keys())))

#Get Average Scoring Marigin
avg_scoring_margin = statistics.get_average_scoring_margin(1,atlanta_hawks_game_ids_list)
statistics.add_to_csv(list=avg_scoring_margin,statistic="scoring_margin", team=next(iter(statistics.team_ids[0].keys())))
