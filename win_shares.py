# Purpose of this is to scrape winshare data from basketball-reference.com

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import urllib.request       # Determine whether urllib, urllib2, or requests is best option


# Access Basketball Reference to get league leaders in win shares for each season
#specify the url
site = "https://www.basketball-reference.com/leaders/ws_top_10.html"
#Query the website and return the html to the variable 'page'
page = urllib.request.urlopen(site)
#Parse the html in the 'page' variable and store it in Beautiful Soup format
soup = BeautifulSoup(page)
table = soup.table

# accesses table with year, player, winshares and puts info into a single list of strings.
def make_raw_list(table):
    '''table should be a BeautifulSoup table'''
    raw = []
    for string in table.stripped_strings:
        if string != '*':    #removes hall of fame denotation
            raw.append(string)
    raw = raw[13:]   #removes unneccessary labeling info
    return raw

# create lists with years, league, top 10 leaders in win shares, player page links, win shares
def get_years(raw):
    years = []
    for i in raw:
        x = 0
        if i[0]=='2' or i[0] == '1':
            while x < 10:
                (years.append(i))
                x +=1
            x=0
    return years

def get_league(raw):
    league = []
    for i in raw:
        if len(i)==3:
            while x < 10:
                league.append(i)
                x += 1
            x = 0
     return league

def get_players(raw)
    players = []
    for player in raw:
        if len(player) != 3 and player[0].isalpha():
            players.append(player)
    return players

def get_player_links(source):
    '''source should be a BeautifulSoup table'''
    player_links = []
    for a in source.find_all('a'):
        if 'leagues' not in a['href']:
            player_links.append(a['href'])
    return player_links


def get_win_shares(raw):
    win_shares = []
    for num in raw:
        if num[0] == "(":
            win_shares.append(float(num[1:-1]))
    return win_shares

        

def unique_li(players):
    '''Create list of UNIQUE PLAYER dictionaries with player as key and list of indices in players list'''
    
    unique = []
    full_unique = []
    for individual in players:
        if individual not in unique:
            unique.append(individual)
    for player in unique:
        play_dic = {}
        play_dic[player] = [x for x in range(len(players)) \
                            if players[x] == player \
                            ]
        full_unique.append(play_dic)
    return full_unique


# use year to pull team info from player page
def get_teams(players, player_links):
    teams = []
    for i in range(820):
        fx_player = players[i]
        fx_link = player_links[i]
        if years[i][:2] + years[i][-2:] == '1900':
            fx_year = '2000'
        else:
            fx_year = years[i][:2] + years[i][-2:]
        fx_league = league[i]
        site = 'https://www.basketball-reference.com/%s' % (fx_link)
        page = urllib.request.urlopen(site)
        soup = BeautifulSoup(page)
        for j in soup.table.find_all('a'):
            if (fx_year in j['href']) and (j['href'][1] == 't'):
                fx_team = (j['href'][7:10])
                teams.append(fx_team)
                break
        print(fx_year, fx_player, fx_team) #
    return teams

    
# use team and year to pull wins from
def get_team_wins(teams):
    team_wins = []
    for k in range(820):
        fx_team = teams[k]
        if years[k][:2] + years[k][-2:] == '1900':
            fx_year = '2000'
        else:
            fx_year = years[k][:2] + years[k][-2:]
        site = 'https://www.basketball-reference.com/teams/%s/%s.html' % (fx_team, fx_year)
        page = urllib.request.urlopen(site)
        soup = BeautifulSoup(page)
        paragraphs = (list(soup.find_all('p')))
        fx_wins = int((str(paragraphs[2]))[40:42])
        team_wins.append(fx_wins)
        print(players[k], years[k], teams[k], fx_wins)
    return team_wins()


# Run functions
raw = make_raw_list(table)
years = get_years(raw)
league = get_league(raw)
players = get_players(raw)
player_links = get_player_links(raw)
win_shares = get_win_shares(raw)

# Create dataframe to perform analysis on

df = pd.DataFrame({'Year':years,
                   'League':league,
                   'Player':players,
                    'Win shares':win_shares,
                   'Link':player_links,
                   'Team':teams,
                   'Team Wins':team_wins})



# Graph Team Wins vs Wins Shares
plt.figure(figsize=(10,10))
plt.scatter(team_wins, win_shares)
plt.ylabel('Win Shares')
plt.xlabel('Team Wins')
plt.title('Comparison Between Team Wins and Wins for Top Ten Season Leaders (1947-2019)')
plt.show()




# look at frequency each player has been in the top 10
leaders = 
for i in list(df["Player"]):
    if i not in leaders:
        leaders[i] = 1
    else:
        leaders[i] += 1
        
keys = []
values = []
for key in leaders.keys():
    if leaders[key] > 5:
        keys.append(key)
        values.append(leaders[key])

leader_df = pd.DataFrame({'Name': keys,
                         'Frequency':values})
leader_df.sort_values(by = ['Frequency'], ascending =False)
