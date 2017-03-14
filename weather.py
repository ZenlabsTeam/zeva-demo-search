
from urllib2 import urlopen, Request
from urllib2 import HTTPError
import urllib
import json
import os

def processWeatherRequest(city):
  
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "') and u='c'"
    yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = getWeatherResultString(data)
    
    return res



def getWeatherResultString(data):
    print('IN')
    speech = 'ERROR'
    query = data.get('query')
    if query is None:
        print('Query Not Found')
        return speech

    result = query.get('results')
    if result is None:
        print('Result Not Found')
        return speech

    channel = result.get('channel')
    if channel is None:
        print('Channel Not Found')
        return speech

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        print('Others Not Found')
        return speech

    condition = item.get('condition')
    if condition is None:
        print('Condition Not Found')
        return speech

    # print(json.dumps(item, indent=4))
    print('P2')
    speech = ".Today in poona it's " + condition.get('text') + \
             ", the temperature is " + condition.get('temp') + " " + units.get('temperature') +" now"

    print(speech) 

    return speech

