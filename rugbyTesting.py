import requests, json, datetime
from datetime import datetime
import schedule
import time

counter = 0
def recordRugbyData():
    # login details
    username = 'YOUR USERNAME HERE'
    password = 'YOUR PASSWORD HERE'
    appKey = 'YOUR APPKEY HERE'

    # Bot Log in
    payload = {'username': username, 'password': password}
    headers = {'X-Application': appKey, 'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post('https://identitysso-cert.betfair.com/api/certlogin',
                         data=payload,
                         cert=('PATH TO YOUR CERTIFICATE HERE', 'PATH TO YOUR KEY HERE'),
                         headers=headers)

    # the response is saved as python object
    resp_json = resp.json()
    print('resp_json keys:', resp_json.keys())

    # check if user is logged in and get SSOID
    print(resp_json['loginStatus'])
    SSOID = resp_json['sessionToken']

    # accessing the betting API and adding filters
    bet_url = "https://api.betfair.com/exchange/betting/json-rpc/v1/"
    data_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEvents", "params":' \
               '{"filter":{"textQuery": "Rugby", "marketTypeCode": ["MATCH_ODDS"], "marketProjection": ["RUNNER_METADATA"]}}, "id": 1}'
    headers_betting = {'X-Application': appKey, 'X-Authentication': SSOID, 'content-type': 'application/json'}
    response = requests.post(bet_url, data=data_req.encode('utf-8'), headers=headers_betting)

    data = response.json()

    #converting the python object into a string
    # def jprint(obj):
    #     # create a formatted string of the Python JSON object
    #     text = json.dumps(obj, sort_keys=True, indent=2)
    #     print(text)

    print(type(data['result']))

    # jprint(data["result"][0]['event'])

    # write to file - home vs away team, time
    f = open("recData.txt", "a")
    for el in data['result']:
        name = el['event']['name']
        openDate = el['event']['openDate']
        timezone = el['event']['timezone']
        now = datetime.now()
        time_recorded = now.strftime("%H:%M:%S")
        print('event name: ' + name + " / " + 'openDate: ' + openDate + " " + timezone + " / " + "time_recorded: " + time_recorded)
        toWrite = 'event name: ' + name + " / " + 'openDate: ' + openDate + " " + timezone + " / " + "time_recorded: " + time_recorded
        f.write(toWrite + "\n")
    global counter
    counter +=1
    if counter > 5:
        f.close()
        exit(0)

# Time
schedule.every(10).seconds.do(recordRugbyData)

while True:
    schedule.run_pending()
    time.sleep(1)