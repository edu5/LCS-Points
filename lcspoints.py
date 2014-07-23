import json, requests, datetime, time, collections

current_season_url = "http://na.lolesports.com:80/api/gameStatsFantasy.json?tournamentId=%s&dateBegin=%s&dateEnd=%s"
season_start = datetime.datetime(2014, 05, 19, 0, 0)	#LCS Summer Split Week 1 Date
one_lcs_week = 604800 									#one week in seconds

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
	
	week = raw_input("Enter a LCS week number (1 - 10)")
	week = int(week)
	while week < 1 or week > 10:
		week = raw_input("Invalid week number. (1 - 10)")
		week = int(week)
	
	name = raw_input("Enter name of player (no team name): ")

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
				
	print score