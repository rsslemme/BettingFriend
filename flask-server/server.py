#starting instructions
#CD into flask-server and commmand : python server.py
#CD into client and command : npm start 

from flask import Flask
import json
import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd
import winsound
import time
import fsspec as fs
from flatten_json import flatten

app = Flask(__name__)

#members api route

@app.route("/members")
def members():
    return {"members" : ["member1" , "member2", "member3"]}

    
apiKey = 'ba3d17799cc1ae909ff5992e6e72b8d3'
method = "get"
#sportKey = 'icehockey_nhl' #basketball_ncaab , basketball_nba, baseball_mlb, americanfootball_nfl,  americanfootball_ncaaf
sportKey = 'icehockey_nhl'
#sportKey = 'americanfootball_nfl'
#sportKey = 'baseball_mlb'
#sportKey = 'basketball_nba'
#url = "https://the-odds-api.com"

url = 'https://api.the-odds-api.com/v4/sports/' + sportKey + '/odds/?apiKey=' + apiKey + '&regions=us&markets=h2h,spreads&oddsFormat=american'
secret = ''
auth = HTTPBasicAuth(apiKey, secret)
rsp = requests.request(method, url, headers=None, auth=auth)
data = rsp.text

#print(rsp.content)

#return json objeect should look like this 
#games
    #game1
        #   team1
        #   book1
        #   spread1
        #   price1
        #   team2
        #   book2
        #   spread2
        #   price2
        #   isArb
    #game2
        #   team1
        #   book1
        #   spread1
        #   price1
        #   team2
        #   book2
        #   spread2
        #   price2
        #   isArb

def runScript():
    retString = ''
    gamesDict = []
    f = 0
    url = 'https://api.the-odds-api.com/v4/sports/' + sportKey + '/odds/?apiKey=' + apiKey + '&regions=us&markets=h2h,spreads&oddsFormat=american'
    secret = ''
    auth = HTTPBasicAuth(apiKey, secret)
    rsp = requests.request(method, url, headers=None, auth=auth)
    data = rsp.text
    parseData = json.loads(data)

    while (f < 1000): #howManyGamesDoYouWant
        isArb = False
        try:
            parseDataDict = parseData[f] #this gets the first game
        except:
            #print('-----' + 'script stopped after ' + str(f) + ' games' + '-----')
            #retString += '-----' + 'script stopped after ' + str(f) + ' games' + '-----'
            break
        #print(parseData)
        #print(pd.json_normalize(rsp.text, "id"))
        books = parseDataDict['bookmakers']
        team1BestPrice = ('not important' ,'not important', 0, -5000)
        team2BestPrice = ('not important' ,'not important', 0, -5000)
        acceptableBookies = ['DraftKings' , 'FanDuel' , 'BetRivers' , 'Caesars Sportsbook']#, 'PointsBet (US)' , 'WynnBET'] #'BetMGM
        unAcceptableBookies = ['BetMGM', 'Bovada']
        tempName = ''
        tempPrice = -5000
        for i in books:
            tempName = i['title']
            #print(tempName)
            markets = i['markets']
            tempSize = len(markets)
            if(tempName in acceptableBookies):
                if tempSize >= 2:
                    spread = markets[1] #h2h = markets[0]
                    spreads = spread['outcomes']
                    team1 = spreads[0]
                    team2 = spreads[1]
                    team1Price = team1['price']
                    team2Price = team2['price']
                    team1Name = team1['name']
                    team2Name = team2['name']
                    team1Point = team1['point']
                    team2Point = team2['point']
                    team1Combo = (tempName, team1Name, team1Point, team1Price)
                    team2Combo = (tempName, team2Name, team2Point, team2Price)

                    if team1Combo[3] > team1BestPrice[3]:
                        team1BestPrice = team1Combo
                    
                    if team2Combo[3] > team2BestPrice[3]:
                        team2BestPrice = team2Combo

        #testing scenario
        #print('---------------------------------------------')
        retString += '----'
        #print(team1BestPrice)
        if(team1BestPrice[0] != 'not important' or team1BestPrice[1] != 'not important' or team2BestPrice[1] != 'not important'  or team2BestPrice[0] != 'not important' ):
            if(team1BestPrice[2] + team2BestPrice[2] == 0):
                retString += str(team1BestPrice)
                #print(team2BestPrice)
                retString += str(team2BestPrice)
                #print('---------------------------------------------')
                retString += '----'
        if(float(team1BestPrice[2]) + float(team2BestPrice[2]) == 0.0):
            if(team1BestPrice[3] + team2BestPrice[3] > 0):
                isArb = True
                absPrice1 = str(abs(team1BestPrice[3]))
                absPrice2 = str(abs(team2BestPrice[3]))
                winsound.Beep(2500 , 1000)
                #print(" ----------ARB BET DETECTED---------- ")
                retString += " ----------ARB BET DETECTED---------- "
                if(team1BestPrice[3] > team2BestPrice[3]):
                    #print('Bet 100 on ' + team1BestPrice[1] + ' On the book : ' + team1BestPrice[0])
                    retString+='Bet 100 on ' + team1BestPrice[1] + ' On the book : ' + team1BestPrice[0]
                    #print('Bet ' + absPrice2 + ' on ' + team2BestPrice[1] + ' On the book : ' + team2BestPrice[0])
                    retString+='Bet ' + absPrice2 + ' on ' + team2BestPrice[1] + ' On the book : ' + team2BestPrice[0]
                else :
                    #print('Bet 100 on ' + team2BestPrice[1] + ' On the book : ' + team2BestPrice[0])
                    retString+='Bet 100 on ' + team2BestPrice[1] + ' On the book : ' + team2BestPrice[0]
                    #print('Bet ' + absPrice1  + ' on ' + team1BestPrice[1] + ' On the book : ' + team1BestPrice[0])
                    retString+='Bet ' + absPrice1  + ' on ' + team1BestPrice[1] + ' On the book : ' + team1BestPrice[0]
            gameDict = {'book1' : team1BestPrice[0] , 'team1' : team1BestPrice[1], 'spread1' : team1BestPrice[2] , 'price1' : team1BestPrice[3] , 'book2' : team2BestPrice[0] , 'team2' : team2BestPrice[1], 'spread2' : team2BestPrice[2] , 'price2' : team2BestPrice[3], 'isArb' : isArb}
            retString2 = gameDict
            gamesDict.append(gameDict)
            #gamesDict += {f : gameDict}
        #here if we need to do a dict of dicts, use looping index as game
        f+=1
    finalRet = json.dumps(gamesDict)

    with open('C://Project//Output//out.json', 'w') as fout:
        json.dump(gamesDict, fout)
        
    return finalRet  #gamesDict
        

@app.route('/arbs')
def arbs():
    retObj = runScript()
    return retObj

if __name__ == "__main__":
    app.run(debug=True)