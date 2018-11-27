#UPE FALL CODING CHALLENGE
#KATHIR ILANGO
#UID: 704927385
#Year: 2
#MAJOR: CSE

import requests
import json

base_url = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com"
headers = {'content-type':'application/x-www-form-url'}
UP = "UP"
DOWN="DOWN"
LEFT="LEFT"
RIGHT="RIGHT"

def getToken(uid):      #gets the token

    url = base_url + "/session"
    data = {"uid":uid}
    token = requests.post(url,data,headers)
    token_json = json.loads(token.text)
    print ("token:"+token_json["token"])
    return token_json["token"]

def getState(url):      #returns the state of the game

    state = requests.get(url,headers=headers)
    return json.loads(state.text)

def getResult(url,action):      #returns the result of an action

    action = {"action":action}
    result = requests.post(url,action,headers)
    result_json = json.loads(result.text)
    return result_json["result"]

def solveMaze(url,visited,access_token,cx,cy):      #recursive function to solve a maze

    x = cx
    y = cy
    visited[y][x] = True
    
#UP
    if (y-1>=0 and visited[y-1][x] == False):       #only check move if spot has not been visited
        result = getResult(url,UP)
        if (result == "SUCCESS"):
            visited[y][x] = True
            if (solveMaze(url,visited,access_token,x,y-1) == True):
                return True
            getResult(url,DOWN)
        elif (result == "WALL"):            #set wall to a visited spot so it does not get check again
            visited[y-1][x] = True
        elif (result == "END"):
            return True

#DOWN
    if (y+1<len(visited) and visited[y+1][x] == False):
        result = getResult(url,DOWN)
        if (result == "SUCCESS"):
            visited[y][x] = True
            if (solveMaze(url,visited,access_token,x,y+1) == True):
                return True
            getResult(url,UP)
        elif (result == "WALL"):
            visited[y+1][x] = True
        elif (result == "END"):
            return True
#LEFT
    if (x-1>=0 and visited[y][x-1] == False):
        result = getResult(url,LEFT)
        if (result == "SUCCESS"):
            visited[y][x] = True
            if (solveMaze(url,visited,access_token,x-1,y) == True):
                return True
            getResult(url,RIGHT)
        elif (result == "WALL"):
            visited[y][x-1] = True
        elif (result == "END"):
            return True

#RIGHT
    if (x+1<len(visited[y]) and visited[y][x+1] == False):
        result = getResult(url,RIGHT)
        if (result == "SUCCESS"):
            visited[y][x] = True
            if (solveMaze(url,visited,access_token,x+1,y) == True):
                return True
            getResult(url,LEFT)
        elif (result == "WALL"):
            visited[y][x+1] = True
        elif (result == "END"):
            return True

    return False


ACCESS_TOKEN = getToken("704927385")
state_url = base_url+"/game?token="+ACCESS_TOKEN

init_state = getState(state_url)
totalLevels = init_state["total_levels"]
completedLevels = 0

while (completedLevels < totalLevels):
    state = getState(state_url)
    print (state)
    w = state["maze_size"][0]
    h = state["maze_size"][1]
    visited = [[False for i in range(w)] for j in range(h)]     #create grid to keep track of visited spots
    start_xy = state["current_location"]
    start_x = start_xy[0]
    start_y = start_xy[1]
    
    working = solveMaze(state_url,visited,ACCESS_TOKEN,start_x,start_y)
    if (working == False):      #if maze is not properly solved
        print ("PREMATURE EXIT")
        exit(0)
    completedLevels = completedLevels+1
print (getState(state_url))
print ("ALL MAZES PASSED")  #all mazes solved by this point

