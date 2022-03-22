import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# reading the csv file
relative_data_dir = 'season-1213_csv.csv'
data = pd.read_csv(relative_data_dir)

## CONSTANTS
# number of matches played throughout the season
MATCHES = 380
# number of matches that each team played throughout the season
TEAM_MATCHES_PER_SEASON = 38
TOP_SIX = ['Man United', 'Man City', 'Chelsea', 'Arsenal', 'Tottenham', 'Everton']
# had to put teams manually to maintain the league ranking
TEAMS = ['Man United', 'Man City', 'Chelsea', 'Arsenal', 'Tottenham',
         'Everton', 'Liverpool', 'West Brom', 'Swansea', 'West Ham',
         'Norwich', 'Fulham', 'Stoke', 'Southampton', 'Aston Villa',
         'Newcastle', 'Sunderland', 'Wigan', 'Reading', 'QPR']


def halves_result_comparison(data):
    """ Returns a dictionary to compare the changes in results between
        half-time and full-time. """
    ret = {
        'Home Win to Home Win' : 0,
        'Home Win to Draw' : 0,
        'Home Win to Home Lose' : 0,
        'Draw to Home Win' : 0,
        'Draw to Draw' : 0,
        'Draw to Home Lose' : 0,
        'Home Lose to Home Win' : 0,
        'Home Lose to Draw' : 0,
        'Home Lose to Home Lose' : 0
    }
    for i in range(MATCHES):
        # Home team was winning at half-time
        if data['HTR'][i] == 'H':
            # Home team won at full-time
            if data['FTR'][i] == 'H':
                ret['Home Win to Home Win'] = ret['Home Win to Home Win']+1
            # Draw at full-time
            elif data['FTR'][i] == 'D':
                ret['Home Win to Draw'] = ret['Home Win to Draw']+1
            # Home team lost at full-time
            elif data['FTR'][i] == 'A':
                ret['Home Win to Home Lose'] = ret['Home Win to Home Lose']+1
        # Draw at half-time
        elif data['HTR'][i] == 'D':
            if data['FTR'][i] == 'H':
                ret['Draw to Home Win'] = ret['Draw to Home Win']+1
            elif data['FTR'][i] == 'D':
                ret['Draw to Draw'] = ret['Draw to Draw']+1
            elif data['FTR'][i] == 'A':
                ret['Draw to Home Lose'] = ret['Draw to Home Lose']+1
        # Home team was losing at half-time
        elif data['HTR'][i] == 'A':
            if data['FTR'][i] == 'H':
                ret['Home Lose to Home Win'] = ret['Home Lose to Home Win']+1
            elif data['FTR'][i] == 'D':
                ret['Home Lose to Draw'] = ret['Home Lose to Draw']+1
            elif data['FTR'][i] == 'A':
                ret['Home Lose to Home Lose'] = ret['Home Lose to Home Lose']+1
    return ret

def team_statistic_per_season(data, team, stat_type):
    """ Returns  a specific statistic (such as goals, shots, fouls... etc)
    from the dataset for a specific team throughout the whole season. """
    ret = 0
    for i in range(MATCHES):
        if data['HomeTeam'][i] == team:
            # this condition is checked because the full-time
            # goals are given in another format
            if stat_type == 'FTG':
                ret = ret + data['FTHG'][i]
            else:
                # add H if it's a home team
                ret = ret + data['H' + stat_type][i]
        elif data['AwayTeam'][i] == team:
            # this condition is checked because the full-time
            # goals are given in another format
            if stat_type == 'FTG':
                ret = ret + data['FTAG'][i]
            else:
                # add A if it's an away team
                ret = ret + data['A' + stat_type][i]
    return ret

def avg_betting_per_season(data, team, result):
    """ Returns the average betting for a specific result (win, draw or lose)
        for a specific team throughout the season. """
    ret = 0
    for i in range(MATCHES):
        if data['HomeTeam'][i] == team:
            if result == 'W':
                # BbAvH gets the rate of win for the home team
                ret = ret + data['BbAvH'][i]
            elif result == 'D':
                # BbAvD gets the rate of draw
                ret = ret + data['BbAvD'][i]
            elif result == 'L':
                # BbAvA gets the rate of lose for the home team
                ret = ret + data['BbAvA'][i]
        # if the team is the away team they get reversed
        elif data['AwayTeam'][i] == team:
            if result == 'W':
                ret = ret + data['BbAvA'][i]
            elif result == 'D':
                ret = ret + data['BbAvD'][i]
            elif result == 'L':
                ret = ret + data['BbAvH'][i]
    # dividing the sum over the number of matches for the team and rounding
    ret = round(ret/TEAM_MATCHES_PER_SEASON,2)
    return ret


# adding title to the pie chart
plt.title('Half-time VS Full-time Results')

# creating the pie chart
halves_result_comparison = halves_result_comparison(data)
plt.pie(halves_result_comparison.values(), labels = halves_result_comparison.keys(), autopct='%1.0f%%', startangle=90)

# showing the pie chart
plt.show()

top_six_goals = []
top_six_shots = []
top_six_shots_on_target = []

# populating the lists with the values of goals, shots and shots on target
for i in range(len(TOP_SIX)):
    top_six_goals.append(team_statistic_per_season(data,TOP_SIX[i],'FTG'))
    top_six_shots.append(team_statistic_per_season(data,TOP_SIX[i],'S'))
    top_six_shots_on_target.append(team_statistic_per_season(data,TOP_SIX[i],'ST'))

# setting the width of each bar
bar_width = 0.2

# x-axis index
x_index = np.arange(len(TOP_SIX))
plt.xticks(ticks=x_index, labels=TOP_SIX)

# adding a bar for each stat
plt.bar(x_index-bar_width, top_six_shots, width=bar_width, label='Shots')
plt.bar(x_index, top_six_shots_on_target, width=bar_width, label='Shots on Target')
plt.bar(x_index+bar_width, top_six_goals, width=bar_width, label='Goals')
plt.legend()

# adding title to the graph
plt.title('Shots vs Shots on Target vs Goals for Top 6')

# showing the bars graph
plt.show()

# getting the betting rates for each team in the league (win/draw/lose)
bettings = []
for team in TEAMS:
    team_betting = [avg_betting_per_season(data, team, res) for res in ['W', 'D', 'L']]
    bettings.append(team_betting)

# configuring the table properties
fig, ax =plt.subplots(1,1)
ax.axis('off')
ax.set_title('Average Betting Rates for Team Results')

# creating the table
ax.table(cellText=bettings, rowLabels= TEAMS, colLabels= ['Win', 'Draw', 'Lose'], 
loc='center', colWidths= [0.13]*3, rowColours =['green']+["orange"]*16+['red']*3,
colColours =["orange"]*3,)

# showing the table
plt.show()
