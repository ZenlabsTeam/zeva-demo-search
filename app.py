#!/usr/bin/env python

import urllib
import json
import os
import urllib2
import datetime
import duckduckgo
import weather
from flask import Flask
from flask import request
from flask import make_response
from pyowm import OWM


# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    speech = 'Sorry not able to get result'
    try:
        result = req.get("result")
        parameters = result.get("parameters")
        given = parameters.get("given-name")
        resolvedQuery = result.get("resolvedQuery")
        
        print(given)
        print(resolvedQuery)
        print(result.get("action"))
        if result.get("action") == "whatis":
            speech = duckduckgo.get_zci(given)
            
            if speech.find('http://') != -1  or speech.find('https://') != -1 or speech == 'Sorry, no results.':
                speech = duckduckgo.get_zci(resolvedQuery)
                if speech.find('http://') != -1  or speech.find('https://') != -1:
                    speech='Sorry!!! Unable to retive any abstract from search result.'
                
            
        elif result.get("action") == "greetings":
            username = 'Anand'
            contextsList=result.get("contexts")
            for context in contextsList :
                if context.get("name") == "userinfo":
                    username = context.get("parameters").get("given-name")
            print(given)
            print(username)
            currentTime = datetime.datetime.utcnow();
            print(currentTime.hour )
            speech = weather.processWeatherRequest('pune') 
            if currentTime.hour < 7:
                speech=',Good morning. '
            elif 7 <= currentTime.hour < 13:
                speech=',Good afternoon. '
            else:
                speech=',Good evening. ' 
            speech = 'Hey '+ username +speech+'.You have a flight to banglore at 6:30 make sure that you check-in by 4:30.May I help you with something more?'
    except:
        speech = 'Sorry Internal Error'
        
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "zeva-saerch"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
