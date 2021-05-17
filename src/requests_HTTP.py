# functions todo with making HTTP requests
import yaml
import json
import http.client
#import httplib
import urllib.parse
#import urllib

config = yaml.safe_load(open("../config.yaml"))

serverAddress = config['network']['server']['domain'] + ':' + str(config['network']['server']['port']) 

###
# gets access token for making authorized http requests
###
def login():

    #global token

    # acquire sensitive information
    clientDomain = config['auth']['SPA']['domain']
    clientID = config['auth']['M2M']['clientID']
    clientSecret = config['auth']['M2M']['clientSecret']
    audience = config['auth']['API']['audience']

    # connect to domain
    conn = http.client.HTTPSConnection(clientDomain)
    #conn = httplib.HTTPSConnection(clientDomain)
    # form request
    payload = '{"client_id":"' + clientID + '","client_secret":"' + clientSecret + '","audience":"' + audience  + '","grant_type":"client_credentials"}'
    headers = {'content-type': "application/json"}
    # make request
    conn.request("POST", "/oauth/token", payload, headers)
    # use response
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    token = data['access_token']
    return(token)

def openConnection():
   if(config['network']['server']['protocol'] == 'https'):
       return http.client.HTTPSConnection(serverAddress)
       #return httplib.HTTPSConnection(serverAddress)
   else:
       return http.client.HTTPSConnection(serverAddress)
       #return httplib.HTTPConnection(serverAddress)

###
# adds a new vehicle record to web server db
# @param {string} identifer of vehicle, decoded for vehicle record info
###
def addNewVehicle(identifier, token):
    # decode identifier string...
    params = urllib.parse.urlencode({
    #params = urllib.urlencode({
        'identifier': identifier,
        'entrance_id': 'id0',
        'entrance_time': 0,
        'exit_id': 'id1',
        'exit_time': 1
    })

    conn = openConnection()

    conn.request('POST', '/api/vehicle?' + params, headers={'authorization': 'Bearer ' + token})

    res = conn.getresponse()
    print(res.status)

###
# update bounding box info for video stream
# @param {string} id of the junction/camera
# @param {double} height of bounding box
# @param {double} width of bounding box
# @param {double} x coord of top left of bounding box
# @param {double} y coord of top left of bounding box
###
def updateBoundingBox(id, height, width, x, y, token):
    params = urllib.parse.urlencode({
    #params = urllib.urlencode({
        'id': id,
        'height': height,
        'width': width,
        'x': x,
        'y': y
    })

    conn = openConnection()

    conn.request('POST', '/api/vehicle/boundingbox?' + params, headers={'authorization': 'Bearer ' + token})

    res = conn.getresponse()
    print(res.status)

# demo
def demo():
    token = login()

    print(token)
    addNewVehicle("nothing", token)
    updateBoundingBox('id0', 80, 60, 540.52, 120.28, token)

demo()

