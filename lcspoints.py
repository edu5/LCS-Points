import json, requests, datetime, time, collections

current_season_url = "http://na.lolesports.com:80/api/gameStatsFantasy.json?tournamentId=%s&dateBegin=%s&dateEnd=%s"
one_lcs_week = 604800 									#one week in seconds


###########

current_split = "2014 Summer Split"
season_start = datetime.datetime(2014, 05, 19, 0, 0)	#LCS Summer Split 2014 Week 1 Date
#LCS Summer Split 2014 Teams
team_tags = {
	#NA Teams
	"C9": "Cloud9 ",
	"CRS": "Curse",
	"COL": "compLexity ",
	"EG": "Evil Geniuses",
	"TSM": "Team SoloMid",
	"LMQ": "LMQ",
	"CLG": "Counter Logic Gaming",
	"DIG": "Team Dignitas",
	
	#EU Teams
	"CW": "Copenhagen Wolves",
	"GMB": "Gambit Gaming",
	"ROC": "ROCCAT",
	"ALL": "Alliance",
	"FNC": "Fnatic",
	"SK": "SK Gaming",
	"MIL": "Millenium",
	"SHC": "Supa Hot Crew"
}

####################

def get_epoch_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def get_data_for_week(region_id, week):
	season_start_epoch = get_epoch_time(season_start)
	offset = one_lcs_week * (week - 1)
	
	start = int(season_start_epoch + offset)     
	end = int(season_start_epoch + (offset + one_lcs_week))
	
	data = requests.get(current_season_url % (region_id, start, end)).text
	return json.loads(data, object_pairs_hook=collections.OrderedDict)

def compute_points_for_player(game):
	total = 0.0
	total += game['kills'] * 2.0
	total -= game['deaths'] * 0.5
	total += game['assists'] * 1.5
	total += game['minionKills'] * 0.01
	total += game['tripleKills'] * 2.0
	total += game['quadraKills'] * 5.0
	total += game['pentaKills'] * 10.0
	
	if game['kills'] > 10 or game['assists'] > 10:
		total += 2
	
	return total

	
def compute_points_for_team(game):
	total = 0.0
	total += game['matchVictory'] * 2.0
	total += game['baronsKilled'] * 2.0
	total += game['dragonsKilled'] * 1.0
	total += game['firstBlood'] * 2.0
	total += game['towersKilled'] * 1.0	
	
	return total
	
	
if __name__ == "__main__":
	print("Obtain LCS Fantasy statistics of a player for the current season!")

	region = raw_input("Enter a region (NA / EU): ")
	while region != "NA" and region != "EU":
		region = raw_input("Invalid region (NA / EU): ")

	# EU = 102, NA = 104
	if region == "NA":
		region = 104
	else:
		region = 102
	
	week = raw_input("Enter a LCS week number (1 - 11): ")
	week = int(week)
	while week < 1 or week > 11:
		week = raw_input("Invalid week number. (1 - 11): ")
		week = int(week)
	
	name = raw_input("Enter name of player (ex: 'Doublelift') or team tag in uppercase (ex: 'CLG'): ")

	data = get_data_for_week(region, week)

	score = 0
	for game_id in data['playerStats']:
		game = data['playerStats'][game_id]
		for key in game:
			if not key.find("player"):
				current_player_name = game[key]['playerName']
				current_player_name = current_player_name.lower()
				current_player_name = current_player_name.replace(' ', '')
				
				if current_player_name == name.lower():
					score += compute_points_for_player(game[key])
				
	for game_id in data['teamStats']:
		game = data['teamStats'][game_id]
		for key in game:
			if not key.find("team"):
				current_team_name = game[key]['teamName']
				if name in team_tags and team_tags[name] == current_team_name:
					score += compute_points_for_team(game[key])
				
	print "Points for", name, "on Week", week, current_split, ":", score
