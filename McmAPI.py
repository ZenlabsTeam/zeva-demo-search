import requests
import json


baseURL='https://isinterface.zensar.com/MCMService/MCMService.svc'
if __name__ == '__main__':
    operationSubUrl='/GetAllMemberNames'
    payload = {"userValue":{"userName":"si47268","password":"Zensar@1"}}
    headerParms={'content-type': 'application/json'}
    payld = json.dumps(payload)
    finalURL=baseURL+operationSubUrl
    print(finalURL)
    ret = requests.post(finalURL,data=payld, headers=headerParms)
    jsonText = string.replace(ret.text,'\\"','"')
    result = json.load(jsonText)
    print(result.get('d'))
    
    