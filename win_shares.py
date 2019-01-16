# Purpose of this is to scrape winshare data from basketball-reference.com

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
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
raw_list = []
for string in table.stripped_strings:
    if string != '*':    #removes hall of fame denotation
        raw_list.append(string)
raw_list = raw_list[13:]   #removes unneccessary labeling info


# create list with years, league, top 10 leaders in win shares, player page links, win shares
years = []
for i in raw_list:
    x = 0
    if i[0]=='2' or i[0] == '1':
        while x < 10:
            (years.append(i))
            x +=1
        x=0

league = []
for i in raw_list:
    if len(i)==3:
        while x < 10:
            league.append(i)
            x += 1
        x = 0

players = []
for player in raw_list:
    if len(player) != 3 and player[0].isalpha():
        players.append(player)

player_links = []
for a in table.find_all('a'):
    if 'leagues' not in a['href']:
        player_links.append(a['href'])

win_shares = []    
for num in raw_list:
    if num[0] == "(":
        win_shares.append(float(num[1:-1]))


        
        
# Create list of UNIQUE PLAYERS





# use year to pull team info from player page
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

    
    
# use team and year to pull wins from
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
    
# Create dataframe to perform analysis on

df = pd.DataFrame({'Year':years,
                   'League':league,
                   'Player':players,
                    'Win shares':win_shares,
                   'Link':href,
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
