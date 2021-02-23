# functions todo with making HTTP requests
import requests
import sys
# local modules
sys.path.append(".")
sys.path.append("../")
import config

def requestTest(): 
    url = "http://" + config.domain + ":" + config.port + "/api/test"
    res = requests.get(url)

    print(res.json())

requestTest()
