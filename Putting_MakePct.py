import operator
import numpy as np
import statistics
import matplotlib.pyplot as plt
from colour import Color
from bs4 import BeautifulSoup
import urllib3

###############    ACCESS WEBPAGES       ####################
def makeSoup(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soupdata = BeautifulSoup(response.data)
    return soupdata

siteURL = []
for i in range(7):
    siteURL.append(i)
siteURL[0] = ''
siteURL[1] = 'http://www.pgatour.com/stats/stat.408.html'   #>25
siteURL[2] = 'http://www.pgatour.com/stats/stat.407.html'   #20-25
siteURL[3] = 'http://www.pgatour.com/stats/stat.406.html'   #15-20
siteURL[4] = 'http://www.pgatour.com/stats/stat.405.html'   #10-15
siteURL[5] = 'http://www.pgatour.com/stats/stat.404.html'   #5-10
siteURL[6] = 'http://www.pgatour.com/stats/stat.02427.html' #3-5

###############    ACCESS TABLE DATA      ###################
def row_number(soupdata):
    for row in table.findAll('tr'):
        tot_row = row
    return tot_row

def parse_table(soupdata):
    currRank = []
    prevRank = []
    playerName = []
    rounds = []
    pctMake = []
    attempts = []
    puttsMade = []
    table = soupdata.find('tbody')
    tot_row = 0
    for row in table.findAll('tr'):
        #for col in row.findAll('td'):
        col = row.find_all('td')
        #column_1 = col[0]
        #currRank.append(column_1)
        #column_2 = col[1]
        #prevRank.append(column_2)
        column_3 = col[2].text
        column_3.strip()
        playerName.append(column_3)
        #column_4 = col[3]
        #rounds.append(column_4) 
        column_5 = col[4].text
        pctMake.append(column_5)            
        #column_6 = col[5]
        #attempts.append(column_6)    
        #column_7 = col[6]
        #puttsMade.append(column_7)
        tot_row += 1
    #return currRank, prevRank, playerName, rounds, pctMake, attempts, puttsMade
    return playerName, pctMake, tot_row

"""
>25 ft: distance1
20-25 ft: distance2
15-20 ft: distance3
10-15 ft: distance4
5-10 ft: distance5
3-5 ft: distance6
"""
###############    CLASS DEFINITION      ###################
class Player:
    id_list={}
    def __init__(self,name, id, dis1=0.0, dis2=0.0, dis3=0.0, dis4=0.0, dis5=0.0, dis6=0.0):
        self.name = name
        self.dis1 = dis1
        self.dis2 = dis2
        self.dis3 = dis3
        self.dis4 = dis4
        self.dis5 = dis5
        self.dis6 = dis6
        self.id = id
        Player.id_list[self.name] = self # save the id as key and self as he value
    def __repr__(self):
        return '({},{},{})'.format(self.name, self.dis1, self.dis2)
    def addDis1(self,distance1):
        self.dis1 = float(distance1)
    def addDis2(self,distance2):
        self.dis2 = float(distance2)
    def addDis3(self,distance3):
        self.dis3 = float(distance3)
    def addDis4(self,distance4):
        self.dis4 = float(distance4)
    def addDis5(self,distance5):
        self.dis5 = float(distance5)
    def addDis6(self,distance6):
        self.dis6 = float(distance6)
    def displayPlayer(self):
        print("Player: ", self.name, '\n'
              ">25 Ft %: ", self.dis1, '\n'
              "20-25 Ft %: ", self.dis2, '\n'
              "15-20 Ft %: ", self.dis3, '\n'
              "10-15 Ft %: ", self.dis4, '\n'
              "5-10 Ft %: ", self.dis5, '\n'
              "3-5 Ft %: ", self.dis6, '\n')
    @classmethod
    def lookup_player_name_by_id(cls, name):
        try:
            return cls.id_list[name] # return the instance with the id 
        except KeyError: # error check for if id does not exist
            raise KeyError("No user with id %s" % str(id))

###############    DATA POPULATION      ###################
PlayerNumber=[]
soupdata = makeSoup(siteURL[1])
playerName, pctMake, tot_row = parse_table(soupdata)
for i in range(0,tot_row):
    PlayerNumber.append(i)
for i in range(1,7):
    soupdata = makeSoup(siteURL[i])
    playerName, pctMake, tot_row = parse_table(soupdata)
    for x in range(0,tot_row):
        name = playerName[x]
        name = name.replace("\xa0", " ")
        name = name.replace("\n", "")
        if i == 1:
            PlayerNumber[x] = Player(name,x)
            Player.addDis1(PlayerNumber[x],pctMake[x])
        if i == 2:
            val = Player.lookup_player_name_by_id(name)
            Player.addDis2(PlayerNumber[val.id],pctMake[x])
        if i == 3:
            val = Player.lookup_player_name_by_id(name)
            Player.addDis3(PlayerNumber[val.id],pctMake[x])
        if i == 4:
            val = Player.lookup_player_name_by_id(name)
            Player.addDis4(PlayerNumber[val.id],pctMake[x])
        if i == 5:
            val = Player.lookup_player_name_by_id(name)
            Player.addDis5(PlayerNumber[val.id],pctMake[x])
        if i == 6:
            val = Player.lookup_player_name_by_id(name)
            Player.addDis6(PlayerNumber[val.id],pctMake[x])

PlayerNumber.sort(key = operator.attrgetter("name"))  
#####################     AVERAGES     #################################
def avg(distance):
    average = sum(distance)/float(len(PlayerNumber))
    return average

avgD1 = avg(float(name.dis1) for name in PlayerNumber)
avgD2 = avg(float(name.dis2) for name in PlayerNumber)
avgD3 = avg(float(name.dis3) for name in PlayerNumber)
avgD4 = avg(float(name.dis4) for name in PlayerNumber)
avgD5 = avg(float(name.dis5) for name in PlayerNumber)
avgD6 = avg(float(name.dis6) for name in PlayerNumber)

#####################     STD DEVS     #################################
stdD1=statistics.stdev(float(name.dis1) for name in PlayerNumber)
stdD2=statistics.stdev(float(name.dis2) for name in PlayerNumber)
stdD3=statistics.stdev(float(name.dis3) for name in PlayerNumber)
stdD4=statistics.stdev(float(name.dis4) for name in PlayerNumber)
stdD5=statistics.stdev(float(name.dis5) for name in PlayerNumber)
stdD6=statistics.stdev(float(name.dis6) for name in PlayerNumber) 

##################   COLOR INITIALIZATION     #########################
red = Color("red")
colors = list(red.range_to(Color("green"),40))

###############     PLAYER SELECTION INPUT    ########################
try:
    playerName_input=str(input('Player Name: '))
except ValueError:
    print("Not a string")
for pos in range(0,tot_row):
    if playerName_input == PlayerNumber[pos].name:
        player_input = pos
        golfer = PlayerNumber[pos].name


#################     COLOR GRADIENT CALC     #############################
def color_grad(distance, avg, std):
    color_loc = 0
    Dcolor = 0
    dtD = 0
    for grad in range(-20,20):
        if distance < (avg + (grad/10.0)*std) and Dcolor == 0:
            Dcolor = colors[color_loc]
            dtD = distance - avg
        if grad == 19 and Dcolor == 0:
            Dcolor = colors[color_loc]
            dtD = distance - avg
        color_loc += 1
    return Dcolor, dtD

D1color, dtD1 = color_grad(PlayerNumber[player_input].dis1, avgD1, stdD1)
D2color, dtD2 = color_grad(PlayerNumber[player_input].dis2, avgD2, stdD2)
D3color, dtD3 = color_grad(PlayerNumber[player_input].dis3, avgD3, stdD3)
D4color, dtD4 = color_grad(PlayerNumber[player_input].dis4, avgD4, stdD4)
D5color, dtD5 = color_grad(PlayerNumber[player_input].dis5, avgD5, stdD5)
D6color, dtD6 = color_grad(PlayerNumber[player_input].dis6, avgD6, stdD6)

#################     SET AXES     #############################
ax = plt.subplot(111)
ax.set_aspect('equal')
ax.set_xlim((-30, 30))
ax.set_ylim((-30, 30))

def color_graph(dia, outer, inner, colour):
    ax.fill_between(dia, inner, outer, color=colour)
    ax.fill_between(dia, -outer, -inner, color=colour)

x6 = np.linspace(-5, 5, 1000, endpoint=True)
D6O = 5.*np.sin(np.arccos(x6/5.))
D6I = 3.*np.sin(np.arccos(x6/3.))
D6I[np.isnan(D6I)] = 0.
color_graph(x6, D6O, D6I, str(D6color))

x5 = np.linspace(-10, 10, 1000, endpoint=True)
D5O = 10.*np.sin(np.arccos(x5/10.))
D5I = 5.*np.sin(np.arccos(x5/5.))
D5I[np.isnan(D5I)] = 0.
color_graph(x5, D5O, D5I, str(D5color))

x4 = np.linspace(-15, 15, 1000, endpoint=True)
D4O = 15.*np.sin(np.arccos(x4/15.))
D4I = 10.*np.sin(np.arccos(x4/10.))
D4I[np.isnan(D4I)] = 0.
color_graph(x4, D4O, D4I, str(D4color))

x3 = np.linspace(-20, 20, 1000, endpoint=True)
D3O = 20.*np.sin(np.arccos(x3/20.))
D3I = 15.*np.sin(np.arccos(x3/15.))
D3I[np.isnan(D3I)] = 0.
color_graph(x3, D3O, D3I, str(D3color))

x2 = np.linspace(-25, 25, 1000, endpoint=True)
D2O = 25.*np.sin(np.arccos(x2/25.))
D2I = 20.*np.sin(np.arccos(x2/20.))
D2I[np.isnan(D2I)] = 0.
color_graph(x2, D2O, D2I, str(D2color))

x1 = np.linspace(-50, 50, 1000, endpoint=True)
D1O = 50.*np.sin(np.arccos(x1/50.))
D1I = 25.*np.sin(np.arccos(x1/25.))
D1I[np.isnan(D1I)] = 0.
color_graph(x1, D1O, D1I, str(D1color))

"""
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 10
fig_size[1] = 10
plt.rcParams["figure.figsize"] = fig_size
plt.rcParams.update({'font.size': 24})
plt.title("Various Distance Make Pcts for " + golfer)
"""

#ax.figure(figsize=(8, 8), dpi=80)
fig = plt.gcf()
fig.set_size_inches(20, 20)
#plt.rcParams["figure.figsize"] = (30,30)
plt.rcParams.update({'font.size': 24})

plt.title("Various Distance Make Pcts for " + golfer)

ax.text(12, 19.25, '+/- Player Value vs Avg\n' + 
        '>25ft: ' + "{0:.2f}".format(dtD1) + ' '
        '|| SDEV: ' + "{0:.2f}".format(stdD1) + '\n'
        '20-25ft: ' + "{0:.2f}".format(dtD2) + ' '
        '|| SDEV: ' + "{0:.2f}".format(stdD2) + '\n'
        '15-20ft: ' + "{0:.2f}".format(dtD3) + ' '
        '|| SDEV: ' + "{0:.2f}".format(stdD3) + '\n'
        '10-15ft: ' + "{0:.2f}".format(dtD4) + ' '
        '|| SDEV: ' + "{0:.2f}".format(stdD4) + '\n'
        '5-10ft: ' + "{0:.2f}".format(dtD5) + ' '
        '|| SDEV: ' + "{0:.2f}".format(stdD5) + '\n'
        '3-5ft: ' + "{0:.2f}".format(dtD6) + ' '
        '|| SDEV: ' + "{0:.2f}".format(stdD6),
        bbox={'facecolor':'white'})

plt.savefig('/Users/Will/Desktop/Various Distance Make Pcts for ' + golfer + '.png')
plt.show()