from xata.client import XataClient
from dotenv import load_dotenv
import os
import random
import base64

def expectedScore(rA, rB):
    return 1/(1+10**((rB-rA)/400)),1/(1+10**((rA-rB)/400))

def finalElo(rA, rB,result):

    expectedrateuser1, expectedrateuser2 = expectedScore(rA,rB)
    resultuser1, resultuser2 = result

    return round(rA + 400*(resultuser1-expectedrateuser1)),round(rB + 400*(resultuser2-expectedrateuser2))


load_dotenv(".env")
db_url_env = os.environ.get("XATA_DATABASE_URL")
api_key_env = os.environ.get("XATA_API_KEY")
xata = XataClient(db_url=db_url_env,api_key=api_key_env)

data = xata.data().query("Users", {
"columns": [
    "email",
    "name",
    "elo"
]
})

users = (data['records'])

user1 = random.randint(0,len(users)-1)
user1id = users[user1]['id']
user2 = user1
while user2 == user1:
    user2 = random.randint(0,len(users)-1)
user2id = users[user2]['id']

data = xata.data().query("Matches", {
"columns": [
    "User1.id",
    "User2.id",
]
})

exists = False
gameid = ""
for datapoint in data["records"]:
    if datapoint["User1"]["id"] == user1id and datapoint["User2"]["id"] == user2id:
        exists = True
        gameid = datapoint["id"]
        break
        
if exists:
    print(gameid)
else:
    data = xata.records().insert("Matches", {
        "User1": user1id,
        "User2": user2id,
    })
    gameid = data["id"]
    
    
    print(gameid)
    
file1 = xata.records().get("Users", user1id, columns=[
    "file.name",
    "file.base64Content"
])

file2 = xata.records().get("Users", user2id, columns=[
    "file.name",
    "file.base64Content"
])

file1content = file1["file"]["base64Content"]
file1contentdecode = base64.standard_b64decode(file1content).decode('utf-8')


file2content = file2["file"]["base64Content"]
file2contentdecode = base64.standard_b64decode(file1content).decode('utf-8')

f = open("player1.py", "w")
f.write((file1contentdecode))
f.close()


f = open("player2.py", "w")
f.write((file1contentdecode))
f.close()


import gamebasemain
game = gamebasemain.Game()
result = game.gameRun(gameid,5000)
if (result[0] + result[1]) >=2:
    result = (0.5,0.5)
finalElo1, finalElo2 = finalElo(users[user1]['elo'],users[user2]['elo'],result)

print("Elo 1: ", users[user1]['elo'],"Final Elo 1: ",finalElo1, "ID: ", users[user1]['id'], "Name:", users[user1]['name'])
print("Elo 2: ",users[user2]['elo'],"Final Elo 2: ",finalElo2, "ID: ", users[user2]['id'],  "Name:", users[user2]['name'])

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
with open(f"videos/{gameid}.mp4", "rb") as f:

    videodata = f.read()

f.close()

response = xata.files().put(
  "Matches",
  gameid,
  "video",
  videodata,
  "video/mp4"
)



