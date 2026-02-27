import requests
import pandas as pd
import os

class Statistics():
    
    
    def __init__(self):
        self.team_ids = self.get_team_ids()
    
    
    
    
    #Creates a list with each entry as a dictionary. Key is the team, value is the team id
    def get_team_ids(self):
        teams_url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams"
        response = requests.get(teams_url)
        data = response.json()
        team_names = []
        for team in data['sports'][0]['leagues'][0]['teams']:
            name = team['team']['displayName']
            id = team['team']['id']
            new_dict = {name: id}
            team_names.append(new_dict)
        return team_names
    
    
    
    #returns a list of all the game ids for the inputed team
    def get_game_ids(self,team_id):
        schedule_url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_id}/schedule"
        response = requests.get(schedule_url)
        data = response.json()
        game_ids=[]
        for game in data['events']:
            game_ids.append(game['id'])
        return game_ids
    
    #Adds a column for a new statistic
    def add_to_csv(self,list,statistic,team):
        #Check if csv file exists
        file = f"data/{team}_data.csv"
        if not os.path.exists(file):
            data = {statistic: list}
            df = pd.DataFrame(data)
            file_path = file
            df.to_csv(file_path,index=False)
        try:
            df = pd.read_csv(file)
            df[statistic] = list
            df.to_csv(file,index=False)
        except FileNotFoundError:
            print(f"Error: The file '{file}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def update_csv(self,team_id,):
        pass

#Identifiers   
    def get_season(self,team_id,year):
        list=[]
        schedule_url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_id}/schedule?season={year}"
        response = requests.get(schedule_url)
        data=response.json()
        for x in range(82):
            list.append(data['events'][0]['season']['displayName'])
        return list
    
    def get_dates(self,team_id,year):
        game_dates=[]
        schedule_url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_id}/schedule?season={year}"
        response = requests.get(schedule_url)
        data = response.json()
        for game in data['events']:
            date = str(game['date'])
            game_dates.append(date.split('T')[0])
        return game_dates       
    
    def get_team(self,team_id):
        pass
    
    def get_opponent(self, team_id, year):
        opp_list = []
        schedule_url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_id}/schedule?season={year}"
        response = requests.get(schedule_url)
        data = response.json()
        for game in data['events']:
            competitors = game['competitions'][0]['competitors']
            for competitor in competitors:
                if competitor['team']['id'] != str(team_id):
                    opp_list.append(competitor['team']['displayName'])
                    break
        return opp_list
    
#Target
    def get_win_loss(self,team_id,year):
        win_list=[]
        schedule_url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_id}/schedule?season={year}"
        response = requests.get(schedule_url)
        data = response.json()
        for game in data['events']:
            competitors = game['competitions'][0]['competitors']
            team_score = None
            opponent_score = None
            for competitor in competitors:
                if competitor['team']['id'] == str(team_id):
                    if 'score' in competitor:
                        team_score = int(competitor['score']['value']) if isinstance(competitor['score'], dict) else int(competitor['score'])
                else:
                    if 'score' in competitor:
                        opponent_score = int(competitor['score']['value']) if isinstance(competitor['score'], dict) else int(competitor['score'])
            # Append empty string for games without final scores (upcoming games)
            if team_score is not None and opponent_score is not None:
                result = 1 if team_score > opponent_score else 0
            else:
                result = ""
            win_list.append(result)
        return win_list
    
#Statistics           
    
    def get_home_away(self, team_id,event_ids_list):
        """
        For each event_id in event_ids_list, fetches the game summary and determines if the team_id is home (1) or away (0).
        Returns a list of 1s and 0s corresponding to home/away for each event.
        """
        home_list = []
        for event_id in event_ids_list:
            url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={event_id}"
            try:
                response = requests.get(url)
                data = response.json()
                competitors = data['header']['competitions'][0]['competitors']
                for competitor in competitors:
                    if competitor['team']['id'] == str(team_id):
                        if competitor.get('homeAway', '').lower() == 'home':
                            home_list.append(1)
                        elif competitor.get('homeAway', '').lower() == 'away':
                            home_list.append(0)
                        else:
                            home_list.append("")  # Unknown
                        break
                else:
                    home_list.append("")  # Team not found in competitors
            except Exception as e:
                home_list.append("")  # Error fetching or parsing
        return home_list

#Scoring
    def get_average_scoring_margin(self,team_id,event_id_list):
        total_points_for = []
        total_points_against = []
        played_flags = []
        for event_id in event_id_list:
            url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={event_id}"
            try:
                response = requests.get(url)
                data = response.json()
                competitors = data['header']['competitions'][0]['competitors']
                points_for = None
                points_against = None
                for competitor in competitors:
                    if competitor['team']['id'] == str(team_id):
                        if 'score' in competitor:
                            points_for = int(competitor['score']['value']) if isinstance(competitor['score'], dict) else int(competitor['score'])
                    else:
                        if 'score' in competitor:
                            points_against = int(competitor['score']['value']) if isinstance(competitor['score'], dict) else int(competitor['score'])
                if points_for is not None and points_against is not None:
                    total_points_for.append(points_for)
                    total_points_against.append(points_against)
                    played_flags.append(True)
                else:
                    total_points_for.append(None)
                    total_points_against.append(None)
                    played_flags.append(False)
            except Exception:
                total_points_for.append(None)
                total_points_against.append(None)
                played_flags.append(False)
        scoring_margins = []
        for i in range(1, len(total_points_for) + 1):
            # Only calculate if all games up to i have been played
            if all(played_flags[:i]):
                points_for_sum = sum([pf for pf in total_points_for[:i] if pf is not None])
                points_against_sum = sum([pa for pa in total_points_against[:i] if pa is not None])
                margin = (points_for_sum - points_against_sum) / i
                scoring_margins.append(round(margin, 2))
            else:
                scoring_margins.append("")
        return scoring_margins
    
    def get_net_rating(self,team_id):
        pass
    
    def get_pace(self,team_id):
        pass

#Shooting
    def get_eFG(self,team_id):
        pass
    
    def get_true_shooting_percentage(self,team_id):
        pass
    
    def get_three_point_rate(self,team_id):
        pass
    
    def get_FTA_per_FGA(self,team_id):
        pass
    
#Rebounding
    def get_defensive_rebounding_percentage(self,team_id):
        pass
    
#Blocks and steals
    def get_block_percentage(self,team_id):
        pass
    
    def get_steals_per_play(self,team_id):
        pass
    
    #Scoring and all splits
    def get_assist_turnover_ratio(self,team_id):
        pass
    
#Defense
    def get_opp_eFG(self,team_id):
        pass
    
    def get_opp_true_shooting(self,team_id):
        pass
    
    def get_opp_turnover_per_pos(self,team_id):
        pass

#Rolling
    def get_rest_days(self,team_id):
        pass
    
    def get_L5_win_percent(self,team_id):
        pass
    
    #in records
    def get_streak(self,team_id):
        streak_url = 'sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{EVENT_ID}/competitions/{EVENT_ID}/competitors/{TEAM_ID}/records'
        