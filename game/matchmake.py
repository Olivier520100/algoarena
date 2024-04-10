from xata.client import XataClient
from dotenv import load_dotenv
import os
import random
import time


def expectedScore(rA, rB):
    return 1/(1+10**((rB-rA)/400)),1/(1+10**((rA-rB)/400))


def winnerCalculate(user1percentage):
    if random.random() < 0.5:
        return 1,0    
    else: 
        return 0,1

def finalElo(rA, rB):

    expectedrateuser1, expectedrateuser2 = expectedScore(rA,rB)
    resultuser1, resultuser2 = winnerCalculate(expectedrateuser1)

    return round(rA + 400*(resultuser1-expectedrateuser1)),round(rB + 400*(resultuser2-expectedrateuser2))




load_dotenv("../algoarena/.env")
db_url_env = os.environ.get("XATA_DATABASE_URL")
api_key_env = os.environ.get("XATA_API_KEY")
xata = XataClient(db_url=db_url_env,api_key=api_key_env)


while True:

    data = xata.data().query("Users", {
    "columns": [
        "email",
        "name",
        "elo"
    ]
    })


    users = (data['records'])

    user1 = random.randint(0,len(users)-1)
    user2 = user1
    while user2 == user1:
        user2 = random.randint(0,len(users)-1)

    finalElo1, finalElo2 = finalElo(users[user1]['elo'],users[user2]['elo'])

    print(users[user1]['elo'])
    print(users[user2]['elo'])
    print(finalElo1)
    print(finalElo2)
    try:
        data = xata.records().update("Users", users[user1]['id'], {
            "elo": finalElo1
        })
        assert data.is_success()
    except:
        print("Error changing elo")   

    try:
        data = xata.records().update("Users", users[user2]['id'], {
            "elo": finalElo2
        })
        assert data.is_success()
    except:
        print("Error changing elo")   











