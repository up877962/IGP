# functions todo with making HTTP requests
import yaml
import json
import http.client
import urllib.parse

config = yaml.safe_load(open("./config.yaml"))

serverAddress = config['network']['server']['protocol'] + '://' + config['network']['server']['domain'] + ':' + str(config['network']['server']['port']) 

def login():
    global token

    # acquire sensitive information
    clientDomain = config['auth']['SPA']['domain']
    clientID = config['auth']['M2M']['clientID']
    clientSecret = config['auth']['M2M']['clientSecret']
    audience = config['auth']['API']['audience']

    # connect to domain
    conn = http.client.HTTPSConnection(clientDomain)
    # form request
    payload = '{"client_id":"' + clientID + '","client_secret":"' + clientSecret + '","audience":"' + audience  + '","grant_type":"client_credentials"}'
    headers = {'content-type': "application/json"}
    # make request
    conn.request("POST", "/oauth/token", payload, headers)
    # use response
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    token = data['access_token']

# adds a new vehicle record to web server db
def addNewVehicle(identifier):
    # decode identifier string...
    params = urllib.parse.urlencode({'identifier': identifier, 'entrance_id': 'id0', 'entrance_time': 0, 'exit_id': 'id0', 'exit_time': 1})

    conn = http.client.HTTPConnection(serverAddress)

    conn.request('POST', '/api/vehicle', params, {'authorization': f'Bearer {token}'})

    res = conn.getresponse()
    print(res) 

def main():
    login()

    #addNewVehicle("nothing")

main()